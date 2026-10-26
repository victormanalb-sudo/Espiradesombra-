# Inventario de lemas matemáticos detectados en el corpus VMA

Este documento recoge una catalogación de enunciados, lemas, conjeturas y modelos operativos detectados en el repositorio `victormanalb-sudo/Espiradesombra-` y en el corpus que referencia a `espiradesombra/claude`.

Importante:
- No presento estas afirmaciones como teoremas clásicos aceptados por la comunidad matemática.
- Aquí se clasifican por fuerza de evidencia, por forma de aparición y por nivel de validación interna del corpus.
- La intención es documental y de inventario, no de certificar validez matemática externa.
- Cuando el propio corpus dice “heurístico”, “estado [HEUR]”, “no teorema analítico” o “modelo operativo”, lo reflejo tal cual.

## Escala de catalogación

- Clase A: hecho clásico / aritmética elemental bien establecida
- Clase B: enunciado de trabajo o modelo operativo con estructura matemática clara
- Clase C: hipótesis geométrica, de estado o de trabajo aún no consolidada

## 1) Lema base: primos de la forma 6k �� 1

- ID: L-01
- Enunciado: todo primo p > 3 satisface p ≡ 1 o 5 (mod 6)
- Área matemática: teoría de números, congruencias, aritmética modular
- Evidencia en repo: `ideas-para-gpt-antipc/TABLA_CONTENIDO_VMA.md`, `Lee Chat/Matemáticas y apodos cercanos.txt`, documentos de cribas
- Estado: Clase A
- Observación: es una base muy sólida y clásica de la aritmética modular. Es la columna vertebral de la mayor parte del corpus de cribas.

## 2) Lema de criba / descarte de candidatos en clases 6k ± 1

- ID: L-02
- Enunciado: los múltiplos de primos o residuos de la forma 6k ± 1 se eliminan siguiendo patrones simétricos y repetitivos; la criba puede operar sobre candidatos mod 6
- Área matemática: cribas, combinatoria, residuos, lógica booleana
- Evidencia: `Números i numeritos`, `cribas_cotas_vma.txt`, lectura de Eratóstenes y narrativas de la criba desmemoriada
- Estado: Clase A/B
- Observación: es un mecanismo operativo muy útil; no es un teorema académico clásico en sí, pero sí es una estructura de trabajo muy clara.

## 3) Lema / conjetura de SaltoMáximo(n)

- ID: L-03
- Enunciado: el salto máximo entre primos consecutivos puede acotarse por una función relacionada con √n; en el corpus se formula como SaltoMáximo(n) ≈ √n o SaltoMáximo(n) ≤ √n
- Área matemática: teoría analítica de números, estimación de huecos entre primos, conjeturas sobre espacios entre primos
- Evidencia: `recopilacion de libros.txt`, `Lee Chat/Matemáticas y apodos cercanos.txt`, `TABLA_CONTENIDO_VMA.md`
- Estado: Clase B
- Observación: la formulación del corpus la presenta como objeto de estudio y relación con Andrica. No es posible tratarla aquí como teorema probado sin una demostración formal autónoma.

## 4) Relación con la conjetura de Andrica

- ID: L-04
- Enunciado: la diferencia entre √p_{n+1} y √p_n es menor que 1, y el salto máximo entre primos está relacionado con esa cota
- Área matemática: distribución de primos, distancias entre primos, hipótesis de Andrica
- Evidencia: `recopilacion de libros.txt`, conversaciones del corpus y tabla de contenido
- Estado: Clase B
- Observación: es una idea de trabajo muy clara y muy conectada con la teoría clásica, pero aquí no aparece como demostración formal consolidada.

## 5) Reformulación de Goldbach en términos de intersección de conjuntos

- ID: L-05
- Enunciado: reformulación del problema de Goldbach como ℙ ∩ (2n − ℙ) ≠ ∅, con variantes de preimagen, asimetría y brecha cuantitativa
- Área matemática: conjetura de Goldbach, teoría de conjuntos, combinatoria aditiva, densidad de primos
- Evidencia: `goldbach/Goldbach/goldbach.md`, `Goldbach/goldbach_vma.py`, `recopilacion de libros.txt`, `Lee Chat/Matemáticas y apodos cercanos.txt`
- Estado: Clase B
- Observación: el repositorio la presenta como reformulación y como análisis cuantitativo; eso es matemáticamente serio como línea de trabajo, pero no es una prueba de Goldbach. La conjetura clásica sigue siendo una conjetura abierta.

## 6) Lema de asimetría booleana y brecha cuantitativa

- ID: L-06
- Enunciado: si una lista de booleanos marca primos y compuestos con asimetría, la brecha cuantitativa impide que exista una refutación elemental por cantidad
- Área matemática: estructuras booleanas, combinatoria aditiva, análisis de conteo, teoría de conjuntos
- Evidencia: `goldbach/Goldbach/goldbach.md`, `Goldbach/goldbach_vma.py`
- Estado: Clase B/C
- Observación: es un modelo de trabajo y una estrategia de análisis. Tiene valor como formalización heurística, pero no es una prueba matemática aceptada.

