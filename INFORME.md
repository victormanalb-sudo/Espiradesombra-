# Informe 2026-09-20 — Kilómetro / DKP / 6 subciclos

Carpeta de hoy:  
`/storage/emulated/0/Documents/claude-main/claude-main/2026-09-20/`

Ayer (sesión): `.../2026-09-19/`

---

## Error que ya estaba resuelto (y se reabrió un momento)

**Mal:** poner `C2 invierte = x` (588 J) mientras C1+C2.5+C3 sacan ~4x del lastre. Eso da η≈4.5. Es el mismo truco de Lee: no contar cómo vuelven los kg.

**Bien (restituido en `kilometro_6subciclos.py`):**

| Pieza | Qué hace | ¿Paga o genera? |
|-------|----------|-----------------|
| C1 | medio RECTO | genera **x** |
| C2.5 | el otro medio | genera **casi x** |
| C3 | UNO inverso | **genera 2x** (no consume) |
| C3.0 / C3.1 | perneo objeto **o** recorrido, misma cota | **δ ≈ 12 J** |
| C2 | invert + regen + **x.5 del recorrido** | regen en C2; el x.5 (cambio de extremo de lastres *anclados al carril*) va **dentro de C2** |

No hay grúa aparte. No hay lift en C3. No se pone invert=x.

Run 20-sep, tanque 15 m, 10 kg:

- **Eje:** η = **0.686**  NO
- **`--dkp`** (el otro módulo pone x.5 = 0): η = **0.945**  NO  
  El scan `--dkp` puede marcar >1: eso es **no contar el x.5**. En dos módulos, alguien lo paga.

Didáctico: boya ida+vuelta se **cancela**. Queda `m_lastre g Δh`. Mar abierto con V cte **no** es fuente extra.

---

## Lo nuevo en el teléfono (19–20 sep)

### En esta carpeta (`copias/`)

| Archivo | Qué es |
|---------|--------|
| `Paper Técnico - Proyecto 33x1_ Geometría Kilométrica y Ciclo de 6 Etapas.md` | Paper VMA, H=1 km, 6 etapas. Pone Neto_C3 (boya) en el **numerador** y no devuelve el fluido → η>1 de papel. `W_motor_C2 = M g θ` no son julios. |
| `Conversación con Gemini.docx` | Chat Gemini (binario; copia aquí). |
| `dkp.txt` `4subciclos.txt` `codigo pa grok.txt` `code togrok2.txt` `togrok3.txt` | Canvas Lee (numpy, +45/−45, `girar()` inventa KE). **No correr.** |

### Download (no copiado: crypto / no Kilómetro)

Varios `MDC v21–v24` y PDFs de factorización/RSA en Download. **No se analizan aquí** (ataques a cifra). El informe de energía no los usa.

También: `aliado.pdf`, vídeos grok/33x1, `claude-main.zip`.

### Código útil (raíz de hoy)

- `kilometro_6subciclos.py` — ledger cerrado, 6 piezas
- `kilometro_didactico.py` — hermético / mar / nunca neutro
- `gemelo_4ciclos.py` `dkp_lee_corregido.py`
- `COMPARATIVA_HONESTA.md` `RESPUESTA_A_LEE.md`

```bash
python3 /storage/emulated/0/Documents/claude-main/claude-main/2026-09-20/kilometro_6subciclos.py
python3 /storage/emulated/0/Documents/claude-main/claude-main/2026-09-20/kilometro_didactico.py
```

---

## Cómo hablar C1 / C2 / C3 sin liarnos

1. **C3 genera.** 2x. C3.0/C3.1 casi nada.
2. **C2** = invertir + recuperar R + **x.5 para cambiar lastres de extremo** (los que van al *recorrido*, no un perneo de cota).
3. Perneo objeto/recorrido **no** es el lift.
4. Si C2 solo “cuesta x”, reabrimos el ciclo. El x.5, si cambia cota, es **n × m g Δh** dentro de C2.

33×1 civil: inercia + buffer. η_rt < 1. Siguiente TRL: tanque medido, no otro canvas.
