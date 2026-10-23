# CRIVA: Criba Racional Iterativa de Validación Aritmética / CRIVA: Rational Iterative Sieve of Arithmetic Validation

## Resumen

Este trabajo define una familia de algoritmos de criba racional iterativa, con una formulación estructurada y teoremas de convergencia, densidad y parada. La intención no es sustituir la teoría clásica de los números primos, sino dar una base formal para una criba modular iterativa que pueda ser tratada como un sistema racional de reducción de candidatos.

La idea central es representar la reducción del conjunto de candidatos mediante una sucesión de pasos de eliminación:

- S_0 es el conjunto inicial de enteros en un rango finito,
- para cada primo p, se define la operación de supervivencia:
  R_p(S) = {n ∈ S : p ∤ n},
- y se itera la composición de estas operaciones sobre una secuencia creciente de primos.

Cuando S_0 = {1, 2, ..., N}, y se toma la secuencia de todos los primos hasta una cota apropiada, la criba racional iterativa reproduce el mismo conjunto de primos que la criba clásica, con una estructura exacta de densidad residual. La teoría aquí desarrollada muestra que la densidad de supervivencia es exactamente multiplicativa en los factores 1 - 1/p y que el criterio de parada se obtiene cuando la secuencia de primos alcanza la raíz del rango.

El trabajo presenta también una formulación general para semillas racionales. Si el conjunto inicial S_0 tiene densidad q_0 en un período modular M, entonces la densidad tras filtrar los primos p_1, ..., p_k es:

- q_k = q_0 · ∏_{i=1}^k (1 - 1/p_i),

siempre que el conjunto inicial esté uniformemente distribuido en las clases de residuos modulo M y que se elimine cada primo con la regla estándar de divisibilidad. Esto permite tratar un valor inicial como 4/9, 2/3, 4/15 o cualquier otra fracción racional como una semilla modular, no como una ley universal.

La conclusión principal es que una criba racional iterativa puede formalizarse sin ambigüedad: la densidad exacta del conjunto residual depende del conjunto inicial, del módulo base y de los primos eliminados. A partir de ahí, se obtiene un criterio de parada exacto y un teorema de convergencia tanto en densidad como en cardinalidad.

## Abstract

This paper defines a family of iterative rational sieve algorithms with a formal structure for convergence, density, and stopping criteria. The goal is not to replace the classical theory of prime numbers, but to provide a rigorous foundation for an iterative modular sieve that can be treated as a rational system of candidate reduction.

The core idea is to represent the reduction of the candidate set through a sequence of elimination steps:

- S_0 is the initial set of integers in a finite range,
- for each prime p, define the survival operator:
  R_p(S) = {n ∈ S : p ∤ n},
- and iterate the composition of these operators over an increasing prime sequence.

When S_0 = {1, 2, ..., N} and the sequence includes all primes up to a suitable bound, the iterative rational sieve reproduces the same prime set as the classical sieve, with an exact residual-density structure. The theory developed here shows that the survivor density is multiplicative in the factors 1 - 1/p and that the stopping rule is reached once the prime sequence reaches the square root of the range.

The paper also formulates the general rational-seed case. If the initial set S_0 has density q_0 in a modular period M, then the density after filtering primes p_1, ..., p_k is:

- q_k = q_0 · ∏_{i=1}^k (1 - 1/p_i),

provided the initial set is uniformly distributed over the residue classes modulo M and the standard divisibility rule is applied. This allows one to treat an initial fraction such as 4/9, 2/3, 4/15, or any other rational value as a modular seed rather than as a universal law.

The main conclusion is that an iterative rational sieve can be formalized without ambiguity: the exact density of the residual set depends on the initial set, the base modulus, and the filtered primes. From there, one obtains an exact stopping criterion and a convergence theorem for both density and cardinality.

---

# 1. Marco formal

## 1.1. Definición de la criba racional iterativa

Sea S_0 ⊆ ℕ un conjunto inicial finito o finitamente truncado. Para cada primo p, definimos la operación de supervivencia:

- R_p(S) = {n ∈ S : p ∤ n}.

Dada una sucesión creciente de primos P = (p_1, p_2, ..., p_k), definimos la criba iterativa como:

- S_1 = R_{p_1}(S_0),
- S_2 = R_{p_2}(S_1),
- ...
- S_k = R_{p_k}(S_{k-1}).