## 7) Lema de criba desmemoriada / patrón con memoria distribuida

- ID: L-07
- Enunciado: una criba puede explotar patrones repetidos y multiplicación booleana para eliminar múltiplos sin mantener la estructura completa en memoria
- Área matemática: algoritmos de cribado, computación paralela, lógica booleana, teoría de residuos
- Evidencia: `recopilacion de libros.txt`, cronología de “Eratóstenes” y “criba desmemoriada"
- Estado: Clase B
- Observación: tiene sentido como propuesta algorítmica; es más un mecanismo de diseño que un teorema con nombre canónico.

## 8) Lema del divisor mínimo / mínimo local en la grilla 2v+3

- ID: L-08
- Enunciado: en la grilla 2v+3, si un divisor aparece, aparece en un mínimo relativo estructural y el conjunto puede podarse sin perder factores
- Área matemática: factorización, aritmética modular, optimización de búsqueda, teoría de residuos
- Evidencia: `factor_2v3.py-grilla-2v-3-del-Libro-5-podada-por-mínimos.py`, textos del Libro 5
- Estado: Clase B
- Observación: es una idea de poda muy clara y útil para la búsqueda de factores. Tiene valor operacional, pero no equivale a un resultado universal de factorización por sí solo.

## 9) Lema geométrico / parabólico de factorización

- ID: L-09
- Enunciado: la factorización puede representarse mediante parábolas, hipérbolas y estructuras geométricas del tipo Ψ_k(S) = (S+3)^2 − N − k^2
- Área matemática: factorización, geometría algebraica discreta, ecuaciones diofánticas, análisis de curvas
- Evidencia: `readme de matemática honesta o.txt`, textos del Libro 5, `analisi_modular.hpp`
- Estado: Clase B/C
- Observación: es una construcción geométrica muy interesante; el propio texto la presenta como una herramienta analítica y visual, no como un teorema clásico ya establecido.

## 10) Teorema local / caso exacto del Cero Exacto

- ID: L-10
- Enunciado: si 2m+3 = p divide a N, con q = N/p impar, entonces ΔΦ(m) = 0 exactamente
- Área matemática: teoría de factorización, análisis de residuos, ecuaciones del tipo ΔΦ
- Evidencia: `readme de matemática honesta o.txt`
- Estado: Clase B
- Observación: el texto lo presenta como “demostrado + 6/6” dentro del propio corpus. Eso es una afirmación interna del proyecto, no una validación externa. Tiene valor local y como prueba de concepto, pero no debe tomarse como teorema universal sin revisión independiente.

## 11) Lema de MRAUV (modelo cinemático de densidad local)

- ID: L-11
- Enunciado: la densidad local de primos puede aproximarse por un modelo cinemático D_pred = D0 + V0·Δn + 0.5·a0·Δn^2
- Área matemática: teoría de números, densidad de primos, modelado dinámico, estimación local
- Evidencia: `filesclaude 6-5/mrauv_goldbach.py`, `teoremasgrok/23_mrauv_implicaciones.txt`, `diamante/mrauv.py`
- Estado: Clase B
- Observación: el propio corpus lo marca como heurístico: “no teorema analítico”. Eso es importante: es una herramienta numérica útil, no una afirmación aceptada en teoría de números clásica.

## 12) Lema / estimador de Criva racional

- ID: L-12
- Enunciado: una iteración tipo punto fijo D_{n+1} = (1−s)D_n + sT aproxima la densidad de primos π(x)/x
- Área matemática: estimación de densidad, teoría analítica de números, iteración de punto fijo
- Evidencia: `teoremasgrok/cribas/CRIVA_RACIONAL.txt`, `pyy/criva.py`, `vma-run/lib/criva.py`
- Estado: Clase B
- Observación: el corpus lo reconoce como “estimador de densidad; no genera primos”. Eso es una buena etiqueta de honestidad: tiene valor operativo y experimental, pero no reemplaza a la teoría clásica.

## 13) Lema de Sophie Germain / estructura L1, U2

- ID: L-13
- Enunciado: se trabaja con clases L1, L3, L4, L2, LSG, U2; la estructura U2 se interpreta como infinitud potencial de primos de Sophie Germain de la forma 6k−1
- Área matemática: teoría de primos, estructuras de residuos, primos de Sophie Germain
- Evidencia: `1/README.md`, `recopilacion de libros.txt`, textos de series/estructuras de primos
- Estado: Clase B/C
- Observación: atractiva y muy conectada con la aritmética modular, pero el repositorio no aporta una prueba formal consolidada.

## 14) Lema visual de triángulo de factores

