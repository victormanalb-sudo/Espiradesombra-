# CRIVA: Criba Racional Iterativa de Validación Aritmética
# CRIVA: Rational Iterative Sieve of Arithmetic Validation

## Resumen / Abstract

Este trabajo presenta un marco matemático y algorítmico para una familia de cribas modulares iterativas en la que la supervivencia de candidatos se modela mediante operadores de eliminación por primos y la densidad residual se expresa como un producto racional. El objetivo principal no es sustituir la teoría clásica de los números primos, sino ofrecer una formulación exacta y reproducible de una criba modular iterativa con criterio de parada claro, ley de densidad y tratamiento explícito del caso de semillas racionales.

The present work introduces a mathematical and algorithmic framework for a family of iterative modular sieves in which the survival of candidates is modeled by prime-elimination operators and the residual density is expressed as a rational product. The main objective is not to replace the classical theory of prime numbers, but to provide an exact and reproducible formulation of an iterative modular sieve with a clear stopping rule, a density law, and an explicit treatment of rational-seed cases.

La estructura central del trabajo es la siguiente:

- se define un operador de supervivencia R_p(S) = {n ∈ S : p ∤ n};
- se itera la composición de operadores sobre una sucesión de primos;
- se demuestra que la composición es conmutativa;
- se obtiene la densidad residual exacta mediante un producto de factores (1 - 1/p);
- y se establece un criterio exacto de parada cuando se filtran todos los primos menores o iguales a √N.

The central structure of the paper is:

- define a survival operator R_p(S) = {n ∈ S : p ∤ n};
- iterate the composition of operators over a prime sequence;
- prove that these compositions commute;
- derive the exact residual density through a product of factors (1 - 1/p);
- and establish an exact stopping criterion when all primes ≤ √N have been filtered.

Esta formulación se denomina CRIVA, por Criba Racional Iterativa de Validación Aritmética. La presentación se mantiene dentro del marco de una exploración matemática reproducible, con énfasis en la exactitud modular, la periodicidad y la interpretación racional de la semilla inicial.

This formulation is named CRIVA, for Rational Iterative Sieve of Arithmetic Validation. The presentation remains within the framework of a reproducible mathematical exploration, emphasizing modular exactness, periodicity, and the rational interpretation of the initial seed.

---

## 1. Introducción / Introduction

La criba clásica de Eratóstenes constituye el ejemplo más elemental de reducción iterativa de candidatos. Dado un intervalo [1, N], se eliminan todos los múltiplos de cada primo p ≤ √N; los supervivientes son exactamente los primos del rango considerado. En la práctica, esa idea puede generalizarse de varias maneras: haciendo la eliminación sobre clases de residuos, sobre módulos periódicos, o sobre densidades iniciales no triviales.

The classical sieve of Eratosthenes is the most elementary example of iterative candidate reduction. Given an interval [1, N], one removes all multiples of each prime p ≤ √N; the survivors are exactly the primes in the range. In practice, that idea can be generalized in several ways: by elimination over residue classes, over periodic modules, or over nontrivial initial densities.

El presente trabajo formaliza una versión que se puede describir como una criba racional iterativa: la estructura residual se analiza como un conjunto de elementos que sobreviven a una sucesión de filtrados, y la densidad residual se expresa de forma multiplicativa. La intención es mantener la exactitud del modelo, evitar la confusión entre densidad universal y densidad modular concreta, y dar una regla de paro que sea rigurosa dentro del rango finito considerado.

The present work formalizes a version that can be described as an iterative rational sieve: the residual structure is analyzed as a set of elements surviving a sequence of filters, and the residual density is expressed multiplicatively. The intention is to preserve model exactness, avoid confusion between a universal density and a concrete modular density, and provide a stopping rule that is rigorous within the finite range under consideration.

---

## 2. Definiciones básicas / Basic definitions

### Definición 1. Operador de supervivencia / Definition 1. Survival operator

Sea S ⊆ ℕ y sea p un primo. Se define:

R_p(S) = {n ∈ S : p ∤ n}.

Este operador elimina exactamente los elementos de S que son múltiplos de p.

Let S ⊆ ℕ and let p be prime. Define:

