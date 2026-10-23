# Criba modular iterativa, convergencia rápida y criterios de parada

## Resumen

Este trabajo desarrolla una formulación técnica y matemática de la criba modular iterativa como método para contar primos y estimar la densidad prima en intervalos finitos. La idea central es simple y muy antigua: en lugar de testar cada entero individualmente, se trabaja con una estructura modular que elimina de golpe todas las clases de residuos que no pueden ser primos. La diferencia respecto de la criba clásica de Eratóstenes es principally que la criba modular se plantea como una iteración de reducción del conjunto de candidatos, adaptada a la estructura del módulo y al rango de trabajo.

La criba modular iterativa se basa en la observación de que, para una lista de primos pequeños, las clases de residuos coprimos con su producto quedan preservadas, mientras que todas las otras clases se eliminan. Si se toma:

- P_k = ∏_{p ≤ p_k} p,
- A_k = {a mod P_k : gcd(a, P_k) = 1},

entonces la densidad exacta de candidatos en la red modular es:

- |A_k| / P_k = φ(P_k) / P_k = ∏_{p ≤ p_k} (1 - 1/p).

Esta cantidad no es una aproximación ad hoc: es la densidad exacta de la familia de residuos coprimos con el producto de los primos pequeños. Es precisamente el punto de partida de la criba modular. A partir de ahí, la densidad real de primos en el rango completo se puede recuperar con un criterio de parada explícito: cuando se han tamizado todos los primos p ≤ √N, los sobrevivientes del conjunto de candidatos son exactamente los primos mayores que √N y, eventualmente, el número 1.

También se estudia la convergencia rápida. La densidad de candidatos se reduce por factores del tipo 1 - 1/p, y el producto sobre los primos pequeños converge a una ley del tipo 1 / log x, con el factor clásico e^{-γ}. Este comportamiento explica por qué la reducción modular es muy efectiva: cada 새 etapa no cambia la estructura de la criba de forma arbitraria; más bien, elimina una fracción constante del conjunto de candidatos que, multiplicada iterativamente, produce una convergencia rápida hacia la densidad real del intervalo.

El trabajo incluye además un análisis de los criterios de parada y de cómo se puede usar un valor inicial como 4/9, 2/3, 4/15 o cualquier otra fracción como estimación de base. La clave es que esas fracciones sólo son exactas si provienen de una estructura modular concreta. Por ejemplo:

- si se parte de la familia de enteros no divisibles entre 2 y 3, la densidad del candidato modular es 1/3;
- si se parte de la estructura 6k ± 1, la fracción inicial es 1/3 del conjunto total;
- si se filtra además por 5, el factor exacto es 4/15;
- y, en general, una familia modular de base M produce una densidad exacta φ(M) / M.

La idea de “4/9” o “2/3” puede ser útil como estimación local o heurística, pero no es una ley universal. La densidad exacta sólo surge cuando se define explícitamente el conjunto modular inicial, el rango, y la lista de primos eliminados. Sobre esa base, la criba modular iterativa permite un tratamiento riguroso del conteo, la estimación y el criterio de parada.

## 1. Objetivo y marco de trabajo

El problema general es el siguiente: dado N, queremos contar primos en [2, N] o, al menos, estimar la densidad de primos en ese intervalo. La criba modular iterativa propone una estrategia basada en la reducción del espacio de candidatos usando congruencias.

La referencia universal es la criba de Eratóstenes. La variante modular iterativa se define como una filtración progresiva del conjunto de residuos módulo P_k, donde P_k es el producto de los primos pequeños que se quiere usar para eliminar candidatos.

Se define:

- P_k = ∏_{p ≤ p_k} p,
- A_k = {a mod P_k : gcd(a, P_k) = 1}.

Entonces el número de clases supervivientes es:

- |A_k| = φ(P_k).

La densidad en una longitud periódica de tamaño P_k es exactamente:

