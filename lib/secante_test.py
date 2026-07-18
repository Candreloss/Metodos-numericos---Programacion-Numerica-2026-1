# EJECUTAR desde la raíz: python -m lib.secante_test

from lib.secante import SecantRoots


def run_case(func_str, x0, x1, label):
    print("=" * 70)
    print(f"Prueba Secante: {label}")
    print(f"f(x) = {func_str}")
    print(f"x0 = {x0}, x1 = {x1}")

    solver = SecantRoots(func_str, x0, x1, tol=1e-8, max_iter=100)
    result = solver.solve()

    if not result["success"]:
        print(f"ERROR: {result['error_message']}")
        raise AssertionError(f"Secante falló en {label}")

    print(f"Resultado: {result['solution']:.10f}")
    print(f"Mensaje: {result['message']}")
    return result


def test_secant():
    cases = [
        ("e^(x)+2^(-x)+2*cos(x)-6", 1.0, 2.0, "Ejercicio 1"),
        ("ln(x-1)+cos(x-1)", 1.3, 2.0, "Ejercicio 2"),
        ("2*x*cos(2*x)-cos(x-1)^2", 2.0, 3.0, "Ejercicio 3 (intervalo [2,3])"),
        ("(x-2)^2-ln(x)", 1.0, 2.0, "Ejercicio 4 (intervalo [1,2])"),
    ]

    for func_str, x0, x1, label in cases:
        run_case(func_str, x0, x1, label)

    print("\nTodas las pruebas de Secante completaron correctamente.")


if __name__ == "__main__":
    test_secant()