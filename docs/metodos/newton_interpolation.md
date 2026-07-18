# Interpolación de Newton (Diferencias Divididas)

## Descripción
Construye el polinomio interpolante de grado n usando diferencias divididas. Ventaja sobre Lagrange: soporta grado parcial y es más estable para agregar puntos.

## Fórmula
P(x) = f[x_0] + f[x_0,x_1]·(x - x_0) + f[x_0,x_1,x_2]·(x - x_0)(x - x_1) + ...

Donde f[x_0,...,x_k] son las diferencias divididas en la diagonal de la tabla.

## Parámetros
- `x`: list[float] — abscisas
- `y`: list[float] — ordenadas
- `eval_point`: float — punto de evaluación
- `degree`: int | None — grado del polinomio (None = n-1)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": {
        "value": float,
        "symbolic_value": float,
        "polynomial": str,
        "polynomial_expr": sympy.Expr,
        "coefficients": list[float],
        "table": list[list[float]]
    } | None,
    "steps": list[dict],
    "error_message": str | None
}
```

## Ejemplo
```python
solver = NewtonInterpolation([1, 2, 3, 4], [1, 4, 9, 16], 2.5, degree=2)
result = solver.solve()
```

## Limitaciones
- Requiere al menos 2 puntos
- Valores x deben ser distintos
- Grado no puede exceder n-1
