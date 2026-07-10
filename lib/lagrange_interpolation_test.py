"""
Pruebas para la clase LagrangeInterpolation.

Estos tests validan el comportamiento del método de interpolación de Lagrange
implementado en lib/lagrange_interpolation.py. Se cubren:
  - Casos de éxito con polinomios de grado 1, 2 y 3.
  - Verificación de que el polinomio pasa por los puntos conocidos.
  - Cálculo del polinomio expandido y de las bases L_i(x).
  - Casos de error: dimensiones incompatibles, menos de 2 puntos y x duplicados.
  - Verificación de la estructura de los pasos (steps) registrados para la GUI.

Ejecutar desde la raíz del proyecto:
    .venv/bin/python -m lib.lagrange_interpolation_test
"""
import math
from lib.lagrange_interpolation import LagrangeInterpolation


def aprox_igual(a, b, tol=1e-6):
    """
    Compara dos valores float con una tolerancia absoluta.

    Necesario porque el cálculo numérico involucra divisiones y productos
    sucesivos que pueden introducir errores de redondeo pequeños.
    Una comparación estricta (==) sería demasiado frágil para floats.

    Parámetros:
    - a, b: valores a comparar.
    - tol: tolerancia absoluta máxima permitida (1e-6 es suficiente aquí
      porque los valores esperados no son ni enormes ni minúsculos).
    """
    return abs(a - b) < tol


def test_polinomio_lineal_2_puntos():
    """
    Caso base: 2 puntos => polinomio de grado 1 (recta).

    Datos: (1,2) y (3,6). La recta que los une es y = 2x.
    Se evalúa en x=2 y se espera P(2) = 4.
    Verifica tanto la ruta numérica (value) como la simbólica (symbolic_value).
    """
    x = [1.0, 3.0]
    y = [2.0, 6.0]
    # Recta: y = 2x  =>  P(2) = 4
    res = LagrangeInterpolation(x, y, 2.0).solve()
    assert res["success"] is True, f"Se esperaba éxito: {res.get('error_message')}"
    sol = res["solution"]
    assert aprox_igual(sol["value"], 4.0), f"P(2) esperado 4.0, got {sol['value']}"
    assert aprox_igual(sol["symbolic_value"], 4.0)
    print("OK test_polinomio_lineal_2_puntos")


def test_polinomio_cuadratico_3_puntos():
    """
    3 puntos => polinomio de grado 2.

    Datos: (1,1), (2,4), (3,9) que pertenecen a y = x^2.
    Se evalúa en x=2.5 => se espera 6.25.
    Además verifica que el polinomio expandido contenga el término "x**2"
    (ignorando espacios para robustez del string).
    """
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]  # y = x^2
    # P(2.5) esperado = 6.25
    res = LagrangeInterpolation(x, y, 2.5).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["value"], 6.25), f"P(2.5) esperado 6.25, got {sol['value']}"
    assert aprox_igual(sol["symbolic_value"], 6.25)
    # Polinomio expandido debe ser x**2. Se quitan espacios por si sympy
    # lo formatea como "x**2" u otra forma equivalente.
    assert "x**2" in sol["polynomial"].replace(" ", ""), \
        f"Polinomio esperado x**2, got {sol['polynomial']}"
    print("OK test_polinomio_cuadratico_3_puntos")


def test_evaluacion_en_punto_conocido():
    """
    Propiedad clave de la interpolación: evaluar el polinomio en uno de los
    puntos de datos x_i conocidos debe devolver exactamente y_i.

    Esto se cumple por construcción, ya que L_i(x_i)=1 y L_j(x_i)=0 (j≠i),
    por lo tanto P(x_i) = y_i.

    Datos: (0,1), (1,3), (2,7) que siguen y = 2x^2 + 1.
    Se recorren todos los puntos y se verifica P(x_i) = y_i.
    """
    x = [0.0, 1.0, 2.0]
    y = [1.0, 3.0, 7.0]  # y = 2x^2 + 1
    for xi, yi in zip(x, y):
        res = LagrangeInterpolation(x, y, xi).solve()
        assert res["success"] is True, res.get("error_message")
        sol = res["solution"]
        assert aprox_igual(sol["value"], yi), \
            f"P({xi}) esperado {yi}, got {sol['value']}"
        assert aprox_igual(sol["symbolic_value"], yi)
    print("OK test_evaluacion_en_punto_conocido")


def test_polinomio_cubico_4_puntos():
    """
    4 puntos => polinomio de grado 3.

    Datos: (0,1), (1,2), (2,5), (3,10) que pertenecen a y = x^2 + 1.
    Se evalúa en x=1.5 => se espera 3.25. Aunque hay 4 puntos (grado ≤ 3),
    como los datos siguen un polinomio de grado 2, el término cúbico debe
    anularse y el resultado coincide con x^2+1.
    """
    x = [0.0, 1.0, 2.0, 3.0]
    y = [1.0, 2.0, 5.0, 10.0]  # y = x^2 + 1
    # P(1.5) = 1.5^2 + 1 = 3.25
    res = LagrangeInterpolation(x, y, 1.5).solve()
    assert res["success"] is True, res.get("error_message")
    sol = res["solution"]
    assert aprox_igual(sol["value"], 3.25), f"P(1.5) esperado 3.25, got {sol['value']}"
    print("OK test_polinomio_cubico_4_puntos")


