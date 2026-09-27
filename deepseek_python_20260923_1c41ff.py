# -*- coding: utf-8 -*-
"""
MDC v18 INSTRUMENTADO — contadores de iteraciones reales
Víctor Manzanares Alberola · VMA / 33x1
"""
from fractions import Fraction
import math
import time

# ── CONTADORES GLOBALES ──────────────────────────────────────────────────
class Contadores:
    def __init__(self):
        self.iter_k_densa = 0
        self.iter_k_espiral = 0
        self.iter_k_bisect = 0
        self.comprob_m_rueda = 0
        self.comprob_m_criba = 0
        self.segmentos_espiral = 0
        self.bisecciones = 0
        self.d_frac_llamadas = 0

    def reset(self):
        self.__init__()

    def __repr__(self):
        return (f"Contadores(\n"
                f"  iter_k_densa   = {self.iter_k_densa}\n"
                f"  iter_k_espiral = {self.iter_k_espiral}\n"
                f"  iter_k_bisect  = {self.iter_k_bisect}\n"
                f"  comprob_m_rueda= {self.comprob_m_rueda}\n"
                f"  comprob_m_criba= {self.comprob_m_criba}\n"
                f"  segmentos_esp  = {self.segmentos_espiral}\n"
                f"  bisecciones    = {self.bisecciones}\n"
                f"  d_frac_llamadas= {self.d_frac_llamadas}\n"
                f")")

C = Contadores()

# ── CONSTANTES ───────────────────────────────────────────────────────────
PRIMOS    = [2, 3, 5, 7, 11, 13, 17, 19, 23]
PRIMORIAL = math.prod(PRIMOS)
E_MINUS_1_OVER_2 = (math.e - 1) / 2   # ≈ 0.8591409

# ── RODA ─────────────────────────────────────────────────────────────────
def pasa_rueda(m):
    C.comprob_m_rueda += 1
    if m < 1:
        return False
    return math.gcd(2 * m + 3, PRIMORIAL) == 1

def proper_valid(m, pas=1):
    for _ in range(500):
        if m < 1:
            return None
        if pasa_rueda(m):
            return m
        m += pas
    return None

# ── FUNCIÓ D'ONA I ESPELL ────────────────────────────────────────────────
def d_frac(m, N):
    C.d_frac_llamadas += 1
    D = 2 * (2 * m + 3)
    return Fraction(N % D, D) - Fraction(1, 2)

def m_espell(m, N):
    B = 2 * m + 3
    if B <= 1 or B >= N:
        return None
    A = N // B
    if A < 3:
        return None
    me = (A - 3) // 2
    return me if me >= 1 else None

def desfase_espell(m, N):
    dB = d_frac(m, N)
    me = m_espell(m, N)
    if me is None:
        return Fraction(0)
    return dB - d_frac(me, N)

def check_factor(m, N):
    D = 2 * m + 3
    return D > 1 and D < N and (N % D == 0)

