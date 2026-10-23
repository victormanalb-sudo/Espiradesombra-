# Densidad de primos y conteo histórico: de Legendre a MRAUV

## Resumen

La historia del conteo de primos es una de las líneas más profundas de la teoría de números. Desde la infinitud de primos demostrada por Euclides hasta la distribución analítica de la función π(x), el problema de entender cómo se distribuyen los primos ha acompañado a la matemática durante siglos. La necesidad no era solo conceptual: también era práctica. Contar primos y estimar su densidad se convirtió en un problema central para la aritmética computacional, la factorización, la seguridad y la infraestructura digital moderna.

Este trabajo ofrece una lectura histórica y comparativa del desarrollo del conteo de primos, desde Legendre hasta los métodos modernos de criba y de modelado local, incluyendo el enfoque MRAUV. La comparación se hace con atención a la diferencia entre dos tipos de enfoque: por un lado, los métodos históricos y computacionales de conteo exacto de primos; por otro, los modelos locales de densidad que buscan describir la evolución de la frecuencia de primos en ventanas finitas. La conclusión principal es que Legendre y sus variantes históricas están en la línea de la aritmética combinatoria y de la criba; MRAUV, por su parte, es más bien un modelo fenomenológico de densidad local, útil para heurística y segmentación, pero no un sustituto del cuerpo clásico de la teoría de los números primos.

El estudio aquí presentado reconstruye la evolución del problema desde la teoría analítica hasta la práctica computacional, con especial atención a la dimensión histórica y a la distinción entre exactitud global, aproximación local y rendimiento real del algoritmo. Lo que se busca es mostrar que el conteo de primos no es un único problema, sino una familia de enfoques con distintos objetivos: contar exactamente, estimar con precisión, modelar localmente, o trabajar en la práctica con el hardware disponible.

## 1. Introducción: la densidad y el conteo de primos como problema histórico

La cuestión de cómo se distribuyen los primos es una de las más antiguas y más profundas de la matemática. Al menos desde Euclides, se sabe que hay infinitos primos, pero esa infinitud no dice nada sobre su ritmo de aparición. La pregunta central no es sólo si los primos son infinitos, sino cómo se reparten en la recta numérica.

La historia del problema se divide en dos grandes líneas:

- una línea analítica, que busca comprender π(x) y su comportamiento asintótico;
- una línea combinatoria y computacional, que busca contar primos de forma exacta o cercana mediante técnicas de exclusión, eliminación y tamizado.

La primera línea culmina en la formulación clásica de la distribución de primos:

- π(x) ~ x / log x,
- y más precisiones usando la integral logarítmica y la función zeta.

La segunda línea lleva a los métodos de Legendre, Meissel, Lehmer, y a la familia de cribas y técnicas de cálculo de rangos grandes. El punto de contacto entre ambos enfoques es que ambos buscan responder a la misma pregunta: ¿cómo se comporta la densidad de primos?

La diferencia es que:

- la teoría analítica ofrece una ley de densidad global;
- los métodos combinatorios ofrecen procedimientos de conteo exacto o casi exacto;
- y los modelos locales como MRAUV buscan una representación de la variación local en ventanas finitas.

## 2. Euclides y la infinitud: el primer gran dato histórico

Euclides demostró que el conjunto de primos es infinito. Este resultado no resuelve el problema de la densidad, pero sí fija un punto de partida esencial: los primos no son un conjunto finito ni marginal. Son una estructura profunda del sistema numérico.

La infinitud de los primos es la base de toda la teoría posterior. Sin ella, no existiría la idea de una distribución no trivial del conjunto primo. No basta con decir que hay primos; hay que decir cómo aparecen y con qué densidad.

La influencia de Euclides es enorme porque su demostración muestra que el conjunto primo es estable bajo un tipo de estructura multiplicativa muy fuerte. La teoría de números no puede ignorar esta base. La criba, el conteo y la distribución de primos nacen de ese hecho fundamental.

## 3. Euler y la función zeta: la densidad como problema analítico

Leonhard Euler dio un paso decisivo al conectar los primos con la función zeta:

