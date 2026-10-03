#!/usr/bin/env python3
"""
Corrección del canvas de Lee (el .py con numpy, +45/−45, girar() crea KE).

Mismas clases: Lastre, Objeto, DKP.
Mismos nombres de subciclos. Física VMA (sesión 2026-09-19):

  C1   RECTO  medio recorrido          → genera
  C2   BATERÍA  giro x.5 (invertir)    → gen y mot
  C2.5 RECTO  el otro medio            → genera   (Lee lo dejaba a 0 J)
  C3   RECTO  UNO inverso + transfer   → genera + recicla lastres

Sin numpy. Termux / Grok Build.

python3 dkp_lee_corregido.py
python3 dkp_lee_corregido.py --lee-geom   # Δh=90 m como el canvas, ledger igual de cerrado
"""
from __future__ import annotations

import argparse
import json
import math
import os

G = 9.81

# --- geometría CANÓNICA (tanque kilometro_sim), no +45/−45 ---
RADIO = 5.0
DH = 15.0
M_LASTRE = 10.0
M_OBJ = 30.0
ETA_GEN = 0.85
ETA_LIFT = 0.90
ETA_MOT = 0.90
DRAG = 0.06
E_PERNO = 1.5
N_PERNOS = 4
VUELTAS = 1.5
STOCK = 5


def mgh(m: float, dh: float) -> float:
    return m * G * dh


class Lastre:
    """Un kg en ALTA o BAJA. soltar genera; reciclar CUESTA (η_lift)."""

    def __init__(self, m: float, dh: float, n_alta: int):
        self.m = m
        self.dh = dh
        self.n_alta = n_alta
        self.n_baja = 0

    def tomar_alta(self) -> bool:
        if self.n_alta <= 0:
            return False
        self.n_alta -= 1
        return True

    def aparcar_baja(self) -> None:
        self.n_baja += 1

    def transfer_a_alta(self) -> tuple[int, float]:
        """C3: lastres al otro punto. Paga lift. Devuelve (n, E_lift)."""
        n = self.n_baja
        lift = n * mgh(self.m, self.dh) / ETA_LIFT
        self.n_alta += n
        self.n_baja = 0
        return n, lift

    def swap_bateria(self) -> int:
        """C2 x.5: extremos intercambiados. Cuenta aparte del lift C3."""
        n = self.n_baja
        self.n_alta += n
        self.n_baja = 0
        return n


class Objeto:
    def __init__(self) -> None:
        self.s = 0.0  # 0 ALTA local, 1 BAJA local
        self.fase = 1  # +1 ida, −1 vuelta

    def recto(self, frac: float, sentido: int) -> None:
        self.fase = sentido
        self.s = min(1.0, max(0.0, self.s + sentido * frac))