- d_k = φ(P_k) / P_k = ∏_{p ≤ p_k} (1 - 1/p).

Esto es una densidad exacta para la estructura modular, no una aproximación heurística. La iteración consiste en aumentar k, y por tanto aumentar P_k, hasta que se alcanza una cantidad de filtrado suficiente para operar con un rango finito y obtener un conteo preciso o una estimación fiable.

## 2. La criba modular iterativa

### 2.1. Definición formal

Sea I = [1, N]. Fijamos una lista de primos pequeños p_1, ..., p_r. La criba modular iterativa toma la familia de enteros en I y elimina todos los números congruentes a 0 modulo p_i para cada i = 1,...,r. El conjunto resultante es:

- C_r(N) = {n ≤ N : gcd(n, P_r) = 1},

con:

- P_r = ∏_{i=1}^r p_i.

Si r es tal que p_r ≥ √N, entonces todo número compuesto ≤ N tiene algún factor primo p ≤ √N, y por tanto el conjunto C_r(N) contiene solo primos y, eventualmente, el valor 1. Más precisamente:

- si p_r ≥ √N, entonces para n ≤ N, n > 1, se tiene:
  - n ∈ C_r(N) si y solo si n es primo.

Esto es el punto de exactitud fuerte de la criba modular iterativa. La criba no solo aproxima; cuando la lista de primos filtrados alcanza la raíz del rango, produce el conjunto exacto de primos.

### 2.2. Estructura del módulo

La clave es que la eliminación se hace por clases de residuos modulo P_r. En lugar de mirar cada n individualmente, se trabaja con el conjunto de residuos permitidos:

- R_r = {a mod P_r : gcd(a, P_r) = 1}.

Así, el problema se vuelve totalmente modular. Para un intervalo de longitud L = N, el número de candidatos sobrevivientes es:

- S_r(N) = #{m ∈ [1, N] : gcd(m, P_r) = 1}.

Si N = q P_r + t, con 0 ≤ t < P_r, entonces:

- S_r(N) = q · φ(P_r) + #{a ∈ [1, t] : gcd(a, P_r) = 1}.

Esto es una fórmula extremadamente útil: la criba modular iterativa permite obtener un número exacto de candidatos supervivientes en un rango finito si se conoce la estructura del módulo y el residuo final.

### 2.3. El caso exacto del conteo de primos

Si se toma r tal que p_r ≥ √N, entonces la fórmula anterior ya da un conteo exacto de primos si se excluye el 1.

La fórmula es:

- π(N) = S_r(N) - 1,

siendo r tal que P_r tiene todos los primos pequeños que pueden dividir a un número ≤ N, y r se ha elegido de modo que p_r ≥ √N.

Esto convierte la criba modular iterativa en una herramienta exacta. La exactitud no es una propiedad “intuitiva”; es una propiedad estructural del módulo cuando se filtran todos los divisores pequeños.

## 3. Convergencia rápida y densidad de candidatos

### 3.1. Factor de densidad por primo

La densidad de candidatas tras filtrar el primo p es:

- 1 - 1/p.

Por tanto, si se filtran todos los primos pequeños hasta p_k, la reducción final es:

- d_k = ∏_{p ≤ p_k} (1 - 1/p).

Esta cantidad es no sólo útil; es exacta en el modelo modular, y puede interpretarse como la probabilidad de que un entero aleatorio no sea divisible por ningún primo pequeño. En otras palabras, si se trabaja con la distribución uniforme sobre el conjunto de enteros, la fracción de candidatos supervivientes es exactamente esta cantidad.

La teoría clásica indica que:

- ∏_{p ≤ x} (1 - 1/p) ~ e^{-γ} / log x.

Esto es el punto que conecta la criba modular con la distribución global de primos. La convergencia es rápida en el sentido de que el producto de factores (1 - 1/p) decrece de forma muy regular, y cada paso nuevo elimina una fracción casi proporcional a 1/p.

