# Gemelos comparativos: BESS vs ZypyZape (FW/Quijote) vs condensador síncrono

**Autor:** Víctor Manzanares Alberola · **Fecha:** 23 de octubre de 2026
**Alcance:** construcción y ejecución de los 4 gemelos digitales y el módulo
económico de la propuesta dirigida a Grok, con dos correcciones acordadas
antes de construirlo (ver §6).

---

## 1. Resumen ejecutivo

- Los 4 sistemas se simularon ante pérdidas de generación de −100, −200 y
  −500 MW en una red de 2 GW. Para −100 y −200 MW todos recuperan la
  frecuencia por encima del nadir de forma similar; **el condensador
  síncrono tiene el mejor nadir** (más inercia efectiva por diseño), seguido
  de cerca por BESS y ZypyZape. Para −500 MW **los 4 sistemas colapsan**
  (la red no tiene reserva primaria suficiente, con o sin dispositivo):
  a esa escala, qué dispositivo se elija es irrelevante.
- En CAPEX, **ZypyZape firmware-only es ~55× más barato por MW que el
  BESS** y ~14× más barato que el condensador síncrono. ZypyZape+Quijote
  queda en un punto intermedio.
- Con el precio FCR actual (≈112.000 €/MW·año) y un despliegue pequeño
  (25 MW, un parque), **ZZ-FW amortiza en ~2 meses y el BESS no amortiza
  en 15 años** a ese precio (necesita >131.000 €/MW·año, por encima del
  precio actual, solo para ROI15=0%).
- **La Parte 9 de la propuesta original (payback de 1 mes a escala de
  toda la flota eólica mundial) estaba mal planteada**, como el propio
  Víctor sospechaba. Corregida con una curva de demanda saturante y un
  techo físico de mercado (~15 GW), el resultado correcto es: retrofitar
  **toda** la flota (1.041 GW) da un payback de 37-212 años porque el
  98,6% de esa capacidad no tiene comprador para este servicio; retrofitar
  **solo** la cantidad que el mercado puede absorber (15 GW) da un
  payback de 0,5-3,1 años. La estrategia racional es la segunda, no la
  primera.

---

## 2. Qué se construyó y qué limitaciones tiene declaradas

**Modelo de red:** ecuación de oscilación agregada de un solo nudo
(swing equation) con gobernador de estatismo (droop) y retardo de primer
orden — el modelo estándar en estudios de RoCoF/respuesta rápida de
frecuencia (ENTSO-E, Anderson & Mirheydar). No es un modelo EMT ni de
flujo de cargas; es el nivel de detalle adecuado para comparar nadir,
ROCOF y potencia de respuesta entre tecnologías, no para diseño de
protecciones.

**Viento:** proceso de Ornstein-Uhlenbeck (v_base=11,4 m/s, σ=1,5) con
ráfaga (+3,5 m/s, t=45-55s) y calma (−5 m/s, t=65-75s) superpuestas, tal
como se pidió.

**Los 4 gemelos**, cada uno como una función de control sobre la misma
interfaz:
- **BESS:** SOC, límite C-rate, eficiencia round-trip 88%, respuesta
  droop+RoCoF con filtro de primer orden (100 ms).
- **ZypyZape FW:** inercia sintética H_zz = 0,5·J·ω²/S, calculada en cada
  paso a partir de ω(viento), inyección P = −2·H_zz·S/f0·(df/dt) acotada
  por P_ZZ_frac.
- **ZypyZape+Quijote:** igual que FW más una masa deslizante que cambia J
  radialmente (5-55 m) según el signo de la desviación de frecuencia,
  con coste de actuador (fuerza centrífuga × desplazamiento) restado de
  la potencia neta inyectada.
- **Condensador síncrono:** respuesta de inercia pura e instantánea,
  P = −2·H·S/f0·(df/dt)·η, sin lógica de control digital.

**Lo que NO se pudo verificar — declarado honestamente:** esta sesión no
tiene acceso al repositorio real de ZypyZape (`01_CONTEXT_ZYPYZAPE.txt`,
`zypyzape_twin_v4_7_quijote.py`). Los parámetros J, f_ciclo, P_ZZ_frac,
masa de Quijote, etc. son los que tú citaste en la propuesta, marcados
como **[ASUNCIÓN]** en el código (`src/gemelos.py`). Si me pasas el repo
o los ficheros, recalculo con los valores reales.