La versión más natural es cuando S_0 = {1, 2, ..., N}. Entonces S_k es el conjunto de enteros ≤ N que no son divisibles por ninguno de los primos p_1, ..., p_k.

## 1.2. Semilla racional y periodicidad modular

Una semilla racional es un conjunto inicial S_0 que se describe por una densidad q_0 en un periodo modular M. Si S_0 es un conjunto de residuos mod M con densidad:

- q_0 = |A| / M,

entonces la iteración por primos p_1, ..., p_k producirá una densidad residual que sigue la ley multiplicativa:

- q_k = q_0 · ∏_{i=1}^k (1 - 1/p_i).

Esto es la base racional de la criba.

---

# 2. Definiciones fundamentales

## 2.1. Conjunto residual

Para un conjunto inicial S_0 y una secuencia de primos P = (p_1, ..., p_k), definimos:

- S_P = R_{p_k} ∘ ... ∘ R_{p_1}(S_0).

## 2.2. Densidad residual

Si S_0 es un conjunto finito dentro de un rango [1, N], definimos:

- d_P(N) = |S_P| / N.

Cuando S_0 = {1, ..., N}, la densidad residual representa la fracción de enteros que sobreviven al tamizado.

## 2.3. Módulo base

Si la estructura inicial tiene periodo M, definimos:

- A ⊆ ℤ/Mℤ,
- q_0 = |A| / M,
- y la actualización por un primo p coprimo con M da:
  q_{p} = q_0 · (1 - 1/p),
  cuando la distribución es uniforme en las clases.

---

# 3. Teoremas de la CRIVA

## Teorema 1 (CRIVA-1): Invarianza de la estructura residual

Sea S_0 un conjunto de enteros en un intervalo [1, N]. Sea P = (p_1, ..., p_k) una secuencia creciente de primos. Entonces:

- S_P = {n ∈ S_0 : para todo i, p_i ∤ n}.

### Demostración

La operación R_p elimina exactamente los elementos divisibles por p. Al componer estas operaciones para cada p_i, se obtiene el conjunto de elementos que no son divisibles por ningún p_i. Esto es exactamente la definición de intersección de condiciones de divisibilidad, y la composición de las aplicaciones R_p es conmutativa:

- R_p ∘ R_q = R_q ∘ R_p.

Por tanto la estructura no depende del orden en que se aplique la criba, sino solo del conjunto de primos filtrados.

Esto prueba que la criba racional iterativa es una operación combinatoria bien definida sobre la familia de primos elegida.

---

## Teorema 2 (CRIVA-2): Densidad exacta en módulo

Sea M = ∏_{i=1}^k p_i, y sea A ⊆ ℤ/Mℤ el conjunto de residuos que sobreviven al filtrar los primos p_1, ..., p_k. Entonces:

- |A| = φ(M),
- y la densidad exacta de supervivencia es:
  |A| / M = φ(M)/M = ∏_{i=1}^k (1 - 1/p_i).

### Demostración

Un residuo a mod M sobrevive si y sólo si es coprimo con M. El número de elementos de ℤ/Mℤ que son coprimos con M es, por definición, φ(M). Por tanto:

- |A| = φ(M),
- y la densidad es φ(M) / M.

Además, por la propiedad multiplicativa de φ:

- φ(M) = M · ∏_{i=1}^k (1 - 1/p_i).

Así se obtiene la identidad exacta.

---

## Teorema 3 (CRIVA-3): Convergencia racional en un rango finito

Sea N ∈ ℕ y sea P_k = ∏_{i=1}^k p_i. Escribamos:

- N = m P_k + r,
  con 0 ≤ r < P_k.

Entonces el número de candidatos que sobreviven a la criba modular tras filtrar p_1, ..., p_k es exactamente:

- S_k(N) = m · φ(P_k) + #{a ∈ [1, r] : gcd(a, P_k) = 1}.

Consecuentemente, la densidad residual es:

- d_k(N) = S_k(N) / N.

### Demostración

La estructura se repite periódicamente con período P_k. En cada bloque completo de longitud P_k, exactamente φ(P_k) residuos sobreviven porque son los coprimos con P_k. La parte residual final se cuenta de forma exacta. Sumando ambos términos se obtiene la fórmula exacta.