R_p(S) = {n ∈ S : p ∤ n}.

This operator removes exactly the elements of S that are multiples of p.

### Definición 2. Criba iterativa / Definition 2. Iterative sieve

Sea P = (p_1, ..., p_k) una secuencia creciente de primos. Definimos:

S_0 = S,
S_j = R_{p_j}(S_{j-1}) para 1 ≤ j ≤ k.

Equivalentemente,

S_k = R_{p_k} ∘ ... ∘ R_{p_1}(S).

Let P = (p_1, ..., p_k) be an increasing sequence of primes. Define:

S_0 = S,
S_j = R_{p_j}(S_{j-1}) for 1 ≤ j ≤ k.

Equivalently,

S_k = R_{p_k} ∘ ... ∘ R_{p_1}(S).

### Definición 3. Densidad residual / Definition 3. Residual density

Si S ⊆ [1, N], definimos la densidad residual como:

δ(S) = |S| / N.

Cuando el contexto es modular, y si A ⊆ ℤ/Mℤ, entonces:

δ(A) = |A| / M.

If S ⊆ [1, N], define the residual density as:

δ(S) = |S| / N.

When the context is modular, and A ⊆ ℤ/Mℤ, then:

δ(A) = |A| / M.

---

## 3. Proposiciones elementales / Elementary propositions

### Proposición 1. Conmutatividad de los filtros / Proposition 1. Commutativity of the filters

Para cualesquiera primos p, q se cumple:

R_p ∘ R_q = R_q ∘ R_p.

### Demostración / Proof

Un entero n pertenece a R_p(R_q(S)) si y solo si n ∈ S, p ∤ n y q ∤ n. La misma condición caracteriza a R_q(R_p(S)). Por tanto ambos operadores coinciden sobre cualquier conjunto S.

For any primes p, q,

R_p ∘ R_q = R_q ∘ R_p.

### Proof

An integer n belongs to R_p(R_q(S)) iff n ∈ S, p ∤ n and q ∤ n. The same condition characterizes R_q(R_p(S)). Hence both operations coincide on every set S.

### Consecuencia / Consequence

La composición de los filtros no depende del orden en que se apliquen, sino únicamente del conjunto de primos involucrados.

The composition of the filters does not depend on the order in which they are applied, only on the set of primes involved.

---

## 4. Teorema de densidad exacta / Exact density theorem

### Teorema 1. Densidad en un módulo base / Theorem 1. Density in a base modulus

Sea M = ∏_{i=1}^k p_i, y sea A ⊆ ℤ/Mℤ el conjunto de residuos que sobreviven a la eliminación de los primos p_1, ..., p_k. Entonces:

A = {a mod M : gcd(a, M) = 1},

y por consiguiente:

|A| = φ(M),

con lo cual:

δ(A) = |A| / M = φ(M) / M = ∏_{i=1}^k (1 - 1/p_i).

Let M = ∏_{i=1}^k p_i, and let A ⊆ ℤ/Mℤ be the set of residues surviving the elimination of the primes p_1, ..., p_k. Then:

A = {a mod M : gcd(a, M) = 1},

and therefore:

|A| = φ(M),

hence:

δ(A) = |A| / M = φ(M) / M = ∏_{i=1}^k (1 - 1/p_i).

### Demostración / Proof

Un residuo a mod M sobrevive a la criba si y solo si no es divisible por ninguno de los primos p_i. Eso es exactamente la condición gcd(a, M) = 1. El número de elementos de ℤ/Mℤ que son coprimos con M es, por definición, φ(M). La identidad multiplicativa de Euler da:

φ(M) = M ∏_{i=1}^k (1 - 1/p_i).

Dividiendo por M se obtiene la fórmula buscada.

A residue a mod M survives the sieve if and only if it is divisible by none of the primes p_i. That is exactly the condition gcd(a, M) = 1. The number of elements of ℤ/Mℤ that are coprime to M is, by definition, φ(M). Euler's multiplicativity yields:

φ(M) = M ∏_{i=1}^k (1 - 1/p_i).

Dividing by M gives the desired formula.

### Observación / Remark

La expresión ρ_k = ∏_{i=1}^k (1 - 1/p_i) es la densidad exacta del conjunto residual en un período modular completo y no debe confundirse con una constante universal. Es la densidad del módulo elegido tras los filtros aplicados.

