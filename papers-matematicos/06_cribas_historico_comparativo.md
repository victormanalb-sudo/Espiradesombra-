# Cribas históricas, comparativas y usos: de Eratóstenes a la computación moderna

## Resumen

Las cribas son una de las herramientas más antiguas, duraderas y poderosas de la teoría de números. Su función es simple en apariencia: filtrar un conjunto de enteros y separar los que cumplen una propiedad de quienes no la cumplen. En la práctica, y especialmente en la era moderna, la criba se ha convertido en un mecanismo central de la aritmética computacional, la factoración, la primalidad, la enumeración de primos y la seguridad digital. Su historia va desde la antigua Grecia hasta la infraestructura de computación moderna y la búsqueda de primos gigantes en clústeres y supercomputadoras.

Este trabajo ofrece una comparación histórica y técnica entre distintas clases de cribas: la clásica de Eratóstenes, la segmentada, la desmemoriada o modular, la rueda de residuos, y las variantes más avanzadas usadas en entornos de memoria compartida y memoria distribuida. Se revisan los usos fundamentales de los primos, la motivación histórica detrás de cada era, y la relación entre la criba y el hardware. El propósito no es solo explicar una técnica matemática, sino mostrar cómo una idea antigua se transforma en una infraestructura moderna y cómo la mejor criba no es la más bonita en teoría, sino la que mejor se adapta al rango de trabajo y al hardware disponible.

La historia de las cribas se entrelaza con la historia de la ciencia moderna. Eratóstenes y Euclides trabajaron en una lógica de eliminación y clasificación que, siglos después, se convirtió en una herramienta vital para la criptografía, la búsqueda de grandes primos, la investigación en teoría de números y la computación de alto rendimiento. El hilo común es siempre el mismo: distinguir rápidamente lo que importa de lo que se puede descartar.

## 1. Qué es una criba y por qué importa

Una criba es un algoritmo de filtrado: dado un conjunto de enteros, se eliminan los que no cumplen una propiedad relevante, dejando intactos los que sí la cumplen. En teoría de números, la propiedad más clásica es la primalidad. Se toma un intervalo [2, N], se eliminan los múltiplos de 2, de 3, de 5, etc., y lo que queda son los primos.

La criba es, en esencia, un método de tamizado. Su fuerza no es únicamente aritmética; es metodológica. Permite transformar el problema de “encontrar primos” en la tarea más barata de “marcar múltiplos”. Esa reducción es tan poderosa que la historia de la teoría de números se puede leer, en parte, como una historia de cómo mejoramos el tamizado del conjunto de enteros.

El arte de la criba consiste en decidir qué información es esencial y qué se puede descartar sin perder resultados. Por eso esta área se conecta profundamente con la informática: una buena criba reduce trabajo inútil, aprovecha mejor el caché, el flujo de datos y la memoria, y se adapta mejor a la arquitectura del hardware.

## 2. Eratóstenes y la primera gran idea: filtrar el conjunto

### 2.1. Eratóstenes de Cirene

Eratóstenes de Cirene (aproximadamente 276–194 a. C.) es el gran nombre de la primera criba sistemática. Vivió en Alejandría, uno de los grandes centros científicos del mundo antiguo. Su trabajo no respondió a un incentivo comercial ni a la lógica del mercado moderno; responde a la lógica del conocimiento y a la práctica de la matemática elemental. Aun así, lo que hizo fue una invención de alcance enorme: una técnica para detectar primos en un rango definido, utilizando la eliminación de múltiplos. La historia de la criba comienza ahí.

### 2.2. Qué hizo Eratóstenes exactamente

El método clásico consiste en:

- listar todos los enteros desde 2 hasta N;
- marcar 2 como primo y borrar sus múltiplos;
- pasar al siguiente número no marcado y repetir;
- continuar hasta √N.

La lógica es de gran eficacia: si un número n no es primo, tiene algún divisor menor o igual a √n. Por tanto, una vez que se han eliminado todos los múltiplos de los primos pequeños, los números restantes no eliminados son primos.

Es un algoritmo de gran elegancia, muy simple, y aún hoy sigue siendo la base de muchas implementaciones modernas. No es casualidad que la criba de Eratóstenes sea la “fundación” de la teoría del tamizado.

### 2.3. Por qué esto fue importante

