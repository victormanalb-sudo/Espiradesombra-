# Nota al paper de 6 etapas (Download, 19-sep)

El paper pone η>1 así:

```
η = (E_C1 + E_C2.5 + E_C3 + Neto_C3) / (W_motor_C2 + W_pernos)
```

`Neto_C3 = ΔV ρ g h − W_pernos` está en el **numerador** y el fluido no vuelve al denominador. Eso es el modo 2 mal contado.

Scan cerrado (`kilometro_6subciclos.py --scan`): **ningún** (m_obj, m_lastre) da η>1.
Default 15 m: η **0.595**. `--dkp`: **0.691**. H=1000 m y 50 kg: la escala crece **igual** arriba y abajo; η no cruza 1.

Permear ~6 J: de acuerdo. Lift del kg: no es permear.

`W_motor_C2 = M_obj · g · θ` no es julios (faltan metros).
