#!/usr/bin/env python3
"""
kilometro_zonas.py — C1 medio, C2 1.5 vueltas, C2.5 un cuarto + censo de lastres.

Zonas:
  ALTA / MEDIO / BAJA  — stock aparcado (cota)
  OBJ                  — perneado al objeto (viaja con s)
  PATH_ALTA / PATH_MEDIO / PATH_BAJA — perneado al recorrido

Perneo objeto↔recorrido: misma cota, ΔPE≈0, coste δ.
C2 x.5: los de PATH cambian de extremo (ALTA↔BAJA). Eso SÍ mueve cota; va DENTRO de C2.
C3 genera (uno inverso). C3.0/C3.1 solo pernos.

  python3 kilometro_zonas.py
  python3 kilometro_zonas.py --stock 6 --dkp
"""
from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List

G = 9.81
ZONAS = ("ALTA", "MEDIO", "BAJA", "OBJ", "PATH_ALTA", "PATH_MEDIO", "PATH_BAJA")


class P:
    m_obj = 30.0
    m_lastre = 10.0
    dh = 15.0
    eta_gen = 0.85
    eta_mot = 0.90
    drag = 0.06
    e_perno = 1.5
    n_pernos = 4
    frac_c1 = 0.5
    frac_c25 = 0.25
    vueltas_c2 = 1.5
    frac_c3 = 1.0
    stock = 5
    dkp = False


def mgh(p: P) -> float:
    return p.m_lastre * G * p.dh


def censo(lastres: List[dict]) -> Dict[str, int]:
    d = {z: 0 for z in ZONAS}
    for L in lastres:
        d[L["zona"]] += 1
    return d


def fmt_censo(d: Dict[str, int]) -> str:
    bits = [f"{z}:{d[z]}" for z in ZONAS if d[z]]
    return "  ".join(bits) if bits else "(vacío)"


def pin(p: P, ledger: dict) -> None:
    ledger["E_pin"] += p.e_perno * p.n_pernos


def mover(lastres: List[dict], origen: str, destino: str, n: int = 1) -> int:
    k = 0
    for L in lastres:
        if k >= n:
            break
        if L["zona"] == origen:
            L["zona"] = destino
            k += 1
    return k


def gen_recto(p: P, frac: float) -> float:
    return p.eta_gen * (1 - p.drag) * mgh(p) * frac


