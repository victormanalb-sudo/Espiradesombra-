# El Límite Manzanares: Extracción de Energía en Molinos Anidados  
## Análisis Teórico para Rotores Montados sobre Aspas de Rotores Primarios

**Autor:** Víctor Manzanares Alberola (con asistencia analítica)  
**Fecha:** 26 de octubre de 2026  
**Versión:** Borrador técnico 1.0

---

### Resumen

Se formaliza el **Límite Manzanares** como la extensión conceptual del límite de Betz a configuraciones en las que un rotor secundario (mini-molino) está montado sobre el aspa de un rotor primario. En esta geometría el viento relativo visto por el mini-rotor crece con la velocidad angular del rotor anfitrión. Se demuestra que, aunque el coeficiente de potencia local del secundario puede aparecer superior a 16/27 cuando se normaliza con el viento freestream, la potencia neta del sistema agregado permanece acotada por el límite de Betz del área barrida del rotor primario (o por sus extensiones multi-actuador conocidas). El “límite” Manzanares describe precisamente esta amplificación aparente del viento relativo y la contabilidad energética correcta entre potencia mecánica prestada y potencia extraída del viento.

---

### 1. Introducción

El límite de Betz (1919–1920) establece que ningún disco actuador ideal puede extraer más de \( C_P = 16/27 \approx 0.593 \) de la energía cinética del viento que atraviesa su área. La derivación asume un rotor fijo respecto a un marco inercial y un flujo axial unidimensional.

Cuando un mini-rotor se monta sobre el aspa de un rotor mayor (configuración “molino dentro de molino”), el marco de referencia del mini-rotor ya no es inercial. La velocidad tangencial \( \Omega r \) del punto de montaje se suma vectorialmente al viento axial, generando un viento relativo (viento aparente) significativamente mayor. Cuanto más rápido gira el rotor primario, mayor es el viento que “choca” contra el mini-rotor. Este es el fenómeno que el Límite Manzanares pretende capturar.

La literatura más cercana es el concepto **X-Rotor** (proyecto Horizon 2020), que coloca rotores secundarios en las puntas de un rotor primario vertical y los utiliza como toma de potencia aerodinámica (“caja de cambios aerodinámica”). Estudios recientes muestran eficiencias de conversión del 87–90 % de la potencia primaria hacia los secundarios.

---

### 2. Recuerdo del límite de Betz

Para un disco actuador de área \( A \), con velocidad freestream \( U_\infty \) y factor de inducción axial \( a \), la potencia extraída es:

\[
P = 2 \rho A U_\infty^3 a (1-a)^2
\]

El máximo ocurre en \( a = 1/3 \):

\[
C_P^{\text{Betz}} = \frac{16}{27} \approx 0.593
\]

El viento a través del disco es \( U_d = U_\infty (1-a) \) y el viento lejano a sotavento es \( U_w = U_\infty (1-2a) \).

---

### 3. Configuración de molinos anidados

- **Rotor primario**: área barrida \( A_p \), radio \( R \), velocidad angular \( \Omega \), tip-speed ratio \( \lambda_p = \Omega R / U_\infty \), factor de inducción \( a_p \).
- **Mini-rotor (secundario)**: área \( A_s \ll A_p \), montado a radio \( r \leq R \) (típicamente cerca de la punta), con su propio generador.

El viento relativo visto por el mini-rotor es aproximadamente:

\[
V_{\text{rel}} = \sqrt{ \bigl[ U_\infty (1 - a_p) \bigr]^2 + (\Omega r)^2 }
\]

Cuando \( \lambda_p \gtrsim 5 \)–\( 7 \) (valores típicos de turbinas modernas), el término tangencial domina y 

\[
V_{\text{rel}} \approx \Omega r = \lambda_p \frac{r}{R} U_\infty
\]

---

### 4. Potencia aparente del mini-rotor

La potencia máxima teórica que el mini-rotor puede extraer de su viento relativo es:

\[
P_s^{\text{max}} = C_P^{\text{Betz}} \cdot \frac{1}{2} \rho A_s V_{\text{rel}}^3
\]

Si se normaliza erróneamente con el viento freestream \( U_\infty \), se obtiene un “\( C_P \) aparente” que puede superar ampliamente 16/27:

\[
C_P^{\text{aparente}} = \frac{P_s}{\frac{1}{2} \rho A_s U_\infty^3} = C_P^{\text{Betz}} \left( \frac{V_{\text{rel}}}{U_\infty} \right)^3
\]

Este es el **Límite Manzanares** en su formulación local: el coeficiente de potencia *observado* respecto al viento lejano crece con el cubo de la amplificación de velocidad relativa.