**Monte Carlo:** 25 réplicas × 200 s por combinación (sistema × ΔP), no
las 100 réplicas × 1h de la propuesta original — por tiempo de cómputo
de esta sesión. El método es idéntico; solo cambia N y el horizonte. 300
simulaciones en total, ~1 minuto.

**Un hallazgo de modelado que no estaba en la propuesta:** sin control
secundario (AGC) — fuera del alcance pedido, que se centra en respuesta
rápida (0-30s) — el estatismo primario por sí solo deja la frecuencia
permanentemente unos 0,1-0,25 Hz por debajo de 50 Hz tras el evento. Por
eso "tiempo de recuperación a >49,9 Hz" no es una métrica útil aquí (se
reporta pero hay que leerla con esa salvedad); en su lugar se añadió
**t_nadir** (tiempo hasta el mínimo), que sí es comparable entre sistemas
y es la métrica estándar en estudios de FFR/inercia.

**Colapso del sistema (ΔP=−500 MW):** con un gobernador tope de 300 MW
(15% de 2 GW) y una pérdida de 500 MW, ningún dispositivo de los 4
(todos de pocos MW de capacidad) puede cerrar ese hueco. El modelo
detecta cuando f cae por debajo de 47,0 Hz y lo marca como colapso
(fuera de alcance simular el deslastre de carga en sí) en vez de
reportar frecuencias negativas sin sentido físico, que es lo que salía
en una primera versión del código antes de esta corrección.

---

## 3. Resultados físicos

![f(t)](figuras/01_frecuencia_tiempo.png)

![ROCOF vs ΔP](figuras/02_rocof_vs_dp.png)

| Sistema | ΔP (MW) | f_nadir (Hz) | t_nadir (s) | ROCOF máx (Hz/s) | Colapsa |
|---|---|---|---|---|---|
| SyncCond | −100 | 49,536 | 2,84 | 0,293 | no |
| BESS | −100 | 49,525 | 2,78 | 0,308 | no |
| ZZ_Quijote | −100 | 49,523 | 2,80 | 0,309 | no |
| ZZ_FW | −100 | 49,521 | 2,80 | 0,308 | no |
| SyncCond | −200 | 48,524 | 5,80 | 0,587 | no |
| BESS | −200 | 48,462 | 5,72 | 0,618 | no |
| ZZ_Quijote | −200 | 48,469 | 5,78 | 0,615 | no |
| ZZ_FW | −200 | 48,458 | 5,78 | 0,615 | no |
| **todos** | **−500** | **≈46,98** | **≈2,3-2,5** | **≈1,47-1,55** | **sí (100% de las réplicas)** |

La diferencia entre sistemas en el nadir a −100/−200 MW es real pero
pequeña (centésimas de Hz): a esta escala de perturbación, el nadir lo
domina la inercia propia de la red (H_sys=4s, S_base=2GW), no los pocos
MW que aporta cada dispositivo. El condensador síncrono gana por tener
más "inercia × potencia" disponible (H·S=500 MVA·s) que un parque eólico
de 25 MW (H·S≈68 MVA·s) o una batería de 1 MW.

---

## 4. Resultados económicos

![CAPEX/OPEX](figuras/03_capex_opex.png)

| Sistema | CAPEX (€/MW) | OPEX (€/MW·año) | Payback* | ROI 15a* |
|---|---|---|---|---|
| BESS | 1.100.000 | 17.000 | 11,7 años | −16,8% |
| ZZ-FW | 19.000 | 3.500 | 0,2 años | 5.407% |
| ZZ-Quijote | 108.000 | 7.000 | 1,0 años | 837% |
| SyncCond | 275.000 | 4.500 | 2,6 años | 277% |

*con el precio FCR actual (111.240 €/MW·año en un deployment pequeño
de 25 MW — ver §4.2 sobre por qué el precio cambia con la escala).