The expression ρ_k = ∏_{i=1}^k (1 - 1/p_i) is the exact density of the residual set in a complete modular period and must not be confused with a universal constant. It is the density of the chosen modulus after the applied filters.

---

## 5. Teorema de conteo en intervalos finitos / Finite-interval counting theorem

### Teorema 2. Conteo exacto en [1, N] / Theorem 2. Exact counting in [1, N]

Sea N ∈ ℕ, y sea P_k = ∏_{i=1}^k p_i. Entonces el número de enteros en [1, N] que sobreviven a la eliminación de p_1, ..., p_k es:

S_k(N) = m φ(P_k) + #{a ∈ [1, r] : gcd(a, P_k) = 1},

donde N = m P_k + r con 0 ≤ r < P_k.

Let N ∈ ℕ and let P_k = ∏_{i=1}^k p_i. Then the number of integers in [1, N] surviving the elimination of p_1, ..., p_k is:

S_k(N) = m φ(P_k) + #{a ∈ [1, r] : gcd(a, P_k) = 1},

where N = m P_k + r with 0 ≤ r < P_k.

### Demostración / Proof

Los residuos modulo P_k se repiten periódicamente. En cada bloque completo de longitud P_k, exactamente φ(P_k) residuos sobreviven. El término restante r se cuenta de forma exacta por la segunda parte de la fórmula. Sumando ambos resultados se obtiene el total exacto.

The residues modulo P_k repeat periodically. In each complete block of length P_k, exactly φ(P_k) residues survive. The remaining part r is counted exactly by the second term. Adding both parts yields the exact total.

---

## 6. Criterio de parada exacto / Exact stopping criterion

### Teorema 3. Parada en la raíz / Theorem 3. Stopping at the square root

Sea N ∈ ℕ. Si la sucesión de primos filtrados cumple:

p_k ≥ √N,

entonces todo entero n ∈ [2, N] que sobreviva a la criba es primo.

Let N ∈ ℕ. If the prime sequence used in the sieve satisfies:

p_k ≥ √N,

then every integer n ∈ [2, N] that survives the sieve is prime.

### Demostración / Proof

Si n ≤ N es compuesto, entonces n = ab con 1 < a ≤ b < n. Cualquiera de sus divisores propios tiene un primo divisor p ≤ √n ≤ √N. Al filtrar todos los primos menores o iguales a √N, todo número compuesto queda eliminado. Por tanto, los únicos supervivientes distintos de 1 son los primos en el intervalo considerado.

If n ≤ N is composite, then n = ab with 1 < a ≤ b < n. Any proper divisor has a prime divisor p ≤ √n ≤ √N. Once all primes less than or equal to √N are filtered, every composite number is eliminated. Therefore, the only survivors different from 1 are the primes in the interval under consideration.

### Observación / Remark

Este es el criterio de parada exacto de la criba modular iterativa en un rango finito. En contexto práctico, se puede reemplazar por una cota de estabilidad ε si se desea continuar la criba sin llegar exactamente a la raíz.

This is the exact stopping criterion for the iterative modular sieve in a finite range. In a practical context, it can be replaced by a stability threshold ε when one wishes to continue the sieve without reaching the exact square root.

---

## 7. Semillas racionales / Rational seeds

### Definición 4. Semilla racional / Definition 4. Rational seed

Se llama semilla racional a una configuración inicial A_0 ⊆ ℤ/Mℤ con densidad:

q_0 = |A_0| / M,

donde q_0 ∈ ℚ.

A rational seed is an initial configuration A_0 ⊆ ℤ/Mℤ with density:

q_0 = |A_0| / M,

where q_0 ∈ ℚ.

### Teorema 4. Evolución racional de la densidad / Theorem 4. Rational evolution of the density

Si una semilla racional A_0 se filtra con una secuencia de primos p_1, ..., p_k, y si la distribución inicial es uniforme dentro del módulo base, entonces la densidad residual satisface:

q_k = q_0 ∏_{i=1}^k (1 - 1/p_i).