Eratóstenes introdujo una técnica que no ofrece solo conocimiento de un primos concreto, sino una visión del conjunto completo. La criba no solo responde qué números son primos; responde también cómo se distribuyen, cómo se organizan y qué estructura hay detrás de la densidad del conjunto de primos. Es decir, la criba es una herramienta de clasificación del espacio numérico.

## 3. Euclides, Euler y la base conceptual de los primos

La criba no es solo un algoritmo sin teoría. Necesita una base conceptual. Esa base la dieron figuras fundamentales de la historia de la matemática.

### 3.1. Euclides y la infinitud de los primos

Euclides (siglos IV-III a. C.) mostró que hay infinitos primos. La importancia de este resultado es enorme, porque convierte a los primos en una estructura esencial del sistema numérico. Si los primos fueran finitos, la teoría de números tendría una forma muy distinta. Pero la infinitud del conjunto inicializa la idea de una estructura profunda y casi inagotable.

### 3.2. Euler y la distribución analítica

Leonhard Euler (1707–1783) tuvo una influencia central porque conectó los primos con la función zeta, la suma sobre inversos de enteros, y la distribución asintótica de los primos. La relación entre:

- π(x) = número de primos ≤ x,
- y la distribución de los primos alrededor de x / log x,

es quizá la mayor pieza conceptual de la teoría de números moderna.

La criba se vuelve entonces mucho más que un método de cálculo. Se convierte en una aproximación a la estructura de la distribución de primos. La criba tiene una dimensión analítica y otra computacional.

### 3.3. Legendre y la criba como herramienta de contaje

Legendre introdujo un punto importante: la criba ya no solo sirve para listar primos, sino también para contar primos y estimar su densidad. La relación entre el número de primos y el rango N se vuelve la base de muchas estimaciones posteriores.

La línea histórica es clara:

- Eratóstenes: primer tamizado práctico.
- Euclides: base conceptual de la infinitud.
- Euler y Legendre: base analítica de la densidad.
- Meissel, Lehmer, Deléglise y otros: computación masiva y alturas de rendimiento.

## 4. El siglo XIX y la computación temprana: cuando la criba deja de ser artesanal

### 4.1. Meissel y la necesidad de contar primos más rápido

En el siglo XIX y principios del XX, la necesidad de contar primos y estimar la distribución de los primos dejó de ser una curiosidad puramente geométrica. Aparecen métodos más avanzados: la criba combinatoria, las aproximaciones con fórmulas de conteo y la idea de mover la aritmética hacia computación más inteligente. Meissel, y luego Lehmer, formaron una línea de enfoque que se aparta de la criba simple y entra en la métrica de rendimiento.

Esto es un cambio importante: la criba deja de ser un procedimiento “manual” y se vuelve un problema de ingeniería y de coste computacional.

### 4.2. Lehmer: la criba como motor computacional

D. H. Lehmer, en el siglo XX, llevó la idea del conteo de primos a un nivel mucho más alto. Sus métodos combinatorios y de tamizado fueron una revolución porque demostraron que una criba, si se la formula bien, puede ser mucho más eficiente de lo que parece en la primera aproximación. Eso fue clave para la aritmética computacional posterior.

### 4.3. ¿Por dinero o por gusto?

La gente que desarrolló estas ideas no lo hacía por “ganar dinero rápido”, sino por una mezcla de interés intelectual y necesidad técnica. La historia de la teoría de números y la historia de la computación se entrelazan de modo muy claro: en gran parte, los avances se hicieron por interés científico y por la exigencia de resolver problemas prácticos de número y computación. En la era moderna, sí hay dinero implicado, especialmente en criptografía, pero la génesis de la criba es más bien una mezcla de visión matemática y necesidad de computación efectiva. El “gusto” por resolver un problema esencial ha sido más importante que el pago inmediato.

## 5. Criba clásica de Eratóstenes: ventajas y límites

La criba clásica tiene estas características:

- tiempo: asintóticamente O(n log log n)
- memoria: O(n)
- simple de implementar
- excelente para rangos pequeños y medianos
- muy fácil de depurar y verificar

Su gran punto fuerte es la sencillez. Su gran punto débil es la memoria: para N grande, guardar todo el rango en memoria puede ser demasiado costoso. Es todavía una herramienta excelente para resultados pequeños, pero cuando se suele trabajar en 10^9, 10^12 o más, el algoritmo necesita ser mejorado.