class DKP:
    def __init__(self, dh: float = DH, dkp: bool = False):
        self.dh = dh
        self.dkp = dkp
        self.lastre = Lastre(M_LASTRE, dh, STOCK)
        self.objeto = Objeto()
        self.E_gen = 0.0
        self.E_mot = 0.0
        self.E_pin = 0.0
        self.E_c1 = self.E_c2 = self.E_c25 = self.E_c3 = 0.0
        self.log: list[str] = []

    def _pin(self) -> None:
        self.E_pin += E_PERNO * N_PERNOS

    def _recto_gen(self, frac: float, sentido: int) -> float:
        if not self.lastre.tomar_alta():
            return 0.0
        self._pin()
        avail = mgh(M_LASTRE, self.dh) * frac * (1.0 - DRAG)
        e = ETA_GEN * avail
        self.E_gen += e
        self.objeto.recto(frac, sentido)
        self._pin()
        self.lastre.aparcar_baja()
        return e

    def subciclo_1(self) -> dict:
        """RECTO medio → genera. Lee: soltar 90 m + girar() inventa KE."""
        e = self._recto_gen(0.5, +1)
        self.E_c1 += e
        self.log.append(f"C1 RECTO medio {e:.1f} J  A/B={self.lastre.n_alta}/{self.lastre.n_baja}")
        return {"canal": "recto", "E_gen": e, "frac": 0.5}

    def subciclo_2(self, vueltas: float = VUELTAS) -> dict:
        """BATERÍA: invertir julios (giro x.5). Lee: girar() crea ½Iω² de la nada."""
        m_path = self.lastre.n_baja * M_LASTRE
        m_spin = M_OBJ + m_path
        w_loop = m_spin * G * self.dh
        full = int(vueltas)
        half = vueltas - full
        e_inv = ETA_GEN * (1.0 - DRAG) * w_loop * full
        mot_inv = (w_loop * full) / ETA_MOT * (1.0 + DRAG)
        swap = m_path * G * self.dh if abs(half - 0.5) < 1e-9 else 0.0
        if self.dkp:
            mot_swap, paid = 0.0, "DKP"
        else:
            mot_swap, paid = swap / ETA_MOT, "eje"
        self.E_gen += e_inv
        self.E_c2 += e_inv
        self.E_mot += mot_inv + mot_swap
        nswap = self.lastre.swap_bateria()
        self.log.append(
            f"C2 BATERÍA invert {vueltas} gen {e_inv:.1f} mot {mot_inv+mot_swap:.1f} "
            f"SWAP {nswap} via {paid}"
        )
        return {"canal": "bateria", "E_gen": e_inv, "E_mot": mot_inv + mot_swap}

    def subciclo_2_5(self) -> dict:
        """RECTO el otro medio → genera. Lee lo ponía a 0 J (solo asignaba Z)."""
        e = self._recto_gen(0.5, +1)
        self.E_c25 += e
        self.log.append(f"C2.5 RECTO otro medio {e:.1f} J")
        return {"canal": "recto", "E_gen": e, "frac": 0.5}

    def subciclo_3(self) -> dict:
        """RECTO uno inverso + transfer. Lee: sumaba la misma KE otra vez."""
        e = self._recto_gen(1.0, -1)
        self.E_c3 += e
        n, lift = self.lastre.transfer_a_alta()
        self.E_mot += lift
        self.objeto.s = 0.0
        self.log.append(f"C3 RECTO inverso UNO {e:.1f} J  TRANSFER {n} lift {lift:.1f} J")
        return {"canal": "recto", "E_gen": e, "frac": 1.0, "transfer": n, "E_lift": lift}

    def ciclo_completo(self, n: int = STOCK) -> dict:
        ok = 0
        for _ in range(n):
            if self.lastre.n_alta <= 0:
                break
            self.subciclo_1()
            self.subciclo_2()
            self.subciclo_2_5()
            self.subciclo_3()
            ok += 1
        net = self.E_gen - self.E_mot - self.E_pin
        denom = self.E_mot + self.E_pin
        return {
            "ciclos": ok,
            "stock_final": [self.lastre.n_alta, self.lastre.n_baja],
            "E_gen_C1_recto_medio": round(self.E_c1, 2),
            "E_gen_C2_bateria": round(self.E_c2, 2),
            "E_gen_C25_recto_otro_medio": round(self.E_c25, 2),
            "E_gen_C3_recto_inverso_uno": round(self.E_c3, 2),
            "E_gen_recto": round(self.E_c1 + self.E_c25 + self.E_c3, 2),
            "E_gen": round(self.E_gen, 2),
            "E_mot": round(self.E_mot, 2),
            "E_pin": round(self.E_pin, 2),
            "E_net": round(net, 2),
            "eta_real": round(self.E_gen / denom, 3) if denom else None,
            "eta_gt_1": False,
            "bugs_de_Lee": {
                "numpy": "este Termux no lo tiene",
                "girar_crea_KE": "ω = 2π·vueltas/dt → KE enorme y falsa",
                "C3_resuma_KE": "energia_cinetica se volvía a sumar",
                "C25_a_cero": "el otro medio SÍ genera",
                "subir_nunca_llamado": "Lastre.subir existía y no se usaba → η aparente",
                "Delta_h_90m": "canvas +45/−45; tanque canónico 15 m",
                "eta_aparente": "neta / mgh sin lift = truco contable",
            },
            "log": self.log,
        }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lee-geom", action="store_true", help="Δh=90 m como el canvas")
    ap.add_argument("--dkp", action="store_true")
    ap.add_argument(
        "--out",
        default="/storage/emulated/0/Documents/claude-main/claude-main/2026-09-19",
    )
    a = ap.parse_args()
    dh = 90.0 if a.lee_geom else DH
    r = DKP(dh=dh, dkp=a.dkp).ciclo_completo()
    os.makedirs(a.out, exist_ok=True)
    name = "lee_corregido_90m.json" if a.lee_geom else "lee_corregido.json"
    if a.dkp:
        name = name.replace(".json", "_dkp.json")
    path = os.path.join(a.out, name)
    with open(path, "w") as f:
        json.dump(r, f, indent=2, ensure_ascii=False)
    print("dh", dh, "dkp", a.dkp)
    print("RECTO  C1", r["E_gen_C1_recto_medio"], "C2.5", r["E_gen_C25_recto_otro_medio"],
          "C3", r["E_gen_C3_recto_inverso_uno"])
    print("BATERÍA C2", r["E_gen_C2_bateria"], "mot", r["E_mot"], "net", r["E_net"])
    print("stock", r["stock_final"], "η real", r["eta_real"], "(no >1)")
    print("out", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