If a rational seed A_0 is filtered with a prime sequence p_1, ..., p_k, and if the initial distribution is uniform within the base modulus, then the residual density satisfies:

q_k = q_0 ∏_{i=1}^k (1 - 1/p_i).

### Demostración / Proof

En cada paso, la probabilidad de que un elemento del módulo permanezca tras el filtro por p_i es 1 - 1/p_i. La composición de estas probabilidades sobre la secuencia de primos da el producto multiplicativo. En términos estrictos de cardinalidad, esto es una consecuencia del hecho de que la eliminació de multiplos por p_i descarta exactamente una fracción 1/p_i de las clases restantes cuando la distribución es uniforme.

At each step, the probability that an element of the modulus remains after the p_i filter is 1 - 1/p_i. The composition of these probabilities over the prime sequence gives the multiplicative product. In strict cardinality terms, this follows from the fact that eliminating multiples of p_i discards exactly a fraction 1/p_i of the remaining residue classes when the distribution is uniform.

### Observación / Remark

La fracción racional inicial no tiene carácter universal. Un valor como 4/9, 2/3 o 4/15 solo es una semilla válida si representa una familia concreta de residuos modulo un M determinado. No existe una fracción universal que gobierne todos los rangos y todas las configuraciones.

The initial rational fraction does not possess universal meaning. A value such as 4/9, 2/3, or 4/15 is only a valid seed if it represents a concrete residue family modulo a given M. There is no universal fraction governing all ranges and all configurations.

---

## 8. Estructura del algoritmo / Algorithmic structure

### Algoritmo CRIVA / CRIVA algorithm

Entrada:

- N ∈ ℕ,
- una semilla racional q_0 en un módulo base M,
- una secuencia creciente de primos p_1 < ... < p_k.

Salida:

- el conjunto residual S_k,
- la densidad residual q_k,
- y la decisión de parada.

Step 1: Inicializar q = q_0.
Step 2: Para cada primo p en la secuencia: q ← q · (1 - 1/p); eliminar las clases divisibles por p.
Step 3: Si p ≥ √N, detenerse.
Step 4: Devolver S_k y q.

Input:

- N ∈ ℕ,
- a rational seed q_0 in a base modulus M,
- an increasing prime sequence p_1 < ... < p_k.

Output:

- the residual set S_k,
- the residual density q_k,
- and the stopping decision.

Step 1: Initialize q = q_0.
Step 2: For each prime p in the sequence: q ← q · (1 - 1/p); remove residue classes divisible by p.
Step 3: If p ≥ √N, stop.
Step 4: Return S_k and q.

---

## 9. Limitaciones y alcance / Limitations and scope

Este trabajo presenta una formalización exacta de una criba modular iterativa. Sin embargo, no pretende afirmar que la teoría desarrollada sustituye o resuelve problemas clásicos de la teoría analítica de números. Lo que sí ofrece es un marco estructural claro para estudiar:

- densidad residual en intervalos finitos,
- residuos coprimos con módulos producto,
- evoluciones racionales de una semilla inicial,
- y criterios de parada computables.

This work presents an exact formalization of an iterative modular sieve. However, it does not claim that the theory developed replaces or solves classic problems in analytic number theory. What it does provide is a clear structural framework for studying:

- residual density in finite intervals,
- residues coprime to product moduli,
- rational evolutions of an initial seed,
- and computable stopping criteria.

La utilidad principal está en la reproducibilidad: la criba puede implementarse de forma exacta, verificarse en ejemplos pequeños y compararse con la criba de Eratóstenes estándar.

The principal utility lies in reproducibility: the sieve can be implemented exactly, verified on small examples, and compared with the standard Eratosthenes sieve.

---

## 10. Conclusión / Conclusion

La criba racional iterativa define un modelo compacto y exacto para el filtrado modular de candidatos. El elemento principal de la construcción es la identidad

q_k = q_0 ∏_{i=1}^k (1 - 1/p_i),

que expresa la evolución de la densidad residual a lo largo de la secuencia de primos. En el caso de la criba clásica, q_0 = 1 y el conjunto inicial es [1, N], por lo que el algoritmo recupera el conjunto exacto de primos del intervalo cuando la secuencia alcanza la raíz del rango.

