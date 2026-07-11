"""
Pruebas para la clase BisectionMethod.

Estos tests validan el comportamiento del método de bisección
implementado en lib/bisection_method.py. Se cubren:
  - Casos de éxito: raíz clásica (x³-x-2), raíz exacta en extremo,
    convergencia por tolerancia, salida por máximo de iteraciones.
  - Casos de error: sin cambio de signo, f_expr no parseable,
    xl >= xu, f_expr vacía.
  - Verificación de la estructura de los pasos (steps) registrados
    para la GUI.
  - Verificación del contenido de cada step de iteración (claves
    iter, xl, xu, xr, xrold, ea, test, action).

Ejecutar desde la raíz del proyecto:
    .venv/bin/python -m lib.bisection_method_test
"""
from lib.bisection_method import BisectionMethod


def aprox_igual(a, b, tol=1e-2):
    """
    Compara dos valores float con una tolerancia absoluta.

    Para bisección la tolerancia por defecto es 1e-2 (1%) porque el
    error relativo de parada típico es 0.01% y la raíz real puede
    diferir del valor teórico en pocas cifras significativas según
    la tolerancia usada.

    Parámetros:
    - a, b: valores a comparar.
    - tol: tolerancia absoluta máxima permitida.
    """
    return abs(a - b) < tol


def test_raiz_cubica_clasica():
    """
    Caso clásico de Chapra: f(x) = x³ - x - 2 en [1, 2].

    La raíz real es aproximadamente 1.5214 (f(1.5214) ≈ 0). Con
    es=0.01% el método debe converger y el valor hallado debe estar
    cerca de 1.5214.
    """
    res = BisectionMethod("x**3 - x - 2", 1.0, 2.0, es=0.01, imax=100).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["root"], 1.5214), f"Esperado ≈ 1.5214, got {sol['root']}"
    assert sol["error"] < 0.01, f"ea debe ser < 0.01%, got {sol['error']}"
    assert sol["converged"] is True
    print("OK test_raiz_cubica_clasica")


def test_raiz_exacta_en_extremo():
    """
    Caso: f(x) = x - 2 con xl = 2 (f(xl) = 0).

    La raíz está exactamente en el extremo xl. El método debe
    retornar éxito inmediato con iter=0 y error=0.
    """
    res = BisectionMethod("x - 2", 2.0, 3.0).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["root"], 2.0, tol=1e-9), f"Esperado 2.0, got {sol['root']}"
    assert sol["iterations"] == 0
    assert sol["error"] == 0.0
    assert sol["converged"] is True
    print("OK test_raiz_exacta_en_extremo")


def test_sin_cambio_de_signo():
    """
    Caso de error: f(x) = x² + 1 en [0, 1] (siempre positiva).

    No hay cambio de signo (f(xl)*f(xu) > 0). El método debe retornar
    success=False y el mensaje debe mencionar "signo".
    """
    res = BisectionMethod("x**2 + 1", 0.0, 1.0).solve()
    assert res["success"] is False
    assert "signo" in res["error_message"].lower()
    print("OK test_sin_cambio_de_signo")


def test_salida_por_max_iter():
    """
    Caso: imax=3 con una función que requiere más iteraciones.

    El método se detiene por máximo de iteraciones. Debe retornar
    success=True (entrega el mejor valor), converged=False, iter=3.
    """
    res = BisectionMethod("x**3 - x - 2", 1.0, 2.0, es=1e-10, imax=3).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert sol["converged"] is False
    assert sol["iterations"] == 3
    print("OK test_salida_por_max_iter")


def test_convergencia_por_tolerancia():
    """
    Verifica que al exigir es=1e-4 la raíz converja con error < 1e-4.
    """
    res = BisectionMethod("x**3 - x - 2", 1.0, 2.0, es=1e-4, imax=100).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert sol["error"] < 1e-4, f"ea debe ser < 1e-4, got {sol['error']}"
    assert sol["converged"] is True
    print("OK test_convergencia_por_tolerancia")


def test_defaults():
    """
    Sin especificar es ni imax, el método usa defaults es=0.01, imax=100
    y converge para una función estándar.
    """
    res = BisectionMethod("x**3 - x - 2", 1.0, 2.0).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert sol["converged"] is True
    assert sol["iterations"] <= 100
    print("OK test_defaults")


def test_error_f_expr_no_parseable():
    """
    Caso de error: f_expr no se puede parsear.
    """
    res = BisectionMethod("foo(bar)", 0.0, 1.0).solve()
    assert res["success"] is False
    assert "evaluar" in res["error_message"].lower() or "sintaxis" in res["error_message"].lower()
    print("OK test_error_f_expr_no_parseable")


def test_error_xl_mayor_xu():
    """
    Caso de error: xl >= xu (intervalo invertido o degenerado).
    """
    res = BisectionMethod("x - 2", 2.0, 1.0).solve()
    assert res["success"] is False
    assert "menor" in res["error_message"].lower()
    print("OK test_error_xl_mayor_xu")


def test_error_f_expr_vacia():
    """
    Caso de error: f_expr vacía o None.
    """
    res1 = BisectionMethod("", 0.0, 1.0).solve()
    assert res1["success"] is False
    assert "función" in res1["error_message"].lower()
    res2 = BisectionMethod(None, 0.0, 1.0).solve()
    assert res2["success"] is False
    print("OK test_error_f_expr_vacia")


def test_pasos_generados():
    """
    Verifica que la lista de steps contenga los tipos esperados
    (initial, iteration, final) y que el número de steps de
    iteration coincida con el número de iteraciones realizadas.
    """
    res = BisectionMethod("x**3 - x - 2", 1.0, 2.0, es=0.01, imax=100).solve()
    assert res["success"] is True
    tipos = {p["type"] for p in res["steps"]}
    esperados = {"initial", "iteration", "final"}
    assert esperados.issubset(tipos), f"Faltan tipos: {esperados - tipos}"
    n_iter_steps = sum(1 for p in res["steps"] if p["type"] == "iteration")
    assert n_iter_steps == res["solution"]["iterations"], \
        f"Esperaba {res['solution']['iterations']} iter steps, got {n_iter_steps}"
    print("OK test_pasos_generados")


def test_contenido_step_iteracion():
    """
    Verifica que cada step de type=="iteration" tenga las claves
    requeridas: iter, xl, xu, xr, xrold, ea, test, action.
    """
    res = BisectionMethod("x**3 - x - 2", 1.0, 2.0, es=0.01, imax=5).solve()
    assert res["success"] is True
    claves_esperadas = {"iter", "xl", "xu", "xr", "xrold", "ea", "test", "action"}
    for p in res["steps"]:
        if p["type"] == "iteration":
            claves = set(p.keys())
            assert claves_esperadas.issubset(claves), \
                f"Step incompleto: faltan {claves_esperadas - claves}"
    print("OK test_contenido_step_iteracion")


if __name__ == "__main__":
    # Ejecución secuencial de todos los tests. No se usa un framework
    # de tests porque el proyecto no incluye pytest/unittest en
    # requirements. Si un assert falla, Python lanza AssertionError y
    # se detiene aquí.
    test_raiz_cubica_clasica()
    test_raiz_exacta_en_extremo()
    test_sin_cambio_de_signo()
    test_salida_por_max_iter()
    test_convergencia_por_tolerancia()
    test_defaults()
    test_error_f_expr_no_parseable()
    test_error_xl_mayor_xu()
    test_error_f_expr_vacia()
    test_pasos_generados()
    test_contenido_step_iteracion()
    print("\nTodos los tests pasaron.")