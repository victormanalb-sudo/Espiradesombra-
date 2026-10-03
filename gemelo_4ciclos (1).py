#!/usr/bin/env python3
"""
gemelo_4ciclos.py — Termux / Grok Build, SOLO stdlib (sin numpy).

4 subciclos (VMA, 2026-09-19):
  C1   MEDIO recorrido RECTO → genera
  C2   INVIERTE y genera = BATERÍA (giro x.5 del recorrido)
  C2.5 el OTRO medio RECTO → genera
  C3   UNO RECTO en el OTRO sentido → genera
       + cambia lastres de un punto al otro → el de 4 subciclos se puede repetir

C1 + C2.5 = un recorrido (dos medios). C3 = un recorrido inverso.
C2 no es recto: es la cuenta BATERÍA.

Dos cuentas que NO se mezclan (PROTOCOLO estrella):
  BATERÍA   = kg que cambian de cota (stock ALTA ↔ BAJA)
  GENERADOR = julios eléctricos del eje
  RECORRIDO = trabajo de ROTAR la guía x.5 vueltas (recicla extremos)

Lee Arbusto cobraba KE al llamar girar() sin par. Aquí el giro CUESTA o
REGENERA según fase. Reciclar lastre de un extremo al otro NO es gratis:
lo paga el eje, o el otro módulo DKP que está bajando.

Uso:
  python3 /data/data/com.termux/files/home/33x1/gemelo_4ciclos.py
  python3 gemelo_4ciclos.py --vueltas 1.5 --stock 5 --dkp
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict, field
from typing import List

G = 9.81
PI = 3.141592653589793


@dataclass
class P:
    m_obj: float = 30.0      # kg, n=3 → flota
    m_peso: float = 10.0     # kg extra (el 4º) → hunde
    dh: float = 15.0         # m  (tanque canónico, NO 90 m)
    eta_gen: float = 0.85
    eta_mot: float = 0.90
    eta_lift: float = 0.90
    drag: float = 0.06
    E_perno: float = 1.5
    n_pernos: int = 4
    vueltas: float = 1.5     # x.5  (IMPORTANTE: 1.5 vs 2)
    stock: int = 5
    dkp: bool = False        # 2º módulo en oposición: su bajada paga el reciclo


@dataclass
class Led:
    # julios
    E_gen: float = 0.0
    E_mot: float = 0.0
    E_pin: float = 0.0
    E_heat: float = 0.0
    PE_alta: float = 0.0     # inventario
    n_alta: int = 0
    n_baja: int = 0
    n_obj: int = 3
    s: float = 0.0           # 0 = extremo ALTA local, 1 = BAJA local
    phi_turns: float = 0.0
    fase: int = 1            # +1 C1, −1 C3 (φ+π)
    E_gen_c1: float = 0.0     # recto medio
    E_gen_c2: float = 0.0     # batería (invertir)
    E_gen_c25: float = 0.0    # recto otro medio
    E_gen_c3: float = 0.0     # recto uno, sentido inverso
    log: List[str] = field(default_factory=list)

    def pin(self, p: P, n: int = 1) -> None:
        self.E_pin += p.E_perno * p.n_pernos * n


def mgh(p: P) -> float:
    return p.m_peso * G * p.dh


def gen_from_drop(p: P, frac: float) -> tuple[float, float]:
    """Bajada de 1 lastre extra una fracción del Δh. Devuelve (E_elec, E_heat)."""
    avail = mgh(p) * frac * (1.0 - p.drag)
    elec = p.eta_gen * avail
    return elec, avail - elec


def rotate_path(p: P, turns: float, m_on_path: float, coupled_drop: bool) -> dict:
    """
    Giro del RECORRIDO.
    1.0 vuelta  → ∮ g = 0  (solo peaje motor/fricción + regen en fase a favor)
    0.5 extra   → SWAP de extremos: lastres perneados al carril cambian de cota.

    'Invertir julios': media favorable regenera, media desfavorable motoriza.
    Neto de 1 vuelta < 0. El 0.5 extra recicla geometría (paga m g Δh del
    inventario anclado al carril), SALVO DKP: el otro módulo está bajando
    y su par cubre el swap.
    """
    full = int(turns)
    half = turns - full  # 0.5 si 1.5
    # una vuelta: trabajo gravitatorio nulo; peaje ~ drag * (2 m g R_eq)
    # R_eq ~ dh/2  (diámetro vertical)
    m_spin = p.m_obj + m_on_path
    W_loop = m_spin * G * p.dh  # orden de magnitud de una media vertical
    E_gen_inv = p.eta_gen * (1.0 - p.drag) * W_loop * full
    E_mot_inv = (W_loop * full) / p.eta_mot * (1.0 + p.drag)
    # swap 0.5: levanta inventario anclado al carril
    E_swap_ideal = m_on_path * G * p.dh * (1.0 if abs(half - 0.5) < 1e-9 else abs(half) * 2)
    if coupled_drop:
        # DKP: la bajada del otro módulo PAGA el swap (E_mot_swap=0).
        # Su generación es C1 del gemelo, NO se suma aquí (si no, η falsa >1).
        E_mot_swap = 0.0
        E_gen_swap = 0.0
        paid_by = "DKP_otro_modulo_bajando"
    else:
        E_mot_swap = E_swap_ideal / p.eta_mot
        E_gen_swap = 0.0
        paid_by = "eje_del_recorrido"
    return {
        "E_gen": E_gen_inv + E_gen_swap,
        "E_mot": E_mot_inv + E_mot_swap,
        "E_swap_ideal": E_swap_ideal,
        "paid_by": paid_by,
        "full_turns": full,
        "half": half,
    }


def _recto(led: Led, p: P, frac: float, tag: str) -> dict:
    """Movimiento RECTO: extra lastre recorre `frac` de Δh y genera."""
    if led.n_alta <= 0:
        led.log.append(f"{tag} STOP: stock ALTA vacío")
        return {"E_gen": 0.0, "ok": False}
    led.pin(p)
    led.n_alta -= 1
    led.n_obj = 4
    led.PE_alta -= mgh(p)
    e, heat = gen_from_drop(p, frac)
    led.E_gen += e
    led.E_heat += heat
    led.s = min(1.0, led.s + frac)
    led.pin(p)
    led.n_obj = 3
    led.n_baja += 1
    return {"E_gen": e, "ok": True, "frac": frac}


def ciclo1(led: Led, p: P) -> dict:
    """C1: MEDIO recorrido RECTO → genera."""
    led.fase = 1
    led.s = 0.0
    r = _recto(led, p, 0.5, "C1")
    if r["ok"]:
        led.E_gen_c1 += r["E_gen"]
        led.log.append(
            f"C1 RECTO medio {r['E_gen']:.1f} J  s={led.s}  "
            f"A/B={led.n_alta}/{led.n_baja}"
        )
    return r


def ciclo2(led: Led, p: P) -> dict:
    """C2: INVIERTE y genera = BATERÍA (no es recto)."""
    m_on_path = led.n_baja * p.m_peso
    rot = rotate_path(p, p.vueltas, m_on_path, coupled_drop=p.dkp)
    led.E_gen += rot["E_gen"]
    led.E_gen_c2 += rot["E_gen"]
    led.E_mot += rot["E_mot"]
    led.phi_turns += p.vueltas
    if abs(p.vueltas % 1.0 - 0.5) < 1e-9:
        moved = led.n_baja
        led.n_alta += led.n_baja
        led.n_baja = 0
        led.PE_alta += moved * mgh(p)
        led.log.append(f"C2 BATERÍA SWAP {moved} lastres pagado por {rot['paid_by']}")
    led.s = 0.5  # el otro medio lo cierra C2.5
    led.log.append(
        f"C2 BATERÍA invert {p.vueltas}  gen {rot['E_gen']:.1f}  "
        f"mot {rot['E_mot']:.1f}"
    )
    rot["canal"] = "bateria"
    return rot


def ciclo2_5(led: Led, p: P) -> dict:
    """C2.5: el OTRO medio RECTO → genera (cierra el recorrido de C1)."""
    r = _recto(led, p, 0.5, "C2.5")
    if r["ok"]:
        led.E_gen_c25 += r["E_gen"]
        led.s = 1.0
        led.log.append(
            f"C2.5 RECTO otro medio {r['E_gen']:.1f} J  s={led.s}  "
            f"A/B={led.n_alta}/{led.n_baja}"
        )
    return r


def ciclo3(led: Led, p: P) -> dict:
    """
    C3: UNO RECTO en el OTRO sentido → genera.
    Cambia lastres de un punto al otro para que los 4 subciclos se repitan.
    """
    led.fase = -1
    r = _recto(led, p, 1.0, "C3")
    if not r["ok"]:
        return r
    led.E_gen_c3 += r["E_gen"]
    # transferencia punto→punto para el loop de 4. Los kg quedan listos
    # en el otro extremo (= siguiente ALTA). El lift se PAGA (si no, η falsa).
    moved = led.n_baja
    lift = moved * mgh(p) / p.eta_lift
    led.E_mot += lift
    led.n_alta += led.n_baja
    led.n_baja = 0
    led.PE_alta += moved * mgh(p)
    led.s = 0.0
    led.log.append(
        f"C3 RECTO inverso UNO {r['E_gen']:.1f} J  TRANSFER {moved} lastres "
        f"lift {lift:.1f} J → ALTA  A/B={led.n_alta}/{led.n_baja}"
    )
    r["transfer"] = moved
    r["fase"] = "inverso"
    return r


def lee_bugs() -> dict:
    """Lo que hacía el canvas de Lee (NO ejecutar: numpy + julios inventados)."""
    m, dh90, eta = 10.0, 90.0, 0.85
    E_drop = m * G * dh90 * eta  # 7641 J  — Δh 90 m, no el tanque 15 m
    return {
        "girar_crea_KE_sin_par": True,
        "C3_vuelve_a_sumar_la_misma_KE": True,
        "lift_del_lastre_nunca_pagado": True,
        "Delta_h_90m_vs_tanque_15m": True,
        "E_gen_C1_Lee_J": round(E_drop, 1),
        "numpy_en_este_Termux": False,
        "nota": "Eso no es reciclar lastre. Es olvidar el eje y duplicar KE.",
    }


def run(p: P) -> dict:
    led = Led(n_alta=p.stock, n_baja=0, n_obj=3, PE_alta=p.stock * mgh(p))
    pe0 = led.PE_alta
    steps = []
    n_ok = 0
    # repetir C1..C3 hasta vaciar o stock recicla
    for k in range(p.stock + 2):
        r1 = ciclo1(led, p)
        if not r1.get("ok"):
            break
        r2 = ciclo2(led, p)
        r25 = ciclo2_5(led, p)
        r3 = ciclo3(led, p)
        n_ok += 1
        steps.append({"i": k + 1, "C1": r1, "C2": r2, "C2.5": r25, "C3": r3})
        # con SWAP, el stock ALTA se rellena: no es infinito (peaje en C2)
        if k >= p.stock - 1:
            break

    E_net = led.E_gen - led.E_mot - led.E_pin
    dPE = pe0 - led.PE_alta
    # η aparente Lee: E_net / (un solo mgh), ignorando mot y dPE
    eta_lee = E_net / mgh(p) if mgh(p) else 0.0
    # η honesta: eléctrico útil / (eléctrico pagado + |ΔPE| gastada)
    denom = led.E_mot + led.E_pin + max(dPE, 0.0)
    eta_real = led.E_gen / denom if denom > 1e-9 else None

    return {
        "params": asdict(p),
        "ciclos_ok": n_ok,
        "ledger": {
            "E_gen_J": round(led.E_gen, 2),
            "E_gen_C1_recto_medio_J": round(led.E_gen_c1, 2),
            "E_gen_C2_bateria_J": round(led.E_gen_c2, 2),
            "E_gen_C25_recto_otro_medio_J": round(led.E_gen_c25, 2),
            "E_gen_C3_recto_inverso_uno_J": round(led.E_gen_c3, 2),
            "E_gen_recto_J": round(led.E_gen_c1 + led.E_gen_c25 + led.E_gen_c3, 2),
            "E_mot_J": round(led.E_mot, 2),
            "E_pin_J": round(led.E_pin, 2),
            "E_heat_J": round(led.E_heat, 2),
            "E_net_elec_J": round(E_net, 2),
            "PE_alta_ini_J": round(pe0, 2),
            "PE_alta_fin_J": round(led.PE_alta, 2),
            "dPE_bateria_J": round(dPE, 2),
            "stock_final_ALTA": led.n_alta,
            "stock_final_BAJA": led.n_baja,
        },
        "eta_aparente_estilo_Lee": round(eta_lee, 3),
        "eta_real_gen_sobre_pagado": None if eta_real is None else round(eta_real, 3),
        "eta_gt_1_si_olvidas_el_eje": eta_lee > 1.0,
        "eta_real_gt_1": bool(eta_real and eta_real > 1.0),
        "lee_bugs": lee_bugs(),
        "log": led.log,
        "veredicto": {
            "todos_los_ciclos_pueden_APORTAR_elec": True,
            "eso_no_es_sobreunidad": True,
            "C1": "RECTO medio → genera",
            "C2": "BATERÍA: invierte y genera (giro x.5)",
            "C2.5": "RECTO otro medio → genera",
            "C3": "RECTO uno inverso → genera + transfer lastres (loop infinito de 4)",
            "IMPORTANTE": "C1+C2.5 = un recorrido. C3 = uno al revés. C2 = batería.",
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vueltas", type=float, default=1.5, help="x.5 del recorrido")
    ap.add_argument("--stock", type=int, default=5)
    ap.add_argument("--dkp", action="store_true", help="2º módulo paga el SWAP")
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-19",
        help="carpeta fechada en claude-main",
    )
    a = ap.parse_args()
    p = P(vueltas=a.vueltas, stock=a.stock, dkp=a.dkp)
    r = run(p)
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "4ciclos.json")
    with open(path, "w") as f:
        json.dump(r, f, indent=2, ensure_ascii=False)

    here = os.path.abspath(__file__)
    print("=" * 64)
    print("RUTAS (Termux, absolutas)")
    print("  4 ciclos :", here)
    print("  dkp viejo:", "/data/data/com.termux/files/home/33x1/gemelo_dkp.py")
    print("  out      :", os.path.abspath(path))
    print("=" * 64)
    L = r["ledger"]
    print(f"vueltas={p.vueltas}  DKP={p.dkp}  ciclos_ok={r['ciclos_ok']}")
    print(
        f"RECTO  C1 medio {L['E_gen_C1_recto_medio_J']}  "
        f"C2.5 otro {L['E_gen_C25_recto_otro_medio_J']}  "
        f"C3 inverso {L['E_gen_C3_recto_inverso_uno_J']}  "
        f"suma {L['E_gen_recto_J']}"
    )
    print(
        f"BATERÍA C2 {L['E_gen_C2_bateria_J']}  mot {L['E_mot_J']}  "
        f"pin {L['E_pin_J']}  GEN tot {L['E_gen_J']}  NET {L['E_net_elec_J']} J"
    )
    print(f"dPE batería {L['dPE_bateria_J']} J   stock A/B {L['stock_final_ALTA']}/{L['stock_final_BAJA']}")
    print(f"η aparente Lee (olvida eje): {r['eta_aparente_estilo_Lee']}")
    print(f"η real E_gen/(mot+pin+|dPE|): {r['eta_real_gen_sobre_pagado']}")
    print("log:")
    for line in r["log"]:
        print("  ", line)
    print("veredicto:", r["veredicto"]["IMPORTANTE"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
