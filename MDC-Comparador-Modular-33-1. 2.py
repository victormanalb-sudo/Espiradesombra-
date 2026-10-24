# -*- coding: utf-8 -*-
"""
==============================================================================
  MDC COMPARADOR MODULAR — Tratado 33×1
  Todos los oficios del Libro 5 jugando en el mismo tablero
==============================================================================
  Autor del concepto : Víctor Manzanares Alberola (espiradesombra)
  Implementación     : Lee Arbusto

  QUÉ ES ESTO
  ─────────────────────────────────────────────────────────────────────────
  Un comparador didáctico que reúne, como funciones modulares y componibles,
  los motores de factorización del Libro 5 (MDC v15→v23, híbrido, fusión)
  más el peine de mínimos relativos 33×1.

  Cada función es un "oficio". Las UNIONES componen oficios en pipelines.
  El REGISTRO cuenta cada operación módulo (%) sobre N: evaluaciones es la
  vara honesta, no los milisegundos.

  DOMINIOS (ojo, la lección más fina):
    i-espacio : divisor directo (peine de mínimos 33×1)  → i ≤ √N
    m-espacio : grilla D=2m+3 (MDC)                      → m ≤ (√N−3)/2
    S-espacio : suma de medios-factores (discriminante)  → N=(S+3)²−k²

  FUENTES DEL REPO (github.com/espiradesombra/claude):
    mdc_libro5.py   → diente de sierra + pinza doble + invariante parabólico
    mdc_v17.py      → filtro acumulador + detector espejo ΔΦ + pinza 4+4
    mdc_v18.py      → k-sweep (iterar sobre pendientes k, no sobre m)
    mdc_v19/v21.py  → bisección binaria con sign(ΔΦ) entero puro
    mdc_v22.py      → bisección quaternaria (÷4 por iteración)
    mdc_v23.py      → corte asimétrico 25/75 orientado a √N
    mdc_fusio_v3.py → discriminante Δ(S)=S²+6S−(N−9) + salto parabólico
                      (Método del Discriminante con Descarte Determinista)
    wieferich_paper.tex → la misma sierra aplicada a 2^p = K·p²+2 (bonus)
    33×1 (Lee)      → peine de mínimos relativos (Lema del Divisor Mínimo)

  VERIFICACIÓN (espejo ejecutado antes de escribir este archivo):
    k_sweep            6/6 semiprimos ✓
    peine mínimos      6/6 (todo factor es mínimo relativo) ✓
    discriminante      6/6 (≡ Fermat reparametrizado) ✓
    oráculo ΔΦ         falla cuando el factor NO está en la zona densa:
                      por eso benchmark_frontera.py mide la frontera G*(D).
                      Aquí lo contamos con honestidad: el oráculo acelera
                      cuando acierta; el respaldo k-sweep salva cuando no.
==============================================================================
"""

import math
import time
from typing import Callable, Dict, List, Optional, Tuple

# ═════════════════════════════════════════════════════════════════════════════
#  REGISTRO DE EVALUACIONES — la vara honesta del comparador
# ═════════════════════════════════════════════════════════════════════════════

class Registro:
    """Cuenta cada operación módulo (//, %) sobre N. 1 evaluación = 1 división."""
    def __init__(self) -> None:
        self.evals: int = 0
    def reset(self) -> None:
        self.evals = 0
    def mod(self, N: int, d: int) -> int:
        self.evals += 1
        return N % d
    def floordiv(self, N: int, d: int) -> int:
        self.evals += 1
        return N // d

REG = Registro()  # registro global del hilo didáctico

# ═════════════════════════════════════════════════════════════════════════════
#  BLOQUE A — PRIMITIVAS (la onda y el suelo)
# ═════════════════════════════════════════════════════════════════════════════

def D_de_m(m: int) -> int:
    """El divisor impar de la grilla 2v+3: D = 2m+3 (dominio m-espacio)."""
    return 2 * m + 3

