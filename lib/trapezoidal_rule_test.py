"""
Pruebas para la clase TrapezoidalRule.

Estos tests validan el comportamiento de la regla del trapecio
(simple y compuesta) implementada en lib/trapezoidal_rule.py. Se cubren:
  - Casos de éxito con n=1 (simple) y n>1 (compuesta).
  - Verificación de exactitud para funciones lineales (propiedad
    conocida: la regla del trapecio es exacta para polinomios de grado
    menor o igual a 1).
  - Aproximación de funciones no lineales (x^2, sin(x)) con error
    controlado.
  - Casos de error: dimensiones incompatibles, menos de 2 puntos, x no
    creciente y nodos no uniformemente espaciados.
  - Verificación de la estructura de los pasos (steps) registrados para
    la GUI.
  - Comparación opcional con la integral exacta vía sympy.

Ejecutar desde la raíz del proyecto:
    .venv/bin/python -m lib.trapezoidal_rule_test
"""
import math
from lib.trapezoidal_rule import TrapezoidalRule


def aprox_igual(a, b, tol=1e-6):
    """
    Compara dos valores float con una tolerancia absoluta.

    Necesario porque el cálculo numérico involucra sumas y productos
    sucesivos que pueden introducir errores de redondeo pequeños.
    Una comparación estricta (==) sería demasiado frágil para floats.

    Parámetros:
    - a, b: valores a comparar.
    - tol: tolerancia absoluta máxima permitida (1e-6 por defecto).
    """
    return abs(a - b) < tol


def test_un_segmento_lineal():
    """
    Caso base: 2 puntos (n=1) sobre una función lineal f(x) = 2x.

    Datos: (0, 0), (2, 4). La integral exacta de 2x en [0, 2] es 4.
    La regla del trapecio con n=1 debe devolver exactamente 4 (es
    exacta para polinomios de grado <= 1).
    """
    x = [0.0, 2.0]
    y = [0.0, 4.0]  # f(x) = 2x
    res = TrapezoidalRule(x, y).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["value"], 4.0), f"Esperado 4.0, got {sol['value']}"
    assert sol["n"] == 1
    print("OK test_un_segmento_lineal")


def test_un_segmento_constante():
    """
    Caso: 2 puntos (n=1) sobre una función constante f(x) = 5.

    Datos: (1, 5), (3, 5). La integral exacta de 5 en [1, 3] es 10.
    Confirma que la fórmula simple funciona con constantes.
    """
    x = [1.0, 3.0]
    y = [5.0, 5.0]
    res = TrapezoidalRule(x, y).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["value"], 10.0), f"Esperado 10.0, got {sol['value']}"
    print("OK test_un_segmento_constante")


def test_compuesto_parabola():
    """
    Caso compuesto: 5 puntos (n=4) sobre f(x) = x^2.

    Datos: x = [0, 0.5, 1, 1.5, 2], y = x^2.
    La integral exacta de x^2 en [0, 2] es 8/3 ≈ 2.6667.
    La regla del trapecio con n=4 produce I = h/2*(f0 + 2*f1 + 2*f2 +
    2*f3 + f4) = 0.25*(0 + 0.5 + 2 + 4.5 + 4) = 2.75. El error
    relativo es |2.75 - 2.6667|/2.6667 ≈ 3.1%. Se verifica con una
    tolerancia absoluta de 0.1.
    """
    x = [0.0, 0.5, 1.0, 1.5, 2.0]
    y = [xi * xi for xi in x]
    res = TrapezoidalRule(x, y).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    # El valor aproximado de la regla del trapecio es 2.75 (no la
    # integral exacta 8/3). Se verifica que la aproximación sea la
    # esperada para la fórmula del trapecio.
    assert abs(sol["value"] - 2.75) < 1e-6, \
        f"Aproximación trapezoidal esperada 2.75, got {sol['value']}"
    # Sanity: la aproximación debe estar cerca de la integral exacta.
    assert abs(sol["value"] - 8.0 / 3.0) < 0.1
    assert sol["n"] == 4
    print("OK test_compuesto_parabola")


def test_compuesto_seno():
    """
    Caso compuesto: 5 puntos (n=4) sobre f(x) = sin(x) en [0, π].

    La integral exacta de sin(x) en [0, π] es 2.
    Con n=4 y h = π/4 ≈ 0.785, la regla del trapecio produce I ≈ 1.896
    con un error relativo de aproximadamente 5.2%. Se verifica con
    tolerancia 0.15.
    """
    n = 4
    x = [i * math.pi / n for i in range(n + 1)]
    y = [math.sin(xi) for xi in x]
    res = TrapezoidalRule(x, y).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert abs(sol["value"] - 2.0) < 0.15, \
        f"Esperado ≈ 2.0, got {sol['value']}"
    print("OK test_compuesto_seno")


def test_exacto_funcion_lineal():
    """
    Propiedad de la regla del trapecio: es exacta para polinomios de
    grado <= 1. Se verifica con f(x) = 2x, n=1: integral exacta en
    [0, 2] = 4 y la regla del trapecio devuelve exactamente 4.
    """
    x = [0.0, 2.0]
    y = [0.0, 4.0]  # f(x) = 2x
    res = TrapezoidalRule(x, y, f_expr="2*x").solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["value"], 4.0)
    # También debe poder calcular la integral exacta vía sympy.
    assert sol["exact_value"] is not None
    assert aprox_igual(sol["exact_value"], 4.0)
    # Para una función lineal el error debe ser cero (o casi).
    assert sol["error_relativo"] < 1e-6
    print("OK test_exacto_funcion_lineal")


