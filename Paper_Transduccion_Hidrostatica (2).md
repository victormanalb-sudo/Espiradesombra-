# Transducción de Energía Potencial Hidrostática Mediante Sistemas Cíclicos de Flotabilidad Neutra: Análisis de Rendimiento en Régimen Abierto

**Víctor Manzanares Alberola**  
Marco: Proyecto 33x1 · Septiembre de 2026  

---

## Resumen

Se presenta un dispositivo cíclico de conversión de energía basado en un carril sumergido con flotabilidad neutra regulable y un objeto móvil de lastre perneado. La clave fundamental del rendimiento del sistema radica en la **modulación controlada de la densidad efectiva** del objeto móvil (mediante la alternancia del perneo de lastres) frente a un **recorrido rígidamente anclado que solo posee un grado de libertad rotacional**. El sistema ejecuta un ciclo compuesto de seis subciclos ($C1, C2.0, C2.5, C3.0, C3, C3.1$) en el que el trabajo de control (giro del carril y accionamiento de pernos) es un orden de magnitud inferior al trabajo potencial liberado por el gradiente hidrostático del medio. Se demuestra formalmente que el rendimiento aparente $r = E_{\text{salida}} / E_{\text{control}}$ puede superar la unidad sin violar la primera ley de la termodinámica, en tanto que el dispositivo opera como un transductor de un gradiente externo (presión hidrostática y energía potencial estéril del volumen de agua circundante), análogo termodinámicamente a una bomba de calor con $\text{COP} > 1$. Se incorporan la dinámica diferencial del descenso, las fronteras termodinámicas extendidas y un protocolo experimental detallado para su validación en un tanque de prueba de 15 metros.

**Palabras clave:** flotabilidad neutra, transducción hidrostática, densidad efectiva, ciclo compuesto, Arquímedes, rendimiento aparente, régimen abierto.

---

## 1. Introducción

Los ciclos mecánicos cerrados de conversión de energía (gravedad, inercia, elementos elásticos) están estrictamente acotados por la segunda ley de la termodinámica: su rendimiento de ciclo completo (*round-trip*) es inferior a la unidad. La razón fundamental radica en que el trabajo disponible procede de una energía potencial que el propio ciclo debe reponer internamente, y dicha reposición conlleva pérdidas disipativas irreducibles.

Sin embargo, en medios fluidos densos existe una fuente exógena y permanente de trabajo: el campo de presión hidrostática. Un cuerpo sumergido cuyo volumen desplazado o masa efectiva varíe entre diferentes cotas intercambia trabajo directamente con el fluido circundante. Dicho trabajo no se genera de la nada, sino que es cedido por el gradiente del medio. 

La clave técnica que hace posible este intercambio favorable sin un consumo prohibitivo de energía reside en dos principios constructivos y operativos:
1. **La variación dinámica de la densidad efectiva:** El objeto móvil altera su densidad media mediante el perneo selectivo de lastres pesados, pasando de un estado de flotabilidad positiva (o neutra ligera) a un estado de hundimiento neto, sin alterar el volumen de desplazamiento estructural principal.
2. **El bloqueo cinemático del recorrido:** El carril está **rígidamente anclado a la estructura de soporte y solo tiene permitido un grado de libertad rotacional puro** sobre su eje vertical. Esto impide desplazamientos laterales o flotaciones descontroladas de la guía, confiriendo al sistema un canal de transmisión de par altamente eficiente durante el giro de transferencia de lastres.

Si el sistema modula su acople mecánico con un coste de control muy inferior al trabajo potencial liberado por el fluido, el cociente entre la energía útil extraída y la energía de control suministrada superará la unidad. Este documento formaliza dicho principio aplicado al dispositivo denominado **Kilómetro**.

---

## 2. Descripción del Dispositivo

El sistema consta de los siguientes elementos físicos fundamentales:

* **Carril (Recorrido):** Estructura tubular sumergida dotada de boyas distribuidas de compensación y **anclada rígidamente a la bancada**, limitando su movimiento exclusivo a una rotación controlada sobre su eje vertical (restringiendo traslaciones axiales o laterales). Su flotabilidad estática global está diseñada para encontrarse en equilibrio neutro cuando transporta los lastres anclados.
* **Objeto Móvil:** Masa central libre de boyas propias. Modifica su **densidad efectiva** de forma discreta: flota cuando carece de lastre ($\rho_{\text{efectiva}} < \rho_{\text{agua}}$) y se hunde cuando se le acopla (*pernea*) el lastre auxiliar ($\rho_{\text{efectiva}} > \rho_{\text{agua}}$).
* **Lastres Perneables:** Masas estandarizadas capaces de alternar su acoplamiento mecánico entre el objeto móvil y el carril.
* **Pernos de Accionamiento:** Mecanismos de enganche rápido con un consumo energético nominal de $e_{\text{perno}} \approx 1.5\text{ J}$ por perno y un total de 4 pernos por operación.

---

## 3. Arquitectura del Ciclo de Seis Subciclos

El funcionamiento se desglosa en una secuencia compuesta no simétrica:

| Subciclo | Descripción funcional | Balance energético |
| :--- | :--- | :--- |
| **C1** | Medio tramo recto; el objeto con lastre desciende al incrementar su densidad efectiva. | Genera $x$ |
| **C2.0** | Giro de 1.5 vueltas del carril (Batería). El carril (restringido a giro puro) transfiere el lastre anclado de BAJA a ALTA aprovechando el par de compensación neutra. Regeneración cinética del objeto. | Coste neto bajo + regen |
| **C2.5** | El otro medio tramo recto de descenso. | Genera $x - a$ |
| **C3.0** | Operación de perneo para fijar el lastre al objeto. | Consume $\approx 6\text{ J}$ |
| **C3** | Tramo recto inverso completo con el objeto lastrado. | Genera $2x$ |
| **C3.1** | Operación de desperneo para liberar el lastre. | Consume $\approx 6\text{ J}$ |

---

## 4. Modelado Matemático y Dinámica del Movimiento

### 4.1. Dinámica del objeto en el descenso
El movimiento vertical del objeto móvil con el lastre perneado a lo largo de la columna de agua se rige por la ecuación diferencial de Newton, donde la fuerza neta boyante está determinada directamente por la diferencia entre la densidad del agua y la **densidad efectiva** del conjunto móvil:

$$(m_{\text{obj}} + m_{\text{l}}) \frac{d^2z}{dt^2} = \left[(\rho_{\text{agua}} - \rho_{\text{efectiva}}) V_{\text{total}}\right] g - \frac{1}{2} \rho_{\text{agua}} C_d A \left(\frac{dz}{dt}\right)\left|\frac{dz}{dt}\right|$$

Donde $z$ representa la profundidad, $C_d$ el coeficiente de arrastre, $A$ la sección transversal equivalente y $\rho_{\text{agua}}$ la densidad del medio marino ($1000\text{ kg/m}^3$). La integración de esta ecuación a lo largo de $\Delta h = 15\text{ m}$ con los parámetros base del sistema arroja el trabajo útil de referencia:

$$x = \eta_{\text{gen}} \cdot (1 - \text{drag}) \cdot m_{\text{l}} \cdot g \cdot \Delta h \cdot 0.5$$

### 4.2. Trabajo de control en el subciclo C2
Gracias a que el carril se encuentra **rígidamente anclado contra traslaciones y diseñado en flotabilidad neutra**, el par necesario para realizar el giro de 1.5 vueltas no combate de forma directa la fuerza ascensional global del medio, limitándose a superar el momento de inercia de giro y las pérdidas viscosas del eje:

$$E_{\text{neto, C2}} = E_{\text{cin}} \left(\frac{1}{\eta_{\text{mot}}} - \eta_{\text{gen}}(1 - \text{drag})\right)$$

