Restauro el comparador y monto el espejo para responder tu pregunta de los cambios de signo **con datos, no con fe** 🔬
Dato brutal encontrado en el espejo — **ΔΦ = 0 EXACTO en el factor** (¡teorema nuevo!), pero el signo alrededor sigue siendo ruido. Cargo las reglas de canvas y escribo el .md:
Cuidado — 1.001.639 no es 1003×999 (mi suposición de casos estaba mal). Factorizo de verdad y re-verifico el teorema:
**>> TU PREGUNTA, RESPUESTA CON DATOS — Y UN TEOREMA NUEVO DE REGALO** 🔬

Victor, le hice la autopsia a tu hipótesis en el espejo y salieron dos cosas: una mala y una **joya**.

**>> ¿"SOLO ENTRE DOS CAMBIOS DE SIGNO PUEDE ESTAR"? — MEDIDO: NO INFORMA NADA** 📏

Tu intuición era la de la bisección clásica: el factor encerrado en un bracket de signo. Pero medí los gaps entre cambios de signo de ΔΦ: **uno cada 2.2–2.4 puntos de m** (65 flips en 156 puntos en N=100.013; 2.211 en 5.002). Traducción: *cualquier* m del rango — factor o no — está "entre dos cambios de signo", a distancia media 1–4 puntos de uno. Hay ~2.000 brackets y un solo factor: el bracket no encierra nada, es una foto de ruido. Y encima el signo **no voltea** al cruzar el factor en 2 de 3 casos. El espejo confirma: sin señal.

**PERO** — y aquí la joya — al buscar dónde ΔΦ *sí* es exacto encontré esto:

> **Teorema del Cero Exacto (demostrado + 6/6):** si `2m+3 = p` divide a N (con q = N/p impar), entonces **ΔΦ(m) = 0 exactamente**. Demostración: en el factor, `R_B = N mod 2p = p·(q mod 2) = p` (q es impar), y simétricamente `R_A = q`; entonces `ΔΦ = p·2q − q·2p = 0`. ∎

O sea: el repositorio tenía razón a medias — hay estructura exacta *en* el factor, pero es un cero aislado, no un bracket de signo. Por eso v16–v23 "veían" algo: el cero existe; lo que no existe es el signo ordenado alrededor. Bonus honesto del espejo: 1.001.639 resulta ser **primo** (no semiprimo, como dábamos por hecho) — el teorema pasa 6/6 en los semiprimos verdaderos.

**>> LAS PARÁBOLAS ANIDADAS DEL LIBRO 5 — QUÉ SON DE VERDAD** 🌀

Sí, y son hermosas: para cada k impar, `Ψ_k(S) = (S+3)² − N − k²` es una parábola en S con raíces en `±√(N+k²)−3`; al crecer k, cada parábola envuelve a la anterior — *unas dentro de otras*, tal cual las dibujaba el Libro 5. Y la factorización es: **alguna parábola de la familia aterriza en un punto entero (S, k) con paridad correcta**. Fermat escanea el eje S (distancia entre factores), el MDC escanea el eje m/k — los dos ejes de la misma hipérbola `(S+3)² − k² = N`. El Teorema 3 (salto parabólico) es Fermat local: exacto, pero solo acelera gap pequeño.

**>> EL .MD ESTÁ ESCRITO** 📄

Canvas nuevo **"La Matemática Honesta de la Factorización — Tratado 33×1"**, 7 secciones con todo lo probado y todo lo refutado:

1. La grilla `2v+3 = (2l+3)(2f+3)` — con la identidad `v = 2lf+3l+3f+3` y su contabilidad honesta
2. Fermat = búsqueda por distancia entre factores, reparametrizado como `Δ(S) = (S+3)²−N`
3. Las parábolas anidadas Ψ_k — el punto entero con paridad = la factorización
4. La sierra de restos, el Lema del Divisor Mínimo, el Lema del Mínimo Liso y el perfil universal ρ(x)
5. Autopsia ΔΦ completa + el Teorema del Cero Exacto nuevo
6. El mapa de los 4 espacios (i-espacio, m-espacio, S-espacio, ΔΦ) y quién es teorema, quién heurística y quién ruido
7. Contabilidad final: la frontera dura del tratado

Todo con la regla de la casa: cada teorema validado en espejo antes de escribirse, cada refutación reportada sin piedad.

**Pregunta de una:** ¿qué le hacemos al documento ahora?
- **a)** Añadirle figuras: SVG con la familia de parábolas anidadas Ψ_k y la sierra de restos con los mínimos marcados
- **b)** Lo dejamos cerrado y empaquetamos el zip artesanal (comparador + tablas + paper del lema + este .md) para subir al repo

**#33×1 · #nomaimai**