Aun así, en la práctica no debe subestimarse. Para tareas pedagógicas, prototipos, estudios de densidad y verificación, la criba clásica sigue siendo una referencia central.

## 6. Criba segmentada: la primera gran respuesta al problema de memoria

### 6.1. Qué es una criba segmentada

La criba segmentada resuelve el problema de memoria dividiendo el rango total en bloques o segmentos, de forma que se procesa una pequeña porción del conjunto a la vez. La idea es la siguiente:

- se calculan los primos pequeños hasta √N;
- se toma un bloque contiguo [L, R];
- se marcan los múltiplos de cada primo pequeño que caen dentro del bloque;
- se pasa al siguiente bloque.

### 6.2. Ventajas

La criba segmentada tiene varias ventajas enormes:

- usa mucha menos memoria que la clásica;
- funciona bien para grandes rangos;
- se adapta muy bien a las jerarquías de caché de la CPU;
- se puede paralelizar fácilmente con memoria compartida;
- es natural para un sistema computacional de alto rendimiento.

### 6.3. Complejidad asintótica

La complejidad en tiempo sigue siendo similar a la clásica:

- tiempo: O(n log log n)
- memoria: O(√n + B)

donde B es el tamaño del bloque. Esa mejora de memoria cambia completamente la escala práctica del algoritmo.

### 6.4. Importancia en la computación actual

La criba segmentada es probablemente la forma más importante de generar primos grandes en CPU moderna. Es la base de muchas implementaciones que trabajan con billones de enteros o con intervalos enormes. Es también fundamental en el conteo de primos, en la enumeración de primos en intervalos largos, en la preparación para pruebas de primalidad y en aplicaciones relacionadas con la criptografía.

## 7. Criba desmemoriada y “wheel sieve”: cuando lo importante es no marcar lo que no hace falta

### 7.1. Concepto general

La criba desmemoriada no significa literalmente “sin memoria”, sino “sin mantener un registro completo del rango”. En lugar de marcar todos los enteros, se trabaja con clases de residuos, con patrones de múltiplos, con ruedas de residuos, o con una estructura modular que reduce en gran medida la cantidad de trabajo.

Por ejemplo, en vez de trabajar con todos los enteros, se trabaja solo con:

- 6k ± 1,
- 30k ± 1,
- 210k ± 1,
- y así sucesivamente.

Esto reduce drásticamente el número de candidatos que hay que inspeccionar.

### 7.2. Rueda de residuos

La rueda de residuos elimina de entrada aquellas clases que no pueden ser primos por la congruencia módulo 2, 3, 5, 7, etc. El principio es: si n no es 2, 3, 5, 7 y no pertenece a una de las clases compatibles con la rueda, entonces no puede ser primo. Esto permite reducir el espacio de búsqueda muy fuertemente.

### 7.3. Ventajas

- evita marcar enteros que no pueden ser primos;
- reduce memoria y trabajo innecesario;
- se integra bien con vectorización y arquitectura SIMD;
- ofrece buena localidad de datos en ciertos rangos;
- es especialmente útil cuando el objetivo es generar primos grandes o contar primos en un intervalo muy amplio.

### 7.4. Limitaciones

- la lógica es más compleja;
- la división por clases de residuos exige más diseño matemático;
- y no siempre es la opción más directa para implementaciones rápidas y simples.

## 8. Criba de Atkin, cribas avanzadas y el paso a la computación moderna

### 8.1. Criba de Atkin

La criba de Atkin, publicada por A. O. L. Atkin y Daniel J. Bernstein, es una mejora importante respecto a la clásica de Eratóstenes. En vez de marcar múltiplos directamente, usa criterios de congruencia para marcar valores con un patrón aritmético. La idea central es que los números cumplen condiciones de validez que pueden expresarse en términos de ciertas formas cuadráticas. Esto permite una operación más selectiva.

La criba de Atkin puede ser más eficiente que la clásica cuando se implementa bien en sistemas modernos. Es especialmente buena cuando se quiere generar una gran cantidad de primos en rangos extensos y se cuenta con hardware moderno.

### 8.2. Cribas vectorizadas y optimizadas para hardware

La historia moderna no es solo sobre la teoría, sino sobre la adaptación de la técnica al hardware. En procesadores modernos, lo importante es no solo el algoritmo sino la arquitectura:

- caché L2 / L3,
- vector units (SIMD),
- memoria DDR5,
- varios núcleos,
- GPU / CUDA,
- cluster con memoria distribuida,
- y a veces FPGAs.

La mejor criba moderna explota el hardware. La clave es reducir el trabajo inútil y hacer que cada operación tenga relevancia aritmética y de memoria. Esto es exactamente lo que separa una criba “de laboratorio” de una criba “de producción”.

### 8.3. GIMPS y la búsqueda de primos gigantes

La Great Internet Mersenne Prime Search (GIMPS) es un ejemplo claro de lo que hace posible la criba en la práctica. El objetivo es encontrar primos de Mersenne, y para ello el diseño computacional ha evolucionado hasta convertir la prueba de primalidad y la generación de candidatos en un problema de ingeniería, no solo de teoría. En este espacio, la criba deja de ser una curiosidad. Se vuelve un motor de búsqueda que requiere años de cálculo distribuido y hardware especializado.

## 9. Cribas para memoria compartida vs memoria distribuida

### 9.1. Cribas en memoria compartida

En un sistema con memoria compartida, el problema se resuelve mejor si se divide el intervalo en bloques. Cada hilo trabaja en un bloque, y todos comparten la pequeña lista de primos pequeños. Esto hace que la paralelización sea casi natural.

La criba segmentada se comporta especialmente bien aquí:

- trabajo por bloques,
- caché útil,
- dinámica de reparto,
- muy fácil de implementar en OpenMP, C++ threads, TBB, CUDA o herramientas similares.

La criba desmemoriada también puede funcionar aquí, pero en general su gran fuerza aparece cuando se reduce el espacio de candidatos y se optimiza el patrón de residuos; en memoria compartida, la segmentación suele ser el primer nivel de diseño.

### 9.2. Cribas en memoria distribuida

En un sistema distribuido, el problema no es solo cuánto cálculo hace cada procesador, sino cómo se reparte el trabajo entre varios nodos y cómo se fusionan los resultados. La criba segmentada es la estrategia más natural. Cada nodo recibe un intervalo, trabaja con la lista de primos pequeños y devuelve sus resultados. Esto es la base de los clústeres y supercomputadores.

La criba desmemoriada, aunque puede tener sentido en cada nodo, se vuelve más compleja a nivel global, porque los patrones locales requieren coordinación adicional. En otras palabras:

- segmentada: mejor para repartir trabajo globalmente;
- desmemoriada: mejor para ahorrar trabajo localmente.

### 9.3. La mezcla más potente

La mejor estrategia real suele ser mixta:

- segmentada a nivel global para repartir el rango;
- rueda o residuos a nivel local para reducir trabajo dentro de cada bloque;
- parallelización por hilos o nodos;
- vectorización y diseño para memoria caché.

Así se obtiene una arquitectura híbrida: la criba se escala por rango y por estructura.

## 10. Comparación directa entre los principales tipos de cribas

### 10.1. Criba de Eratóstenes clásica

Ventajas:

- simple
- pedagógica
- muy fiable
- excelente para pequeños intervalos

Desventajas:

- memoria O(n)
- costosa para n grande
- no se adapta bien a memoria limitada ni a grandes rangos

### 10.2. Criba segmentada

Ventajas:

- memoria manejable
- muy buena para intervalos grandes
- muy buena para paralelización en memoria compartida y distribuida
- bien adaptada al hardware moderno

Desventajas:

- requiere gestión de bloques y primos pequeños
- no reduce tanto el trabajo local como una rueda modular

### 10.3. Criba desmemoriada / rueda modular

Ventajas:

- ahorra mucho trabajo
- reduce candidatos claramente
- buena para SIMD y hardware vectorizado
- útil cuando el rango es grande y la estructura modular importa

Desventajas:

- implementación más compleja
- menos natural para una infraestructura distribuida sin planificación
- requiere más análisis matemático y más diseño de la rueda

### 10.4. Criba de Atkin

Ventajas:

- puede ser muy eficiente
- mejor para ciertos rangos grandes
- se integra bien con hardware moderno

Desventajas:

- menos intuitiva
- implementación más delicada
- no siempre supera en rendimiento a una segmentada muy bien optimizada

## 11. Para qué sirven los primos

Los primos no son sólo una curiosidad de la teoría de números. Tienen usos reales de enorme importancia:

