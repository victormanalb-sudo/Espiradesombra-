# -*- coding: utf-8 -*-
"""
==============================================================================
  MDC — CORTES ARMÓNICOS + REGULA FALSI (extensión sobre mdc_v18)
  Sustituye la bisección secuencial 50/50 de k_sweep_bisectat por:

    1) K cortes FIJOS, calculados de una sola vez con la partición exacta
         m_i = n / (i·(i+1))      (la que salió de "R/(i+1)")
       cuya suma telescopa exactamente a n (cobertura total garantizada,
       sin el resto perdido del (e-1)/2 ≈ 0.859 del esquema factorial).
       Todos los cortes son independientes entre sí → evaluables en
       paralelo (GPU/hilos), a diferencia de la bisección actual que
       depende del resultado del nivel anterior.

    2) Localización de TODOS los tramos con cambio de signo de ΔΦ en
       una sola pasada sobre el vector de signos (no solo "la mitad").

    3) Dentro de cada tramo marcado: en vez de partir 50/50, se usa
       interpolación lineal (regula falsi) sobre los dos valores de
       ΔΦ ya calculados, así que el siguiente punto cae donde la
       recta que une ambos extremos cruza el cero — no en el punto
       medio a ciegas. Si la secante no da corte claro (curvatura
       fuerte), se cae a la pinça doble (V/A ya calculada en el
       código base) para un salto cuadrático.

  AUTOR base: Víctor Manzanares Alberola (mdc_v18.py)
  Esta extensión: cortes armónicos + regula falsi sobre esa base.

  ──────────────────────────────────────────────────────────────────────
  HALLAZGO IMPORTANTE (benchmark 2026-09-24) — LEER ANTES DE USAR
  ──────────────────────────────────────────────────────────────────────
  k_sweep_regula_falsi() (sección 3) tiene un fallo de diseño: los K
  cortes fijos se reparten según POSICIÓN en m, pero el número de
  dientes de ΔΦ dentro de un tramo depende de su anchura en k
  (n_k = k_hi-k_lo), no de su anchura en m. Verificado: falla en
  encontrar factores que sí encuentra la bisección clásica.

  k_sweep_armonico_recursiu() (sección 4) corrige eso — el criterio de
  parada/recursión vuelve a ser n_k, y solo cambia CÓMO se elige el
  corte (secante en vez de punto medio) una vez el tramo ya es fiable.

  PERO al probar ambas contra mdc_v18() completo con N =
  6238334643561017 (p=1386294431, q=4500007, m_target=2250002, un
  factor justo por encima de la criba de 2M), **el propio mdc_v18()
  original también falla en encontrarlo** — no es una regresión de
  este módulo. Causa: n_k ≈ N/(2m) es hiperbólico en m, así que
  bisectar el segmento en m por la mitad no reduce n_k proporcional-
  mente cuando el extremo bajo sigue siendo pequeño. El criterio
  "ΔΦ cambia de signo" con solo 2-3 muestras dentro de un rango con
  potencialmente millones de dientes puede fallar por pura casualidad
  de muestreo — y aquí falla.

  Conclusión: k_sweep_armonico_recursiu() (secante) SÍ converge en
  menos evaluaciones que la bisección clásica cuando el signo de ΔΦ ya
  es fiable (n_k moderado) — pero no resuelve el hueco de fondo, que
  es anterior: decidir cuándo ese signo es fiable. Antes de adoptar la
  secante en producción, valdría la pena:
    1) Medir con qué frecuencia el hueco de la criba [lim_criba, m_conv]
       afecta a casos reales (¿fue mala suerte de este N o es
       sistemático?).
    2) Explorar bisectar en log(m) o en k en vez de m lineal para los
       segmentos que tocan m pequeño, igualando la reducción de n_k
       por paso.
    3) Solo entonces, aplicar la secante como mejora de segundo orden.
  ──────────────────────────────────────────────────────────────────────
==============================================================================
"""

