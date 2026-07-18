# EJECUTAR desde la raíz: python -m lib.newton_raphson_test

from lib.newton_raphson import NewtonRoots


def run_case(func_str, x0, label):
    print("=" * 70)
    print(f"Prueba Newton-Raphson: {label}")
    print(f"f(x) = {func_str}")
    print(f"x0 = {x0}")

    solver = NewtonRoots(func_str, x0, tol=1e-8, max_iter=100)
    result = solver.solve()

    if not result["success"]:
        print(f"ERROR: {result['error_message']}")
        raise AssertionError(f"Newton-Raphson falló en {label}")

    print(f"Resultado: {result['solution']:.10f}")
    print(f"Mensaje: {result['message']}")
    return result


def test_newton():
    cases = [
        ("e^(x)+2^(-x)+2*cos(x)-6", 1.5, "Ejercicio 1"),
        ("ln(x-1)+cos(x-1)", 1.5, "Ejercicio 2"),
        ("2*x*cos(2*x)-cos(x-1)^2", 2.5, "Ejercicio 3 (intervalo [2,3])"),
        ("(x-2)^2-ln(x)", 1.5, "Ejercicio 4 (intervalo [1,2])"),
    ]

    for func_str, x0, label in cases:
        run_case(func_str, x0, label)

    print("\nTodas las pruebas de Newton-Raphson completaron correctamente.")


if __name__ == "__main__":
    test_newton()