- ζ(s) = Σ 1/n^s
- y su factorización en producto sobre primos,
- lo que permitió relacionar la estructura de los primos con el comportamiento analítico de una función compleja.

Ese punto es crucial porque muestra que la teoría de números ya no es solo una colección de observaciones aisladas. Tiene una estructura de conjunto, de producto y de distribución analítica. La densidad de los primos se vuelve parte de la geometría del análisis complejo.

La conexión entre la función zeta y los primos conduce a la ley de distribución asintótica:

- π(x) ~ x / log x

y a la integral logarítmica:

- Li(x) = ∫_2^x dt / log t

El teorema de los números primos confirmó que el número de primos menores que x crece como x / log x, y que la densidad global decrece como 1 / log x. Esta relación no solo es bella; es la base del análisis moderno de la distribución de primos.

## 4. Legendre y la idea del conteo por exclusión

La contribución de Adrien-Marie Legendre es históricamente central, porque marca la transición desde la teoría analítica hacia una estrategia más combinatoria y computable del conteo de primos.

Legendre no planteó solo una fórmula de aproximación; planteó una forma de contar primos mediante la exclusión de múltiplos. La idea básica del método de Legendre se resume en que: si quieres contar primos hasta x, no necesitas probar cada n entero individualmente; puedes intentar excluir los compuestos usando los primos pequeños.

La intuición es muy simple y muy poderosa:

- todo compuesto tiene un divisor menor o igual que √n;
- por tanto, un número n puede ser primo solo si no es divisible por ningún primo pequeño ≤ √n.

Esto ya es una forma de criba. No es la criba de Eratóstenes en la implementación moderna, pero sí es la misma lógica esencial: reducir el conjunto de candidatos mediante la eliminación de múltiplos.

Desde la perspectiva histórica, esto fue crucial porque:

- formalizó un enfoque de exclusión;
- ofreció una base computable para el conteo;
- y abrió la puerta a la evolución que llegaría con Meissel, Lehmer y la aritmética computacional moderna.

## 5. Meissel y Lehmer: del conteo clásico a la computación real

La siguiente gran etapa es la de Meissel y Lehmer. Aquí ya no hablamos solo de conceptos; hablamos de cálculo práctico.

### 5.1. Meissel

Meissel desarrolló una línea de trabajo orientada a contar primos a través de metodologías combinatorias más eficientes. Su enfoque era más útil para rangos grandes que la mera prueba directa de primalidad. La clave es que el conteo de primos ya no se pensaba como una operación aislada, sino como una operación sobre un conjunto grande y estructurado.

La idea general era reducir el problema de contar primos a un problema de contar enteros sin divisores pequeños. Esto es exactamente la misma lógica de la criba, pero formulada con mayor fuerza combinatoria.

### 5.2. Lehmer

Lehmer mejoró dichos métodos y los hizo mucho más útiles en la práctica. Lo importante no es que fuera una vez “más rápido” de forma abstracta, sino que convirtió estas ideas en un procedimiento computable para valores grandes. El valor de su trabajo es doble:

- por un lado, pone la aritmética combinatoria a disposición del cálculo;
- por otro, muestra que los métodos de conteo pueden ser extremadamente potentes si están diseñados para el hardware real, no solo para la teoría pura.

De esta manera, el esquema histórico queda claro: Legendre ofreció la idea, Meissel la materializó en un método preciso, y Lehmer la hizo viable para el cálculo serio.

## 6. La criba como mecanismo de conteo exacto

La criba de Eratóstenes es la gran referencia histórica del tipo de técnicas que se usan para contar primos. La idea es simple:

- generar todos los números del intervalo;
- eliminar múltiplos de 2, 3, 5, ... ;
- lo que queda son los primos.

Es, por tanto, un algoritmo exacto. La gran pregunta ya no es “si funciona”, sino “si funciona de forma eficiente”. La respuesta depende de:

- el rango N,
- la memoria disponible,
- la velocidad del hardware,
- y la estructura del algoritmo a implementar.

La criba clásica tiene una complejidad asintótica muy buena:

- tiempo: O(n log log n)
- memoria: O(n)