def test_error_dimensiones_incompatibles():
    """
    Caso de error: x e y con longitudes distintas.

    No se puede formar un conjunto coherente de puntos (x,y), así que la
    clase debe retornar success=False y un mensaje que mencione "incompatibles".
    """
    res = LagrangeInterpolation([1.0, 2.0], [3.0], 1.5).solve()
    assert res["success"] is False
    assert "incompatibles" in res["error_message"].lower()
    print("OK test_error_dimensiones_incompatibles")


def test_error_un_solo_punto():
    """
    Caso de error: menos de 2 puntos.

    Con un solo punto no se puede construir un polinomio interpolante
    (grado mínimo 1 = recta con 2 puntos). El mensaje debe mencionar "al menos 2".
    """
    res = LagrangeInterpolation([1.0], [2.0], 1.5).solve()
    assert res["success"] is False
    assert "al menos 2" in res["error_message"].lower()
    print("OK test_error_un_solo_punto")


def test_error_x_duplicados():
    """
    Caso de error: valores de x duplicados.

    Si x tiene un valor repetido, el denominador (x_i - x_j) sería cero y se
    generaría una división indeterminada. La clase debe detectar esto y
    retornar success=False mencionando "distintos" o "duplicado".
    """
    x = [1.0, 1.0, 3.0]
    y = [2.0, 5.0, 6.0]
    res = LagrangeInterpolation(x, y, 2.0).solve()
    assert res["success"] is False
    assert "distintos" in res["error_message"].lower() or "duplicado" in res["error_message"].lower()
    print("OK test_error_x_duplicados")


def test_pasos_generados():
    """
    Verifica que la lista de steps generada contenga todos los tipos esperados
    y la cantidad correcta de cada uno.

    Tipos esperados: initial, basis_start, term, basis_end, sum, polynomial.
    Además, para n puntos de datos debe haber exactamente n entradas de tipo
    "basis_start" (una por cada base L_i calculada).
    """
    x = [1.0, 2.0, 3.0]
    y = [1.0, 4.0, 9.0]
    res = LagrangeInterpolation(x, y, 2.5).solve()
    assert res["success"] is True
    # Conjunto de los tipos presentes en los pasos.
    tipos = {p["type"] for p in res["steps"]}
    esperados = {"initial", "basis_start", "term", "basis_end", "sum", "polynomial"}
    # Todos los tipos esperados deben aparecer al menos una vez.
    assert esperados.issubset(tipos), f"Faltan tipos: {esperados - tipos}"
    # n puntos => n basis_start, n basis_end
    n_basis_start = sum(1 for p in res["steps"] if p["type"] == "basis_start")
    assert n_basis_start == len(x)
    print("OK test_pasos_generados")


def test_base_lagrange():
    """
    Verifica las propiedades definitorias de las bases de Lagrange.

    Para cada base L_i(x):
      - L_i(x_i) debe valer 1 (delta de Kronecker).
      - L_i(x_j) debe valer 0 para todo j ≠ i.

    Estas propiedades son las que garantizan que P(x_i) = y_i, es decir,
    que el polinomio pasa exactamente por todos los puntos de datos.
    """
    import sympy
    x = [0.0, 1.0, 2.0]
    y = [1.0, 3.0, 7.0]
    res = LagrangeInterpolation(x, y, 1.0).solve()
    sol = res["solution"]
    # Debe haber una base por cada punto de datos.
    assert len(sol["basis"]) == 3
    x_sym = sympy.Symbol('x')
    # Cada L_i evaluada en x_i debe ser 1
    for i, L_i in enumerate(sol["basis"]):
        val = float(L_i.subs(x_sym, x[i]))
        assert aprox_igual(val, 1.0), f"L_{i}(x_{i}) debe ser 1, got {val}"
    # Cada L_i evaluada en x_j (i!=j) debe ser 0
    for i, L_i in enumerate(sol["basis"]):
        for j, xj in enumerate(x):
            if i != j:
                val = float(L_i.subs(x_sym, xj))
                assert aprox_igual(val, 0.0), f"L_{i}(x_{j}) debe ser 0, got {val}"
    print("OK test_base_lagrange")


def test_ejemplo_chapra():
    """
    Ejemplo basado en el libro de Chapra (Métodos Numéricos para Ingenieros).

    Datos: (1,1.5), (2,2.5), (3,3.5), (4,4.5) que siguen y = x + 0.5.
    Se evalúa en x=2.5 => se espera P(2.5) = 3.0.

    Aunque hay 4 puntos (grado ≤ 3), como los datos siguen una recta, el
    polinomio resultante degenera a grado 1 y coincide con x + 0.5.
    """
    # Chapra ejemplo 13.1 / similar
    x = [1.0, 2.0, 3.0, 4.0]
    y = [1.5, 2.5, 3.5, 4.5]  # y = x + 0.5
    res = LagrangeInterpolation(x, y, 2.5).solve()
    assert res["success"] is True
    sol = res["solution"]
    assert aprox_igual(sol["value"], 3.0), f"P(2.5) esperado 3.0, got {sol['value']}"
    print("OK test_ejemplo_chapra")


if __name__ == "__main__":
    # Ejecución secuencial de todos los tests. No se usa un framework de
    # tests porque el proyecto no incluye pytest/unittest en requirements.
    # Si un assert falla, Python lanza AssertionError y se detiene aquí.
    test_polinomio_lineal_2_puntos()
    test_polinomio_cuadratico_3_puntos()
    test_evaluacion_en_punto_conocido()
    test_polinomio_cubico_4_puntos()
    test_error_dimensiones_incompatibles()
    test_error_un_solo_punto()
    test_error_x_duplicados()
    test_pasos_generados()
    test_base_lagrange()
    test_ejemplo_chapra()
    print("\nTodos los tests pasaron.")