![ROI vs horizonte](figuras/04_roi_horizonte.png)

### 4.1 Sensibilidad al precio del servicio

![Sensibilidad](figuras/05_sensibilidad_roi_precio.png)

**P3 — ¿a qué precio se cruza el ROI de ZZ vs BESS?** No se cruza en
ningún punto del rango de precios probado (5.000-150.000 €/MW·año):
ZZ-FW tiene mejor ROI que BESS incluso al precio-suelo del mercado. Lo
que sí tiene un cruce es el propio BESS contra la rentabilidad: **BESS
necesita un precio ≥131.400 €/MW·año solo para que su ROI a 15 años sea
0%** — por encima del precio FCR alemán actual.

### 4.2 Por qué el precio no puede ser una constante a escala de flota

![Saturación](figuras/06_saturacion_mercado.png)

El precio FCR de 112.000 €/MW·año es un precio de escasez que existe
porque el mercado FCR europeo son ~3.000 MW. Se modeló el precio como
una función decreciente de la oferta acumulada desplegada (saturación
hiperbólica, suelo ≈20.000 €/MW·año) y, más importante, se fijó un
**techo físico de mercado** de ~15 GW: la reserva de frecuencia que la
red europea entera puede necesitar (FCR+aFRR+inercia sintética,
dimensionada por el mayor incidente N-1, no por cuánta oferta exista).
Por encima de ese volumen, MW adicionales retrofitados **no tienen
comprador para este servicio concreto**, por barato que sea el CAPEX.

### 4.3 Parte 9 reescrita: escenario de flota global

| Estrategia | MW retrofitados | CAPEX total | Ingreso de mercado/año | Payback |
|---|---|---|---|---|
| Retrofit de TODA la flota (416.532 molinos, 1.041 GW), FW | 1.041.330 | 19.785 M€ | 530 M€ (acotado al techo) | **37,3 años** |
| Retrofit de TODA la flota, Quijote | 1.041.330 | 112.464 M€ | 530 M€ | **212,2 años** |
| Retrofit SOLO hasta saturación del mercado, FW | 15.000 | 285 M€ | 530 M€ | **0,54 años** |
| Retrofit SOLO hasta saturación del mercado, Quijote | 15.000 | 1.620 M€ | 530 M€ | **3,06 años** |

Esto reemplaza el "payback: 1 mes, ROI 1.100%" de la propuesta original,
que surgía de multiplicar el precio de escasez actual por 346× el tamaño
del mercado del que ese precio depende. El 98,6% de la flota mundial
nunca tendría comprador para este servicio aunque técnicamente funcione
—siguen vendiendo energía normalmente, solo no cobran por inercia—.

### 4.4 LCOS

![LCOS](figuras/07_lcos_bess.png)

LCOS solo tiene sentido para un activo que almacena y cicla energía
(BESS: 78-460 €/MWh según ciclos diarios). ZZ-FW, ZZ-Quijote y SyncCond
son capacidad de servicio, no energía almacenada — no se fuerza una
cifra de LCOS para ellos.

---

## 5. Respuestas explícitas

**P1. ¿ZZ-FW ofrece el mismo servicio de red que BESS?**
En nadir y ROCOF, prácticamente sí a −100/−200 MW (diferencias de
centésimas de Hz); en tiempo de respuesta, BESS es más rápido (filtro de
100 ms vs. la dinámica rotor-dependiente de ZZ); en CAPEX, ZZ-FW gana
por 1-2 órdenes de magnitud. BESS puede además absorber potencia
(cargar) de forma controlada, algo que ZZ no hace de la misma manera.

**P2. ¿ZZ-Quijote aporta algo que FW no aporte, que justifique su CAPEX
extra?**
En este modelo, Quijote añade J variable y por tanto algo más de rango
de inercia sintética (P_pico ~1,9× mayor que FW a −100MW), pero multiplica
el CAPEX por ~5,7×. Para servicios de red puros no se recupera esa
diferencia en el ROI comparado con FW (ambos ganan a BESS igualmente,
pero FW gana más). Esto confirma H2: el caso de uso de Quijote está en
microrredes/aislados u otros servicios no modelados aquí (p.ej. control
de potencia activa más fino), no en el mercado de frecuencia de red.

