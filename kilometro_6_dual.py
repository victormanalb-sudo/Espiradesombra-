#!/usr/bin/env python3
"""
kilometro_6_dual.py — 6 subciclos, stock, DOS cuentas. Termux / stdlib.

Los 6 (nombres VMA, 20-sep):
  C1    medio RECTO
  C2.0  giro 1.5 del carril (batería: invertir + 0.5 SWAP)
  C2.5  el otro medio / dejar subir
  C3.0  perneo lastre→objeto (misma cota, ΔPE=0)
  C3    UNO RECTO inverso (objeto lastrado BAJA)
  C3.1  desperneo lastre→carril (misma cota)

Dos cinemáticas (el móvil tiene las dos y se contradicen):
  lastre  INFORME 20-sep / gemelo_4ciclos: C1 y C2.5 generan con lastre
  flota   docx «C1 objeto con tendencia arriba»: C1+C2+C2.5 flota;
          C2.5 0 elec; solo C3 genera al bajar lastrado

Dos cuentas (nunca mezclar):
  CERRADA   round-trip 1ª ley. El SWAP de lastre se PAGA. η_rt < 1.
  CONTROL   solo motor de giro + pernos. r puede >1. Es COP, no generador.

Uso:
  python3 kilometro_6_dual.py
  python3 kilometro_6_dual.py --cinematica flota
  python3 kilometro_6_dual.py --cinematica lastre --dkp
  python3 kilometro_6_dual.py --scan
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict, field
from typing import List

G = 9.81


@dataclass
class P:
    m_obj: float = 30.0
    m_lastre: float = 10.0
    dh: float = 15.0
    eta_gen: float = 0.85
    eta_mot: float = 0.90
    eta_lift: float = 0.90
    drag: float = 0.06
    e_perno: float = 1.5
    n_pernos: int = 4
    vueltas: float = 1.5
    stock: int = 5
    dkp: bool = False
    cinematica: str = "lastre"  # lastre | flota


@dataclass
class Led:
    E_gen: float = 0.0
    E_mot_giro: float = 0.0
    E_mot_swap: float = 0.0
    E_pin: float = 0.0
    E_heat: float = 0.0
    gen_c1: float = 0.0
    gen_c2: float = 0.0
    gen_c25: float = 0.0
    gen_c3: float = 0.0
    pin_c30: float = 0.0
    pin_c31: float = 0.0
    n_alta: int = 0
    n_baja: int = 0
    n_obj: int = 3
    s: float = 0.0
    log: List[str] = field(default_factory=list)

    def pin(self, p: P) -> float:
        d = p.e_perno * p.n_pernos
        self.E_pin += d
        return d


def mgh(p: P, m: float | None = None) -> float:
    return (p.m_lastre if m is None else m) * G * p.dh


def gen_drop(p: P, m: float, frac: float) -> tuple[float, float]:
    avail = m * G * p.dh * frac * (1.0 - p.drag)
    elec = p.eta_gen * avail
    return elec, avail - elec


def giro_c2(p: P, n_path: int) -> dict:
    """1 vuelta: ∮g=0, peaje motor/regen. 0.5 extra: SWAP de lastres en el carril."""
    full = int(p.vueltas)
    half = p.vueltas - full
    m_spin = p.m_obj + n_path * p.m_lastre
    W_loop = m_spin * G * p.dh
    E_gen = p.eta_gen * (1.0 - p.drag) * W_loop * full
    E_mot = (W_loop * full) / p.eta_mot * (1.0 + p.drag)
    E_swap_ideal = n_path * mgh(p) * (1.0 if abs(half - 0.5) < 1e-9 else abs(half) * 2.0)
    if p.dkp:
        E_mot_swap = 0.0
        paid = "DKP_otro_modulo"
    else:
        E_mot_swap = E_swap_ideal / p.eta_mot
        paid = "eje"
    return {
        "E_gen": E_gen,
        "E_mot": E_mot,
        "E_mot_swap": E_mot_swap,
        "E_swap_ideal": E_swap_ideal,
        "paid_by": paid,
        "full": full,
        "half": half,
        "n_path": n_path,
    }


def paso_c1(led: Led, p: P) -> dict:
    if p.cinematica == "flota":
        # Objeto sin lastre extra: tiende ARRIBA. El agua hace el trabajo.
        # Si extraes elec aquí, estás cobrando PE del fluido. En cuenta CERRADA
        # eso se devuelve (no es fuente). En CONTROL sí cuenta como salida.
        e, heat = gen_drop(p, p.m_obj, 0.5)
        led.gen_c1 += e
        led.E_gen += e
        led.E_heat += heat
        led.s = 0.5
        led.log.append(f"C1 FLOTA medio  gen {e:.1f} J  (PE fluido, no lastre)")
        return {"ok": True, "E_gen": e, "canal": "fluido"}
    if led.n_alta <= 0:
        led.log.append("C1 STOP: ALTA vacía")
        return {"ok": False, "E_gen": 0.0}
    led.pin(p)
    led.n_alta -= 1
    led.n_obj = 4
    e, heat = gen_drop(p, p.m_lastre, 0.5)
    led.gen_c1 += e
    led.E_gen += e
    led.E_heat += heat
    led.s = 0.5
    led.pin(p)
    led.n_obj = 3
    led.n_baja += 1
    led.log.append(f"C1 LASTRE medio  gen {e:.1f} J  A/B={led.n_alta}/{led.n_baja}")
    return {"ok": True, "E_gen": e, "canal": "lastre"}


def paso_c20(led: Led, p: P) -> dict:
    n_path = led.n_baja
    rot = giro_c2(p, n_path)
    led.gen_c2 += rot["E_gen"]
    led.E_gen += rot["E_gen"]
    led.E_mot_giro += rot["E_mot"]
    led.E_mot_swap += rot["E_mot_swap"]
    moved = 0
    if abs(p.vueltas % 1.0 - 0.5) < 1e-9 and n_path:
        moved = led.n_baja
        led.n_alta += led.n_baja
        led.n_baja = 0
    led.log.append(
        f"C2.0 GIRO {p.vueltas}  gen {rot['E_gen']:.1f}  "
        f"mot {rot['E_mot']:.1f}  swap {rot['E_mot_swap']:.1f} "
        f"({rot['paid_by']})  SWAP {moved}  A/B={led.n_alta}/{led.n_baja}"
    )
    rot["ok"] = True
    rot["moved"] = moved
    return rot


def paso_c25(led: Led, p: P) -> dict:
    if p.cinematica == "flota":
        # Dejas subir al objeto del todo. 0 elec (docx C1-arriba / GROK_4CICLOS).
        led.s = 1.0
        led.log.append("C2.5 FLOTA subir del todo  gen 0.0 J")
        return {"ok": True, "E_gen": 0.0, "canal": "boya"}
    if led.n_alta <= 0:
        led.log.append("C2.5 STOP: ALTA vacía")
        return {"ok": False, "E_gen": 0.0}
    led.pin(p)
    led.n_alta -= 1
    led.n_obj = 4
    e, heat = gen_drop(p, p.m_lastre, 0.5)
    led.gen_c25 += e
    led.E_gen += e
    led.E_heat += heat
    led.s = 1.0
    led.pin(p)
    led.n_obj = 3
    led.n_baja += 1
    led.log.append(f"C2.5 LASTRE otro medio  gen {e:.1f} J  A/B={led.n_alta}/{led.n_baja}")
    return {"ok": True, "E_gen": e, "canal": "lastre"}


def paso_c30(led: Led, p: P) -> dict:
    d = led.pin(p)
    led.pin_c30 += d
    if led.n_alta <= 0:
        led.log.append("C3.0 perneo FALLA: no hay lastre en ALTA")
        return {"ok": False, "E_pin": d}
    led.n_alta -= 1
    led.n_obj = 4
    led.log.append(f"C3.0 PERNEO  {d:.1f} J  objeto n=4  A/B={led.n_alta}/{led.n_baja}")
    return {"ok": True, "E_pin": d}


def paso_c3(led: Led, p: P) -> dict:
    if led.n_obj < 4:
        led.log.append("C3 STOP: objeto sin lastre extra")
        return {"ok": False, "E_gen": 0.0}
    m = p.m_lastre + (p.m_obj if p.cinematica == "flota" else 0.0)
    # flota: baja el conjunto objeto+lastre (neto ≈ lastre, boya cancela objeto)
    # lastre: solo el extra recorre Δh (objeto anclado al carril)
    if p.cinematica == "flota":
        e, heat = gen_drop(p, p.m_lastre, 1.0)  # boya del objeto se cancela ida/vuelta
    else:
        e, heat = gen_drop(p, p.m_lastre, 1.0)
    led.gen_c3 += e
    led.E_gen += e
    led.E_heat += heat
    led.s = 0.0
    led.log.append(f"C3 BAJA lastrado  gen {e:.1f} J  (m_ref={m:.1f} kg, neto lastre)")
    return {"ok": True, "E_gen": e}


def paso_c31(led: Led, p: P) -> dict:
    d = led.pin(p)
    led.pin_c31 += d
    led.n_obj = 3
    led.n_baja += 1
    led.log.append(f"C3.1 DESPERNEO  {d:.1f} J  lastre en BAJA  A/B={led.n_alta}/{led.n_baja}")
    return {"ok": True, "E_pin": d}


def un_ciclo(led: Led, p: P) -> bool:
    r1 = paso_c1(led, p)
    if not r1.get("ok"):
        return False
    paso_c20(led, p)
    r25 = paso_c25(led, p)
    if not r25.get("ok"):
        return False
    r30 = paso_c30(led, p)
    if not r30.get("ok"):
        return False
    r3 = paso_c3(led, p)
    if not r3.get("ok"):
        return False
    paso_c31(led, p)
    return True


def cuentas(led: Led, p: P, n_ok: int, n_alta0: int) -> dict:
    d_stock = n_alta0 - led.n_alta
    pe_stock = max(d_stock, 0) * mgh(p)
    pe_fluido = 0.0
    if p.cinematica == "flota" and led.gen_c1:
        # C1 cobró PE del fluido. En cuenta CERRADA el agua vuelve.
        pe_fluido = led.gen_c1 / max(p.eta_gen * (1.0 - p.drag), 1e-9)
    paga_control = led.E_mot_giro + led.E_pin
    paga_cerrada = led.E_mot_giro + led.E_mot_swap + led.E_pin + pe_stock + pe_fluido
    r_control = led.E_gen / paga_control if paga_control else float("inf")
    eta_rt = led.E_gen / paga_cerrada if paga_cerrada else float("inf")
    kwh = led.E_gen / 3.6e6
    return {
        "ciclos_ok": n_ok,
        "stock_ini_ALTA": n_alta0,
        "stock_fin_ALTA": led.n_alta,
        "stock_fin_BAJA": led.n_baja,
        "d_stock": d_stock,
        "GEN": {
            "C1": round(led.gen_c1, 2),
            "C2.0_regen": round(led.gen_c2, 2),
            "C2.5": round(led.gen_c25, 2),
            "C3": round(led.gen_c3, 2),
            "total_J": round(led.E_gen, 2),
            "total_kWh": round(kwh, 6),
        },
        "PAGA": {
            "C2.0_motor_J": round(led.E_mot_giro, 2),
            "C2.0_swap_J": round(led.E_mot_swap, 2),
            "C3.0_pin_J": round(led.pin_c30, 2),
            "C3.1_pin_J": round(led.pin_c31, 2),
            "control_J": round(paga_control, 2),
            "cerrada_J": round(paga_cerrada, 2),
            "pe_stock_J": round(pe_stock, 2),
            "pe_fluido_J": round(pe_fluido, 2),
        },
        "CONTROL_COP": round(r_control, 4),
        "CONTROL_gt_1": r_control > 1.0,
        "ETA_RT_cerrada": round(eta_rt, 4),
        "ETA_RT_gt_1": eta_rt > 1.0,
        "nota_control": "COP: no cuentas el SWAP. No es generador. No se vende.",
        "nota_cerrada": "1ª ley: el 0.5 del carril mueve lastre de cota. η_rt<1.",
        "dkp": p.dkp,
        "cinematica": p.cinematica,
    }


def imprimir(p: P, c: dict, log: List[str]) -> None:
    print("=" * 72)
    print(
        f"6 SUBCICLOS  cinematica={p.cinematica}  dkp={p.dkp}  "
        f"m_obj={p.m_obj} m_l={p.m_lastre} dh={p.dh} stock={p.stock}"
    )
    print("=" * 72)
    print("GENERA (J)")
    for k, v in c["GEN"].items():
        print(f"  {k:16} {v}")
    print("PAGA (J)")
    for k, v in c["PAGA"].items():
        print(f"  {k:16} {v}")
    print()
    print(f"  CONTROL COP     {c['CONTROL_COP']:.4f}   >1? {c['CONTROL_gt_1']}")
    print(f"  η_rt CERRADA    {c['ETA_RT_cerrada']:.4f}   >1? {c['ETA_RT_gt_1']}")
    print(f"  stock ALTA {c['stock_ini_ALTA']} → {c['stock_fin_ALTA']}   BAJA {c['stock_fin_BAJA']}")
    print()
    print("  " + c["nota_control"])
    print("  " + c["nota_cerrada"])
    print()
    print("LOG")
    for line in log:
        print("  ", line)


def scan(cinematica: str) -> list:
    print("=" * 72)
    print(f"SCAN η_rt CERRADA  cinematica={cinematica}")
    print("=" * 72)
    found = []
    mls = [5, 10, 20, 50]
    mos = [5, 10, 30]
    print(f"{'m_obj':>8} |", end="")
    for ml in mls:
        print(f" ml={ml:>4}", end="")
    print()
    for mo in mos:
        print(f"{mo:>8.0f} |", end="")
        for ml in mls:
            p = P(m_obj=mo, m_lastre=ml, cinematica=cinematica, dkp=False)
            led = Led(n_alta=p.stock)
            n_ok = 0
            for _ in range(p.stock):
                if not un_ciclo(led, p):
                    break
                n_ok += 1
            c = cuentas(led, p, n_ok, p.stock)
            eta = c["ETA_RT_cerrada"]
            mark = "*" if eta > 1 else " "
            print(f" {eta:6.3f}{mark}", end="")
            if eta > 1:
                found.append((mo, ml, eta))
        print()
    print("  * = η_rt>1 (no debería salir si el SWAP está en la cuenta)")
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cinematica", choices=("lastre", "flota"), default="lastre")
    ap.add_argument("--dkp", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--m-obj", type=float, default=30.0)
    ap.add_argument("--m-lastre", type=float, default=10.0)
    ap.add_argument("--dh", type=float, default=15.0)
    ap.add_argument("--stock", type=int, default=5)
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-20",
    )
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    if a.scan:
        scan("lastre")
        scan("flota")
        return 0

    p = P(
        m_obj=a.m_obj,
        m_lastre=a.m_lastre,
        dh=a.dh,
        stock=a.stock,
        dkp=a.dkp,
        cinematica=a.cinematica,
    )
    led = Led(n_alta=p.stock)
    n_ok = 0
    for _ in range(p.stock):
        if not un_ciclo(led, p):
            break
        n_ok += 1
    c = cuentas(led, p, n_ok, p.stock)
    imprimir(p, c, led.log)
    name = f"6dual_{p.cinematica}{'_dkp' if p.dkp else ''}.json"
    path = os.path.join(a.out, name)
    with open(path, "w") as fh:
        json.dump({"params": asdict(p), "cuentas": c, "log": led.log}, fh, indent=2)
    print("out", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
