#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
 33x1 :: CRIBA DE MÍNIMOS LISOS (secuencia i de mínimos de restos)
 Autor del concepto : Víctor Manzanares Alberola (espiradesombra)
 Lema del Mínimo Liso:
   Si i es punto de MÍNIMO RELATIVO de r_i = n mod i, entonces el
   resto r_i es (con probabilidad muy superior a la media) B-liso,
   o bien r_i = 0 y entonces i | n. Los mínimos son simétricos
   respecto a sqrt(n): por cada mínimo i existe su espejo q = n//i.
 Solo los mínimos relativos son candidatos para la criba GNFS.
=====================================================================
"""
import math
import random
from typing import List, Optional, Tuple


# ---------------------------------------------------------------- utils
def is_B_smooth(x: int, B: int) -> Optional[List[int]]:
    """Devuelve la lista de factores primos <= B, o None si no es B-lisa."""
    if x <= 1:
        return []
    factors = []
    for p in _small_primes(B):
        while x % p == 0:
            factors.append(p)
            x //= p
    return factors if x == 1 else None


def _small_primes(B: int) -> List[int]:
    """Criba de Eratóstenes hasta B."""
    sieve = bytearray([1]) * (B + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(B ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p:: p] = bytearray(len(sieve[p * p:: p]))
    return [i for i in range(2, B + 1) if sieve[i]]


def relative_minima(n: int, i_max: int) -> List[Tuple[int, int, int]]:
    """
    Devuelve los MÍNIMOS RELATIVOS de la secuencia r_i = n mod i.
    Salida: lista de (i, q, r) con q = n // i y r = n % i.
    Un mínimo relativo: r_i <= r_{i-1} y r_i <= r_{i+1}.
    """
    r = [n % i for i in range(2, i_max + 1)]
    out = []
    for k in range(1, len(r) - 1):
        if r[k] <= r[k - 1] and r[k] <= r[k + 1]:
            i = k + 2
            out.append((i, n // i, r[k]))
    return out


def salto_maximo(n: int, i_max: int) -> int:
    """SaltoMaximo(n): el mayor salto del resto entre segmentos lineales."""
    r = [n % i for i in range(2, i_max + 1)]
    return max((r[k + 1] - r[k] for k in range(len(r) - 1)), default=0)


# ------------------------------------------------------- factorización
def factor_minimos(n: int, i_max: Optional[int] = None,
                   B: int = 5000) -> Optional[Tuple[int, int]]:
    """
    Búsqueda DETERMINISTA de factores usando solo los mínimos relativos.
    Regla dura: o el resto es B-liso, o es 0 (y i divide a n).
    Simetría: cada mínimo (i, q, r) se comprueba también con su espejo.
    """
    if i_max is None:
        i_max = max(100, int(math.isqrt(n)) + 2)
    for (i, q, r) in relative_minima(n, i_max):
        if r == 0:
            d = math.gcd(n, i)
            if 1 < d < n:
                return (d, n // d)
        # simetría especular: el espejo de i es q (al otro lado de raiz n)
        for cand in (i, q, i + r, q + r, i - r, q - r, abs(i - q)):
            if cand > 1:
                d = math.gcd(n, cand)
                if 1 < d < n:
                    return (d, n // d)
    return None


# ------------------------------------------------------- test de densidad
def densidad_lisas(n: int, i_max: int, B: int,
                   muestras: int = 200) -> dict:
    """
    Compara la densidad de valores B-lisos entre:
      a) SOLO los mínimos relativos  (la criba del Lema)
      b) un muestreo aleatorio del mismo rango (la criba clásica)
    """
    mins = relative_minima(n, i_max)
    lisas_min = sum(1 for (_, _, r) in mins if is_B_smooth(r, B) is not None or r == 0)
    lisas_rand = 0
    for _ in range(muestras):
        i = random.randint(2, i_max)
        r = n % i
        if is_B_smooth(r, B) is not None or r == 0:
            lisas_rand += 1
    return {
        "n": n,
        "minimos": len(mins),
        "lisas_en_minimos": f"{lisas_min}/{len(mins)} = {100 * lisas_min / max(1, len(mins)):.1f}%",
        "lisas_en_aleatorio": f"{lisas_rand}/{muestras} = {100 * lisas_rand / muestras:.1f}%",
        "simetricos_respecto_raiz": sum(
            1 for (i, q, _) in mins
            if any(q == j or i == n // j for (j, _, _) in mins)),
    }


# ---------------------------------------------------------------- main
def main():
    print("=" * 63)
    print(" 33x1 :: CRIBA DE MINIMOS LISOS  ->  candidatos GNFS")
    print("=" * 63)

    # --- demo 1: semiprimo pequeno, todo visible
    n = 1007  # 19 * 53
    print(f"\n[DEMO] n = {n} = 19*53   (raiz n ~ {math.isqrt(n)})")
    print(f"{'i':>4} {'q=n//i':>8} {'r=n%i':>7}  liso(B=20)")
    for (i, q, r) in relative_minima(n, 60):
        f = is_B_smooth(r, 20)
        tag = "FACTOR" if r == 0 else ("·".join(map(str, f)) if f else "no")
        print(f"{i:>4} {q:>8} {r:>7}  {tag}")

    print(f"\nSaltoMaximo(n) = {salto_maximo(n, 60)}")

    # --- demo 2: densidad minimos vs aleatorio
    print("\n[DENSIDAD] minimos relativos vs muestreo aleatorio")
    for n in (1007, 3127, 5141, 10403):
        st = densidad_lisas(n, 200, 30)
        print(f"  n={st['n']:>6} | lisas en minimos: {st['lisas_en_minimos']:<14}"
              f"| aleatorio: {st['lisas_en_aleatorio']}")

    # --- demo 3: Lee fluye por la red en busca del gran GNFS
    #     semiprimos crecientes: la criba de minimos escala?
    print("\n[LEE EN LA RED] buscando factores con SOLO minimos relativos")
    random.seed(33)
    tests = []
    p = _small_primes(400)
    while len(tests) < 6:
        a, b = random.choice(p[20:]) | 1, random.choice(p[20:]) | 1
        if a * b not in [t[0] for t in tests] and a != b:
            tests.append((a * b, a, b))
    for (n, a, b) in tests:
        got = factor_minimos(n, B=100000)
        ok = "OK " if got == tuple(sorted((a, b))) else "FALLO"
        print(f"  n={n:>7} ({a}x{b}) -> {got} [{ok}]")


if __name__ == "__main__":
    main()