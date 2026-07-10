"""
Pruebas para NewtonInterpolation (diferencias divididas).
Ejecutar desde la raíz:
    .venv/bin/python -m lib.newton_interpolation_test
"""
from lib.newton_interpolation import NewtonInterpolation


def aprox_igual(a, b, tol=1e-6):
    return abs(a - b) < tol


def test_lineal_2_puntos():
    x = [1.0, 3.0]
    y = [2.0, 6.0]
    res = NewtonInterpolation(x, y, 2.0).solve()
    assert res["success"] is True, res.get("error_message")
    assert aprox_igual(res["solution"]["value"], 4.0)
    assert aprox_igual(res["solution"]["symbolic_value"], 4.0)
    print("OK test_lineal_2_puntos")


def test_cuadratico_3_puntos():
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    res = NewtonInterpolation(x, y, 2.5).solve()
    assert res["success"] is True
    assert aprox_igual(res["solution"]["value"], 6.25)
    assert "x**2" in res["solution"]["polynomial"].replace(" ", "")
    print("OK test_cuadratico_3_puntos")


def test_evaluacion_punto_conocido():
    x = [0.0, 1.0, 2.0]
    y = [1.0, 3.0, 7.0]
    for xi, yi in zip(x, y):
        res = NewtonInterpolation(x, y, xi).solve()
        assert aprox_igual(res["solution"]["value"], yi), f"P({xi})={res['solution']['value']} != {yi}"
    print("OK test_evaluacion_punto_conocido")


def test_con_grado():
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.5, 2.5, 3.5, 4.5]
    res = NewtonInterpolation(x, y, 2.5, degree=1).solve()
    assert res["success"] is True
    assert aprox_igual(res["solution"]["value"], 3.0)
    print("OK test_con_grado")


def test_coincide_con_lagrange():
    from lib.lagrange_interpolation import LagrangeInterpolation
    x = [0.0, 1.0, 2.0, 3.0]
    y = [1.0, 2.0, 5.0, 10.0]
    for eval_p in [0.5, 1.5, 2.5]:
        r1 = LagrangeInterpolation(x, y, eval_p).solve()
        r2 = NewtonInterpolation(x, y, eval_p).solve()
        assert r1["success"] and r2["success"]
        assert aprox_igual(r1["solution"]["value"], r2["solution"]["value"]), \
            f"Divergen en x={eval_p}: L={r1['solution']['value']}, N={r2['solution']['value']}"
    print("OK test_coincide_con_lagrange")


def test_error_dimensiones():
    res = NewtonInterpolation([1.0, 2.0], [3.0], 1.5).solve()
    assert not res["success"]
    assert "incompatibles" in res["error_message"].lower()
    print("OK test_error_dimensiones")


def test_error_min_2_puntos():
    res = NewtonInterpolation([1.0], [2.0], 1.5).solve()
    assert not res["success"]
    assert "al menos 2" in res["error_message"].lower()
    print("OK test_error_min_2_puntos")


def test_error_x_duplicados():
    res = NewtonInterpolation([1.0, 1.0, 3.0], [2.0, 5.0, 6.0], 2.0).solve()
    assert not res["success"]
    assert "duplicado" in res["error_message"].lower() or "distintos" in res["error_message"].lower()
    print("OK test_error_x_duplicados")


def test_pasos_generados():
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    res = NewtonInterpolation(x, y, 2.5).solve()
    assert res["success"]
    tipos = {p["type"] for p in res["steps"]}
    esperados = {"initial", "table_col", "coefficients", "evaluation", "polynomial"}
    assert esperados.issubset(tipos), f"Faltan: {esperados - tipos}"
    assert len(res["solution"]["coefficients"]) == len(x)
    assert len(res["solution"]["table"]) == len(x)
    print("OK test_pasos_generados")


def test_tabla_diferencias():
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    res = NewtonInterpolation(x, y, 2.5).solve()
    tabla = res["solution"]["table"]
    assert aprox_igual(tabla[0][0], 1.0)
    assert aprox_igual(tabla[1][0], 4.0)
    assert aprox_igual(tabla[2][0], 9.0)
    assert aprox_igual(tabla[1][1], 3.0)
    assert aprox_igual(tabla[2][1], 5.0)
    assert aprox_igual(tabla[2][2], 1.0)
    print("OK test_tabla_diferencias")


if __name__ == "__main__":
    test_lineal_2_puntos()
    test_cuadratico_3_puntos()
    test_evaluacion_punto_conocido()
    test_con_grado()
    test_coincide_con_lagrange()
    test_error_dimensiones()
    test_error_min_2_puntos()
    test_error_x_duplicados()
    test_pasos_generados()
    test_tabla_diferencias()
    print("\nTodos los tests pasaron.")