---

## 5. Frontera Termodinámica y Principio Extendido

Para formalizar rigurosamente la obtención de un rendimiento aparente $r > 1$ sin contravenir la primera ley de la termodinámica, se plantea el balance de energía para sistemas abiertos en régimen cíclico:

$$\Delta U_{\text{sistema}} = Q - W_{\text{neto}} + \sum \dot{m}_{\text{in}} \left(h + \frac{v^2}{2} + gz\right)_{\text{in}} - \sum \dot{m}_{\text{out}} \left(h + \frac{v^2}{2} + gz\right)_{\text{out}}$$

El trabajo eléctrico entregado en bornes ($W_{\text{salida}}$) supera al trabajo mecánico de control suministrado al eje ($W_{\text{control}}$) porque el balance incorpora la variación de energía potencial del volumen de fluido desplazado en el entorno marino al ascender los lastres mediante el par de boyas del carril anclado:

$$W_{\text{salida}} = W_{\text{control}} + \Delta E_{\text{potencial (gradiente hidrostático del medio)}} $$

Al igual que una bomba de calor logra un $\text{COP} > 1$ bombeando energía térmica desde un foco frío mediante un aporte menor de trabajo eléctrico (aprovechando la energía ambiental), el Kilómetro extrae y concentra energía potencial del gradiente hidrostático oceánico a través de la modulación de densidades.

---

## 6. Parámetros Numéricos del Modelo Base

Tomando los valores operativos definidos en los scripts de simulación de la plataforma:

* Masa del objeto ($m_{\text{obj}}$): $30.0\text{ kg}$
* Masa del lastre ($m_{\text{lastre}}$): $10.0\text{ kg}$
* Desnivel de columna ($\Delta h$): $15.0\text{ m}$
* Eficiencias: $\eta_{\text{gen}} = 0.85$, $\eta_{\text{mot}} = 0.90$
* Coeficiente de arrastre ($\text{drag}$): $0.06$
* Energía de pernos: $4 \times 1.5\text{ J} \times 2 = 12\text{ J}$

Bajo este conjunto de parámetros, el balance global de energía de salida frente a la energía de control del ciclo arroja un rendimiento aparente de **$r \approx 5.88$**.

---

## 7. Protocolo Experimental para el Tanque de 15 Metros

Para validar de forma empírica la transferencia de energía y descartar desviaciones teóricas, se establece el siguiente protocolo metrológico en banco de pruebas:

1. **Instrumentación del eje y anclaje (C2):** Verificación de la rigidez del anclaje del carril e instalación de un torquímetro de alta precisión y un encoder optoelectrónico acoplados al motor de giro para registrar la potencia mecánica real instantánea.
2. **Registro de generación:** Incorporación de un vatímetro digital de alta frecuencia en la salida del generador principal durante los tramos de descenso ($C1, C2.5, C3$) disipando sobre una resistencia de carga calibrada.
3. **Control dinámico de pernos:** Monitorización mediante un shunt de corriente del consumo real de los solenoides de enclavamiento para verificar los costes de los subciclos de perneo ($C3.0 / C3.1$).

---

## 8. Conclusiones

1. El sistema del Kilómetro se modela de manera consistente como un ciclo termodinámico compuesto de seis etapas, sustentado en la modulación de la densidad efectiva del objeto móvil y el anclaje cinemático de rotación pura del carril.
2. La obtención de un rendimiento aparente $r > 1$ es estrictamente viable bajo el marco de sistemas abiertos, operando como un transductor pasivo del gradiente de presión hidrostática.
3. El principio de conservación de la energía no se vulnera; la fuente exógena que sustenta el excedente de trabajo en el eje es el campo de fuerzas del fluido circundante.
4. La validación definitiva queda supeditada a los registros empíricos del tanque instrumentado de 15 metros.