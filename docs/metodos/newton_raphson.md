# Newton-Raphson

## Descripción
Método iterativo de segundo orden para encontrar raíces de funciones. Usa la derivada para converger cuadráticamente cerca de la raíz.

## Fórmula
x_{k+1} = x_k - f(x_k) / f'(x_k)

## Parámetros
- `func_str`: str — expresión sympy de f(x) (ej. "x**3 - x - 2")
- `x0`: float — aproximación inicial
- `tol`: float — tolerancia error relativo % (default 1e-5)
- `max_iter`: int — máximo de iteraciones (default 150)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": float | None,
    "steps": list[dict],  # historial de iteraciones
    "message": str,
    "error_message": str | None
}
```

## Ejemplo
```python
solver = NewtonRoots("cos(x) - x", 0.5)
result = solver.solve()  # solution ≈ 0.739085
```

## Limitaciones
- Requiere derivada analítica (sympy)
- Fallo si f'(x_k) = 0 (división por cero)
- Puede divergir si x₀ está lejos de la raíz
- No maneja raíces múltiples (convergencia lineal)
