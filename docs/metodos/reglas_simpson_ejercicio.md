# Reglas de Simpson — Resolución del Ejercicio 21.13

Guía paso a paso para resolver el ejercicio 21.13 de Chapra usando el programa.

## Datos del ejercicio

Función: `f(x) = 2·e^(−1.5x)`, integral de `a = 0` a `b = 0.6`.

| x    | 0     | 0.05   | 0.15   | 0.25   | 0.35   | 0.475  | 0.6    |
|------|-------|--------|--------|--------|--------|--------|--------|
| f(x) | 2.0   | 1.8555 | 1.5970 | 1.3746 | 1.1831 | 0.9808 | 0.8131 |

## Paso 1 — Abrir el programa

```bash
.venv/bin/python main.py
```

## Paso 2 — Seleccionar el método

En la barra lateral izquierda, hacer clic en **"📐 Reglas de Simpson"**.

## Paso 3 — Cargar el preset

1. En el panel izquierdo, abrir el combo **"Ejemplo:"**.
2. Seleccionar **"Ejercicio 21.13"**.
3. Los campos se llenan automáticamente:
   - `x`: `0, 0.05, 0.15, 0.25, 0.35, 0.475, 0.6`
   - `f(x)`: `2, 1.8555, 1.5970, 1.3746, 1.1831, 0.9808, 0.8131`
   - `f(x) opcional`: `2*exp(-1.5*x)`
   - Método: `Auto`

## Paso 4 — Calcular

Presionar **"Calcular y Graficar"**. El programa aplica el algoritmo SimpInt:
como los datos tienen espaciado desigual, agrupa segmentos contiguos con `h`
compatible y aplica Simpson 1/3, Simpson 3/8 o trapecio según corresponda.

## Paso 5 — Interpretar resultados

### Pestaña "Resultado"

- **Método**: Simpson combinado (datos desiguales)
- **I ≈ 0.79128167** — valor aproximado de la integral
- **Integral exacta = 0.79124045** — calculada con sympy
- **Error relativo ≈ 0.0052%** — excelente precisión

### Pestaña "Paso a Paso"

Muestra cada aplicación de regla:

```
Simpson 1/3 en segmentos [0..2] (x=0..0.15) → área = ...
Simpson 1/3 en segmentos [2..4] (x=0.15..0.35) → área = ...
Trapecio en segmentos [4..5] (x=0.35..0.475) → área = ...
Trapecio en segmentos [5..6] (x=0.475..0.6) → área = ...
```

### Pestaña "Gráfica"

Visualización de los nodos, la curva original `f(x) = 2e^(−1.5x)` y los
segmentos sombreados que se usaron para la integración.

## Paso 6 — Comparar con la solución analítica

La integral analítica exacta:

```
∫₀^0.6 2·e^(−1.5x) dx = 2·[−1/1.5 · e^(−1.5x)]₀^0.6
                     = 2/1.5 · (1 − e^(−0.9))
                     = 0.79124045...
```

| Método | Valor aproximado | E_t |
|--------|-----------------|-----|
| Trapecio (todos los segmentos) | 0.79288 | 0.21% |
| **Simpson combinado** | **0.79128** | **0.0052%** |

El método combinado Simpson-trapecio es ~40 veces más preciso que usar
solo trapecio para estos datos espaciados en forma desigual.

## Notas

- Para nodos uniformemente espaciados, el programa usa el algoritmo SimpInt
  de Chapra directamente (Simpson 3/8 para los últimos 3 segmentos si n es
  impar, Simpson 1/3 múltiple para el resto).
- Para nodos desiguales, agrupa segmentos contiguos con h compatible y aplica
  la regla de mayor orden disponible.