### 3.2. Entender la convergencia rápida

Cuando se trata de primos pequeños:

- el primer factor es 1/2, que elimina la mitad de los enteros;
- el siguiente factor es 2/3, que elimina un tercio del resto;
- luego llega 4/5, luego 6/7, etc.

La composición de estos factores produce:

- d_1 = 1/2,
- d_2 = 1/3,
- d_3 = 4/15 ≈ 0.2667,
- d_4 = 8/35 ≈ 0.2286,
- etc.

Estos valores describen exactamente la fracción de enteros que sobreviven a la eliminación de los primos pequeños. Es una evidencia clara de que la reducción modular es rápida y no lineal: cada primo pequeño elimina una parte importante del espacio de candidatos, y la iteración hace converger el conjunto a la densidad de primos reales.

### 3.3. Relación con la densidad de primos real

La densidad de primos alrededor de x es aproximadamente:

- 1 / log x.

La cantidad d_k se comporta de forma muy parecida, pero con un prefactor clásico de la teoría analítica. La conexión es:

- d_k ≈ e^{-γ} / log p_k,

por lo que la estructura modular se vuelve una versión finita y exacta de la ley de distribución de primos. La función zeta y la ley de los números primos explican por qué esta densidad es la correcta en el límite; la criba modular iterativa ofrece una forma computable de desplegar esa ley a escala finita.

## 4. Exactitud y densidad exacta desde un valor inicial

Este punto es importante porque la fracción inicial puede depender de cómo se haya elegido el conjunto de antecedentes. No existe una única fracción inicial universal; existe una fracción exacta asociada al conjunto modular elegido.

### 4.1. Ejemplo 1: partir de todos los enteros

Si se parte de todo el conjunto de enteros, la fracción inicial es 1. Entonces al eliminar 2 y 3 se obtiene:

- q_2 = 1 · (1 - 1/2) · (1 - 1/3) = 1/3.

Esto es exacto en el modelo de residuos mod 6.

### 4.2. Ejemplo 2: partir de la clase 6k ± 1

Si se parte de la familia de enteros que ya están restringidos a la clase 6k ± 1, entonces la fracción inicial es:

- q_0 = 2/6 = 1/3.

En ese caso, al eliminar 5, se tiene:

- q_1 = q_0 · (1 - 1/5) = (1/3) · 4/5 = 4/15.

Es decir, la cota exacta de residuos posibles modulo 30 para esta estructura es 4/15.

### 4.3. Ejemplo 3: fracción 4/9

La fracción 4/9 no es una ley general. Es sólo una fracción posible si se está trabajando en una familia particular de candidatos ya reducida, por ejemplo, una estructura que elimina ciertos residuos con una regla claramente definida. En una criba modular real, la fracción debe derivarse del conjunto inicial A_0 y de los factores (1 - 1/p) asociados a los primos filtrados.

En otras palabras:

- 4/9 puede ser una fracción local o heurística,
- pero una densidad exacta sólo existe si se define explícitamente el conjunto modular inicial y la lista de primos que se eliminan.

La forma general es:

- q_k = q_0 · ∏_{p ≤ p_k} (1 - 1/p),

cuando el conjunto inicial se interpreta con una distribución uniforme en una estructura modular. Aquí q_0 es la fracción inicial del conjunto de candidatos. Esta fórmula es exacta para la familia modular si la estructura inicial es uniforme en el período.

### 4.4. Reducción exacta y rango finito

En el caso de un rango finito [1, N], la densidad exacta del conjunto de residuos que sobreviven al módulo P_k se puede escribir como:

- q_k(N) = #{ n ≤ N : gcd(n, P_k) = 1 } / N.

Esto es una cantidad exacta. Si se toma N = q P_k + r, entonces:

- q_k(N) = q · φ(P_k) / N + #{a ≤ r : gcd(a, P_k) = 1} / N.