from fractions import Fraction

from mdc_v18 import (
    d_frac, m_espell, desfase_espell, check_factor,
    k_sweep, k_sweep_bisectat, proper_valid, pinca_doble,
)


# ============================================================================
#  1) CORTES ARMÓNICOS FIJOS  m_i = n / (i·(i+1))
# ============================================================================

def generar_cortes_armonicos(m_ini: int, m_fi: int, K: int = 40) -> list[int]:
    """
    Genera hasta K+2 puntos de corte en [m_ini, m_fi], pegados al
    extremo denso m_fi y decreciendo hacia m_ini con paso m_i = n/(i(i+1)):

        b_0 = m_fi
        b_1 = m_fi - n/2
        b_2 = b_1 - n/6      (= m_fi - 2n/3)
        b_3 = b_2 - n/12     (= m_fi - 3n/4)
        ...
        b_i = m_fi - n·i/(i+1)   →  b_i → m_ini cuando i→∞

    La suma de los saltos es EXACTA: Σ n/(i(i+1)) = n (telescópica,
    1/(i(i+1)) = 1/i - 1/(i+1)), así que el último corte cae siempre
    en m_ini, sin resto residual que cubrir aparte.
    """
    n = m_fi - m_ini
    if n <= 0:
        return [m_ini]

    cortes = [Fraction(m_fi)]
    pos = Fraction(m_fi)
    R = Fraction(n)
    for i in range(1, K + 1):
        salto = R / (i + 1)
        pos -= salto
        R -= salto
        cortes.append(pos)
        if pos <= m_ini:
            break
    if cortes[-1] > m_ini:
        cortes.append(Fraction(m_ini))

    enteros = sorted(set(max(m_ini, min(m_fi, int(c))) for c in cortes))
    return enteros


def _signo(x: Fraction) -> int:
    return (x > 0) - (x < 0)


# ============================================================================
#  2) REFINAMIENTO POR SECANTE (regula falsi) + PINÇA DOBLE
# ============================================================================

def refinar_secante(m_a: int, m_b: int, N: int,
                     max_iter: int = 25) -> int | None:
    """
    Dado [m_a, m_b] con ΔΦ de signo opuesto en los extremos, converge
    al cero SIN bisectar 50/50: el siguiente punto se calcula por
    interpolación lineal ponderada por |ΔΦ|, y solo cuando la secante
    no aporta información nueva (mismo signo tras el corte, curvatura
    fuerte) se recurre a la pinça doble (V/A) para un salto cuadrático.
    """
    def _valid(m):
        return proper_valid(m, 1) or proper_valid(m, -1)

    m_a = _valid(m_a)
    m_b = _valid(m_b)
    if m_a is None or m_b is None or m_a >= m_b:
        return None

    if check_factor(m_a, N):
        return 2 * m_a + 3
    if check_factor(m_b, N):
        return 2 * m_b + 3

    df_a = desfase_espell(m_a, N)
    df_b = desfase_espell(m_b, N)

    for it in range(max_iter):
        if m_b - m_a <= 4:
            f = k_sweep(N, m_a, m_b, verbose=False)
            if f:
                return f
            return None

        if _signo(df_a) == _signo(df_b):
            # no debería pasar si el llamador confirmó cambio de signo,
            # pero por seguridad: bisección clásica como red de emergencia
            m_c = (m_a + m_b) // 2
        else:
            denom = abs(df_a) + abs(df_b)
            frac = (abs(df_a) / denom) if denom != 0 else Fraction(1, 2)
            m_c = m_a + int(frac * (m_b - m_a))
            m_c = max(m_a + 1, min(m_b - 1, m_c))

        m_c = _valid(m_c)
        if m_c is None or not (m_a < m_c < m_b):
            m_c = (m_a + m_b) // 2
            m_c = _valid(m_c)
            if m_c is None or not (m_a < m_c < m_b):
                return k_sweep(N, m_a, m_b, verbose=False)

        if check_factor(m_c, N):
            return 2 * m_c + 3

        df_c = desfase_espell(m_c, N)

        if _signo(df_a) != _signo(df_c):
            m_b, df_b = m_c, df_c
        elif _signo(df_c) != _signo(df_b):
            m_a, df_a = m_c, df_c
        else:
            # secante estancada: probamos el salto cuadrático de la pinça
            cinc = pinca_doble(m_c, N)
            salt = cinc['salt_f'] or cinc['salt_r']
            usado = False
            if salt and m_a < salt < m_b:
                if check_factor(salt, N):
                    return 2 * salt + 3
                df_s = desfase_espell(salt, N)
                if _signo(df_a) != _signo(df_s):
                    m_b, df_b = salt, df_s
                    usado = True
                elif _signo(df_s) != _signo(df_b):
                    m_a, df_a = salt, df_s
                    usado = True
            if not usado:
                # último recurso: reduce por bisección para no bucle infinito
                if m_c <= m_a or m_c >= m_b:
                    m_c = (m_a + m_b) // 2
                m_a, df_a = m_c, df_c

    return k_sweep(N, m_a, m_b, verbose=False)