def test_error_len_distintas():
    """
    Caso de error: x e y con longitudes distintas.
    La clase debe retornar success=False y un mensaje que mencione
    "incompatibles".
    """
    res = TrapezoidalRule([0.0, 1.0, 2.0], [0.0, 1.0]).solve()
    assert res["success"] is False
    assert "incompatibles" in res["error_message"].lower()
    print("OK test_error_len_distintas")


def test_error_un_solo_punto():
    """
    Caso de error: menos de 2 puntos (solo 1).
    No se puede formar ni un solo segmento. El mensaje debe mencionar
    "al menos 2".
    """
    res = TrapezoidalRule([1.0], [2.0]).solve()
    assert res["success"] is False
    assert "al menos 2" in res["error_message"].lower()
    print("OK test_error_un_solo_punto")


def test_error_x_no_creciente():
    """
    Caso de error: x no estrictamente creciente.
    Se pasa x = [2, 1] (decreciente). El mensaje debe mencionar
    "creciente".
    """
    res = TrapezoidalRule([2.0, 1.0], [4.0, 1.0]).solve()
    assert res["success"] is False
    assert "creciente" in res["error_message"].lower()
    print("OK test_error_x_no_creciente")


def test_error_no_uniforme():
    """
    Caso de error: nodos no uniformemente espaciados.
    Se pasa x = [0, 0.5, 1.2, 2.0] con h no constante. El mensaje
    debe mencionar "uniforme".
    """
    res = TrapezoidalRule([0.0, 0.5, 1.2, 2.0], [0.0, 0.25, 1.44, 4.0]).solve()
    assert res["success"] is False
    assert "uniforme" in res["error_message"].lower()
    print("OK test_error_no_uniforme")


def test_pasos_generados():
    """
    Verifica que la lista de steps generada contenga todos los tipos
    esperados y la cantidad correcta de cada uno.

    Tipos esperados: initial, segment, final.
    Para n segmentos debe haber exactamente n entradas de tipo
    "segment".
    """
    x = [0.0, 0.5, 1.0, 1.5, 2.0]
    y = [xi * xi for xi in x]
    res = TrapezoidalRule(x, y).solve()
    assert res["success"] is True
    tipos = {p["type"] for p in res["steps"]}
    esperados = {"initial", "segment", "final"}
    assert esperados.issubset(tipos), f"Faltan tipos: {esperados - tipos}"
    n_segment = sum(1 for p in res["steps"] if p["type"] == "segment")
    assert n_segment == 4, f"Esperaba 4 segmentos, got {n_segment}"
    print("OK test_pasos_generados")


def test_integral_exacta_sympy():
    """
    Verifica que cuando se provee f_expr, se calcule la integral
    exacta vía sympy y el error relativo.

    Datos: f(x) = x^2 en [0, 2]. Integral exacta = 8/3 ≈ 2.6667.
    Con n=4 la regla del trapecio aproxima con un error del orden de
    h^2 ≈ 0.0625, así que el error relativo debe ser positivo y menor
    a 5%.
    """
    x = [0.0, 0.5, 1.0, 1.5, 2.0]
    y = [xi * xi for xi in x]
    res = TrapezoidalRule(x, y, f_expr="x**2").solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert sol["exact_value"] is not None
    assert aprox_igual(sol["exact_value"], 8.0 / 3.0), \
        f"Esperado 8/3, got {sol['exact_value']}"
    assert sol["error_relativo"] is not None
    assert 0.0 < sol["error_relativo"] < 10.0, \
        f"Error relativo esperado en (0, 10)%, got {sol['error_relativo']}"
    print("OK test_integral_exacta_sympy")


def test_f_expr_invalida():
    """
    Caso: f_expr inválida (no se puede parsear). El cálculo numérico
    no debe fallar; simplemente exact_value y error_relativo son None.
    """
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    res = TrapezoidalRule(x, y, f_expr="foo(bar)").solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert sol["exact_value"] is None
    assert sol["error_relativo"] is None
    print("OK test_f_expr_invalida")


def test_f_expr_none():
    """
    Caso: f_expr=None (no se provee función simbólica). El cálculo
    numérico procede y exact_value/error_relativo son None.

    Datos: x = [0, 1, 2], y = x^2, n=2, h=1.
    Aproximación trapezoidal: I = h/2*(f0 + 2*f1 + f2) = 0.5*(0 + 2 + 4)
    = 3.0.
    """
    x = [0.0, 1.0, 2.0]
    y = [0.0, 1.0, 4.0]
    res = TrapezoidalRule(x, y).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert sol["exact_value"] is None
    assert sol["error_relativo"] is None
    # El valor numérico debe seguir calculándose correctamente.
    assert abs(sol["value"] - 3.0) < 1e-6
    print("OK test_f_expr_none")


if __name__ == "__main__":
    # Ejecución secuencial de todos los tests. No se usa un framework
    # de tests porque el proyecto no incluye pytest/unittest en
    # requirements. Si un assert falla, Python lanza AssertionError y
    # se detiene aquí.
    test_un_segmento_lineal()
    test_un_segmento_constante()
    test_compuesto_parabola()
    test_compuesto_seno()
    test_exacto_funcion_lineal()
    test_error_len_distintas()
    test_error_un_solo_punto()
    test_error_x_no_creciente()
    test_error_no_uniforme()
    test_pasos_generados()
    test_integral_exacta_sympy()
    test_f_expr_invalida()
    test_f_expr_none()
    print("\nTodos los tests pasaron.")