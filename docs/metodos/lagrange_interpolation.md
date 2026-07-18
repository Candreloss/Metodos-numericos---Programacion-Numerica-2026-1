# Interpolación de Lagrange

## Descripción
Construye el polinomio único de grado n que pasa por n+1 puntos (x_i, y_i). Evalúa P(x) en un punto dado y retorna la expresión simbólica expandida.

## Fórmula
P(x) = Σ_{i=0}^{n} y_i · L_i(x)

L_i(x) = Π_{j≠i} (x - x_j) / (x_i - x_j)

Propiedad: L_i(x_i) = 1, L_i(x_j) = 0 para i ≠ j

## Parámetros
- `x`: list[float] — abscisas de los puntos conocidos
- `y`: list[float] — ordenadas de los puntos conocidos
- `eval_point`: float — punto donde evaluar P(x)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": {
        "value": float,          # evaluación numérica
        "symbolic_value": float,  # evaluación desde expresión simbólica
        "polynomial": str,       # polinomio expandido
        "polynomial_expr": sympy.Expr,
        "basis": list[sympy.Expr]
    } | None,
    "steps": list[dict],
    "error_message": str | None
}
```

## Ejemplo
```python
solver = LagrangeInterpolation([1, 2, 3], [1, 4, 9], 2.5)
result = solver.solve()  # value ≈ 6.25
```

## Limitaciones
- Requiere al menos 2 puntos
- Valores x deben ser distintos
- Grado alto puede oscilar (fenómeno de Runge)
