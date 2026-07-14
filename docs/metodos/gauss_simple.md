# Gauss Simple (Eliminación Gaussiana)

## Descripción
Resuelve sistemas de ecuaciones lineales Ax = b mediante eliminación hacia adelante y sustitución hacia atrás. Soporta pivoteo parcial opcional.

## Algoritmo
1. Construir matriz aumentada [A | b]
2. Para cada columna k (0 a n-2):
   - Opcional: pivoteo parcial (intercambiar fila k con la de mayor |A[i][k]|)
   - Para cada fila i > k: calcular factor = A[i][k] / A[k][k], restar factor × fila k
3. Sustitución hacia atrás desde x[n-1] hasta x[0]

## Parámetros
- `A`: list[list[float]] — matriz n×n de coeficientes
- `b`: list[float] — vector de términos independientes (longitud n)
- `pivoting`: bool — True para pivoteo parcial (default True)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": list[float] | None,
    "steps": list[dict],
    "error_message": str | None
}
```

## Ejemplo
```python
solver = GaussSimple([[2, 1], [1, 3]], [5, 6], pivoting=True)
result = solver.solve()  # solution = [1.8, 1.4]
```

## Limitaciones
- Sin pivoteo falla si hay elemento diagonal cero
- Sensible a matrices mal condicionadas