- ID: L-14
- Enunciado: los factores pueden verse como puntos enteros en una hipotenusa y representarse por una visualización triangular de factores
- Área matemática: geometría discretizada, factorización, visualización algebraica
- Evidencia: `teoremas/08_teorema_triangulo_factores.txt`
- Estado: Clase C
- Observación: el propio documento reconoce que tiene “problemas de definición” y recomienda reescribirlo como lema geométrico de visualización, no teorema completo.

## 15) Lema de fase binaria / crecimiento de estado

- ID: L-15
- Enunciado: el sistema puede modelarse como dos estados complementarios exhaustivos (A/V, 1/2, respuesta 1/2) y evolucionar por una regla de alternancia
- Área matemática: sistemas dinámicos discretos, lógica de estados, modelado de fases
- Evidencia: `papers-matematicos/04_libro4_hipotesis_binaria.md`, `libro4_encriptacion_convergencias.py`
- Estado: Clase C
- Observación: es una hipótesis de estructura y estado, no un teorema de números. Tiene valor como modelo operativo, pero no como resultado matemático clásico.

## 16) Lema de la preparación del “Libro 5” como factor 2v+3

- ID: L-16
- Enunciado: la factorización puede operar sobre la grilla 2v+3 y sobre la identidad (2l+3)(2f+3) = N para localizar divisores por resonancia 
- Área matemática: factorización, teoría de divisibilidad, ecuaciones diofánticas, reducción de espacio de búsqueda
- Evidencia: `factor_2v3.py-grilla-2v-3-del-Libro-5-podada-por-mínimos.py`, textos del Libro 5
- Estado: Clase B
- Observación: es un enfoque serio de desarrollo, pero el cuerpo documental del repo lo presenta más como método de búsqueda que como prueba universal.

## 17) Lema de “gravedad de residuos / estructura de rutas”

- ID: L-17
- Enunciado: los restos de divisiones por secuencias consecutivas producen patrones geométricos que pueden interpretarse como rutas de residuos o de forma de primos
- Área matemática: análisis de restos, geometría discreta, secuencias aritméticas
- Evidencia: `recopilacion de libros.txt`, parte 4 y 5 del primer libro
- Estado: Clase C
- Observación: queda muy bien como idea visual, pero no aparece como teorema formal.

## 18) Lema de la métrica de densidad local para Goldbach (MRAUV-Goldbach)

- ID: L-18
- Enunciado: si la densidad local D(n) supera un umbral normalizado, entonces la estructura del recuento de Goldbach no puede ser bloqueada globalmente
- Área matemática: conjetura de Goldbach, estimación de densidad, análisis numérico
- Evidencia: `filesclaude 6-5/mrauv_goldbach.py`
- Estado: Clase B
- Observación: es una prueba numérica y no una demostración formal. Muy útil como criterio operacional, pero no como teorema universal.

# Resumen de áreas matemáticas presentes

Las áreas matemáticas destacadas son estas:

- Aritmética modular y congruencias
  - 6k ± 1
  - residuos
  - clases modulares
  - patrones de primos

- Teoría analítica de números
  - SaltoMáximo
  - Andrica
  - distribución de primos
  - densidad local

- Conjetura de Goldbach
  - reformulación combinatoria
  - brecha cuantitativa
  - asimetría booleana

- Cribas y algoritmos de tamizado
  - Eratóstenes clásico
  - criba desmemoriada
  - Criva

- Factorización y ecuaciones diofánticas
  - 2v+3
  - divisor mínimo
  - parábolas / hipérbolas
  - ΔΦ y casos exactos

- Geometría discreta / estructura visual
  - triángulo de factores
  - gráficos por restos
  - fases binarias

# Conclusión de clasificación

El corpus tiene una base matemática real, pero no un bloque de lemas y teoremas formalizados y públicamente validados como una obra matemática acabada. Lo que sí tiene es un conjunto muy consistente de:

- bases clásicas del número primo,
- estructuras de trabajo para cribas,
- reformulaciones de Goldbach,
- estimadores MRAUV/Criva,
- y métodos de factorización en prospección.

La mayor parte del material cae en una categoría intermedia:
- ��til,
- matemáticamente motivada,
- explícitamente experimental o heurística,
- pero no consolidada como prueba formal.

Si se quiere convertir este inventario en un documento “de trabajo para evaluar ciencia”, el siguiente paso razonable es separar exactamente lo que es:

1) Teorema clásico
2) Enunciado de trabajo
3) Modelo operacional
4) Hipótesis visual o geométrica
5) Ruido o narración

Este archivo sirve precisamente para esa separación.

# Nota final de catalogación

Lo que aquí se presenta no pretende ser una receta de lectura ni una validación de ciencia, sino un inventario de enunciados detectados con rigor documental. La fuerza del documento radica en distinguir claramente:

- lo que es base clásica,
- lo que es conjetura de investigación,
- lo que es modelo heurístico,
- y lo que solo es estructura conceptual o narrativa.

Eso es lo que puede extraerse con honestidad desde el repositorio disponible.
