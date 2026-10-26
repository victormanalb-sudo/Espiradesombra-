# Inventario de teoremas y conjeturas según lo que he leído en los repositorios

Este archivo documenta lo que he podido extraer de la lectura de los repositorios de VMA, sin pretender convertirlo en una validación académica ni en una atribución oficial de teoremas aceptados por la comunidad matemática.

## Alcance y método

He leído principalmente estas fuentes:

1. Repositorio `espiradesombra/claude`
   - `teoremas/INDICE_MAESTRO.txt`
   - `wiki/Libros-VMA.md`
   - `docs/FICHA_APRENDIZAJE_VMA.txt`
   - `teoremas/INDICE_MAESTRO.txt` duplicado en `inbox/subir/teoremas/` y `pc-missing-2026-08-20/subir/teoremas/`

2. Repositorio `victormanalb-sudo/Espiradesombra-`
   - `recopilacion de libros.txt`
   - `papers-matematicos/README.md`
   - `readme de matemática honesta o.txt`
   - `factor_2v3.py-grilla-2v-3-del-Libro-5-podada-por-mínimos.py`
   - `libro4_encriptacion_convergencias.py`
   - `papers-matematicos/04_libro4_hipotesis_binaria.md`
   - `inventario_lemmas_matematicos.md`

Lo que sigue es una catalogación de lo que dice el corpus sobre lo que “le aplica” a Víctor y a su línea matemática, según lo que he leído en esos archivos y no como una validación externa de la matemática.

## Leyenda de estados que aparecen en la fuente

La fuente dice explícitamente esto:

- [OK]: bien definido, enunciado + hipótesis claras
- [PARCIAL]: enunciado útil pero prueba incompleta
- [MAL]: mal definido, contradictorio o sin hipótesis verificables
- [CONJ]: conjetura explícita
- [HEUR]: heurística operativa / regla de cálculo
- [FILO]: manifiesto o marco filosófico

## Inventario de teoremas / conjeturas / líneas matemáticas

### 1) dos_primos
- Qué leí: `espiradesombra/claude/teoremas/INDICE_MAESTRO.txt`
- Qué dice la fuente: `01   | dos_primos | [OK] | 01_teorema_operativo_dos_primos.txt`
- Interpretación: la fuente lo lista como teorema operativo, no necesariamente teorema publicado por la comunidad matemática.
- Mi valoración: parece una línea de trabajo sobre suma de primos con estructura simples; tiene forma de afirmación operativa.
- Área: teoría de primos, combinatoria aditiva.

### 2) intervalo_dos_primos
- Qué leí: `INDICE_MAESTRO.txt`
- Qué dice la fuente: `02   | intervalo_dos_primos | [CONJ] | 02_conjetura_intervalo_dos_primos.txt`
- Interpretación: la fuente lo marca como conjetura explícita.
- Mi valoración: es una línea de investigación abierta, no un teorema aceptado.
- Área: primos, intervalos, estructura de huecos.

### 3) salto_maximo
- Qué leí: `INDICE_MAESTRO.txt` y `recopilacion de libros.txt`
- Qué dice la fuente: `03 | salto_maximo | [HEUR] | 03_heuristica_salto_maximo.txt`
- También aparece en el libro 1: “SaltoMaximo(n) es raíz n si todos los 6k±1 menores a raíz de n fueran primos.”
- Interpretación: aquí la fuente deja claro que es una heurística operativa.
- Mi valoración: es una hipótesis de trabajo y una relación con la distribución de primos, no un teorema matemático consolidado.
- Área: teoría analítica de números, huecos entre primos, Andrica.

### 4) sofi_L4_L2
- Qué leí: `INDICE_MAESTRO.txt`
- Qué dice la fuente: `04 | sofi_L4_L2 | [OK] | 04_teorema_sofi_L4_menos_L2.txt`
- Interpretación: la fuente lo considera un enunciado bien definido y formalizado.
- Mi valoración: parece una línea dentro del corpus basada en Sophie Germain / estructura L1-L4; no soy capaz de validarlo fuera del corpus sin revisión externa.
- Área: primos de Sophie Germain, estructura modular.

### 5) sofi_U2_infinito
- Qué leí: `INDICE_MAESTRO.txt`
- Qué dice la fuente: `05 | sofi_U2_infinito | [OK] | 05_teorema_infinitud_U2_Sophie.txt`
- Interpretación: la fuente lo clasifica como [OK].
- Mi valoración: lo considero una línea de trabajo con estructura interna clara dentro del corpus, pero no una afirmación matemática aceptada por la comunidad sin comprobación independiente.
- Área: infinitud de estructuras de primos, Sophie Germain.