# ── K-SWEEP ──────────────────────────────────────────────────────────────
def k_sweep(N, m_ini, m_fi, verbose=False):
    if m_ini < 1:
        m_ini = 1
    if m_fi < m_ini:
        return None
    pos_ini = 2 * m_ini + 3
    pos_fi  = 2 * m_fi  + 3
    k_lo = max(1, N // pos_fi)
    k_hi = N // pos_ini
    if k_lo > k_hi:
        return None
    n_k = k_hi - k_lo + 1
    if verbose:
        print(f"      [k_sweep] k∈[{k_lo:,},{k_hi:,}] n_k={n_k:,}")
    for k in range(k_lo, k_hi + 1):
        C.iter_k_densa += 1   # comptador principal
        candidat = N // k
        if candidat < 3:
            continue
        if candidat % 2 == 0:
            continue
        if N % candidat == 0 and 1 < candidat < N:
            return candidat
    return None

def k_sweep_bisectat(N, m_ini, m_fi, llindar_k=1_000_000,
                     profunditat=50, verbose=False):
    for it in range(profunditat):
        pos_i = 2 * m_ini + 3
        pos_f = 2 * m_fi  + 3
        k_lo  = max(1, N // pos_f)
        k_hi  = N // pos_i
        n_k   = k_hi - k_lo + 1
        if n_k <= llindar_k:
            # k-sweep directe, però comptabilitzat com espiral
            for k in range(k_lo, k_hi + 1):
                C.iter_k_espiral += 1
                candidat = N // k
                if candidat < 3 or candidat % 2 == 0:
                    continue
                if N % candidat == 0 and 1 < candidat < N:
                    return candidat
            return None
        # Bisecció
        C.bisecciones += 1
        m_c  = (m_ini + m_fi) // 2
        m_e  = proper_valid(m_ini, 1)
        m_cm = proper_valid(m_c,  1)
        m_f  = proper_valid(m_fi, -1)
        if not (m_e and m_cm and m_f):
            break
        # Comprovació directa dels punts de bisecció
        for mp in [m_e, m_cm, m_f]:
            r = k_sweep(N, mp, mp, verbose=False)
            if r:
                return r
        df_e  = desfase_espell(m_e,  N)
        df_cm = desfase_espell(m_cm, N)
        df_f  = desfase_espell(m_f,  N)
        if df_e * df_cm < 0:
            m_fi = m_cm
        elif df_cm * df_f < 0:
            m_ini = m_cm
        else:
            pos_e = 2 * m_e + 3
            pos_f2 = 2 * m_f + 3
            R2_e = (N % pos_e) % (pos_e - 1) if pos_e > 1 else 10**18
            R2_f = (N % pos_f2) % (pos_f2 - 1) if pos_f2 > 1 else 10**18
            if R2_e <= R2_f:
                m_fi = m_cm
            else:
                m_ini = m_cm
    return None

# ── ESPIRAL ──────────────────────────────────────────────────────────────
def generar_sondes_sota_mconv(m_conv, N):
    segments = []
    salta    = Fraction(m_conv, 2)
    posicio  = Fraction(m_conv)
    for i in range(1, 200):
        m_fi_seg = int(posicio)
        posicio -= salta
        m_ini_seg = max(1, int(posicio))
        if m_fi_seg >= 1 and m_fi_seg > m_ini_seg:
            segments.append((m_ini_seg, m_fi_seg))
            C.segmentos_espiral += 1
        if m_ini_seg <= 1:
            break
        salta = salta * Fraction(1, i + 1)
        if salta < Fraction(1, 4):
            segments.append((1, int(posicio)))
            C.segmentos_espiral += 1
            break
    segments.sort(key=lambda s: s[1], reverse=True)
    return segments

# ── ORQUESTRADOR INSTRUMENTAT ────────────────────────────────────────────
def mdc_v18_inst(N, verbose=True):
    C.reset()
    t0 = time.perf_counter()

    if verbose:
        print(f"\n{'═'*72}")
        print(f"  MDC v18 INSTRUMENTADO — N = {N:,}  ({len(str(N))} dígits)")
        print(f"{'═'*72}")

    # F0: precondicions
    for p in PRIMOS:
        if N % p == 0 and p < N:
            t_ms = (time.perf_counter() - t0) * 1000
            if verbose:
                print(f"  [F0] Factor trivial: {p}")
            return p, t_ms, C
    r = math.isqrt(N)
    if r * r == N:
        t_ms = (time.perf_counter() - t0) * 1000
        if verbose:
            print(f"  [F0] Quadrat perfecte: {r}")
        return r, t_ms, C

    m_max  = (math.isqrt(N) - 3) // 2
    m_conv = int(E_MINUS_1_OVER_2 * m_max)

    # Criba roda fins a 2M (o √N si és menor)
    lim_criba = min(math.isqrt(N) + 1, 2_000_000)
    for m_c in range(1, lim_criba):
        C.comprob_m_criba += 1
        if pasa_rueda(m_c):
            D = 2 * m_c + 3
            if N % D == 0 and D < N:
                t_ms = (time.perf_counter() - t0) * 1000
                if verbose:
                    print(f"  [F0] Factor petit (criba): {D:,}")
                return D, t_ms, C

    if verbose:
        print(f"  [F0] m_max={m_max:,}  m_conv={m_conv:,}  "
              f"(zona densa = {m_max-m_conv:,})")

    # F1: k-sweep zona densa
    if verbose:
        print(f"  [F1] K-sweep zona densa...")
    pos_conv = 2 * m_conv + 3
    pos_max  = 2 * m_max  + 3
    k_lo_d = max(1, N // pos_max)
    k_hi_d = N // pos_conv
    n_k_d  = k_hi_d - k_lo_d + 1
    if verbose:
        print(f"       k∈[{k_lo_d:,},{k_hi_d:,}]  n_k={n_k_d:,}")
    factor = k_sweep(N, m_conv, m_max, verbose=False)
    if factor:
        t_ms = (time.perf_counter() - t0) * 1000
        if verbose:
            print(f"  ✅ Factor trobat a zona densa: {factor:,}")
        return factor, t_ms, C
    if verbose:
        print(f"       ✗ No trobat a zona densa.")

    # F2: espiral
    if verbose:
        print(f"  [F2] Espiral 1/(2·i!) sota m_conv...")
    segments = generar_sondes_sota_mconv(m_conv, N)
    if verbose:
        print(f"       {len(segments)} segments generats")
    for idx, (mi, mf) in enumerate(segments):
        factor = k_sweep_bisectat(N, mi, mf, llindar_k=1_000_000,
                                  profunditat=50, verbose=False)
        if factor:
            t_ms = (time.perf_counter() - t0) * 1000
            if verbose:
                print(f"  ✅ Factor trobat a espiral #{idx+1}: {factor:,}")
            return factor, t_ms, C

    t_ms = (time.perf_counter() - t0) * 1000
    if verbose:
        print(f"  ✗ No trobat.")
    return None, t_ms, C

# ── PROVES ───────────────────────────────────────────────────────────────
def prova(N, desc):
    print(f"\n{'█'*72}")
    print(f"  📋 {desc}")
    print(f"  N = {N:,}")
    factor, t_ms, cont = mdc_v18_inst(N, verbose=True)
    print(f"\n  Resultat: factor={factor:,}  temps={t_ms:.3f} ms")
    print(f"  {cont}")
    if factor:
        assert N % factor == 0
        print(f"  ✅ {factor:,} × {N//factor:,}")
    return factor, t_ms, cont

if __name__ == "__main__":
    casos = [
        (59 * 61,        "59 × 61  (q−p = 2 < √N ≈ 60)"),
        (59 * 1009,      "59 × 1009  (q−p = 950 > √N ≈ 244)"),
        (100003 * 100019,"100003 × 100019  (q−p = 16 < √N ≈ 100011)"),
    ]
    resultats = []
    for N, desc in casos:
        f, t, c = prova(N, desc)
        resultats.append((N, desc, f, t, c))

    print(f"\n\n{'█'*72}")
    print(f"  RESUM FINAL")
    print(f"{'█'*72}")
    for N, desc, f, t, c in resultats:
        print(f"\n  {desc}")
        print(f"    Factor: {f:,}   Temps: {t:.3f} ms")
        print(f"    iter_k_densa={c.iter_k_densa:,}  "
              f"iter_k_espiral={c.iter_k_espiral:,}  "
              f"biseccions={c.bisecciones}")
        print(f"    comprob_m_rueda={c.comprob_m_rueda:,}  "
              f"comprob_m_criba={c.comprob_m_criba:,}  "
              f"segmentos_esp={c.segmentos_espiral}")