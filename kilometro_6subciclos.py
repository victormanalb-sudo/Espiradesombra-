#!/usr/bin/env python3
"""
kilometro_6subciclos.py — 6 subciclos VMA, ledger cerrado, busca η>1.

  C1    medio RECTO → genera
  C2.0  giro x.5: motor + regen (BATERÍA)
  C2.5  el otro medio RECTO → genera
  C3.0  perneo (poner lastre)  ~6 J
  C3    UNO RECTO inverso → GENERA (no consume)
  C3.1  desperneo ~6 J
  Reciclo de lastres: C2 x.5 vueltas (SWAP extremos). NO se cobra lift en C3.

Sin trampas: todo lo que entra y sale se cuenta.
Termux / stdlib.

  python3 kilometro_6subciclos.py
  python3 kilometro_6subciclos.py --scan
  python3 kilometro_6subciclos.py --m-obj 5 --m-lastre 100
"""
from __future__ import annotations

import argparse
import json
import os

G = 9.81


class Params:
    def __init__(self) -> None:
        self.m_obj = 30.0
        self.m_lastre = 10.0
        self.dh = 15.0
        self.eta_gen = 0.85
        self.eta_mot = 0.90
        self.eta_lift = 0.90
        self.drag = 0.06
        self.e_perno = 1.5
        self.n_pernos = 4
        self.vueltas = 1.5
        self.n_swap = 2  # lastres que el x.5 de C2 intercambia de extremo a extremo
        self.dkp = False  # True: SWAP lo paga el otro módulo (mot_swap=0)


def mgh(m: float, dh: float) -> float:
    return m * G * dh


def ciclo(p: Params) -> dict:
    """
    Notación VMA:
      lastres se PERNEAN al objeto o al recorrido (misma cota → ΔPE = 0).
      C1 = x, C2.5 ≈ x, C3 = 2x (genera).
      C2 invierte x y recupera R*x. El x.5 va DENTRO de C2, no hay grúa SWAP.
      C3.0 y C3.1 = δ (pernos).
    """
    e_full = mgh(p.m_lastre, p.dh)
    x = p.eta_gen * (1 - p.drag) * e_full * 0.5  # C1 medio
    R = (p.eta_gen * (1 - p.drag)) / (p.eta_mot and (p.eta_mot / (1 + p.drag)) or 1)
    # R = regen/motor de un mismo tramo ≈ eta_gen(1-d) / [1/eta_mot * (1+d)]
    R = p.eta_gen * (1 - p.drag) * p.eta_mot / (1 + p.drag)

    gen_c1 = x
    gen_c25 = 0.95 * x  # casi x
    gen_c3 = 2.0 * x  # UNO inverso, GENERA
    inv_c2 = x  # C2 invierte x
    rec_c2 = R * x  # recupera R*x  (el 2x de C2 es escala de tramo, no una grúa)
    pin_c30 = p.e_perno * p.n_pernos
    pin_c31 = p.e_perno * p.n_pernos
    delta = pin_c30 + pin_c31

    gen_total = gen_c1 + gen_c25 + gen_c3 + rec_c2
    paga_total = inv_c2 + delta
    neto = gen_total - paga_total
    eta = gen_total / paga_total if paga_total else float("inf")

    # ΔPE si el x.5 cambiara de cota los kg anclados al recorrido (no es perneo)
    pe_si_cota = p.n_swap * e_full

    return {
        "x": x,
        "R": R,
        "gen_c1": gen_c1,
        "gen_c25": gen_c25,
        "gen_c3": gen_c3,
        "gen_c2": rec_c2,
        "mot_c2": inv_c2,
        "mot_swap": 0.0,
        "pin_c30": pin_c30,
        "pin_c31": pin_c31,
        "lift": 0.0,
        "gen_total": gen_total,
        "paga_total": paga_total,
        "neto": neto,
        "eta": eta,
        "eta_gt_1": eta > 1.0,
        "R_c2": R,
        "pe_si_x5_cambia_cota": pe_si_cota,
        "stock_si_perneo_misma_cota": "ALTA se vacía salvo que el x.5 mueva la cota",
    }