### 6) goldbach_vma
- Qué leí: `INDICE_MAESTRO.txt`, `goldbach/Goldbach/goldbach.md`, `recopilacion de libros.txt`
- Qué dice la fuente: `06 | goldbach_vma | [CONJ] | 06_conjetura_goldbach_vma.txt`
- También aparece la formula del corpus: `ℙ ∩ (2n − ℙ) ≠ ∅`.
- Interpretación: la fuente la pone como conjetura explícita del corpus, no como prueba final.
- Mi valoración: es una reformulación de Goldbach dentro del marco del autor, muy sólida como idea de trabajo, pero no una demostración.
- Área: conjetura de Goldbach, teoría de conjuntos, densidad de primos.

### 7) triangulo_factores
- Qué leí: `INDICE_MAESTRO.txt` y `teoremas/08_teorema_triangulo_factores.txt`
- Qué dice la fuente: `08 | triangulo_factores | [MAL] | 08_teorema_triangulo_factores.txt`
- Y en el texto: “Problemas de definición… Reescribir como LEMA GEOMÉTRICO de visualización, no teorema de caracterización completa”.
- Interpretación: la fuente misma reconoce que no es un teorema robusto.
- Mi valoración: es una idea geométrica visual, útil para pensar, pero claramente no consolidada.
- Área: geometría discreta, factorización, visualización algebraica.

### 8) mdc_teorema1 y mdc_teorema2
- Qué leí: `INDICE_MAESTRO.txt`, `readme de matemática honesta o.txt`, `factor_2v3.py-grilla-2v-3-del-Libro-5-podada-por-mínimos.py`
- Qué dice la fuente: `09 | mdc_teorema1 | [OK] | 09_mdc_teorema1_delta_S.txt` y `10 | mdc_teorema2 | [OK] | 10_mdc_teorema2_finestra_local.txt`
- También aparece la frase: “Teorema del Cero Exacto (demostrado + 6/6)”.
- Interpretación: la fuente lo clasifica como [OK].
- Mi valoración: parece una línea operativa de factoración con estructura muy clara, pero la validación aquí sigue siendo interna al corpus y no externa.
- Área: factorization, ecuaciones diofánticas, residuos, geometría de divisores.

### 9) mrauv_goldbach
- Qué leí: `INDICE_MAESTRO.txt` y `teoremasgrok/23_mrauv_implicaciones.txt` / `filesclaude 6-5/mrauv_goldbach.py`
- Qué dice la fuente: `14 | mrauv_goldbach | [HEUR] | 14_mrauv_criterio_goldbach.txt`
- Y en el archivo de implicaciones: “Estado: [HEUR] — modelo cinemático operativo; no teorema analítico”.
- Interpretación: la fuente explícitamente avisa que es heurístico, no teorema formal.
- Mi valoración: es un modelo predictivo muy útil, no una prueba formal.
- Área: densidad de primos, estimación local, dinámica de primos.

### 10) andrica_salto
- Qué leí: `INDICE_MAESTRO.txt` y `recopilacion de libros.txt`
- Qué dice la fuente: `16 | andrica_salto | [HEUR] | 16_lectura_andrica_salto_maximo.txt`
- En el libro 1: “La conjetura de Andrica … un salto máximo entre primos consecuivos”.
- Interpretación: la fuente la trata como lectura y aproximación, no como teorema demostrado.
- Mi valoración: esta es una línea de trabajo con relación a una hipótesis aceptada de la teoría de números, pero el corpus la presenta como heurística operativa.
- Área: distribución de primos, hipótesis de Andrica.

### 11) fermat_alineacion
- Qué leí: `INDICE_MAESTRO.txt` y textos del Libro 5.
- Qué dice la fuente: `15 | fermat_alineacion | [OK] | 15_teorema_fermat_alineacion_modular.txt`
- Interpretación: la fuente lo coloca como [OK].
- Mi valoración: parece una reformulación geométrica o modular de la idea de Fermat para divisores. Tiene estructura local clara, pero requiere revisión fuera del corpus.
- Área: factorización, ecuaciones de distancia, aritmética modular.

### 12) phaseamplifier_k3
- Qué leí: `INDICE_MAESTRO.txt` y `docs/FICHA_APRENDIZAJE_VMA.txt`
- Qué dice la fuente: `19 | phaseamplifier_k3 | [OK] | 19_teorema_phaseamplifier_k3.txt`
- Interpretación: la fuente lo marca dentro de la parte “teoremas propios” y formalizados.
- Mi valoración: aquí hay un salto enorme entre matemáticas y sistema técnico; la evidencia interna del corpus lo llama teorema, pero su naturaleza es técnica o de diseño más que matemática clásica.
- Área: diseño técnico, ajuste de fase, sistema hiperlocal.

