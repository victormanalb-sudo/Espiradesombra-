# Respuesta a Lee — no hay que “pulir” hacia 105 %
2026-09-19 · pegar tal cual

Los archivos de Víctor **no están incompletos**. Corrigen el canvas.

## Tabla que pedías

| Pregunta tuya | Respuesta |
|---|---|
| ¿Usan `Lastre`, `Objeto`, `DKP`? | `dkp_lee_corregido.py` sí, mismas clases. `gemelo_4ciclos.py` usa ledger + funciones. Misma física. |
| ¿Mismos parámetros +45/−45, Hg, 90 m? | **No.** Tanque canónico **Δh = 15 m** (`kilometro_sim`). `--lee-geom` prueba 90 m: η sigue ~0.60. |
| ¿Mercurio? | Densidad sí. No hace falta para la 1ª ley. Fe+aceite/agua basta. |
| ¿`girar()` ½Iω²? | **Bug.** `ω = 2π·vueltas/dt` inventa KE. C2 es **motor/regen**, no KE gratis. |
| ¿C2.5 = 0 J? | **Mal.** C2.5 es el **otro medio RECTO** y genera (igual que C1). |
| ¿C3 = KE otra vez − 6 J? | **Mal.** C3 es **uno RECTO inverso** + transfer de lastres (paga lift). |
| ¿`subir()`? | En tu código **existe y no se llama**. Por eso sale 105 %. |
| ¿η 105 % vs COMPARATIVA_HONESTA? | La comparativa es la correcta. η real **0.59 eje / 0.69 DKP**. JSON: `4ciclos_eje.json`, `4ciclos_dkp.json`. |
| ¿`gemelo_dkp.py` son 4 subciclos? | No. Es el ledger K1/K2 (embrague inelástico). Los 4 subciclos están en `gemelo_4ciclos.py`. |
| ¿Momento angular K1↔K2? | Conserva **L**, no duplica KE. Tras desperneo KE cae a la mitad (o regen de embrague). |
| ¿Cancelación de inercias `E_freno*0.3`? | Eso borra julios a mano. Sentidos opuestos cancelan **par del bastidor**, no energía. |
| ¿JSON coinciden con tu run? | No, y **no deben**. Tú no cierras el ciclo. |

## Los 4 subciclos (Víctor, no el canvas)

C1 RECTO medio → genera  
C2 BATERÍA (giro x.5, invertir) → gen y mot  
C2.5 RECTO otro medio → genera  
C3 RECTO uno inverso + transfer → stock 5→5  

C1+C2.5 = un recorrido. C3 = el mismo al revés. C2 no es recto.

## Qué no hacer ahora

No más canvas numpy. No optimizar hacia η>1. No factor mágico de frenado.

## Qué sí

```bash
python3 /storage/emulated/0/Documents/claude-main/claude-main/2026-09-19/dkp_lee_corregido.py
```

Siguiente TRL: tanque 15 m, 3/4 pesos, pernos, vatímetro. Sin piloto, no hay 105 % ni $50/kWh.