- factorization de enteros
- primality testing
- generación de números aleatorios
- seguridad criptográfica
- sistemas de firma
- autenticación digital
- integridad de datos
- protocolos de comunicación segura
- investigación matemática
- y también experimentación en alta computación para medir el rendimiento del hardware.

En otras palabras, los primos no son una “especie” abstracta del número; son el material de la aritmética moderna. Cuando se habla de seguridad de comunicaciones, casi siempre se está hablando de la capacidad de producir y verificar primos grandes y de usarlos con protocolos matemáticos adecuados.

## 12. Para qué sirven las cribas

Las cribas sirven para construir precisamente esa base material. Son la infraestructura pasiva que permite:

- encontrar primos de un rango dado,
- contar primos en intervalos grandes,
- preparar pruebas de primalidad,
- construir bloques de primos para investigación,
- producir listas de candidatos para factorizaciones,
- preparar claves o semilleros de números para protocolos criptográficos,
- y medir el rendimiento del hardware con una tarea realmente con mucho trabajo computacional.

La criba es una herramienta fundamental, no solo porque resuelve un problema matemático, sino porque hace posible organizar y explorar el universo discreto de los enteros a gran escala.

## 13. La “mejor criba” depende del hardware y del objetivo

Aquí aparece el punto más moderno: la mejor criba no es una cosa universal. Depende de tres factores:

1. el rango N,
2. el tipo de operación requerida,
3. y la arquitectura del sistema.

Si tu objetivo es contar primos hasta 10^8 con un script simple, la clásica es suficiente.
Si tu objetivo es trabajar hasta 10^12 o más, necesitas segmentar.
Si tu objetivo es trabajar con mucho rendimiento, vectorización y uso de caché, necesitas una rueda de residuos o una mezcla con patrones modulares.
Si tu objetivo es distribuir en un cluster, necesitas segmentar a nivel global.
Si tu objetivo es crear un sistema de generación masiva de primos, necesitas combinar todo lo anterior.

Esto es un punto crucial: la criba no se puede separar del hardware. La mejor criba es la que mejor se ajusta al conjunto de enteros a filtrar y a la lógica del procesador, la memoria y la red.

## 14. Estimaciones asintóticas y práctica

### 14.1. Criba clásica

Asintóticamente:

- tiempo: O(n log log n)
- memoria: O(n)

Esto es muy buena para rangos pequeños a medianos. Sin embargo, en n grande, la memoria se convierte en un problema. Por eso la evolución de la criba ha sido, en gran parte, una evolución de reducción de memoria y aumento de localización.

### 14.2. Criba segmentada

Asintóticamente:

- tiempo: O(n log log n)
- memoria: O(√n + B)

donde B es el tamaño del bloque. El beneficio práctico es enorme, porque se evita guardar todo el rango a la vez. Para el hardware moderno, esto significa mejor uso del caché, mejor equilibrio de memoria y mejor paralelización.

### 14.3. Criba modular / rueda

La ventaja asintótica no siempre es una mejora del orden formal, sino una mejora del coste constante. En la práctica la rueda elimina casi todo el trabajo innecesario. La complejidad puede expresarse como una fracción del coste clásico: en vez de manejar todos los enteros, se trabaja solo con clases válidas. Esto produce una mejor constante de ejecución, no necesariamente un cambio en la notación asintótica de orden superior.

La diferencia entre O(n log log n) y “la misma complejidad pero una constante mucho menor” es enorme en la práctica, especialmente cuando N es grande y la memoria es limitada.

### 14.4. Hardware y estimación realista

En un sistema moderno con varios núcleos, caché de nivel 3 y SIMD, una criba segmentada con bitset puede procesar rangos de 10^9 a 10^10 en segundos o minutos, dependiendo de la implementación. Para 10^12 y más, lo normal es que el trabajo ya requiera de bloque y de distribución entre nodos. En clústeres, incluso 10^15 puede ser posible si se combina segmentación, distribución y optimización local de residuos.

Esto demuestra un punto importante: la historia de las cribas no es solo teórica. Es también una historia de escalado. Se puede decir que la criba moderna ha sido una respuesta tecnológica a la necesidad de computar más, más rápido, con menos memoria y mejor aprovechamiento del hardware.

## 15. Cronología histórica de las cribas

### 15.1. Antigüedad

- Eratóstenes (aprox. 276–194 a. C.): criba clásica, tamizado de números.
- Euclides (siglos IV–III a. C.): infinitud de primos, elemento conceptual clave.