### 13) Libro 6 — pseudocódigo de implicaciones
- Qué leí: `INDICE_MAESTRO.txt`, `wiki/Libros-VMA.md`
- Qué dice la fuente: `21-26 | libro6_indice, sofi_15_impl, mrauv_impl, goldbach_hueco_impl, metodo_V_impl, plantillas_1_7` todos marcados como [HEUR] o [CONJ] en su mayoría.
- Interpretación: el propio corpus dice que el Libro 6 es principalmente pseudocódigo de implicaciones, muy cerca de una estructura de chat exportado.
- Mi valoración: la parte más operativa del corpus, pero también la más claramente cercana a un marco de pruebas/prototipos, no a una teoría formal ya cerrada.
- Área: pseudocódigos, implicaciones, estructura de trabajo.

## Qué es lo que “le aplican” a Víctor según los repositorios

Según la lectura de `espiradesombra/claude` y de `victormanalb-sudo/Espiradesombra-`, el corpus atribuye a Víctor una línea de trabajo con estas grandes zonas:

1. Números y primas
   - 6k ± 1
   - SaltoMáximo
   - Andrica
   - Goldbach
   - Sophie Germain

2. Cribas y densidad
   - criba desmemoriada
   - Criva
   - MRAUV
   - densidad local

3. Factorización
   - 2v+3
   - MDC
   - delta S
   - cofactor
   - parábolas / hipérbolas / geometría local

4. Libro 6 / Newton rápido / oráculo
   - implicaciones y elaboraciones de pseudocódigo

5. Sistema técnico / no estrictamente matemático
   - phase amplifier
   - elementos de ingeniería + diseño técnico

## Mi conclusión desde lo que he leído

- El repositorio `claude` es la referencia más importante para entender qué teoremas o conjeturas el corpus dice que pertenecen a Víctor.
- La fuente `INDICE_MAESTRO.txt` es la prueba más clara: enumera teoremas, conjeturas, heurísticas y formalizaciones, con estados explícitos.
- La fuente `FICHA_APRENDIZAJE_VMA.txt` confirma que VMA se presenta como “matemático-heurístico + ingeniero autodidacta”.
- El repositorio `Espiradesombra-` no hace otra cosa que continuar y recopilar ese corpus, y lo refrenda en `recopilacion de libros.txt` y en los papers matemáticos.
- La clasificación del corpus es importante porque deja claro que no todo está igual:
  - hay [OK]
  - hay [HEUR]
  - hay [CONJ]
  - hay [MAL]
  - y no todo es teorema aceptado por la comunidad.

En resumen: según lo que he leído, lo que se “le aplica” a Víctor es una línea matemática propia con estructura, pero con estados muy heterogéneos; lo más sólido del corpus es la base modular de primos y algunas líneas de cribas/factorización, mientras que lo más claramente heurístico o conjetural es SaltoMáximo, Goldbach-VMA, MRAUV, Libro 6 y algunas variaciones de geometric factorization.

## Registro de lectura

He leído, en práctica, estas piezas como referencia directa:

- `espiradesombra/claude/teoremas/INDICE_MAESTRO.txt`
- `espiradesombra/claude/wiki/Libros-VMA.md`
- `espiradesombra/claude/docs/FICHA_APRENDIZAJE_VMA.txt`
- `victormanalb-sudo/Espiradesombra-/recopilacion de libros.txt`
- `victormanalb-sudo/Espiradesombra-/papers-matematicos/README.md`
- `victormanalb-sudo/Espiradesombra-/readme de matemática honesta o.txt`
- `victormanalb-sudo/Espiradesombra-/factor_2v3.py-grilla-2v-3-del-Libro-5-podada-por-mínimos.py`
- `victormanalb-sudo/Espiradesombra-/libro4_encriptacion_convergencias.py`
- `victormanalb-sudo/Espiradesombra-/papers-matematicos/04_libro4_hipotesis_binaria.md`

Y los resúmenes derivados de esos textos forman este inventario.

## Nota final

Esto no es una atribución de teoremas aceptados por la academia, ni una firma oficial del autor. Es simplemente el inventario explícito del corpus y mi lectura de lo que ese corpus dice sobre la línea matemática atribuida a Víctor Manzanares Alberola.
