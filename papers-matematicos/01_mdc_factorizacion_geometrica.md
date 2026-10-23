# MDC como factorización geométrica por fase

## Resumen

El Método Diofántico Cinemático (MDC) puede entenderse como una estrategia de factorización basada en la observación de que el problema de encontrar un factor de N puede reformularse como la detección de un cambio de signo en una función de fase asociada a una familia de valores m. En lugar de buscar divisores por ensayo directo, se explora un dominio m y se inspecciona un desfase ΔΦ(m, N) que cambia de signo cuando se cruza una región en la que el factor candidato se vuelve relevante.

La versión original del corpus VMA presenta una lógica muy clara:

- elegir una frontera m_inicial < m < m_final;
- recorrer un rango de candidatos m;
- evaluar un desfase ΔΦ(m, N);
- localizar un intervalo donde ΔΦ cambia de signo;
- refinar el corte por secante o bisección para aproximar el factor.

La propuesta aquí es formalizar este procedimiento como una forma de factorización por geometría de fases.

## 1. Motivación

Dado un entero impar N, queremos encontrar un divisor no trivial d de N. En vez de explorar todos los divisores potenciales, restringimos la búsqueda a una familia de valores m que parametriza una estructura de residuos y de “ángulos” asociados al problema. El punto central es que el conjunto de residuos de N respecto a una familia de formas cuadráticas o lineales produce una función

ΔΦ(m, N)

que cambia de signo precisamente cuando m atraviesa una región cercana a un factor relevante.

Es decir, se asume la existencia de un mapa:

m ↦ ΔΦ(m, N)

con la propiedad empírica de que en una vecindad del factor divisor se produce un cambio de signo o una intersección de ramas. Esto convierte la factoración en un problema de localización de raíces.

## 2. Estructura del método

Se parte del intervalo [m_min, m_max], donde m_max ≈ √N o un valor cercano. El autor del corpus usa la idea de una zona densa alrededor de la raíz cuadrada y luego subdivide la zona por cortes armónicos.

La familia de cortes usa una progresión de la forma

m_i = N / (i(i+1))

o equivalentes, que permiten cubrir el intervalo con particiones telescópicas. Esta elección no es aleatoria: la suma de los incrementos se mantiene acotada y genera una partición natural del rango de búsqueda.

Una vez definidos los cortes, se calcula ΔΦ(m_i, N) en cada punto y se detectan los tramos con signo opuesto.

## 3. Refinamiento por secante

Cuando se detectan dos puntos a < b tales que

ΔΦ(a, N) · ΔΦ(b, N) < 0,

se puede refinar la raíz usando interpolación lineal:

m_c = a + λ(b-a),

con

λ = |ΔΦ(a)| / (|ΔΦ(a)| + |ΔΦ(b)|).

Esto constituye un refinamiento por secante, mejor que una bisectación ciega. Si la secante no da un valor fiable, se aplica una pinza doble o un último paso de bisección.

El método se puede resumir así:

1. elegir partición inicial;
2. localizar signos opuestos;
3. refinar con secante;
4. confirmar factor con verificación final.

## 4. Interpretación geométrica

La vista geométrica del método consiste en pensar que cada m define una “trayectoria” o “fase” del problema asociado a N. Al variar m, la fase cambia continuamente hasta que se cruza una zona crítica. La factorización se vuelve entonces un problema de detectar intersecciones entre dos ramas del espacio de fases.

Esto explica por qué el autor habla de:

- “pinza 4+4”,
- “desfase espiral”,
- “cortes armónicos”,
- “curvas de fase”,
- “zona densa [m_conv, m_max]”.

La estructura es más cercana a la teoría de raíces y a la geometría de funciones que a la aritmética elemental pura.

## 5. Observación computacional

La experiencia del corpus sugiere que:

- la secante acelera la convergencia si los signos están bien determinados;
- la bisección sigue siendo garantía de seguridad cuando la curva es ruidosa;
- la falla no está en la secante en sí, sino en decidir cuándo el signo de ΔΦ es fiable.

En otras palabras, el problema real no es calcular la raíz, sino detectar el intervalo correcto en un paisaje discontínuo y dinámico.

## 6. Forma formal simplificada

Sea f(m) = ΔΦ(m, N). El método busca m* tal que f(m*) = 0. Se construye una partición

m_0 < m_1 < ... < m_k

con cortes armónicos o equivalentes, y se evalúa

f(m_i).

Si f(m_i) y f(m_{i+1}) tienen signos opuestos, el intervalo [m_i, m_{i+1}] encierra una raíz. Luego se refina con

m_{new} = m_i + λ(m_{i+1}-m_i),

λ = |f(m_i)| / (|f(m_i)| + |f(m_{i+1})|).

Cuando dicho refinamiento falla, la estrategia recurre a bisección.

## 7. Conclusión

El MDC, entendiendo su lógica más amplia, puede describirse como una familia de algoritmos de factorización por localización de raíces de una función de fase. El elemento central no es “dividir N”, sino “seguir la señal de un desfase” hasta que la estructura de la factorización emerge.

Esto le da al método una personalidad muy distinta de la criba clásica:

- más geométrica,
- más cinemática,
- más dependiente de la forma del desfase,
- más adecuada para una lectura en términos de “trayectorias” o “curvas de búsqueda”.

Ese punto de vista es especialmente útil como base para trabajos exploratorios y mini-papers matemáticos.

## Versión breve de una hipótesis

Hipótesis: si la función de fase ΔΦ(m, N) presenta cambio de signo en una vecindad de un factor d, entonces una estrategia de partición armónica y refinamiento por secante permite localizar d con coste inferior a la prueba lineal clásica dentro de una región densa.

## Referencias de entorno

- `espiradesombra/claude` — sección de MDC
- archivos del corpus VMA: `mdc_regula_falsi.py`, `mdc_v18` (en la tradición del repo)
- observaciones de densidad local y partición del rango de búsqueda