def imprimir(p: Params, r: dict) -> None:
    print("=" * 70)
    print(
        f"m_obj={p.m_obj} kg  m_lastre={p.m_lastre} kg  dh={p.dh} m  "
        f"dkp={p.dkp}"
    )
    print(
        f"eta_gen={p.eta_gen} eta_mot={p.eta_mot} eta_lift={p.eta_lift} "
        f"drag={p.drag}"
    )
    print("=" * 70)
    print(f"  x = C1 = {r['x']:.2f} J     R = {r['R']:.3f}")
    print("GENERA:")
    print(f"  C1    x                   {r['gen_c1']:10.2f} J")
    print(f"  C2.5  casi x              {r['gen_c25']:10.2f} J")
    print(f"  C3    2x  (GENERA)        {r['gen_c3']:10.2f} J")
    print(f"  C2    recupera R*x        {r['gen_c2']:10.2f} J")
    print(f"  TOTAL GEN                 {r['gen_total']:10.2f} J")
    print()
    print("PAGA:")
    print(f"  C2    invierte x          {r['mot_c2']:10.2f} J")
    print(f"  C3.0  perneo objeto/carril{r['pin_c30']:10.2f} J")
    print(f"  C3.1  desperneo           {r['pin_c31']:10.2f} J")
    print(f"  SWAP-grúa                 {r['mot_swap']:10.2f} J  (0: no existe)")
    print(f"  TOTAL PAGA                {r['paga_total']:10.2f} J")
    print()
    print(f"NETO {r['neto']:.2f} J")
    print(f"η = {r['eta']:.4f}   ¿>1? {'SÍ' if r['eta_gt_1'] else 'NO'}")
    print()
    print("Lastre: perneo al OBJETO o al RECORRIDO (misma cota, ΔPE=0).")
    print("C2 = invert x + regen R*x + x.5 (dentro de C2, no grúa).")
    print(f"Si el x.5 cambiara la COTA de {p.n_swap} kg: ΔPE={r['pe_si_x5_cambia_cota']:.0f} J (no es perneo).")


def scan(*, dkp: bool) -> list:
    print("=" * 70)
    print(f"SCAN η  (dkp={dkp})")
    print("=" * 70)
    m_lastres = [5, 10, 20, 50, 100, 200]
    m_objs = [0.1, 0.5, 1, 2, 5, 10, 20, 30]
    print(f"{'m_obj':>8} |", end="")
    for ml in m_lastres:
        print(f" ml={ml:>4}", end="")
    print()
    print("-" * 70)
    found = []
    for mo in m_objs:
        print(f"{mo:>8.1f} |", end="")
        for ml in m_lastres:
            p = Params()
            p.m_obj = mo
            p.m_lastre = ml
            p.dkp = dkp
            r = ciclo(p)
            eta = r["eta"]
            mark = "*" if eta > 1 else " "
            print(f" {eta:6.3f}{mark}", end="")
            if eta > 1:
                found.append((mo, ml, eta, dkp))
        print()
    print()
    if found:
        print("η>1:")
        for row in found:
            print(f"  m_obj={row[0]} m_lastre={row[1]} η={row[2]:.4f} dkp={row[3]}")
    else:
        print("NO hay η>1 en este rango (lift cerrado).")
    print()
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--dkp", action="store_true")
    ap.add_argument("--m-obj", type=float, default=30.0)
    ap.add_argument("--m-lastre", type=float, default=10.0)
    ap.add_argument("--dh", type=float, default=15.0)
    ap.add_argument("--eta-gen", type=float, default=0.85)
    ap.add_argument("--eta-mot", type=float, default=0.90)
    ap.add_argument("--eta-lift", type=float, default=0.90)
    ap.add_argument("--drag", type=float, default=0.06)
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-19",
    )
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    if a.scan:
        f1 = scan(dkp=False)
        f2 = scan(dkp=True)
        path = os.path.join(a.out, "scan_6subciclos.json")
        with open(path, "w") as fh:
            json.dump(
                {"eje": f1, "dkp": f2, "nota": "η>1 solo si omites lift o mot_swap"},
                fh,
                indent=2,
            )
        print("out", path)
        return 0

    p = Params()
    p.m_obj = a.m_obj
    p.m_lastre = a.m_lastre
    p.dh = a.dh
    p.eta_gen = a.eta_gen
    p.eta_mot = a.eta_mot
    p.eta_lift = a.eta_lift
    p.drag = a.drag
    p.dkp = a.dkp
    r = ciclo(p)
    imprimir(p, r)
    name = "6subciclos_dkp.json" if a.dkp else "6subciclos.json"
    path = os.path.join(a.out, name)
    with open(path, "w") as fh:
        json.dump({"params": p.__dict__, "run": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()}}, fh, indent=2)
    print("out", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
