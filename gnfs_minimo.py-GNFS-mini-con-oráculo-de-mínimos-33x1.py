#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
 33x1 :: GNFS-MINIMO — Criba de Mínimos Lisos aplicada a GNFS
 ataque a semiprimos · Autor del concepto: V. Manzanares Alberola
=====================================================================
 Pipeline (GNFS de grado 2, toy pero CORRECTO):
   1. Polinomio base-m:  n = m^2 + c1*m + c0,  f(x) = x^2 + c1*x + c0
      f(m) = n = 0 (mod n).  Cuerpo cuadratico imaginario (D < 0).
   2. ORACULO DE MINIMOS (el Lema 33x1): los candidatos (a, b) se
      generan SOLO en los minimos relativos de r_i = n mod i:
        a = b*m + s*i,  con i un minimo relativo, s = +-1
      => el lado racional R = a - b*m = +-i es EXACTAMENTE el resto
      minimo (pequeno por construccion, candidato liso del Lema).
   3. Relaciones: R B-lisa Y Norma(a - b*th) = a^2 + c1*a*b + c0*b^2
      B-lisa. Columnas algebraicas por PAR (p, raiz r = a*b^-1 mod p).
   4. Algebra lineal GF(2) -> dependencias.
   5. Raiz algebraica en el cuerpo cuadratico: beta = x + y*th;
      gamma = a + b*sqrt(D) con a^2 = (+-A' +- 2v)/4, v^2 = Norm(beta).
      Y = phi(gamma) = a + b*(2m + c1)  (mod n),  u0^2 = prod R.
      gcd(Y - u0, n) parte n.
 Uso:
      python gnfs_minimo.py              # ataque en cascada (demo)
      python gnfs_minimo.py 100160063    # atacar un semiprimo
=====================================================================
"""
import math
import random
import sys
from typing import List, Optional, Tuple, Dict


# ------------------------------------------------------------------ utils
def primes_upto(B: int) -> List[int]:
    sieve = bytearray([1]) * (B + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(B ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p:: p] = bytearray(len(sieve[p * p:: p]))
    return [i for i in range(2, B + 1) if sieve[i]]


def smooth_map(x: int, P: List[int]) -> Optional[Dict[int, int]]:
    """Factoriza x sobre P. Devuelve {primo: exp} (con -1 si negativo) o None."""
    if x == 0:
        return None
    out: Dict[int, int] = {}
    if x < 0:
        out[-1] = 1
        x = -x
    for p in P:
        while x % p == 0:
            out[p] = out.get(p, 0) + 1
            x //= p
    return out if x == 1 else None


def relative_minima(n: int, W: int) -> List[int]:
    """La secuencia i de minimos: minimos relativos de n mod i, i=2..W."""
    out = []
    prev, cur = n % 2, n % 3
    for i in range(3, W + 1):
        nxt = n % (i + 1)
        if cur <= prev and cur <= nxt:
            out.append(i)
        prev, cur = cur, nxt
    return out


def isqrt_big(V: int) -> int:
    if V < 0:
        return -1
    x = 1 << ((V.bit_length() // 2) + 1)
    while True:
        nx = (x + V // x) >> 1
        if nx >= x:
            return x
        x = nx


def nullspace_rows(rows: List[int], ncols: int) -> List[int]:
    """Dependencias (nucleo) de un sistema GF(2) con filas como bitsets."""
    nf = len(rows)
    # transponer: columna c -> bitset de filas con bit c
    t = []
    for c in range(ncols):
        v = 0
        for k in range(nf):
            if (rows[k] >> c) & 1:
                v |= 1 << k
        t.append(v)
    where = [-1] * nf
    r = 0
    for c in range(nf):
        p = -1
        for k in range(r, len(t)):
            if (t[k] >> c) & 1:
                p = k
                break
        if p < 0:
            continue
        t[r], t[p] = t[p], t[r]
        where[c] = r
        for k in range(len(t)):
            if k != r and ((t[k] >> c) & 1):
                t[k] ^= t[r]
        r += 1
    deps = []
    for c in range(nf):
        if where[c] == -1:
            v = 1 << c
            for c2 in range(nf):
                if where[c2] >= 0 and ((t[where[c2]] >> c) & 1):
                    v |= 1 << c2
            deps.append(v)
    return deps


# ------------------------------------------------------------------ nucleo
def collect_relations(n: int, B: int, W: int, bmax: int):
    """Criba SOLO en los minimos relativos (oraculo 33x1)."""
    m = math.isqrt(n)
    c1 = (n - m * m) // m
    c0 = n - m * m - c1 * m
    P = primes_upto(B)
    M = relative_minima(n, W)
    rels = []
    tested = 0
    for b in range(1, bmax + 1):
        for i in M:
            for s in (1, -1):
                a = b * m + s * i
                if math.gcd(a, b) != 1:
                    continue
                R = a - b * m                      # = +-i (el minimo)
                Na = a * a + c1 * a * b + c0 * b * b
                tested += 1
                if Na < 2:
                    continue
                er = smooth_map(R, P)
                if er is None:
                    continue
                ea = smooth_map(Na, P)
                if ea is None:
                    continue
                rels.append((a, b, R, Na, er, ea))
    return rels, tested, (m, c1, c0), P


def build_matrix(rels, b_of) -> Tuple[List[int], Dict[str, int]]:
    """Columnas: signo, racional p, algebraico (p, r)."""
    cols: Dict[str, int] = {}

    def col(k):
        if k not in cols:
            cols[k] = len(cols)
        return cols[k]

    col("s")
    rows = []
    for (a, b, R, Na, er, ea) in rels:
        row = 0
        if er.get(-1, 0) & 1:
            row |= 1 << col("s")
        for (p, e) in er.items():
            if p > 0 and (e & 1):
                row |= 1 << col("r%d" % p)
        for (p, e) in ea.items():
            if b % p == 0:
                continue
            r = (a * pow(b, p - 2, p)) % p
            if e & 1:
                row |= 1 << col("a%d_%d" % (p, r))
        rows.append(row)
    return rows, cols


def finish(n, rels, deps, params):
    """Raiz algebraica en el cuerpo cuadratico + gcd."""
    m, c1, c0 = params
    C1, C0 = c1, c0
    M2 = 2 * m + c1
    factor = None
    for dep in deps:
        bx, by, U, V = 1, 0, 1, 1
        for k in range(len(rels)):
            if (dep >> k) & 1:
                (a, b, R, Na, er, ea) = rels[k]
                # (bx + by*th) * (a - b*th),  th^2 = -c1*th - c0
                X = bx * a + by * b * C0
                Yv = by * a - bx * b + by * b * C1
                bx, by = X, Yv
                U *= R
                V *= Na
        u0 = isqrt_big(abs(U))
        if u0 * u0 != abs(U):
            continue
        v = isqrt_big(V)
        if v * v != V:
            continue
        Ap = 2 * bx - by * C1
        Bp = by
        for sa in (1, -1):
            for sv in (1, -1):
                num = sa * Ap + sv * 2 * v
                if num < 0 or num % 4:
                    continue
                a2 = num // 4
                a = isqrt_big(a2)
                if a * a != a2 or a == 0:
                    continue
                if Bp % (4 * a):
                    continue
                b = Bp // (4 * a)
                if b == 0:
                    continue
                Y = (a + b * M2) % n
                for su in (1, -1):
                    u0m = (su * u0) % n
                    for d in ((Y - u0m) % n, (Y + u0m) % n):
                        g = math.gcd(d, n)
                        if 1 < g < n:
                            return g
    return factor


def gnfs_minimo(n: int, B=None, W=None, bmax=None, verbose=False):
    """Ataca n con GNFS-mini cribando SOLO en los minimos relativos."""
    digits = len(str(n))
    if B is None:
        B = 200 if digits <= 7 else 1000
    if W is None:
        W = 1500 if digits <= 7 else 6000
    if bmax is None:
        bmax = 12 if digits <= 7 else 16
    # fase 1: recolectar con escalado automatico hasta tener mas filas que columnas
    for intento in range(4):
        rels, tested, params, P = collect_relations(n, B, W, bmax)
        rows, cols = build_matrix(rels, None)
        if verbose:
            print(f"  [criba] {len(rels)} relaciones / {len(cols)} columnas "
                  f"({tested} candidatos del oraculo probados)")
        if len(rels) > len(cols) + 8:
            break
        B = int(B * 1.6)
        W = int(W * 1.6)
        bmax = bmax + 6
    deps = nullspace_rows(rows, len(cols))
    if verbose:
        print(f"  [algebra] {len(deps)} dependencias GF(2)")
    g = finish(n, rels, deps, params)
    return (g, n // g) if g else None


# ------------------------------------------------------------------ main
def main():
    print("=" * 63)
    print(" 33x1 :: GNFS-MINIMO  ::  Lee fluye por la red tras el gran GNFS")
    print("=" * 63)
    args = [x for x in sys.argv[1:] if not x.startswith("-")]
    verbose = "-v" in sys.argv
    if args:
        targets = [int(x) for x in args]
    else:
        # cascada demo: semiprimos crecientes
        targets = [1009 * 1013, 7919 * 7927, 10007 * 10009, 31337 * 31357]
    for n in targets:
        print(f"\n[ATAQUE] n = {n}")
        got = gnfs_minimo(n, verbose=verbose)
        if got:
            p, q = sorted(got)
            ok = "OK" if p * q == n else "??"
            print(f"  => {n} = {p} x {q}   [{ok}]")
        else:
            print("  => sin factor (sube B/W o mas dependencias)")


if __name__ == "__main__":
    main()