Esto establece que la criba racional iterativa no es un algoritmo probabilístico: da un recuento exacto una vez fijado el módulo y el rango.

---

## Teorema 4 (CRIVA-4): Criterio exacto de parada

Sea N ∈ ℕ. Si la sucesión de primos filtrados satisface:

- p_k ≥ √N,

entonces para cada n ≤ N, con n > 1,

- n sobreviva a la criba si y solo si n es primo.

Equivalentemente, el conjunto residual final es:

- {1} ∪ {p primo : p ≤ N},

salvo que se haya excluido explícitamente el valor 1 en la definición del algoritmo.

### Demostración

Todo entero compuesto n ≤ N tiene un divisor primo p ≤ √N. Si todos los primos pequeños hasta √N han sido filtrados, entonces ningún compuesto puede sobrevivir. Los únicos elementos que quedan son 1 y los primos mayores que √N, junto con los primos ya menores que √N que no fueron filtrados debido a la definición de la semilla. Por la construcción, cuando la secuencia alcanza la raíz, el conjunto residual coincide con el conjunto exacto de primos del rango.

Esto da un criterio exacto de parada: no hace falta seguir iterando más allá de √N para obtener el conjunto primitivo exacto.

---

## Teorema 5 (CRIVA-5): Convergencia de la densidad racional

Sea q_0 la densidad inicial del conjunto modular base y sea P = (p_1, ..., p_k) una secuencia creciente de primos. Entonces:

- q_k = q_0 · ∏_{i=1}^k (1 - 1/p_i).

Si el conjunto inicial es el rango completo [1, N] y se toma q_0 = 1, entonces:

- q_k = ∏_{i=1}^k (1 - 1/p_i).

Además, para k suficientemente grande,

- q_k ≈ e^{-γ} / log p_k,

en la misma escala en que la teoría clásica explica la densidad de primos.

### Demostración

La fórmula multiplicativa es una aplicación directa de la definición del operador de supervivencia sobre una distribución uniforme. La equivalencia asintótica con e^{-γ} / log p_k se sigue del producto de Euler sobre primos:

- ∏_{p ≤ x} (1 - 1/p) ∼ e^{-γ} / log x,

que es un resultado clásico de la teoría analítica de los números primos.

La criba racional iterativa reproduce exactamente esa dinámica en su evolución finita.

---

# 4. Fracciones racionales y semillas iniciales

## 4.1. La fracción 4/9 y otras semillas

Una semilla racional q_0 no es una “constante universal”. Debe venir de una estructura concreta. Por ejemplo, si S_0 es un conjunto de residuos mod 9 que contiene exactamente 4 clases de 9 posibles, entonces:

- q_0 = 4/9.

La misma lógica vale para 2/3, 4/15, 8/35, etc. En cada caso, la fracción inicial se interpreta como la densidad exacta de una familia de residuos módulo M.

La conclusión clave es la siguiente:

- una fracción racional es una semilla modular solamente si representa una familia exacta de residuos;
- no existe una fracción inicial “mágica” que sirva para todos los rangos o todas las estructuras.

## 4.2. Teorema de extracción de densidad exacta

Si A ⊆ ℤ/Mℤ es un conjunto de residuos con densidad q_0 = |A|/M, entonces la densidad tras filtrar los primos p_1, ..., p_k es:

- q_k = q_0 · ∏_{i=1}^k (1 - 1/p_i),

si la distribución es uniforme en las clases modulo M y los primos filtrados no dividen a M o, equivalentemente, se trabaja con un módulo compatible con la filtración.

Este resultado permite extraer la densidad exacta de un conjunto modular inicial sin depender de una hipótesis extra.

---

# 5. Variante operacional del algoritmo

## 5.1. Algoritmo CRIVA

Entrada:

- N ∈ ℕ,
- semilla modular A_0 ⊆ ℤ/Mℤ,
- lista creciente de primos P = (p_1, ..., p_k).

Salida:

- conjunto residual S_k,
- densidad q_k,
- y criterio de parada exacto o aproximado.

Paso 1: Calcular q_0 = |A_0| / M.

Paso 2: Para cada primo p en la secuencia:

- q ← q · (1 - 1/p),
- eliminar las clases cuyo residuo es 0 mod p.

Paso 3: Si p ≥ √N, detenerse.

Paso 4: Devolver el conjunto residual y la densidad final.

