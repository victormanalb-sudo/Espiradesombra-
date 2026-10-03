#!/usr/bin/env python3
"""
valor_elewit.py — qué se puede COBRAR, con números del propio dossier VMA.

No vende η>1 ni RSA. Tres productos civiles, tres TRL distintos:

  A  ZypyZape firmware   inercia/sincronismo en parque existente
  B  Kilómetro tanque    buffer mecánico (batería, η_rt<1)
  C  Quijote palas       hardware; fuera del SOW Elewit fase 0

Cifras de licencia e inercia: RESUMEN-HONESTO + ONE_PAGER_ELEWIT (2026-07).
Cifras de tanque: física stdlib, no un BOM medido.

  python3 valor_elewit.py
  python3 valor_elewit.py --mw 50 --turbinas 10 --p-mw 5
  python3 valor_elewit.py --tanque-m 15 --lastre-t 50
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass

G = 9.81


@dataclass
class Parque:
    n_turbinas: int = 10
    p_mw: float = 5.0  # NREL 5 MW, el gemelo que ya tienes


@dataclass
class Mercado:
    # €/MW/año — banda conservadora del RESUMEN-HONESTO (no inventada hoy)
    ffr_lo: float = 400.0
    ffr_hi: float = 800.0
    inercia_lo: float = 600.0
    inercia_hi: float = 1200.0
    licencia_once_lo: float = 8_000.0
    licencia_once_hi: float = 12_000.0
    licencia_ano_lo: float = 1_000.0
    licencia_ano_hi: float = 2_000.0
    # Fase 0–2 ONE_PAGER_ELEWIT
    estudio_lo: float = 30_000.0
    estudio_hi: float = 80_000.0
    piloto_sim_lo: float = 80_000.0
    piloto_sim_hi: float = 200_000.0
    piloto_campo_lo: float = 500_000.0
    piloto_campo_hi: float = 2_000_000.0


@dataclass
class Tanque:
    dh: float = 15.0
    lastre_kg: float = 10.0
    eta_rt: float = 0.65  # gemelo 4ciclos eje ~0.59, dkp ~0.69
    ciclos_dia: int = 40  # buffer de pico, no base-load
    capex_eur_por_kwh: float = 250.0  # techo honesto vs Energy Vault ~200-350


def mw_parque(p: Parque) -> float:
    return p.n_turbinas * p.p_mw


def producto_a(p: Parque, m: Mercado) -> dict:
    mw = mw_parque(p)
    once = (m.licencia_once_lo * mw, m.licencia_once_hi * mw)
    ano = (
        (m.ffr_lo + m.inercia_lo + m.licencia_ano_lo) * mw,
        (m.ffr_hi + m.inercia_hi + m.licencia_ano_hi) * mw,
    )
    return {
        "nombre": "A — ZypyZape firmware (parque existente)",
        "mw": mw,
        "turbinas": p.n_turbinas,
        "p_mw": p.p_mw,
        "cobrable_hoy": "estudio 30–80 k€. Piloto sim 80–200 k€. Campo 0.5–2 M€.",
        "licencia_once_eur": {"lo": round(once[0]), "hi": round(once[1])},
        "recurrente_eur_ano": {"lo": round(ano[0]), "hi": round(ano[1])},
        "desglose_recurrente": {
            "ffr_eur_mw_ano": [m.ffr_lo, m.ffr_hi],
            "inercia_eur_mw_ano": [m.inercia_lo, m.inercia_hi],
            "soporte_eur_mw_ano": [m.licencia_ano_lo, m.licencia_ano_hi],
        },
        "fase0_estudio_eur": [m.estudio_lo, m.estudio_hi],
        "fase1_piloto_sim_eur": [m.piloto_sim_lo, m.piloto_sim_hi],
        "fase2_piloto_campo_eur": [m.piloto_campo_lo, m.piloto_campo_hi],
        "condicion": "sin 2 turbinas con PLC y telemetría esto es un PDF, no un contrato",
        "no_vender": ["η>1", "RoCoF mejor que BESS", "Kilómetro en el mismo SOW", "33×1 paz"],
    }


def kwh_ciclo(t: Tanque) -> float:
    return t.eta_rt * t.lastre_kg * G * t.dh / 3.6e6


def producto_b(t: Tanque) -> dict:
    kwh = kwh_ciclo(t)
    kwh_dia = kwh * t.ciclos_dia
    kwh_ano = kwh_dia * 365
    # precio OMIE grosero 80 €/MWh = 0.08 €/kWh, con η ya metida
    eur_ano_energia = kwh_ano * 0.08
    capex = max(kwh, 1e-9) * t.capex_eur_por_kwh
    # a escala toy el capex/kWh no tiene sentido: el banco es un instrumento
    banco_es_instrumento = t.lastre_kg < 1000 or t.dh <= 20
    return {
        "nombre": "B — Kilómetro buffer (batería mecánica, η_rt<1)",
        "dh_m": t.dh,
        "lastre_kg": t.lastre_kg,
        "eta_rt": t.eta_rt,
        "kWh_por_ciclo": round(kwh, 6),
        "kWh_dia": round(kwh_dia, 4),
        "kWh_ano": round(kwh_ano, 2),
        "eur_ano_si_solo_energia_OMIE80": round(eur_ano_energia, 2),
        "capex_techo_eur_si_fuera_almacen": round(capex, 2),
        "veredicto": (
            "BANCO DE FÍSICA, no producto de kWh. El dinero del tanque 15 m es "
            "el dato medido que desbloquea Elewit, no el julios×precio."
            if banco_es_instrumento
            else "A esta escala ya es almacén: competir con Energy Vault / Gravitricity."
        ),
        "escala_para_1_MWh": {
            "lastre_t_si_dh_15m": round(1e3 / max(t.eta_rt * G * 15 / 3.6e6, 1e-18) / 1000, 1),
            "dh_m_si_lastre_50t": round(1e3 / max(t.eta_rt * 50e3 * G / 3.6e6, 1e-18), 1),
        },
        "no_vender": ["r_control>1 como generador", "mercurio", "$50/kWh sin BOM"],
    }


def producto_c() -> dict:
    return {
        "nombre": "C — Quijote (masas en palas)",
        "trl": "concepto + gemelo. No SOW Elewit fase 0.",
        "valor": "demo mecánica de puerta, no sustituye BESS ni inercia contractual",
        "cobrable_hoy": 0,
        "cuando": "después de A en campo y fatiga medida",
    }


def imprimir(a: dict, b: dict, c: dict) -> None:
    print("=" * 72)
    print("VALOR QUE SÍ SE PUEDE FIRMAR  —  VMA / 33×1 civil  —  2026-09-20")
    print("=" * 72)
    print()
    print(a["nombre"])
    print(f"  Parque {a['turbinas']} × {a['p_mw']} MW = {a['mw']} MW")
    print(f"  Cobrable HOY: {a['cobrable_hoy']}")
    print(
        f"  Licencia once: {a['licencia_once_eur']['lo']:,.0f} – "
        f"{a['licencia_once_eur']['hi']:,.0f} €"
    )
    print(
        f"  Recurrente/año (si hay mercado de inercia+FFR): "
        f"{a['recurrente_eur_ano']['lo']:,.0f} – "
        f"{a['recurrente_eur_ano']['hi']:,.0f} €"
    )
    print(f"  Condición: {a['condicion']}")
    print(f"  No vender: {', '.join(a['no_vender'])}")
    print()
    print(b["nombre"])
    print(f"  Δh={b['dh_m']} m  lastre={b['lastre_kg']} kg  η_rt={b['eta_rt']}")
    print(f"  {b['kWh_por_ciclo']} kWh/ciclo  →  {b['kWh_ano']} kWh/año")
    print(f"  Si solo vendieras energía a 80 €/MWh: {b['eur_ano_si_solo_energia_OMIE80']} €/año")
    print(f"  {b['veredicto']}")
    print(
        f"  Para 1 MWh: {b['escala_para_1_MWh']['lastre_t_si_dh_15m']} t @ 15 m  "
        f"o  {b['escala_para_1_MWh']['dh_m_si_lastre_50t']} m @ 50 t"
    )
    print()
    print(c["nombre"])
    print(f"  {c['valor']}")
    print(f"  Cobrable hoy: {c['cobrable_hoy']} €")
    print()
    print("ORDEN QUE COBRA")
    print("  1. Estudio 90 días (gemelo + dispersión ω)     30–80 k€")
    print("  2. Piloto simulado con datos de UN parque      80–200 k€")
    print("  3. Dos turbinas reales + tanque 15 m medido    0.5–2 M€")
    print("  4. Licencia €/MW. Kilómetro y Quijote DESPUÉS.")
    print("=" * 72)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--turbinas", type=int, default=10)
    ap.add_argument("--p-mw", type=float, default=5.0)
    ap.add_argument("--mw", type=float, default=0.0, help="si >0, ignora turbinas×p")
    ap.add_argument("--tanque-m", type=float, default=15.0)
    ap.add_argument("--lastre-kg", type=float, default=10.0)
    ap.add_argument("--lastre-t", type=float, default=0.0)
    ap.add_argument("--eta-rt", type=float, default=0.65)
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-20",
    )
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    parque = Parque(n_turbinas=a.turbinas, p_mw=a.p_mw)
    if a.mw > 0:
        parque.n_turbinas = 1
        parque.p_mw = a.mw
    t = Tanque(dh=a.tanque_m, lastre_kg=(a.lastre_t * 1000 if a.lastre_t else a.lastre_kg), eta_rt=a.eta_rt)
    A = producto_a(parque, Mercado())
    B = producto_b(t)
    C = producto_c()
    imprimir(A, B, C)
    path = os.path.join(a.out, "valor_elewit.json")
    with open(path, "w") as fh:
        json.dump({"A": A, "B": B, "C": C}, fh, indent=2)
    print("out", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
