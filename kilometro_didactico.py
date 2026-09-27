#!/usr/bin/env python3
"""
kilometro_didactico.py — ¿De dónde sale el η > 1?

Tres modos + la cuenta que faltaba en el MODO 2:

  1 HERMÉTICO     fluido vuelve. ∮g = 0. η < 1
  2 MAR ABIERTO   (mal contado vs bien contado)
  3 NUNCA NEUTRO  perneo antes de parar. fluido vuelve. η < 1

El error clásico del modo 2: sumar MGH de bajada Y MGH de “el mar sube
el objeto”. En ida y vuelta sumergido, Arquímedes se CANCELA:

  bajada (con extra):  (m_obj + m_lastre − ρV) g Δh
  subida (sin extra):  (ρV − m_obj) g Δh
  suma:                m_lastre g Δh     ← solo el lastre

El mar no baja de nivel si el objeto sigue sumergido (V desplazado cte).
η_objeto > 1 solo si el lastre se queda ABAJO (batería abierta).

  python3 kilometro_didactico.py
  python3 kilometro_didactico.py --modo 2
"""
from __future__ import annotations

import argparse
import json
import os

G = 9.81
M_OBJ = 30.0
M_LASTRE = 10.0
DH = 15.0
RHO = 1000.0
V = 0.035  # m³  → ρV = 35 kg  (3 flota / 4 se hunde: 30 vs 40 kg)
ETA_GEN = 0.85
ETA_MOT = 0.90
ETA_LIFT = 0.90
DRAG = 0.06
E_PIN = 1.5 * 4

MGH = M_LASTRE * G * DH
B = RHO * V * G * DH  # “trabajo” de Arquímedes en Δh  (ρV g Δh)


def linea(k, v):
    print(f"  {k:28s} {v}")


def modo_1():
    print("=" * 64)
    print("MODO 1: TANQUE HERMÉTICO  (fluido vuelve, ∮g = 0)")
    print("=" * 64)
    e_gen = ETA_GEN * (1 - DRAG) * MGH
    e_mot = MGH / ETA_MOT * (1 + DRAG)
    e_in = e_mot + 2 * E_PIN
    eta = e_gen / e_in
    linea("E_gen bajada", f"{e_gen:.1f} J")
    linea("E_mot subida", f"{e_mot:.1f} J")
    linea("pernos", f"{2*E_PIN:.1f} J")
    linea("η", f"{eta:.3f}  < 1  batería")
    print()
    return {"eta": round(eta, 3), "fuente": None}


def modo_2():
    print("=" * 64)
    print("MODO 2: MAR ABIERTO")
    print("=" * 64)
    print("  Objeto sumergido todo el ciclo. V desplazado cte → nivel del mar cte.")
    print()
    w_down = (M_OBJ + M_LASTRE) * G * DH - B   # grav extra − boya
    w_up = B - M_OBJ * G * DH                  # boya − peso objeto
    w_ciclo = w_down + w_up                    # = MGH
    e_gen_down = ETA_GEN * (1 - DRAG) * max(w_down, 0)
    e_gen_up = ETA_GEN * (1 - DRAG) * max(w_up, 0)
    e_gen_both = e_gen_down + e_gen_up

    print("  --- fuerzas en Δh (sin η) ---")
    linea("bajada neta (4 pesos)", f"{w_down:.1f} J")
    linea("subida neta (3 pesos)", f"{w_up:.1f} J")
    linea("suma = m_lastre g Δh", f"{w_ciclo:.1f} J  (MGH={MGH:.1f})")
    print()
    print("  CUENTA MAL (Lee / canvas): gen bajada + 'mar paga subida'")
    e_mal_out = ETA_GEN * (1 - DRAG) * MGH
    e_mal_in = 2 * E_PIN
    linea("η_objeto falsa", f"{e_mal_out / e_mal_in:.1f}  (olvidas lastre ABAJO)")
    print()
    print("  CUENTA BIEN, lastre se queda abajo (batería ABIERTA):")
    linea("E_gen (solo extra)", f"{ETA_GEN*(1-DRAG)*MGH:.1f} J")
    linea("pagas", f"{2*E_PIN:.1f} J pernos")
    linea("η_eje", f"{ETA_GEN*(1-DRAG)*MGH / (2*E_PIN):.1f}  >1  DESCARGAS el kg")
    print()
    print("  CUENTA BIEN, lastre VUELVE (ciclo cerrado):")
    e_lift = MGH / ETA_LIFT
    e_out = e_gen_both  # boya se cancela; queda ~η MGH
    e_in = e_lift + 2 * E_PIN
    eta = e_out / e_in
    linea("E_gen ida+vuelta", f"{e_out:.1f} J")
    linea("lift lastre", f"{e_lift:.1f} J")
    linea("η_cerrado", f"{eta:.3f}  < 1")
    print()
    print("  El mar NO es fuente extra. Arquímedes de subida se descuenta")
    print("  en la bajada. Solo queda el lastre. Como Energy Vault.")
    print()
    return {
        "w_down": round(w_down, 1),
        "w_up": round(w_up, 1),
        "suma": round(w_ciclo, 1),
        "MGH": round(MGH, 1),
        "eta_cerrado": round(eta, 3),
        "eta_eje_si_no_lift": round(ETA_GEN * (1 - DRAG) * MGH / (2 * E_PIN), 1),
    }


def modo_3():
    print("=" * 64)
    print("MODO 3: NUNCA NEUTRO  (perneo antes de parar, fluido vuelve)")
    print("=" * 64)
    e_gen = ETA_GEN * (1 - DRAG) * MGH
    e_mot = MGH / ETA_MOT * (1 + DRAG)
    eta = e_gen / (e_mot + 2 * E_PIN)
    linea("η", f"{eta:.3f}  < 1  igual que modo 1")
    print()
    return {"eta": round(eta, 3)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modo", type=int, choices=(1, 2, 3), default=0)
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-19",
    )
    a = ap.parse_args()
    print()
    print("KILÓMETRO DIDÁCTICO")
    print(f"m_obj={M_OBJ} m_lastre={M_LASTRE} ρV={RHO*V:.0f} kg  Δh={DH} m")
    print(f"3 flota ({M_OBJ}<{RHO*V:.0f})  4 se hunde ({M_OBJ+M_LASTRE}>{RHO*V:.0f})")
    print()
    r = {}
    if a.modo in (0, 1):
        r["m1"] = modo_1()
    if a.modo in (0, 2):
        r["m2"] = modo_2()
    if a.modo in (0, 3):
        r["m3"] = modo_3()
    if a.modo == 0:
        print("=" * 64)
        print("CONCLUSIÓN")
        print("  η>1 en el eje = lastre que no vuelve (modo 2 mal contado).")
        print("  Ida+vuelta sumergido: boya se cancela. Queda m g Δh del kg.")
        print("  Cerrar el kg (C3 transfer / lift) → η<1.")
        print("  Eso es el 4-subciclo de gemelo_4ciclos.py.")
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "didactico.json")
    with open(path, "w") as f:
        json.dump(r, f, indent=2)
    print("out", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