# ============================================================================
#  3) ORQUESTADOR: cortes fijos (paralelizables) + secante localizada
# ============================================================================

def k_sweep_regula_falsi(N: int, m_ini: int, m_fi: int,
                          K: int = 40, llindar_k: int = 1_000_000,
                          verbose: bool = False) -> int | None:
    """
    Sustituto de k_sweep_bisectat: en vez de bisectar secuencialmente
    50/50 dependiendo del resultado anterior, genera K cortes fijos
    de antemano (independientes → paralelizables), localiza TODOS los
    tramos con cambio de signo de ΔΦ en una sola pasada, y refina cada
    uno por secante/pinça en vez de bisección ciega.
    """
    if m_ini < 1:
        m_ini = 1
    if m_fi <= m_ini:
        return None

    pos_i = 2 * m_ini + 3
    pos_f = 2 * m_fi + 3
    k_lo = max(1, N // pos_f)
    k_hi = N // pos_i
    if k_hi - k_lo <= llindar_k:
        return k_sweep(N, m_ini, m_fi, verbose=verbose)

    cortes = generar_cortes_armonicos(m_ini, m_fi, K=K)

    validos = []
    for c in cortes:
        mv = proper_valid(c, 1) or proper_valid(c, -1)
        if mv is not None:
            validos.append(mv)
    validos = sorted(set(validos))

    if len(validos) < 2:
        return k_sweep_bisectat(N, m_ini, m_fi, verbose=verbose)

    # --- Evaluación de ΔΦ en todos los cortes ---------------------------
    # (independientes entre sí: candidatas naturales a vectorizar/paralelizar)
    signos = []
    for mv in validos:
        if check_factor(mv, N):
            return 2 * mv + 3
        df = desfase_espell(mv, N)
        signos.append((mv, df, _signo(df)))

    if verbose:
        print(f"    cortes armónicos: {len(validos)} puntos, "
              f"signos={[s for _, _, s in signos]}")

    # --- Localiza TODOS los tramos con cambio de signo, no solo uno -----
    for j in range(len(signos) - 1):
        m_a, _, s_a = signos[j]
        m_b, _, s_b = signos[j + 1]
        if s_a != 0 and s_b != 0 and s_a != s_b:
            factor = refinar_secante(m_a, m_b, N)
            if factor:
                return factor

    # Sin cambio de signo claro en ningún tramo: red de seguridad clásica
    return k_sweep_bisectat(N, m_ini, m_fi, llindar_k=llindar_k, verbose=verbose)


# ============================================================================
#  4) VERSIÓN CORREGIDA: el criterio de subdivisión es n_k, no la posición m
# ============================================================================
#  El fallo de k_sweep_regula_falsi: los K cortes fijos se reparten según
#  la posición en m, pero el número de dientes de ΔΦ dentro de un tramo
#  depende de su ANCHURA EN k (n_k = k_hi-k_lo), no de su anchura en m.
#  Un tramo puede ser "pequeño" en m y aun así contener millones de
#  dientes si está cerca de m=0 (k enorme). Por eso el criterio de
#  parada/recursión tiene que seguir siendo n_k, igual que en el
#  original — lo único que cambia aquí es CÓMO se elige el punto de
#  corte una vez el tramo ya es lo bastante fino: por secante
#  (ponderado por |ΔΦ|) en vez de por el punto medio ciego.
# ============================================================================

def k_sweep_armonico_recursiu(N: int, m_ini: int, m_fi: int,
                               llindar_k: int = 1_000_000,
                               profunditat: int = 80,
                               verbose: bool = False) -> int | None:
    for it in range(profunditat):
        if m_fi <= m_ini:
            return None
        pos_i, pos_f = 2 * m_ini + 3, 2 * m_fi + 3
        k_lo = max(1, N // pos_f)
        k_hi = N // pos_i
        n_k = k_hi - k_lo

        if n_k <= llindar_k:
            return k_sweep(N, m_ini, m_fi, verbose=verbose)

        m_e = proper_valid(m_ini, 1)
        m_f = proper_valid(m_fi, -1)
        if not m_e or not m_f or m_e >= m_f:
            return k_sweep_bisectat(N, m_ini, m_fi,
                                     llindar_k=llindar_k, verbose=verbose)

        if check_factor(m_e, N):
            return 2 * m_e + 3
        if check_factor(m_f, N):
            return 2 * m_f + 3

        df_e = desfase_espell(m_e, N)
        df_f = desfase_espell(m_f, N)

        if _signo(df_e) != _signo(df_f):
            # tramo bracketed: corte por secante, no por punto medio
            denom = abs(df_e) + abs(df_f)
            frac = (abs(df_e) / denom) if denom != 0 else Fraction(1, 2)
            m_c = m_e + int(frac * (m_f - m_e))
            m_c = max(m_e + 1, min(m_f - 1, m_c))
            m_cm = proper_valid(m_c, 1) or proper_valid(m_c, -1)
            if not m_cm or not (m_e < m_cm < m_f):
                m_cm = proper_valid((m_e + m_f) // 2, 1)
            if m_cm and check_factor(m_cm, N):
                return 2 * m_cm + 3
            df_c = desfase_espell(m_cm, N) if m_cm else None
            if m_cm and df_c is not None and _signo(df_e) != _signo(df_c):
                m_fi = m_cm
            elif m_cm and df_c is not None:
                m_ini = m_cm
            else:
                m_ini, m_fi = m_e, (m_e + m_f) // 2
        else:
            # sin cambio de signo en los extremos: no podemos descartar
            # la mitad a ciegas (ahí falló la versión anterior) —
            # usamos el criterio de distancia al cero (R2) del original
            # para decidir qué mitad seguir explorando, y REDUCIMOS n_k
            # a la mitad de todos modos para garantizar progreso.
            m_c = (m_e + m_f) // 2
            m_cm = proper_valid(m_c, 1) or proper_valid(m_c, -1)
            if not m_cm:
                return k_sweep_bisectat(N, m_ini, m_fi,
                                         llindar_k=llindar_k, verbose=verbose)
            if check_factor(m_cm, N):
                return 2 * m_cm + 3
            pos_e, pos_f2 = 2 * m_e + 3, 2 * m_f + 3
            R2_e = (N % pos_e) % (pos_e - 1) if pos_e > 1 else 10**18
            R2_f = (N % pos_f2) % (pos_f2 - 1) if pos_f2 > 1 else 10**18
            if R2_e <= R2_f:
                m_ini, m_fi = m_e, m_cm
            else:
                m_ini, m_fi = m_cm, m_f

    return None