Esto la vuelve muy útil para rangos pequeños y medianos, pero cuando N crece, la memoria se convierte en el problema central. Se hace entonces necesario pasar a técnicas más sofisticadas: cribas segmentadas, ruedas modulares, bitsets, y estructuras de residuos.

## 7. Criba segmentada y rueda modular: la práctica moderna

### 7.1. Criba segmentada

La criba segmentada divide el rango grande en bloques que pueden ser procesados de forma separada. Esta estrategia reduce enormemente la memoria necesaria y hace mucho más fácil adaptar el cálculo a los niveles de caché y a la arquitectura moderna del procesador.

Ventajas:

- mejor uso de la memoria;
- más fácil de paralelizar;
- muy adecuada para intervalos grandes;
- excelente para hardware moderno, CPU multinúcleo y clusters.

### 7.2. Ruleta o rueda modular

La rueda modular trabaja con una idea distinta: no se intenta revisar cada número del conjunto; se trabaja solo con clases de residuos que pueden ser primos. El ejemplo clásico es la estructura modulo 6:

- todo primo mayor que 3 es de la forma 6k ± 1.

Aquello reduce la cantidad de candidatos antes incluso de empezar la eliminación. La estrategia puede generalizarse a residuos 30k ± 1, 210k ± 1 y más. Esto da lugar a lo que se conoce como wheel sieve o “criba por rueda”.

Ventajas:

- reduce muchísimo el espacio de trabajo;
- elimina clases de residuos irrecuperables;
- mejora la constante temporal del algoritmo;
- se vuelve muy útil cuando el rango es grande y la estructura modular es dominante.

### 7.3. Comparación con la criba clásica

La criba clásica es simple, exacta y muy clara. La segmentada y la modular son más avanzadas, porque resuelven el problema práctico de la memoria y del coste de operación. Es decir, no reemplazan el origen, sino lo más profundo: convierten la criba en una herramienta de cálculo real.

## 8. MRAUV: qué es y qué no es

MRAUV aparece dentro de la lógica del repositorio como un modelo de densidad local. La idea central no es contar primos exactamente, sino representarlos como una densidad que cambia con el tiempo o con la variable de rango. En términos prácticos, se puede formular como:

- D_pred ≈ D_0 + V_0 Δn + ½ a_0 (Δn)^2

Esto interpreta la densidad local de primos como un sistema dinámico. En la práctica, es una forma de aproximar la manera en que la densidad local cambia en una ventana finita. Es útil para:

- predecir comportamiento local,
- modelar la evolución de la densidad,
- orientar la búsqueda de primos o el conteo en segmentos,
- y estudiar patrones locales de distribución.

Sin embargo, hay que distinguir dos niveles de uso:

- como modelo heurístico local → útil,
- como sustituto de la teoría analítica o de la criba exacta → no es equivalente.

MRAUV no reemplaza a Legendre ni a la función zeta. No tiene el mismo estatus histórico ni la misma posición en la teoría de números. Lo que ofrece es una ventana de observación local y una forma de entender la densidad prima como un fenómeno dinámico dentro de un rango acotado.

## 9. Comparación entre Legendre, Meissel, Lehmer, criba y MRAUV

### 9.1. Legendre

- objetivo: contar primos o estimar la densidad usando exclusión y conteo por divisibilidad;
- valor histórico: enorme;
- alcance: metodológico y computacional temprano;
- fuerza: fórmula clara, base del conteo moderno;
- debilidad: en la práctica, requiere optimización fuerte para rangos grandes.

### 9.2. Meissel y Lehmer

- objetivo: llevar el conteo de primos a la práctica computacional;
- valor histórico: muy alto;
- alcance: reducción efectiva del trabajo combinatorio;
- fuerza: permiten contar primos exactos a escalas mayores;
- debilidad: dependen de construcciones más sofisticadas y de mejores recursos.

### 9.3. Criba segmentada y wheel sieve

- objetivo: hacer el conteo práctico y escalable;
- valor técnico: enorme;
- alcance: muy útil para grandes rangos y hardware moderno;
- fuerza: gran rendimiento real y adaptabilidad al hardware;
- debilidad: más complejas, requieren diseño de memoria y segmentación.

