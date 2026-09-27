# DKP + Kilómetro vs otros almacenes — comparativa HONESTA
**2026-09-19** · VMA / espiradesombra · gemelo: `gemelo_4ciclos.py`

Lee (el canvas largo) y el gemelo de Termux **no describen el mismo ciclo**.
Lee: Δh = 90 m, `girar()` crea KE, C2.5 = 0 J, C3 vuelve a sumar KE, η aparente 105–530 %.
VMA (sesión Termux): 4 subciclos, tanque Δh = 15 m, ledger cerrado.

## Los 4 subciclos (los que sí coinciden con Víctor)

| Subciclo | Recorrido | Canal | Qué hace |
|----------|-----------|-------|----------|
| **C1** | medio | RECTO | genera |
| **C2** | giro x.5 | **BATERÍA** | invierte y genera |
| **C2.5** | el otro medio | RECTO | genera |
| **C3** | **uno**, sentido inverso | RECTO | genera + mueve lastres al otro punto |

C1 + C2.5 = un recorrido. C3 = el mismo al revés. C2 no es recto.
C3 recicla lastres → stock 5→5, el de 4 se puede repetir.
Run 2026-09-19: η real **0.59** (eje) / **0.69** (`--dkp`). dPE = 0. **η>1 solo si no pagas el lift.**

## Dónde SÍ es distinto (ingeniería, no milagro)

| Frente | Litio / H₂ / Energy Vault / flywheel | DKP + Kilómetro (4 subciclos) |
|--------|--------------------------------------|-------------------------------|
| Física | 1 canal (químico, H₂, solo vertical, solo Jω²) | **Recto + rotatorio + 3/4 densidad + perneo** |
| Qué almacena | e⁻, H₂, mgh bloques, ½Jω² | **Lastres (PE) + fase del recorrido (C2)** |
| Pico | Li ms; Vault 1–5 s; flywheel s | C2/DKP como **buffer de pico** (par + inercia) |
| Reciclo | carga eléctrica / grúa / motor | **x.5 vueltas + C3 transfer** (geometría) |
| Cierre 1ª ley | η_rt < 1 siempre | **igual**: η_rt toy 0.59–0.69 |
| Fuente primaria | no (almacén) | **tampoco** (buffer / respaldo de red) |

Eso es real y ya está en `kilometro_sim/` y `PROTOCOLO_ESTRELLA`.

## Dónde Lee NO coincide (y no se puede vender)

1. **η aparente 105–530 %** = no contar el lift. En el gemelo, C3 **paga** el transfer. η<1.
2. **Δh 90 m (+45/−45)** ≠ tanque canónico **15 m**. Cambia el kWh, no la 1ª ley.
3. **`girar(n)` crea julios** — ω no nace sola; C2 es motor/regen, no KE gratis.
4. **C2.5 = 0 J** — en el modelo VMA C2.5 **genera** (otro medio recto).
5. **C3 solo 50 J de KE** — C3 es **uno recto inverso**, ~2× el medio de C1.
6. **$50/kWh, 10 kWh / 200 m³, vida 30 años** — no hay BOM medido. Energy Vault ~80–90 % rt es el techo honesto a imitar, no a “superar por no cerrar el ciclo”.
7. **Mercurio** — densidad sí; toxicidad, precio y regulación lo descartan frente a acero/hormigón/agua. El corpus ya admite Fe+aceite / salmuera.
8. **“Sin degradación”** — pernos, juntas, fluido, fatiga. Mecánico ≠ eterno.
9. **“Genera en cada ciclo por momento angular”** — L se **reparte**, no se crea. DKP = embrague + desfase, no pozo.

## Frente a cada familia (una línea)

- **Litio:** ellos ganan en ms y densidad Wh/kg. DKP gana si el valor es **inercia/pico + vida mecánica**, no en η>1.
- **H₂:** peor η_rt (~30–50 %). DKP no necesita electrolizador. Sigue siendo almacén, no fuente.
- **Energy Vault / Gravitricity:** **el primo honesto**. Misma física (mgh). La diferencia VMA es **3/4 + perneo + media rotatoria**, no superar 100 %.
- **Flywheel:** C2 es el pariente. DKP añade PE de lastre (C1/C2.5/C3 recto).
- **Mountain gravity:** misma PE; DKP apuesta a **tanque modular** en vez de orografía.

## Frase que sí se puede firmar

> Kilómetro/DKP es un **híbrido recto + batería rotatoria + reciclo de lastres por fase**, pensado para **picos e inercia civil**. Round-trip < 1. El “>100 % aparente” es un ciclo no cerrado. El 4-subciclo infinito es **stock que vuelve**, no julios de más.

Código: `gemelo_4ciclos.py` en esta carpeta.
```bash
python3 /storage/emulated/0/Documents/claude-main/claude-main/2026-09-19/gemelo_4ciclos.py
python3 /storage/emulated/0/Documents/claude-main/claude-main/2026-09-19/gemelo_4ciclos.py --dkp
```