Este cálculo descompone el problema en una parte periódica y un residuo final. Es una forma muy útil para controlar la convergencia y la exactitud de la criba modular iterativa.

## 5. Criterios de parada

La criba modular iterativa exige un criterio claro de detención. Hay dos tipos de criterio:

1. criterio exacto;
2. criterio de convergencia práctica.

### 5.1. Criterio exacto

Se puede detener la iteración cuando la lista de primos filtrados alcanza la raíz del rango:

- p_k ≥ √N.

Entonces, todo número compuesto ≤ N tiene un factor primo menor o igual que √N. Al eliminar de la estructura modular todos estos divisores, solo sobreviven los primos mayores que √N y eventualmente el número 1. Por tanto:

- si p_k ≥ √N, el conjunto residual es exactamente el conjunto de primos en [2, N], salvo 1.

Esto es el criterio exacto absoluto.

### 5.2. Criterio práctico de parada

En aplicaciones de alta escala, puede no resultar conveniente llegar exactamente a √N. En ese caso, se puede definir un criterio de convergencia basado en la estabilidad del conjunto residual.

Por ejemplo:

- si la densidad residual q_k cambia muy poco entre dos pasos,
- o si el número de candidatos aún no descartados se estabiliza dentro de un margen τ,
- entonces la iteración puede detenerse.

La regla puede ser del tipo:

- |q_{k+1} - q_k| < ε,
- o |S_{k+1}(N) - S_k(N)| / N < ε.

También puede combinarse con un umbral de corte por tamaño de primo:

- p_k > c √N,
-
con c cercano a 1 o ligeramente mayor. Esta regla no es exacta, pero es muy útil para una implementación eficiente con un error de control.

### 5.3. Criterio de parada basado en densidad observada

La densidad residual q_k puede compararse con la estimación analítica:

- 1 / log N.

Si el valor observado está ya muy cerca de la ley de distribución de primos global, entonces el algoritmo puede considerarse convergido.

Esto es especialmente útil cuando se trabaja en una ventana grande y no interesa que el algoritmo llegue exactamente a √N, sino que alcance la precisión requerida con la menor cantidad de pasos posibles.

## 6. Relación con la convergencia asintótica de la densidad

La densidad de candidatos luego de filtrar los primos pequeños satisface:

- d_k = ∏_{p ≤ p_k} (1 - 1/p).

La fórmula clásica de la teoría analítica da:

- d_k ≈ e^{-γ} / log p_k.

Esto muestra que la criba modular iterativa ya contiene, en su estructura, la ley de densidad global de los primos. En otras palabras:

- la reducción del conjunto de candidatos por una estructura modular encarna, de forma finita, la misma evolución que la función zeta describe asintóticamente.

Esto es una de las conexiones más profundas entre la teoría analítica y la práctica de la criba. La criba no solo “hace un cálculo”; también refleja la lógica de la densidad.

## 7. La estructura de las clases modulares y la densidad exacta

La densidad exacta de una estructura modular de base M se expresa como:

- d(M) = φ(M) / M,

y en general, si M = ∏_{p ≤ p_k} p, entonces:

- d(M) = ∏_{p ≤ p_k}(1 - 1/p).

Esto permite una formulación muy clara del problema de conteo en intervalos largos:

- se trabaja con el módulo M asociado a los primos pequeños;
- se cuenta cuántos números del intervalo son coprimos con M;
- y se usa la periodicidad para obtener una cuenta exacta en cada bloque.

Este punto es crucial porque la densidad exacta no es una hipótesis; es una cantidad aritmética completamente definida que depende del módulo y del intervalo.

## 8. Método práctico para estimar la densidad exacta desde un valor inicial

La forma general de estimar la densidad exacta en un rango [1, N] es la siguiente:

1. elegir una base modular M,
2. definir el conjunto inicial A_0 de residuos válidos,
3. filtrar los primos pequeños p ≤ p_k,
4. actualizar la fracción por:
   - q_{k+1} = q_k · (1 - 1/p_{k+1}),