The iterative rational sieve defines a compact and exact model for modular filtering of candidates. The main element of the construction is the identity

q_k = q_0 ∏_{i=1}^k (1 - 1/p_i),

which expresses the evolution of residual density along the prime sequence. In the classical sieve case, q_0 = 1 and the initial set is [1, N], so the algorithm recovers the exact prime set in the interval once the sequence reaches the square root of the range.

La nomenclatura CRIVA sirve como una referencia operativa para una familia de algoritmos de criba modular iterativa con semilla racional, densidad multiplicativa y criterio de parada exacto. Es una formulación útil para análisis, demostración y experimentación reproducible, pero no debe entenderse como una sustitución de la teoría clásica en sentido formal estricto.

The name CRIVA serves as an operational reference for a family of iterative modular sieve algorithms with rational seeds, multiplicative density, and exact stopping criteria. It is a useful formulation for analysis, proof, and reproducible experimentation, but it should not be understood as a replacement for classical theory in a strict formal sense.

---

## 11. Versión breve en español / Short Spanish version

La criba racional iterativa se define por la iteración de filtros de divisibilidad sobre una secuencia de primos. Si S_0 es el conjunto inicial y p_1, ..., p_k son los primos filtrados, entonces:

S_k = R_{p_k} ∘ ... ∘ R_{p_1}(S_0).

La densidad residual satisface:

q_k = q_0 ∏_{i=1}^k (1 - 1/p_i).

Cuando se trabaja sobre [1, N], la parada exacta se produce cuando se han filtrado todos los primos ≤ √N. En ese punto, los supervivientes son exactamente los primos del rango y el resto de números compuestos han desaparecido.

The iterative rational sieve is defined by the iteration of divisibility filters over a sequence of primes. If S_0 is the initial set and p_1, ..., p_k are the filtered primes, then:

S_k = R_{p_k} ∘ ... ∘ R_{p_1}(S_0).

The residual density satisfies:

q_k = q_0 ∏_{i=1}^k (1 - 1/p_i).

When working over [1, N], the exact stopping point is reached when all primes ≤ √N have been filtered. At that point, the survivors are exactly the primes in the range, and the remaining composite numbers have disappeared.

---

## 12. Agradecimiento conceptual / Conceptual note

Este documento fue formulado como una versión más académica y más defensable de la lógica built sobre la criba racional iterativa. La formalización mantenida aquí se apoya en dos principios esenciales:

1. la exactitud modular de los residuos coprimos,
2. la multiplicatividad racional de la densidad residual.

This document was formulated as a more academic and defensible version of the logic built around the iterative rational sieve. The formalization maintained here rests on two essential principles:

1. the modular exactness of coprime residues,
2. the rational multiplicativity of the residual density.

Esos principios permiten describir el algoritmo de manera ordenada, reproducible y compatible con la aritmética discreta clásica.

Those principles allow the algorithm to be described in an orderly, reproducible, and classically compatible way.

---

## 13. Referencia compacta de notación / Compact notation reference

- S_0: conjunto inicial
- S_k: conjunto residual tras k filtros
- R_p: operador de supervivencia por primo p
- q_0: densidad inicial
- q_k: densidad residual final
- M: módulo base
- φ: función totient de Euler
- √N: umbral exacto de paro

- S_0: initial set
- S_k: residual set after k filters
- R_p: prime survival operator
- q_0: initial density
- q_k: final residual density
- M: base modulus
- φ: Euler's totient function
- √N: exact stopping threshold

---

## 14. Declaración final / Final statement

El marco CRIVA no debe entenderse como una sustitución de la teoría de números clásica; es una formulación exacta y útil para la exploración computacional de cribas modulares iterativas. Su valor reside en la combinación de tres propiedades: exactitud, periodicidad y densidad racional. Cuando se aplican en un intervalo finito, estos elementos permiten construir una teoría reproducible de filtrado aritmético con regla de parada explícita.

The CRIVA framework should not be understood as a replacement for classical number theory; it is an exact and useful formulation for computational exploration of iterative modular sieves. Its value lies in the combination of three properties: exactness, periodicity, and rational density. When applied to a finite interval, these elements allow one to build a reproducible theory of arithmetic filtering with an explicit stopping rule.
