# Análisis Geométrico Kilométrico, Inversión Cinemática y Dinámica Operativa del Ciclo de 6 Etapas: Proyecto 33x1

**Autor:** Víctor Manzanares Alberola  
**Fecha:** Septiembre de 2026  
**Dominio:** Mecánica de Fluidos Aplicada, Cinemática de Sistemas Submarinos y Termodinámica de Sistemas Abiertos

---

## 1. Introducción y la Geometría del "Kilómetro"

En el diseño de sistemas mecánicos de gran escala orientados al aprovechamiento de desequilibrios gravitacionales e hidrostáticos, la escala espacial define la viabilidad del balance energético. El concepto de **"la forma del kilómetro"** en el *Proyecto 33x1* establece una **topología de trayectoria de escala kilométrica** (con una altura efectiva de operación $H = 1000\text{ m}$) diseñada como un sistema abierto anclado que interactúa con el gradiente marítimo dinámico.

La adopción de una traza kilométrica responde a una necesidad física fundamental: **diluir los costes de inercia y fricción de los puntos de giro frente a la energía potencial acumulada en los tramos rectos**.

### 1.1. Equilibrio de Flotabilidad y Anclaje Estructural
1. **Estado de Carga y Flotabilidad Neutra:** Durante el descenso y la operación activa con lastre, el conjunto carril-objeto-lastre está diseñado hidrodinámicamente para alcanzar un estado de **flotabilidad neutra ponderada** con el medio marino circundante. Esto minimiza las fuerzas de fricción en los puntos de apoyo del eje.
2. **El Anclaje Estructural sin Carga:** Cuando el carril se encuentra descargado (fases de retorno o reconfiguración sin lastre), **no asciende de forma autónoma**, ya que se encuentra firmemente fijado a los cimientos del lecho marino. El sistema depende de un movimiento forzado a lo largo de un eje vertical con un único grado de libertad rotacional.

---

## 2. Las 6 Etapas del Ciclo de Funcionamiento y la Inversión Cinemática

El funcionamiento del sistema se rige por una secuencia sincronizada de **6 subciclos**:

```
[Etapa 1: Tramo Recto Descendente C1] 
         │
         ▼
[Etapa 2: Transición de Giro e Inversión C2] 
         │
         ▼
[Etapa 3: Recuperación Inercial / Regen C2.5] 
         │
         ▼
[Etapa 4: Conmutación de Densidad (Lift C3 - Pernos)] 
         │
         ▼
[Etapa 5: Ascenso Asistido por Gradiente (Trayectoria Extendida C3_recto)] 
         │
         ▼
[Etapa 6: Cierre de Ciclo y Reseteo Geométrico]
```

### Etapa 1: Tramo Recto Descendente ($C1$)
* **Descripción:** El conjunto principal, lastrado con las masas activas, desciende verticalmente a lo largo del segmento inicial de longitud $h_1 = 1000\text{ m}$.
* **Ecuación de aporte:** 
  $$E_{C1} = m_{\text{lastre}} \cdot g \cdot h_1$$

### Etapa 2: Transición de Giro e Inversión ($C2$)
* **Descripción:** Al final del primer tramo, el mecanismo experimenta una inversión de orientación geométrica para encarar el cambio de fase.
* **Ecuación de coste:** 
  $$W_{\text{motor\_C2}} = M_{\text{obj}} \cdot g \cdot \theta_{\text{giro}}$$

### Etapa 3: Recuperación Inercial y Frenado Regenerativo ($C2.5$)
* **Descripción:** El sistema desacelera de forma controlada recuperando momento angular.
* **Ecuación de recuperación:** 
  $$E_{\text{regen}} = \eta_{\text{mec}} \cdot \frac{1}{2} I \omega^2$$

### Etapa 4: Conmutación de Densidad — El Gatillo de los Pernos ($Lift\ C3$)
* **Descripción:** Los pernos internos se desplazan, alterando el volumen de desplazamiento efectivo ($\Delta V$) y desestabilizando el gradiente hidrostático local sin requerir un trabajo interno masivo ($W_{\text{int}} \approx 0$).

### Etapa 5: Ascenso Asistido por Gradiente y Corrección Cinemática de Trayectoria ($C3\_recto$)
* **Descripción:** Tras el cambio de sentido operativo, el objeto móvil ejecuta la fase de ascenso y compensación. Cinemáticamente, para asegurar el correcto reajuste de fase y la restitución del potencial frente al anclaje estructural, **el objeto debe cambiar de sentido y recorrer una distancia superior a la de la bajada ($h_{\text{ascenso}} > h_1$, típicamente $h_{\text{ascenso}} = h_1 + \Delta h_{\text{recorrido}}$)**.
* **Dinámica y Ecuación corregida:** 
  El trabajo de ascenso útil extraído o compensado incorpora la trayectoria extendida de inversión:
  $$E_{C3} = m_{\text{lastre}} \cdot g \cdot (h_1 + \Delta h_{\text{recorrido}})$$

### Etapa 6: Sincronización y Cierre de Ciclo
* **Descripción:** Se alcanza el punto de origen del kilómetro y los pernos retornan a su posición inicial, cerrando el lazo del volumen de control abierto.

---

## 3. Extracción de Trabajo del Gradiente Marítimo Modificado

El trabajo neto extraído no proviene de violar la conservación de la energía en un campo conservativo cerrado, sino de la **modulación local y alteración transitoria del nivel del mar ($h_{\text{mar}}$)** y de la presión hidrostática durante la conmutación de fase. 

Aplicando la primera ley para volúmenes de control abiertos:

$$\frac{dE_{\text{sistema}}}{dt} = \dot{Q} - \dot{W}_{\text{eje}} + \sum_{\text{in}} \dot{m} \left(h + \frac{v^2}{2} + gz\right) - \sum_{\text{out}} \dot{m} \left(h + \frac{v^2}{2} + gz\right) + \int_{\text{control}} P \, dV_{\text{efectivo}}$$

El término de expansión inducido por el perneo frente al gradiente marino canaliza la energía liberada hacia el **eje rotativo central**, validando el modelo físico bajo un estricto rigor termodinámico.