**P3. ¿A qué precio se cruza el ROI de ZZ vs BESS?**
Respondido en §4.1: no se cruzan en el rango probado; BESS necesita
≥131.400 €/MW·año solo para ROI15=0%.

**P4. ¿Punto de saturación del mercado?**
~15 GW de capacidad acumulada [ESTIMACIÓN, no un dato medido], más allá
del cual el precio del servicio cae a su suelo y la capacidad adicional
no encuentra comprador (§4.2-4.3). Esto es el techo físico (lo que la
red necesita), no un techo de precio por unidad.

**P5. ¿El cuello de botella es técnico o económico?**
Depende de la escala: a −500 MW (25% del S_base) es **técnico** — ningún
dispositivo de pocos MW cierra ese hueco, y la red colapsa con o sin
él (la variable que importa ahí es la reserva primaria total del
sistema, no la tecnología del dispositivo). A escala de mercado (Parte
9) es **económico/regulatorio** — el límite no es la física del
dispositivo sino el tamaño del mercado de servicios y, como ya
apuntabas tú mismo, el acceso a OEM: se añadió una partida de CAPEX de
8.000 €/MW por "acceso OEM/certificación" a ZZ-FW y ZZ-Quijote (ausente
en la propuesta original) precisamente para que ese coste no-técnico
quede dentro del número, no solo mencionado en el texto.

---

## 6. Hipótesis contrastadas

- **H1 — ZZ-FW ofrece servicio comparable a BESS con CAPEX ~100× menor:**
  confirmada en CAPEX (58×) y en las métricas físicas a −100/−200 MW;
  parcialmente matizada en tiempo de respuesta (BESS más rápido) y en
  que BESS sí absorbe potencia de forma simétrica.
- **H2 — ZZ-Quijote no justifica su CAPEX extra para servicios de red:**
  confirmada (§P2); su caso de uso probable está fuera de este estudio.
- **H3 — El ROI de ZZ depende críticamente del acceso a OEM (barrera no
  técnica):** no se pudo "contrastar" en el sentido de probar que es la
  barrera dominante, pero se cuantificó una primera estimación de su
  coste (8.000 €/MW) dentro del modelo económico, algo que la propuesta
  original mencionaba en el texto sin ponerle número.
- **H4 — Despliegue masivo → caída del precio FCR → el ROI converge al
  de BESS en 5-10 años:** parcialmente confirmada y corregida: el precio
  cae con el despliegue, pero no converge al de BESS porque incluso al
  precio-suelo (20.000 €/MW·año) ZZ-FW sigue por delante en ROI dado su
  CAPEX tan bajo — lo que de verdad limita el despliegue no es que el
  ROI converja, es que el mercado se satura en volumen (§4.2-4.3).

---

## 7. Dos correcciones hechas antes de construir esto (y por qué)

Antes de escribir una sola línea de código revisé la propuesta y te
señalé dos fallos que habrían producido resultados no creíbles si
Grok los hubiera ejecutado tal cual:

1. **Precio FCR constante multiplicado por 346× el tamaño del mercado
   del que depende ese precio** (Parte 9 original) → sustituido por una
   curva de demanda con saturación + techo físico de mercado (§4.2).
2. **Ausencia de coste de acceso OEM/certificación** en el CAPEX de
   ZypyZape, pese a identificarse en el texto como posible cuello de
   botella (H3) → añadida una partida de 8.000 €/MW [ESTIMACIÓN].

---

## 8. Archivos entregados

```
gemelos_comparativos/
├── src/            código fuente (red.py, gemelos.py, wrapper.py,
│                    economia.py, run_montecarlo.py, run_economia.py,
│                    figuras.py) — reproducible desde cero
├── out/figuras/     7 figuras PNG
├── out/tablas/      6 CSV (métricas físicas crudas y agregadas,
│                    economía base, sensibilidad, escenario de flota,
│                    puntos de cruce)
└── INFORME.md       este documento
```

Para reproducir: `cd src && python3 run_montecarlo.py && python3 run_economia.py && python3 figuras.py`