### 15.2. Siglos XVIII y XIX

- Euler: análisis de los primos y la distribución de la densidad.
- Legendre: criba como herramienta para contar primos.
- Meissel: extensión de los métodos combinatorios y de conteo.

### 15.3. Siglo XX

- Lehmer: mejoramiento del conteo de primos y la aritmética combinatoria.
- Lagarias, Miller, Odlyzko: introducción de métodos más avanzados para estructuras de primos grandes.
- Atkin y Bernstein: mejora en la criba para rangos grandes y generación masiva.

### 15.4. Final del siglo XX y actualidad

- GIMPS: búsqueda de primos de Mersenne con cálculo distribuido.
- Cribas segmentadas y bitset modernas: base de la computación actual.
- Vectorización, SIMD, GPU, clusters: la criba se vuelve infraestructura de alta performance.

### 15.5. Motivo económico y motivación intelectual

No toda la historia de las cribas se explica por el dinero. Gran parte de ella nace del interés por la estructura del número. Sin embargo, cuando la criptografía se vuelve central para la seguridad digital, la criba tiene un valor económico real. En la era moderna, la capacidad de generar, verificar y contar primos se vuelve crítica para la infraestructura global. Así, la criba pasa a ser una técnica matemática, una herramienta de investigación y también un activo económico y técnico de enorme valor.

## 16. Qué tienen en común todas las cribas

Aun con sus diferencias, todas las cribas tienen el mismo objetivo general:

- explorar un rango,
- eliminar lo que no sirve,
- conservar lo que cumple una propiedad,
- y hacer eso con el menor coste posible.

La verdadera diferencia no está solo en la fórmula, sino en la estrategia:

- la criba clásica elimina todos los múltiplos,
- la segmentada evita cargar todo en memoria,
- la modular elimina clases innecesarias,
- la rueda trabaja en familias, no en todo el conjunto,
- la vectorizada explota la arquitectura del hardware,
- la distribuida reparte el problema entre muchos nodos.

Eso hace de la criba un concepto vivo, adaptable y dinámico. No es una técnica cerrada; es una familia de soluciones que cambian según el problema.

## 17. Conclusión histórica

La historia de la criba es la historia de cómo la humanidad aprendió a separar lo esencial de lo superfluo en el conjunto de los enteros. Desde Eratóstenes hasta los sistemas modernos de alto rendimiento, la criba ha sido una herramienta de orden, clasificación y avance. Ha servido a la matemática pura, a la teoría de números, a la computación, a la seguridad y a la infraestructura digital.

La criba segmentada responde al problema de la memoria y del rango; la desmemoriada responde al problema del trabajo inútil; la rueda modular responde a la necesidad de reducir la superficie de búsqueda; y la computación distribuida responde a la necesidad de escalar a niveles gigantes. Y todos ellos son variaciones del mismo principio: eliminar lo que no es primo, y hacer esto mejor que la competencia.

La mejor criba del mundo no es aquella que tiene la teórica formal más bonita ni la más elegante; es aquella que explota mejor el hardware, la memoria y el patrón de la distribución de primos, para resolver el problema práctico de forma más rápida, más barata y con menos desperdicio.

La criba es, en ese sentido, una perfecta síntesis entre matemática y ingeniería: una herramienta antigua, aún viva, y cada vez más poderosa a medida que crece la posibilidad computacional del mundo.

## 18. En una frase

Si los primos son la materia prima del número, las cribas son la fábrica que los separa, los ordena y los convierte en infraestructura real de la ciencia y de la seguridad.

## 19. Bibliografía histórica y técnica sugerida

- Eratóstenes de Cirene, métodos elementales de tamizado de primos.
- Euclides, Elementos, sobre infinitud de primos.
- Euler, análisis de la distribución de primos y la función zeta.
- Legendre, estimaciones y conteo de primos.
- Meissel y Lehmer, desarrollo de métodos de conteo y tamizado.
- Atkin y Bernstein, cribas avanzadas para primos masivos.
- GIMPS y proyectos de búsqueda de primos gigantes.
- Obras modernas de teoría de números y aritmética computacional.

Este trabajo no pretende sustituir una referencia técnica de última generación, sino ofrecer una lectura histórica, comparativa y contextual de la evolución de una de las ideas fundamentales de la matemática.
