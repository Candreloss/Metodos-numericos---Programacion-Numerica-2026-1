# Regla del Trapecio

## Descripción
Integración numérica de datos tabulares. Aproxima el área bajo la curva mediante trapecios. Soporta caso simple (1 segmento) y compuesto (n segmentos). Los nodos deben estar uniformemente espaciados.

## Fórmula
Segmento simple (n=1): I = h·(f₀ + f₁) / 2

Compuesta (n>1): I = h·(f₀ + 2·Σ_{i=1}^{n-1} f_i + f_n) / 2

## Parámetros
- `x`: list[float] — nodos (estrictamente crecientes, espaciado uniforme)
- `y`: list[float] — valores f(x_i) en cada nodo
- `f_expr`: str | None — expresión sympy de f(x) para comparación analítica (opcional)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": {
        "value": float,
        "h": float,
        "n": int,
        "exact_value": float | None,
        "error_relativo": float | None,
        "segments": list[dict],
        "formula": str
    } | None,
    "steps": list[dict],
    "error_message": str | None
}
```

## Ejemplo
```python
solver = TrapezoidalRule([0, 1, 2], [1, 2, 4])
result = solver.solve()  # value = 4.0
```

## Limitaciones
- Requiere nodos uniformemente espaciados
- Al menos 2 puntos
- Exactitud limitada (error O(h²)); usar Simpson para mayor precisión