5. seguir hasta que p_k ≥ √N o hasta que se cumpla un criterio de convergencia,
6. y contar exactamente el número residual con la periodicidad del módulo.

Si M es el producto de los primos pequeños que se han filtrado, entonces la densidad exacta del conjunto que sobrevive es:

- q(M) = φ(M)/M.

Y el número exacto de candidatos vivos en [1, N] es:

- C(N; M) = q·φ(M) + r_0,

con la interpretación clásica de q y de r_0 según la parte entera y el resto de N dividido por M.

Esto da un método exacto y modular para aproximar o contar primos sin recorrer literalmente el conjunto completo.

## 9. Densidad local y estructuras de ventana

La densidad exacta del módulo es muy útil para el rango completo. Pero en muchos problemas de análisis numérico también interesa la densidad local en una ventana [x, x+H]. En ese caso, el enfoque modular se hace aún más útil:

- se trabaja con una ventana local de tamaño H,
- se aplica la misma estructura modular dentro de la ventana,
- se compara la densidad local con la densidad global del módulo.

La comparación entre densidad local y densidad global puede indicarse como:

- D_local ≈ D_global + corrección local,

y la corrección local suele depender del tamaño H y de la posición x. Esto es precisamente el punto en el que la aproximación local puede ser mejor que una ley global, porque la distribución de primos en una ventana pequeña no siempre sigue exactamente la misma curva que la distribución global.

## 10. Conclusión

La criba modular iterativa es una forma muy potente de entender y contar primos. Se apoya en una idea simple pero profunda: la estructura modular reduce el espacio de candidatos de forma exacta y rápida. La reducción por cada primo pequeño se hace con un factor exacto 1 - 1/p, y la multiplicación acumulada de esos factores produce una densidad de candidatos que converge de manera natural hacia la ley de densidad de primos.

Los puntos clave son:

- la densidad exacta de candidatos es φ(M) / M,
- la convergencia se acelera por los factores 1 - 1/p,
- el criterio de parada exacto es p_k ≥ √N,
- y la fracción inicial puede ser cualquier q_0 válido para el conjunto modular elegido, siempre que se defina explícitamente el conjunto inicial.

La fracción 4/9 o cualquier otra fracción puede ser una buena estimación local o una heurística de base, pero solo adquiere un sentido matemático preciso cuando se define a partir de una estructura modular concreta. La densidad exacta no es un número mágico; es una propiedad del sistema de residuos elegido.

En ese sentido, la criba modular iterativa es un puente perfecto entre la historia antigua de Eratóstenes, la teoría analítica moderna de la distribución de primos, y la práctica de cálculo exacto con rangos grandes. Es, por tanto, una de las formas más naturales de entender tanto la densidad prima como la eficiencia computacional del conteo de primos.

## 11. Versión compacta de la idea central

La clave puede resumirse de esta manera:

- elegir un módulo M,
- eliminar los residuos no coprimos con M,
- repetir por los primos pequeños,
- y parar cuando el módulo alcanza la raíz del rango.

En ese punto:

- el conjunto residual es exactamente el conjunto de primos del intervalo,
- y la densidad residual exacta es el producto de los factores 1 - 1/p.

## 12. Forma de uso computacional

Un algoritmo práctico podría seguir la siguiente estructura:

1. fijar un rango [1, N],
2. fijar un módulo inicial M o una lista de primos pequeños,
3. calcular la densidad exacta del conjunto residual via φ(M) / M,
4. filtrar por la lista de primos pequeños,
5. actualizar la densidad residual con q ← q · (1 - 1/p),
6. repetir mientras p ≤ √N,
7. si se alcanza √N, detenerse y contar exactamente el conjunto residual.

Este esquema es claro, modular, exacto y adaptable al hardware. Es precisamente lo que hace de la criba modular iterativa una herramienta valiosa para la teoría y para la práctica.