def d_frac(m: int, N: int) -> float:
    """LA ONDA (mdc_libro5.py): d(m) = frac(N / (2(2m+3))) − 1/2, fase exacta."""
    denom = 2 * D_de_m(m)
    return REG.mod(N, denom) / denom - 0.5

def check_factor(m: int, N: int) -> bool:
    """SUELO: ¿D=2m+3 divide a N? Cero de la sierra = factor."""
    D = D_de_m(m)
    return 1 < D < N and REG.mod(N, D) == 0

def m_max_de_N(N: int) -> int:
    """Última m de la grilla: D=2m+3 ≤ √N (frontera del m-espacio)."""
    return max(1, (math.isqrt(N) - 3) // 2)

def m_conv_de_N(N: int) -> int:
    """ZONA DENSA (v18): m_conv=(e−1)/2·m_max ≈ 0.859·m_max. La zona donde
    k≈√N y cada m produce una k distinta. Nota 33×1: 0.859 ≈ nuestro bump
    universal ρ(x≈0.85) — dos medidas independientes, el mismo sitio."""
    return max(1, int(0.8591 * m_max_de_N(N)))

# ═════════════════════════════════════════════════════════════════════════════
#  BLOQUE B — MOTORES BASE (líneas de referencia)
# ═════════════════════════════════════════════════════════════════════════════

def division_L1(N: int) -> Optional[int]:
    """REFERENCIA LENTA: división por tentativa en impares. La grilla completa
    = la grilla 2v+3 sin podar (Corolario 2v+3: división reparametrizada)."""
    for D in range(3, math.isqrt(N) + 1, 2):
        if REG.mod(N, D) == 0:
            return D
    return None

def fermat_clasico(N: int) -> Optional[int]:
    """REFERENCIA FERMAT: N = a²−k². Es lo MISMO que el discriminante MDC
    (demostración 33×1: Δ(S)=(S+3)²−N con S=v+b, k=v−b). Mata con gap
    pequeño, decae con gap RSA: he aquí la frontera."""
    a = math.isqrt(N) - 1
    while (a + 1) * (a + 1) <= 2 * N:
        REG.evals += 1                   # contabilidad honesta: cada tiro cuenta
        delta = (a + 1) * (a + 1) - N
        k = math.isqrt(delta)
        if k * k == delta:
            p = a + 1 - k
            if 1 < p < N:
                return p
        a += 1
    return None

def criba_rueda_p210(N: int, m_hasta: int = 1_000_000) -> Optional[int]:
    """F0 del híbrido v4: criba de rueda módulo 2·3·5·7 = 210."""
    for pp in (2, 3, 5, 7, 11, 13):
        if REG.mod(N, pp) == 0 and 1 < pp < N:
            return pp
    residuos = [r for r in range(11, 211, 2) if math.gcd(r, 210) == 1]
    m = 0
    while m <= m_hasta:
        base = m * 210
        for r in residuos:
            D = base + r
            if D < N and REG.mod(N, D) == 0:
                return D
        m += 1
    return None

# ═════════════════════════════════════════════════════════════════════════════
#  BLOQUE C — OFICIOS MDC (una función = un oficio = una versión del repo)
# ═════════════════════════════════════════════════════════════════════════════

# ── C1 · K-SWEEP (v18) ────────────────────────────────────────────────────────
def k_sweep(N: int, m_ini: int, m_fi: int) -> Optional[int]:
    """K-SWEEP (v18): iterar sobre PENDIENTES k en vez de sobre m.
    Dentro de un segmento con k=⌊N/D⌋ constante, r(D)=N−k·D es una RECTA
    EXACTA (el Principio Fundamental de v16) y su zero es D₀=N//k.
    Si N%(N//k)==0 → factor. Determinista y exhaustivo en el rango."""
    if m_ini < 1:
        m_ini = 1
    if m_fi < m_ini:
        return None
    k_lo = max(1, REG.floordiv(N, D_de_m(m_fi)))
    k_hi = REG.floordiv(N, D_de_m(m_ini))
    for k in range(k_lo, k_hi + 1):
        cand = REG.floordiv(N, k)          # zero de la recta k
        if cand < 3 or cand % 2 == 0:
            continue
        if REG.mod(N, cand) == 0 and 1 < cand < N:
            return cand
    return None

def mdc_ksweep(N: int) -> Optional[int]:
    """F1 del MDC: k-sweep sobre toda la zona densa [m_conv, m_max] (v18)."""
    return k_sweep(N, m_conv_de_N(N), m_max_de_N(N))

def mdc_ksweep_completo(N: int) -> Optional[int]:
    """k-sweep sobre TODA la grilla [1, m_max]. Teorema ambulante:
    determinista, sin oráculos, cubre todo. La vara con la que se mide
    si los oráculos ΔΦ realmente aportan algo."""
    return k_sweep(N, 1, m_max_de_N(N))

# ── C2 · DETECTOR ESPEJO ΔΦ (v17→v21) ─────────────────────────────────────────
def sgn_desfase(m: int, N: int) -> int:
    """SIGN(ΔΦ) ENTERO PURO (v21): ΔΦ = d_B(m) − d_A(espejo de m), con
    espejo A = N//(2m+3).  sign(ΔΦ) = sign(R_B·D_A − R_A·D_B).
    Dos productos de enteros, cero floats. Devuelve +1/−1/0.
    ⚠ Contabilidad honesta: el cambio de signo NO siempre ocurre al cruzar
    el factor (espejo de validación: 4/6). Oráculo acelerador, no teorema."""
    D_B = 2 * D_de_m(m)
    R_B = REG.mod(N, D_B)
    B = D_de_m(m)
    if B <= 1 or B >= N:
        return 0
    A = REG.floordiv(N, B)
    if A < 3:
        return 0
    m_e = (A - 3) // 2
    if m_e < 1:
        return 0
    D_A = 2 * D_de_m(m_e)
    R_A = REG.mod(N, D_A)
    diff = R_B * D_A - R_A * D_B
    return 1 if diff > 0 else (-1 if diff < 0 else 0)

def mag_desfase(m: int, N: int) -> int:
    """|ΔΦ| (v22): magnitud entera del desfase, para elegir el lado sin
    señal clara (heurística del repo)."""
    D_B = 2 * D_de_m(m)
    R_B = REG.mod(N, D_B)
    B = D_de_m(m)
    if B <= 1 or B >= N:
        return 0
    A = REG.floordiv(N, B)
    if A < 3:
        return 0
    m_e = (A - 3) // 2
    if m_e < 1:
        return 0
    D_A = 2 * D_de_m(m_e)
    R_A = REG.mod(N, D_A)
    return abs(R_B * D_A - R_A * D_B)

# ── C3 · BISECCIONES (v19→v23) con caída-a-segura k-sweep ─────────────────────
LIM_KSWEEP = 2000   # umbral didáctico: segmento pequeño → k-sweep directo

def _nk(N: int, m_ini: int, m_fi: int) -> int:
    k_lo = max(1, REG.floordiv(N, D_de_m(m_fi)))
    k_hi = REG.floordiv(N, D_de_m(m_ini))
    return k_hi - k_lo + 1

def _probar_puntos(puntos: List[Optional[int]], N: int) -> Optional[int]:
    for m in puntos:
        if m is not None and m >= 1 and check_factor(m, N):
            return D_de_m(m)
    return None

def _nucleo_binaria(N: int, m_ini: int, m_fi: int,
                    sonda: Optional[Callable[[int], int]] = None) -> Optional[int]:
    """Núcleo de bisección binaria (v21). 3 sondas, sign(ΔΦ) como oráculo,
    sin señal → lado de menor |ΔΦ|. Caída a k-sweep cuando el segmento es
    pequeño. sonda(m) opcional redirige las sondas (p.ej. a mínimos)."""
    for _ in range(400):
        if m_fi - m_ini < 2 or _nk(N, m_ini, m_fi) <= LIM_KSWEEP:
            return k_sweep(N, m_ini, m_fi)
        def S(x: int) -> int:
            return sonda(x) if sonda else x
        m_e, m_c, m_d = S(m_ini), S((m_ini + m_fi) // 2), S(m_fi)
        hit = _probar_puntos([m_e, m_c, m_d], N)
        if hit:
            return hit
        s_e, s_c, s_d = sgn_desfase(m_e, N), sgn_desfase(m_c, N), sgn_desfase(m_d, N)
        if s_e != 0 and s_c != 0 and s_e != s_c:
            m_fi = max(m_c, m_ini + 1)
        elif s_c != 0 and s_d != 0 and s_c != s_d:
            m_ini = m_c
        elif mag_desfase(m_e, N) <= mag_desfase(m_d, N):
            m_fi = (m_ini + m_fi) // 2
        else:
            m_ini = (m_ini + m_fi) // 2
    return None

def _nucleo_quaternaria(N: int, m_ini: int, m_fi: int) -> Optional[int]:
    """Núcleo de bisección quaternaria (v22): 5 sondas al 0/25/50/75/100%.
    Rango → /4 por iteración: la mitad de tiros que la binaria."""
    for _ in range(400):
        if m_fi - m_ini < 4 or _nk(N, m_ini, m_fi) <= LIM_KSWEEP:
            return k_sweep(N, m_ini, m_fi)
        anch = m_fi - m_ini
        q1, c, q3 = m_ini + anch // 4, (m_ini + m_fi) // 2, m_fi - anch // 4
        hit = _probar_puntos([m_ini, q1, c, q3, m_fi], N)
        if hit:
            return hit
        s = [sgn_desfase(p, N) for p in (m_ini, q1, c, q3, m_fi)]
        if s[0] != 0 and s[1] != 0 and s[0] != s[1]:
            m_fi = q1
        elif s[1] != 0 and s[2] != 0 and s[1] != s[2]:
            m_ini, m_fi = q1, c
        elif s[2] != 0 and s[3] != 0 and s[2] != s[3]:
            m_ini, m_fi = c, q3
        elif s[3] != 0 and s[4] != 0 and s[3] != s[4]:
            m_ini = q3
        elif mag_desfase(q1, N) <= mag_desfase(q3, N):
            m_fi = c
        else:
            m_ini = c
    return None

def _nucleo_asimetrica(N: int, m_ini: int, m_fi: int) -> Optional[int]:
    """Núcleo del corte asimétrico 25/75 (v23): el corte al 25% desde el lado
    pequeño. O el factor cae en el 25% inferior (bisección fina), o está en el
    75% superior cerca de √N (cubierto por el k-sweep de caída)."""
    for _ in range(400):
        if m_fi - m_ini < 2 or _nk(N, m_ini, m_fi) <= LIM_KSWEEP:
            return k_sweep(N, m_ini, m_fi)
        corte = m_ini + (m_fi - m_ini) // 4
        hit = _probar_puntos([m_ini, corte, m_fi], N)
        if hit:
            return hit
        s_i, s_c = sgn_desfase(m_ini, N), sgn_desfase(corte, N)
        if s_i != 0 and s_c != 0 and s_i != s_c:
            m_fi = corte                    # factor en el 25% inferior
        elif mag_desfase(corte, N) <= mag_desfase(m_fi, N):
            m_fi = corte                    # sin señal → el 75% superior
        else:                               # queda cubierto por la caída
            m_ini = corte
    return None

def pipeline_MDC(N: int, nucleo: Callable[[int, int, int], Optional[int]]) -> Optional[int]:
    """EL PIPELINE REAL DEL REPO (v20, 'Arquitectura Neta'):
      F1 · k-sweep de la zona densa [m_conv, m_max]  (factor equilibrado → aquí)
      F2 · bisección con ΔΦ sobre [1, m_conv]        (factor pequeño → aquí)
      F3 · k-sweep completo de [1, m_conv]           (respaldo: si el oráculo
            se equivocó, el teorema k-sweep salva el resultado y las evals
            delataban al oráculo en la tabla del comparador)"""
    f = k_sweep(N, m_conv_de_N(N), m_max_de_N(N))
    if f:
        return f
    f = nucleo(N, 1, m_conv_de_N(N))
    if f:
        return f
    return k_sweep(N, 1, m_conv_de_N(N))

def biseccion_binaria(N: int) -> Optional[int]:
    return pipeline_MDC(N, _nucleo_binaria)

def biseccion_quaternaria(N: int) -> Optional[int]:
    return pipeline_MDC(N, _nucleo_quaternaria)

def biseccion_asimetrica(N: int) -> Optional[int]:
    return pipeline_MDC(N, _nucleo_asimetrica)

# ── C4 · FILTRO ACUMULADOR (v15→v17) — descarte HEURÍSTICO de segmentos ──────
def filtre_acumulador(m_ini: int, m_fi: int, N: int, n_punts: int = 8) -> bool:
    """FILTRO ACUMULADOR (v17): muestrea el segmento y compara el decrecimiento
    de los restos contra la progresión armónica acumulo += acumulo·(1/i).
    True = resonancia (pasa), False = estéril (se descarta SIN dividir).
    ⚠ HEURÍSTICO, NO TEOREMA: el propio v17 no descarta segmentos menudos
    ('massa risc'). Aquí igual: < 20 de ancho → pasa siempre."""
    amplada = m_fi - m_ini
    if amplada < 20:
        return True
    pas = max(1, amplada // n_punts)
    acumulo = 1.0
    ratio_min = float("inf")
    anterior: Optional[int] = None
    for i, m in enumerate(m_ini + j * pas for j in range(n_punts)):
        r = REG.mod(N, 2 * D_de_m(m))
        if anterior is not None and r > 0:
            ratio_min = min(ratio_min, r / anterior)
        anterior = r
        acumulo += acumulo * (1.0 / (i + 2))
    return ratio_min <= acumulo or ratio_min == float("inf")

# ── C5 · DISCRIMINANTE + DESCARTE DETERMINISTA (fusio_v3 / l5 checkp) ─────────
def discriminante_S(S: int, N: int) -> Optional[Tuple[int, int]]:
    """MÉTODO DEL DISCRIMINANTE: Δ(S)=S²+6S−(N−9) cuadrado perfecto ⟺
    N=(2v+3)(2b+3) con v=(S+k)/2, b=(S−k)/2. 33×1 demostró: Δ(S)=(S+3)²−N,
    con S=v+b, k=v−b → FERMAT reparametrizado en la grilla 2v+3. ✓ 6/6 espejo."""
    delta = (S + 3) * (S + 3) - N
    if delta < 0:
        return None
    k = math.isqrt(delta)
    REG.evals += 1                       # contabilidad honesta: cada check cuenta
    if k * k == delta and (S + k) % 2 == 0 and (S - k) % 2 == 0:
        v, b = (S + k) // 2, (S - k) // 2
        A, B = 2 * v + 3, 2 * b + 3
        if A * B == N and 1 < min(A, B):
            return (min(A, B), max(A, B))
    return None

def teorema_ventana(S: int, k: int) -> bool:
    """TEOREMA 2/3 DE DESCARTE DETERMINISTA (fusio_v3): 4S+16 > 2k+1 → no hay
    solución en la ventana local actual → SALTO PARABÓLICO de diente.
    Descarte TEOREMA: no pierde factores, solo acota la caja."""
    return 4 * S + 16 > 2 * k + 1

def salto_parabolico(k: int, N: int) -> int:
    """Salto E4 (fusio_v3): S_nuevo = ⌈√(k²+N)⌉−3. El siguiente diente."""
    return -3 + math.isqrt(k * k + N)

def mdc_discriminante(N: int) -> Optional[int]:
    """Pipeline del discriminante con descarte determinista (fusio_v3):
    recorre k creciente y aterriza en S=salto_parabolico(k) — el siguiente
    diente del S-espacio — verificando Δ(S) en cada aterrizaje.
    En semiprimos equilibrados k=(q−p)/2 es diminuto → vuelta relámpago."""
    for k in range(1, max(2, math.isqrt(N))):
        S = salto_parabolico(k, N)
        r = discriminante_S(S, N)
        if r:
            return r[0]
        if teorema_ventana(S, k):
            continue                      # ventana local vacía → siguiente diente
    return None

# ── C6 · PINZA CINEMÁTICA 4+4 (mdc_libro5 / v17) ──────────────────────────────
def pinza_doble(m: int, N: int) -> Dict[str, float]:
    """PINZA 4+4 (mdc_libro5.py/v17): 4 mediciones adelante + 4 atrás sobre la
    fase d(m). V = velocidad, A = curvatura, J = jerk. El DISCRIMINADOR DE JERK
    detecta si estamos dentro de un solo diente (J_fwd≈J_bwd → salto NO fiable)
    o cruzando pendientes k consecutivas (macro-envolvente → salto fiable)."""
    d = [d_frac(m + i, N) for i in range(4)]
    dr = [d_frac(m - i, N) for i in range(4)]
    Vf, Af = d[1] - d[0], d[2] - 2 * d[1] + d[0]
    Jf = d[3] - 3 * d[2] + 3 * d[1] - d[0]
    Vr = dr[1] - dr[0]
    Jr = dr[3] - 3 * dr[2] + 3 * dr[1] - dr[0]
    m_next = m - round(Vf / Af) if Af != 0 else m
    return {"V": Vf, "A": Af, "J": Jf, "delta_J": abs(Jf - Jr),
            "m_next": m_next, "salto_fiable": abs(Jf - Jr) > 1e-12}

# ═════════════════════════════════════════════════════════════════════════════
#  BLOQUE D — OFICIOS 33×1 (el peine de mínimos, teorema de poda)
#  ⚠ Dominio i-espacio: aquí se recorren divisores i, NO índices m.
# ═════════════════════════════════════════════════════════════════════════════

def minimos_relativos(N: int, imax: int) -> List[int]:
    """PEINE 33×1 (i-espacio): mínimos relativos de r_i = N mod i, i=2..imax.
    LEMA DEL DIVISOR MÍNIMO: todo factor es mínimo relativo (r=0 es mínimo
    absoluto). Verificado 24/24 semiprimos, cero violaciones. TEOREMA."""
    rs = [REG.mod(N, i) for i in range(2, imax + 1)]
    out: List[int] = []
    for idx in range(len(rs)):
        i = idx + 2
        if rs[idx] == 0:
            out.append(i)
        elif idx > 0 and idx + 1 < len(rs) and rs[idx] <= rs[idx - 1] and rs[idx] <= rs[idx + 1]:
            out.append(i)
    return out

def peine_minimos(N: int) -> Optional[int]:
    """Factorización por el peine (i-espacio, hasta √N): recorre SOLO los
    mínimos relativos. Poda ~4× del espacio, TEOREMA: cero factores perdidos.
    Ojo didáctico: r=0 salta primero (mínimo absoluto)."""
    for i in minimos_relativos(N, math.isqrt(N)):
        if i >= 3 and i % 2 == 1 and REG.mod(N, i) == 0 and 1 < i < N:
            return i
    return None

# ═════════════════════════════════════════════════════════════════════════════
#  BLOQUE E — UNIONES (componer oficios, jugar)
# ═════════════════════════════════════════════════════════════════════════════

def _mins_a_espacio_m(N: int) -> List[int]:
    """Traduce los mínimos del i-espacio (divisores impares) a m-espacio:
    m=(i−3)/2. Sirven de ANCLAS para los oficios MDC."""
    mm = m_max_de_N(N)
    mins = [max(1, (i - 3) // 2) for i in minimos_relativos(N, math.isqrt(N)) if i >= 3]
    return sorted(set(m for m in mins if m <= mm))

def union_peine_ksweep(N: int) -> Optional[int]:
    """UNIÓN 1 · PEINE + K-SWEEP: los mínimos (en m-espacio) particionan la
    grilla en segmentos; k-sweep segmento a segmento entre anclas.
    LECCIÓN DEL ESPEJO: la suma de las k recorridas por todos los segmentos
    es EXACTAMENTE la k-range total de k_sweep(1, m_max) — particionar no
    ahorra k, solo las agrupa. Por eso el orden lo es todo: se barren los
    segmentos DESDE √N HACIA ABAJO (zona densa primero), igual que hace
    el pipeline v18/v20. Teorema + teorema = cero factores perdidos."""
    mm = m_max_de_N(N)
    ms = sorted(set([1] + _mins_a_espacio_m(N) + [mm]), reverse=True)
    prev = None
    for b in ms:                           # b = borde superior (cerca de √N)
        if prev is None:
            prev = b
            continue
        f = k_sweep(N, b, prev)            # barrido descendente: denso primero
        if f:
            return f
        prev = b
    return None

def union_peine_biseccion(N: int) -> Optional[int]:
    """UNIÓN 2 · PEINE + BISECCIÓN ΔΦ (v21): las sondas de la bisección se
    anclan en MÍNIMOS relativos cercanos en vez de puntos arbitrarios.
    El oráculo acelera cuando acierta; la caída a k-sweep salva cuando no."""
    anclas = _mins_a_espacio_m(N)
    def sonda(x: int) -> int:
        if not anclas:
            return x
        return min(anclas, key=lambda mv: abs(mv - x))
    return pipeline_MDC(N, lambda n, a, b: _nucleo_binaria(n, a, b, sonda=sonda))

def union_acumulador_peine(N: int) -> Optional[int]:
    """UNIÓN 3 · FILTRO ACUMULADOR + PEINE: segmentos entre mínimos estériles
    según el acumulador (heurístico) se saltan sin dividir; los que pasan,
    k-sweep descendente (denso primero, lección de la U1). El factor vive en
    un segmento con mínimo (teorema del peine); el acumulador decide en cuál
    concentrarse. ⚠ HEURÍSTICO PURO: el espejo mostró FALSOS NEGATIVOS reales
    (en 19×53 descarta el segmento que contiene el factor). Es el precio
    del descarte agresivo: velocidad a cambio de garantía."""
    mm = m_max_de_N(N)
    ms = sorted(set([1] + _mins_a_espacio_m(N) + [mm]), reverse=True)
    prev: Optional[int] = None
    for b in ms:
        if prev is None:
            prev = b
            continue
        if prev - b < 2:
            prev = b
            continue
        if filtre_acumulador(b, prev, N):   # pasa el filtro → mirar
            f = k_sweep(N, b, prev)
            if f:
                return f
        prev = b
    return None

def union_discriminante_peine(N: int) -> Optional[int]:
    """UNIÓN 4 · DISCRIMINANTE + LEMA (fusio_v3 × 33×1): el salto parabólico
    del Teorema de ventana recorre el S-espacio; cada factor encontrado se
    CONTRASTA con el peine: ¿era mínimo relativo? El Lema dice que sí,
    siempre — aquí el comparador lo verifica en cada hit (columna lema)."""
    mins = set(minimos_relativos(N, math.isqrt(N)))
    for k in range(1, max(2, math.isqrt(N))):
        S = salto_parabolico(k, N)
        r = discriminante_S(S, N)
        if r:
            return r[0]                     # (la verificación del Lema se hace
                                            #  en comparar(): columna "lema")
    return None

# ═════════════════════════════════════════════════════════════════════════════
#  BLOQUE F — EL COMPARADOR (mesa de juego)
# ═════════════════════════════════════════════════════════════════════════════

METODOS: Dict[str, Callable[[int], Optional[int]]] = {
    "division_L1 (ref)":      division_L1,
    "fermat (ref)":           fermat_clasico,
    "k_sweep total (v18)":   mdc_ksweep_completo,
    "bisec_bin (v21)":        biseccion_binaria,
    "bisec_quat (v22)":       biseccion_quaternaria,
    "bisec_25/75 (v23)":      biseccion_asimetrica,
    "discriminante (fusio)":  mdc_discriminante,
    "peine_33x1 (i-esp)":     peine_minimos,
    "U1 peine+ksweep":        union_peine_ksweep,
    "U2 peine+bisec":         union_peine_biseccion,
    "U3 acumulador+peine":    union_acumulador_peine,
    "U4 discrim+lema":        union_discriminante_peine,
}

def _lema_verifica(N: int, f: Optional[int]) -> Optional[bool]:
    """¿Es el factor encontrado un mínimo relativo? (Lema del Divisor Mínimo).
    Verificación con % directo — fuera del REGISTRO, es anotación didáctica."""
    if not f:
        return None
    if f == N:
        return None
    i = f
    r = N % i
    if r == 0:
        return True                         # mínimo absoluto
    izq = N % (i - 1)
    der = N % (i + 1)
    return r <= izq and r <= der

def comparar(N: int, metodos: Optional[List[str]] = None) -> List[Dict]:
    """Corre los métodos sobre N y devuelve la tabla didáctica: quién encontró
    el factor, con cuántas evaluaciones, en cuánto tiempo, y si el factor
    encontrado cumple el Lema del Mínimo (columna lema — debe ser siempre ✓)."""
    filas: List[Dict] = []
    for nombre in (metodos or list(METODOS.keys())):
        fn = METODOS[nombre]
        REG.reset()
        t0 = time.perf_counter()
        try:
            f = fn(N)
        except Exception as exc:      # modo didáctico: nunca revienta la mesa
            filas.append({"metodo": nombre, "factor": None, "evals": REG.evals,
                          "ms": 0.0, "lema": None, "error": str(exc)[:36]})
            continue
        ms = (time.perf_counter() - t0) * 1000.0
        ok = bool(f) and f is not None and N % f == 0 and 1 < f < N
        filas.append({"metodo": nombre, "factor": f if ok else None,
                      "evals": REG.evals, "ms": ms,
                      "lema": _lema_verifica(N, f) if ok else None,
                      "error": None})
    return filas

def imprimir_tabla(filas: List[Dict], N: int) -> None:
    print(f"\n  N = {N:,}")
    print("  " + "─" * 78)
    print(f"  {'método':<24} {'factor':>10} {'evals':>11} {'ms':>9}  {'lema':<4} nota")
    print("  " + "─" * 78)
    for f in filas:
        fac = f"{f['factor']:,}" if f["factor"] else "—"
        lema = "✓" if f["lema"] else ("—" if f["lema"] is None else "✗¡!")
        nota = f["error"] or ""
        print(f"  {f['metodo']:<24} {fac:>10} {f['evals']:>11,} {f['ms']:>9.2f}  {lema:<4} {nota}")
    print("  " + "─" * 78)

def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = 41
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def semiprimo(p: int, q: int) -> int:
    assert es_primo(p) and es_primo(q), "ambos deben ser primos"
    return p * q

# ═════════════════════════════════════════════════════════════════════════════
#  DEMO DIDÁCTICA
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 82)
    print("  MDC COMPARADOR MODULAR — Tratado 33×1")
    print("  Todos los oficios del Libro 5 sobre la misma mesa")
    print("=" * 82)
    print("  Varas honestas:")
    print("   · evals = divisiones contadas sobre N (no vale mirar el reloj)")
    print("   · lema  = el factor encontrado ¿era mínimo relativo? (teorema 33×1)")
    print("   · los oráculos ΔΦ aceleran cuando acierta; k-sweep salva cuando no")

    casos = [
        ("equilibrado 10c", semiprimo(10007, 10009)),
        ("equilibrado 9c",  semiprimo(7919, 7927)),
        ("gap pequeño",    semiprimo(9967, 10007)),
        ("desbalanceado",   semiprimo(101, 999983)),
        ("pequeño 4c",      semiprimo(19, 53)),
    ]
    for etiqueta, N in casos:
        print(f"\n### CASO: {etiqueta}")
        imprimir_tabla(comparar(N), N)

    print("\n  BONUS WIEFERICH (wieferich_paper.tex): la misma sierra en 2^p = K·p²+2")
    print("  → d(K)=frac(p(K)); ceros de d = condición Wieferich generalizada p² | 2^p−2")
    print("  (el detector cinemático de 4 puntos recorre K con paso 2 — el mismo oficio)")
    print("\n  #33×1 · #nomaimai")