---

### 5. Contabilidad energética correcta (el verdadero límite)

La energía cinética asociada a \( V_{\text{rel}} \) no proviene únicamente del viento freestream. Una fracción importante proviene del trabajo mecánico realizado por el rotor primario para mantener la velocidad \( \Omega \) frente al empuje (thrust) del mini-rotor.

El empuje del mini-rotor sobre el flujo relativo genera una fuerza de arrastre en el marco del primario, que se opone a su rotación. Por tanto:

\[
P_{\text{mecánica prestada}} = T_s \cdot (\Omega r)
\]

donde \( T_s \) es el empuje del secundario.

La potencia neta entregada a los generadores es:

\[
P_{\text{neta}} = P_{\text{primario, aero}} + P_s^{\text{eléctrica}} - \text{pérdidas}
\]

En el análisis del X-Rotor se obtiene que la eficiencia de conversión de la potencia aerodinámica primaria hacia los secundarios es aproximadamente:

\[
\eta \approx \frac{C_{P,s}}{C_{T,s}} \cdot f(\lambda_p)
\]

con valores prácticos de 87–90 %. Esto confirma que el secundario actúa principalmente como convertidor de la potencia ya extraída por el primario, no como extractor adicional de energía del freestream más allá del límite del primario.

**Conclusión del Límite Manzanares:**  
El sistema agregado no puede superar el límite de Betz (o sus extensiones multi-disco conocidas de Newman \( \approx 0.64 \) o superiores bajo condiciones de recuperación de presión) referido al área barrida del rotor primario. El “exceso” local del mini-rotor es energía mecánica prestada por el primario y posteriormente convertida.

---

### 6. Relación con la literatura

| Concepto | Relación con el Límite Manzanares |
|----------|-----------------------------------|
| Límite de Betz clásico | Caso límite cuando \( \Omega \to 0 \) (mástil fijo) |
| Newman (1986) dual actuator | Extensión a dos discos en serie; \( C_P \approx 0.64 \) |
| X-Rotor (Horizon 2020) | Implementación práctica de rotores secundarios en puntas; conversión 87–90 % |
| Extensiones multi-stage | Posible superación moderada del 16/27 mediante varios discos |

No se ha localizado en la literatura un paper chino que formalice exactamente esta derivación con el nombre o el enfoque de “mástil móvil” / viento relativo dependiente de \( \Omega \). El X-Rotor es el precedente más cercano.

---

### 7. Ejemplo numérico ilustrativo

Supongamos:
- \( U_\infty = 10 \) m/s
- \( \lambda_p = 7 \), \( r = R \)
- \( V_{\text{rel}} \approx 70 \) m/s
- \( A_s / A_p = 0.01 \)

Potencia aparente máxima del mini-rotor (normalizada a \( U_\infty \)):

\[
C_P^{\text{aparente}} \approx 0.593 \times 7^3 \approx 203
\]

Esto es absurdo como coeficiente global, pero correcto como indicador de la amplificación local. La potencia real extraída del viento freestream sigue limitada por el primario.

---

### 8. Conclusiones

1. El Límite Manzanares describe la amplificación del viento relativo en rotores montados sobre aspas en rotación.
2. Localmente el mini-rotor puede “ver” un coeficiente de potencia muy superior a 16/27 cuando se normaliza con \( U_\infty \).
3. Globalmente, la potencia neta del sistema permanece acotada por el límite de Betz del área primaria (o extensiones multi-actuador).
4. La configuración es físicamente válida como toma de potencia aerodinámica (análoga al X-Rotor) y puede ofrecer ventajas de diseño (generadores más ligeros cerca del nivel del suelo, eliminación de caja de cambios, etc.).
5. Cualquier claim de superación neta del límite de Betz en esta configuración requiere demostrar extracción adicional de energía del freestream más allá de la del primario, lo cual no está justificado por la contabilidad energética actual.

---

### Referencias clave

- Betz, A. (1920). Das Maximum der theoretisch möglichen Ausnutzung des Windes durch Windmotoren.
- Newman, B. G. (1986). Actuator-disc theory for vertical-axis wind turbines. *J. Wind Eng. Ind. Aerodyn.*
- Leithead et al. / Morgan et al. (2024–2025). Trabajos sobre el X-Rotor y secondary rotors for VAWT power take-off. *Wind Energy*.
- Extensiones multi-turbine de Betz (Broberg et al., arXiv 2018 y posteriores).

---

*Este documento formaliza el concepto del Límite Manzanares a partir de las discusiones previas y la literatura disponible. Está preparado para iteración, simulación numérica y eventual publicación.*
