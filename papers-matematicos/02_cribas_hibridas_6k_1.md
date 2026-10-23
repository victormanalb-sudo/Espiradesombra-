# Cribas híbridas 6k ± 1 y densidad local de primos

## Resumen

La estructura de cribas que aparece en el corpus de `espiradesombra/claude` se basa en dos ideas recurrentes:

1. restringir la búsqueda a números de la forma 6k ± 1;
2. construir un recorrido local de densidad de primos con una mezcla de filtros geométricos y de fase.

La visión del autor no es una criba clásica “sólo por divisibilidad”, sino una criba híbrida: una combinación de:

- estructura modular 6k ± 1,
- barrido en zonas densas,
- detección de patrones de cambio de signo o de densidad,
- aproximación por modelo cinemático.

## 1. Base modular

Todo entero n > 3 puede escribirse como

n = 6k ± 1,

o bien no es primo, o bien pertenece a la clase de restos relevantes para la prueba de primalidad. Esta observación es clásica, pero aquí toma un papel central: la criba no se diseña como un filtro lineal global, sino como una exploración sobre una estructura modular reducida.

Los candidatos primos se concentran en dos familias:

- 6k + 1
- 6k − 1

Por tanto, la mayoría de la exploración se realiza sobre estas dos progresiones.

## 2. Criba desmemoriada

La expresión “criba desmemoriada” del repo sugiere que la eliminación de múltiplos no requiere mantener una tabla completa del conjunto de enteros. Más bien, la estructura se reconstruye a partir de patrones de separación por residuos.

Esto permite un enfoque de dos fases:

- fase ascendente: abordar el rango [1, √N];
- fase descendente: usar la información recogida para descartar en la zona superior del rango.

La idea es que la eliminación por múltiplos no necesita “recordar” cada paso, sino codificar una regla local de exclusión.

## 3. Criba híbrida

La criba híbrida combina dos niveles:

- un filtrado modular basado en los residuos 6k ± 1;
- un refinamiento por densidad local o región de fase en torno a un valor m.

Formalmente, si p es primo y x es un valor de referencia, la densidad local puede describirse por una función

D(x) ≈ D_0 + V_0 Δn + ½ a_0 (Δn)^2,

que aparece con la formulación MRAUV del repositorio. Esta representación induce un modelo cinemático con un dato inicial D_0, velocidad V_0 y aceleración a_0.

Se trata de una idea útil para producir predicciones locales sin construir una criba completa.

## 4. Densidad local y modelo MRAUV

El autor del corpus habla de un “modelo cinemático de 3 puntos” para predecir π(x). La lectura natural es la siguiente:

- la densidad de primos no parece uniforme en el rango local;
- se comporta como una densidad que cambia con la variación del punto x;
- la evolución puede describirse mediante una aproximación cuadrática local.

Es decir,

π(x + h) − π(x) ≈ D(x) h,

con D(x) modelada por un polinomio cuadrático o por una aproximación a aceleración constante.

Aunque esto no reemplaza la teoría analítica de primos, sí ofrece un marco útil para estimaciones, heurísticas y algoritmos de exploración.

## 5. Relación con Goldbach y Sophie Germain

En el repositorio se conecta la criba con dos tradiciones:

- Goldbach: descomposición de un número par como suma de dos primos;
- Sophie Germain: primos de la forma 2p + 1 con p primo.

La estructura 6k ± 1 vuelve a ser esencial pues la clasificación por restos módulo 6 organiza la búsqueda de primos con un esquema que se adapta bien a la exploración local.

La idea central es que la criba no sólo detecta primos, sino también regiones donde un número par o un primo excepcional se vuelve más probable.

## 6. Heurística simple

Definimos una frontera x y calculamos un estadio local de densidad:

D_pred(x) = D_0 + V_0 Δn + ½ a_0 (Δn)^2.

Entonces la cantidad esperada de primos en [x, x+h] vale aproximadamente

E[π(x+h)-π(x)] ≈ D_pred(x) h.

Esto no es un teorema, pero sí ofrece una herramienta de exploración útil para:

- estimar la localización de primos;
- diseñar búsquedas de factores;
- modelar la variación local de la densidad en una ventana.

## 7. Criba híbrida como procedimiento

Un procedimiento posible es:

1. reducir candidatos a la clase 6k ± 1;
2. construir ventanas de amplitud local h;
3. modelar la densidad con D_pred(x);
4. eliminar los múltiplos esperados;
5. refinar con una comprobación exacta sobre los candidatos restantes.

En forma compacta:

- módulo 6 paraครง 
- ventana local para densidad;
- coerción por factores locales;
- comprobación final exacta.

## 8. Conclusión

La criba híbrida del corpus VMA puede interpretarse como una mezcla de:

- aritmética modular;
- exploración local;
- modelado de densidad;
- heurísticas de fase.

Su valor conceptual es claro: convierte la búsqueda de primos en un problema de estructura local y no sólo de eliminación global.

Esto hace que la criba sea especialmente apta para un mini-paper matemático, porque su forma es reproducible, explicable y fácilmente empíricamente comprobable.

## Hipótesis operativa

Hipótesis: si una progresión de enteros 6k ± 1 es inspeccionada con una ventana local y una densidad estimada D_pred(x), entonces la proporción de primos reales en cada ventana se aproxima mejor que con una criba uniforme simple, y la selección de candidatos se vuelve más eficiente.

## Observación

Esta idea no pretende sustituir la prueba de primalidad clásica ni la teoría analítica de primos; su propósito es estructurar un método de trabajo útil para algoritmos y documentos matemáticos exploratorios.
