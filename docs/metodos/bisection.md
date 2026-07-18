# Método de Bisección

## Descripción
Método robusto de búsqueda de raíces. Divide repetidamente un intervalo [xl, xu] por la mitad, seleccionando el subintervalo donde f(x) cambia de signo.

## Algoritmo
1. Verificar f(xl)·f(xu) < 0 (cambio de signo)
2. xr = (xl + xu) / 2
3. Evaluar test = f(xl)·f(xr)
   - test < 0: raíz en [xl, xr] → xu = xr
   - test > 0: raíz en [xr, xu] → xl = xr
   - test = 0: raíz exacta encontrada
4. Calcular error relativo: ea = |(xr - xrold)/xr|·100%
5. Repetir hasta ea < es o iter ≥ imax

## Parámetros
- `f_expr`: str — expresión sympy de f(x) (ej. "x**2 - 2")
- `xl`: float — extremo inferior del intervalo
- `xu`: float — extremo superior del intervalo (xl < xu)
- `es`: float — tolerancia error relativo % (default 0.01)
- `imax`: int — máximo de iteraciones (default 100)

## Retorno (solve)
```python
{
    "success": bool,
    "solution": {
        "root": float,
        "iterations": int,
        "error": float,
        "converged": bool,
        "f_value": float,
        "xl_final": float,
        "xu_final": float
    } | None,
    "steps": list[dict],
    "error_message": str | None
}
```

## Ejemplo
```python
solver = BisectionMethod("x**3 - x - 2", 0.5, 2.0, es=0.01)
result = solver.solve()  # root ≈ 1.521
```

## Limitaciones
- Requiere cambio de signo en el intervalo
- Convergencia lineal (lenta comparada con Newton/Secante)
- No detecta raíces pares (tangentes al eje x)