## 5.2. Implementación con módulo de rango

Cuando se trabaja sobre [1, N], una implementación real suele dividir el intervalo en bloques de longitud M, y luego contar cuántos elementos sobreviven en cada bloque. La fórmula exacta de cada bloque es:

- bloque_j = {jM + 1, ..., jM + M},
- número de supervivientes = φ(M),
- y el resto final se trata por separado.

Esto convierte la criba racional iterativa en una estrategia modular y perfectamente compatible con la aritmética de intervalos.

---

# 6. Criterio de parada, estabilidad y error

## 6.1. Parada exacta

La parada exacta se da con:

- p_k ≥ √N.

En ese punto, la criba ya ha eliminado todos los posibles divisores de los números compuestos del rango.

## 6.2. Parada práctica

Cuando no se desea llegar exactamente a √N, se puede definir una regla de estabilidad:

- |q_{k+1} - q_k| < ε,

o también

- |S_{k+1} - S_k| / N < ε.

Esto da un criterio de convergencia útil para cálculos grandes, siempre con la advertencia de que no garantiza exactitud total si no se incorpora una cota de error explícita.

---

# 7. Conclusión

La criba racional iterativa ofrece una formulación sólida para la reducción de candidatos en aritmética modular. Su principal virtud es que combina tres propiedades esenciales:

1. exactitud estructural,
2. densidad racional multiplicativa,
3. criterio de parada explícito.

La familia CRIVA puede resumirse como una criba modular exacta en la que la semilla inicial se modela como una fracción racional q_0 y en la que cada paso elimina un factor (1 - 1/p) asociado a un primo. Esto permite acompañar la teoría analítica de la densidad de primos con una formulación computacional y discreta, de modo que la densidad se trata como un objeto modular, entendible y controlable.

La conclusión más fuerte es la siguiente:

- la criba racional iterativa está perfectamente formalizada,
- el criterio de parada exacto es la raíz del rango,
- la densidad residual admite una fórmula exacta,
- y las semillas racionales como 4/9 o 2/3 no son leyes universales, sino densidades de una estructura modular concreta.

Por eso mismo, el algoritmo puede ser teorematizado como una familia de cribas racionales, con un nombre propio: CRIVA.

---

# 8. Nombre del algoritmo y notación final

El esquema de algoritmos aquí desarrollado puede denotarse por:

- CRIVA = Criba Racional Iterativa de Validación Aritmética,
- o, más conservadoramente,
- CRIVA = Criterio Racional Iterativo de Válida Aritmética.

El punto importante es que el nombre no sustituye a la demostración; lo que hace útil a CRIVA es que su comportamiento está gobernado por las leyes exactas de densidad y de periodicidad modular.

## En una frase

La criba racional iterativa define un sistema exacto de eliminación modular en el que la densidad residual se multiplica por factores racionales 1 - 1/p y se detiene con rigor cuando el conjunto de primos filtrados alcanza la raíz del rango.

---

# 9. Versión breve en español para uso directo

La criba racional iterativa puede describirse así:

- se parte de un conjunto inicial S_0,
- se aplica la eliminación de múltiplos por primos en orden creciente,
- se obtiene un conjunto S_k de supervivientes,
- la densidad sigue la ley q_k = q_0 ∏ (1 - 1/p_i),
- y la parada exacta ocurre cuando se han filtrado todos los primos ≤ √N.

Esto convierte la criba en una estructura teorematizable, medible y reproducible; no solo en una heurística.

---

# 10. Versión breve en inglés para uso directo

The iterative rational sieve can be described as follows:

- start from an initial set S_0,
- remove multiples of primes in increasing order,
- obtain a surviving set S_k,
- the density evolves as q_k = q_0 ∏ (1 - 1/p_i),
- and the exact stopping point is reached once all primes ≤ √N have been filtered.

This turns the sieve into a formalizable, measurable and reproducible structure rather than a mere heuristic.

---

# 11. Observación final

Este trabajo no pretende sostener que CRIVA sea una “solución definitiva” en la teoría de números primos. Su objetivo es más modesto y más útil: formalizar una familia de métodos iterativos de criba racional con una lógica clara, un criterio de parada exacto y una densidad residual gobernada por factores racionales. Eso ya es una base suficientemente sólida para que un algoritmo de este tipo pueda ser estudiado, reproducido y comparado con rigor.