def ciclo(p: P) -> dict:
    lastres = [{"id": i, "zona": "ALTA"} for i in range(p.stock)]
    log: List[str] = []
    led = {
        "E_gen_c1": 0.0,
        "E_gen_c2": 0.0,
        "E_gen_c25": 0.0,
        "E_gen_c3": 0.0,
        "E_mot_c2": 0.0,
        "E_pin": 0.0,
        "s": 0.0,
    }
    snaps = []

    def shot(tag: str) -> None:
        d = censo(lastres)
        snaps.append({"paso": tag, "s": round(led["s"], 3), "zonas": d})
        log.append(f"{tag:12s} s={led['s']:.2f}  {fmt_censo(d)}")

    shot("inicio")

    # --- C1: MEDIO recorrido RECTO, genera ---
    tomados = mover(lastres, "ALTA", "OBJ", 1)
    pin(p, led)
    e = gen_recto(p, p.frac_c1)
    led["E_gen_c1"] += e
    led["s"] = p.frac_c1
    # suelta al recorrido a media cota (perneo OBJ → PATH, misma cota)
    pin(p, led)
    mover(lastres, "OBJ", "PATH_MEDIO", tomados)
    shot("C1 medio")

    # --- C2: 1.5 vueltas (invert + regen + x.5 cambio de extremo) ---
    n_path = sum(1 for L in lastres if L["zona"].startswith("PATH"))
    m_spin = p.m_obj + n_path * p.m_lastre
    w_giro = m_spin * G * p.dh
    full = int(p.vueltas_c2)  # 1
    half = p.vueltas_c2 - full  # 0.5
    led["E_gen_c2"] += p.eta_gen * (1 - p.drag) * w_giro * full
    mot_giro = w_giro / p.eta_mot * (1 + p.drag) * full
    # x.5: PATH_BAJA ↔ PATH_ALTA; PATH_MEDIO se queda (cota media)
    n_swap = 0
    if abs(half - 0.5) < 1e-9:
        for L in lastres:
            if L["zona"] == "PATH_ALTA":
                L["zona"] = "PATH_BAJA"
                n_swap += 1
            elif L["zona"] == "PATH_BAJA":
                L["zona"] = "PATH_ALTA"
                n_swap += 1
            elif L["zona"] == "PATH_MEDIO":
                # 0.5 desde medio → el otro medio; etiquetamos BAJA (extremo nuevo)
                L["zona"] = "PATH_BAJA"
                n_swap += 1
        mot_x5 = n_swap * mgh(p) / p.eta_mot
        if p.dkp:
            mot_x5 = 0.0
        led["E_mot_c2"] += mot_giro + mot_x5
        log.append(
            f"C2 1.5vueltas  giro {mot_giro:.0f} J  x.5 n={n_swap} "
            f"{'DKP' if p.dkp else 'eje'} {mot_x5:.0f} J  regen {led['E_gen_c2']:.0f} J"
        )
    else:
        led["E_mot_c2"] += mot_giro
    shot("C2 1.5v")

    # --- C2.5: UN CUARTO de recorrido RECTO, genera ---
    tomados = mover(lastres, "PATH_BAJA", "OBJ", 1) or mover(lastres, "ALTA", "OBJ", 1)
    pin(p, led)
    e = gen_recto(p, p.frac_c25)
    led["E_gen_c25"] += e
    led["s"] = min(1.0, led["s"] + p.frac_c25)  # 0.50+0.25=0.75
    pin(p, led)
    mover(lastres, "OBJ", "PATH_BAJA", tomados)
    shot("C2.5 1/4")

    # --- C3.0 perneo, C3 UNO inverso GENERA, C3.1 desperneo ---
    tomados = mover(lastres, "ALTA", "OBJ", 1) or mover(lastres, "PATH_ALTA", "OBJ", 1)
    pin(p, led)  # C3.0
    e = gen_recto(p, p.frac_c3)
    led["E_gen_c3"] += e
    led["s"] = 0.0  # sentido inverso, acaba listo para C1
    pin(p, led)  # C3.1
    # lastre al recorrido en el extremo donde C2 lo pondrá de ALTA en el siguiente x.5
    mover(lastres, "OBJ", "PATH_BAJA", tomados)
    shot("C3 uno inv")

    gen = led["E_gen_c1"] + led["E_gen_c2"] + led["E_gen_c25"] + led["E_gen_c3"]
    paga = led["E_mot_c2"] + led["E_pin"]
    return {
        "frac": {"C1": p.frac_c1, "C2_vueltas": p.vueltas_c2, "C2.5": p.frac_c25, "C3": p.frac_c3},
        "ledger": {k: round(v, 2) if isinstance(v, float) else v for k, v in led.items()},
        "E_gen": round(gen, 2),
        "E_paga": round(paga, 2),
        "neto": round(gen - paga, 2),
        "eta": round(gen / paga, 4) if paga else None,
        "censo_final": censo(lastres),
        "snaps": snaps,
        "log": log,
        "opinion": (
            "C1 1/2 + C2.5 1/4 = 3/4 del tramo: no cierras el recto "
            "(el cuarto que falta es la PE que no tiras). "
            "C2 1.5 = 1 invert + 0.5 cambio de extremo. Coherente con IMPORTANTE.txt."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stock", type=int, default=5)
    ap.add_argument("--dkp", action="store_true")
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-20",
    )
    a = ap.parse_args()
    p = P()
    p.stock = a.stock
    p.dkp = a.dkp
    r = ciclo(p)
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "zonas_dkp.json" if p.dkp else "zonas.json")
    with open(path, "w") as f:
        json.dump(r, f, indent=2, ensure_ascii=False)

    print("C1=1/2  C2=1.5 vueltas  C2.5=1/4  C3=uno inverso (genera)")
    print("dkp", p.dkp, "stock", p.stock)
    print()
    print("CENSO")
    for s in r["snaps"]:
        print(f"  {s['paso']:12s} s={s['s']:.2f}  {fmt_censo(s['zonas'])}")
    print()
    for line in r["log"]:
        if line.startswith("C2"):
            print(line)
    L = r["ledger"]
    print()
    print(f"gen  C1 {L['E_gen_c1']:.0f}  C2 {L['E_gen_c2']:.0f}  C2.5 {L['E_gen_c25']:.0f}  C3 {L['E_gen_c3']:.0f}  tot {r['E_gen']}")
    print(f"paga C2 {L['E_mot_c2']:.0f}  pin {L['E_pin']:.0f}  tot {r['E_paga']}")
    print(f"η {r['eta']}  neto {r['neto']} J")
    print(r["opinion"])
    print("out", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
