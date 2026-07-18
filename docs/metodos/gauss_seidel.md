# Gauss-Seidel

## Descripción
Método iterativo para resolver sistemas de ecuaciones lineales. Utiliza los valores más recientes de cada incógnita dentro de la misma iteración. Soporta factor de relajación.

## Algoritmo
1. Partir de aproximación inicial x⁽⁰⁾
2. Para cada iteración k:
   - Para cada i: x_i⁽ᵏ⁾ = (b_i - Σ_{j<i} a_ij·x_j⁽ᵏ⁾ - Σ_{j>i} a_ij·x_j⁽ᵏ⁻¹⁾) / a_ii
   - Aplicar relajación: x_i⁽ᵏ⁾ = λ·x_i⁽ᵏ⁾ + (1-λ)·x_i⁽ᵏ⁻¹⁾
   - Calcular error relativo máximo
3. Detener si error ≤ tol o se alcanza max_iter

## Parámetros
- `A`: list[list] — matriz n×n de coeficientes
- `b`: list — vector de términos independientes (n)
- `x0`: list | None — aproximación inicial (None = ceros)
- `tol`: float — tolerancia error relativo % (default 1e-5)
- `max_iter`: int — límite de iteraciones (default 150)
- `relax`: float — factor de relajación (default 1.0)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": list | None,
    "steps": list[dict],
    "error_message": str | None,
    "diag_dominant": bool,
    "dominant_details": list[dict],
    "message": str
}
```

## Ejemplo
```python
solver = GaussSeidel([[4, -1], [-1, 4]], [1, 2], tol=0.01)
result = solver.solve()
```

## Limitaciones
- Convergencia garantizada solo si A es diagonalmente dominante
- Puede divergir si la matriz no cumple condición suficiente
- Elementos diagonales nulos causan fallo
