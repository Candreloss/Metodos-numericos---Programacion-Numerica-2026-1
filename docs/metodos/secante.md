# Método de la Secante

## Descripción
Método iterativo para encontrar raíces de funciones. Similar a Newton-Raphson pero aproxima la derivada numéricamente, evitando el cálculo de f'(x).

## Fórmula
x_{k+1} = x_k - f(x_k)·(x_k - x_{k-1}) / (f(x_k) - f(x_{k-1}))

Requiere dos puntos iniciales x₀ y x₁.

## Parámetros
- `func_str`: str — expresión sympy de f(x) (ej. "x**2 - 4")
- `x0`: float — primera aproximación inicial
- `x1`: float — segunda aproximación inicial
- `tol`: float — tolerancia error relativo % (default 1e-5)
- `max_iter`: int — máximo de iteraciones (default 150)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": float | None,
    "steps": list[dict],
    "message": str,
    "error_message": str | None
}
```

## Ejemplo
```python
solver = SecantRoots("x**3 - x - 2", 0.5, 1.5)
result = solver.solve()  # solution ≈ 1.521379
```

## Limitaciones
- Fallo si f(x_k) - f(x_{k-1}) = 0 (división por cero)
- Convergencia superlineal (orden φ ≈ 1.618), no cuadrática como Newton
- Sensible a mala elección de x₀ y x₁