### 9.4. MRAUV

- objetivo: modelar la densidad local;
- valor: esencialmente heurístico y descriptivo;
- alcance: ventanas y porciones pequeñas del dominio;
- fuerza: útil para intuición local y para segmentación de rangos;
- debilidad: no reemplaza la teoría clásica ni el conteo exacto.

## 10. Exactitud, aproximación y eficiencia

Una comparación seria entre métodos de densidad y conteo debe distinguir tres cosas:

1. exactitud,
2. aproximación,
3. coste computacional.

### 10.1. Exactitud

La exactitud significa que el método devuelve exactamente el número correcto de primos en el rango.

- Legendre y sus variantes: pueden hacer conteo exacto con buen diseño.
- Meissel/Lehmer: también en el dominio del cálculo exacto.
- Cribas modernas: exactas si están bien implementadas.
- MRAUV: no es exacto en el sentido clásico; es predictivo.

### 10.2. Aproximación

La aproximación significa que el método estima la densidad o el número de primos sin necesidad de contar todos los valores.

- la función π(x) y Li(x) ofrecen aproximación analítica de gran valor;
- MRAUV también ofrece aproximación local, pero en un marco fenoménico.

### 10.3. Coste computacional

Eso cambia todo. En la práctica, una aproximación analítica puede ser elegantísima y muy útil, pero no sustituye a una criba exacta cuando lo que se necesita es un recuento fiable. Del mismo modo, MRAUV puede ser útil para estimaciones locales, pero no sustituye a la estructura exacta del conteo clásico.

La conclusión es clara:

- la exactitud global la aporta la criba y los métodos de conteo clásico;
- la aproximación global la aporta la teoría analítica;
- la densidad local la puede aportar MRAUV como modelo dinámico.

## 11. Qué mide la historia: no solo el número, sino la estructura

La historia del conteo de primos no es solo una historia de fórmulas. Es una historia de cómo la humanidad aprendió a “mirar” la estructura del número. La cuestión ya no es solo si un número es primo; es cómo se distribuye el conjunto de primos, cómo cambiará con el rango, y cómo se puede contar sin hacer trabajo inútil.

La verdadera diferencia entre los métodos puede resumirse así:

- métodos analíticos: miran la densidad global;
- métodos de criba: eliminan lo que no sirve;
- modelos locales: tratan la densidad como fenómeno dinámico.

Todos son válidos, pero no tienen la misma naturaleza ni la misma finalidad.

## 12. Conclusión

La comparación histórica de los métodos de densidad y conteo de primos muestra que no hay un único enfoque dominante. Hay varias estrategias, cada una con su función:

- Legendre ofrece la idea estructural del conteo por exclusión;
- Meissel y Lehmer llevan ese enfoque a la computación real;
- la criba moderna, segmentada y modular, hace viable el conteo exacto en rangos grandes;
- el modelo MRAUV representa una forma más local y fenomenológica de entender la densidad de primos;
- y la teoría analítica, basada en la función zeta y el teorema de los números primos, describe la distribución global con una precisión y una belleza que no pueden reemplazarse por modelos locales.

La conclusión más honesta es que Legendre y la tradición combinatoria del conteo de primos forman la base histórica real del problema; MRAUV, en cambio, es mejor entendido como un modelo de densidad local útil para intuición, aproximación y segmentación, pero no como una sustitución del cuerpo clásico de la teoría de números. En la práctica, la mejor estrategia para el cálculo real es combinar estas líneas: usar la teoría analítica para entender la ley global, la criba para contar exactamente, y los modelos locales para orientar el comportamiento en ventanas finitas.

## 13. En una frase

Legendre cuenta primos por exclusión; MRAUV describe cómo cambia la densidad local; y la criba moderna hace posible que los dos caminos se conviertan en cálculo real.

## 14. Nota de lectura

Este trabajo no pretende sustituir a un tratado clásico de la teoría de los números primos ni a una monografía de aritmética computacional; pretende ser una reconstrucción histórica y comparativa del problema del conteo y la densidad de primos, con atención a la diferencia entre exactitud global, aproximación local y uso práctico del hardware.
