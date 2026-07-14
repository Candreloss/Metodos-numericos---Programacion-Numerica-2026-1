# EJECUTAR desde la raíz: python -m lib.secante_test

from lib.secante import SecantRoots

def test_secant():
    print("="*60)
    print("   TEST: MÉTODO DE LA SECANTE")
    print("="*60)
    
    # Función de prueba
    func_str = "exp(-x) - x"
    x0 = 0.0
    x1 = 1.0
    tol = 1e-5

    print(f"Función a evaluar : f(x) = {func_str}")
    print(f"Puntos iniciales  : x0 = {x0}, x1 = {x1}")
    print(f"Tolerancia        : {tol}\n")

    # Instanciar y resolver
    solver = SecantRoots(func_str, x0, x1, tol=tol)
    result = solver.solve()

    if not result["success"]:
        print(f"Error en la ejecución: {result['error_message']}")
        return

    # Imprimir tabla de resultados
    print(f"{'Iter':<5} | {'x_i':<12} | {'f(x_i)':<15} | {'Error (%)':<15}")
    print("-" * 55)
    
    for step in result["steps"]:
        iter_num = step["iter"]
        x_val = f"{step['x']:.6f}"
        fx_val = f"{step['fx']:.2e}"
        err_val = f"{step['error']:.6f}" if step["error"] is not None else "---"
        
        print(f"{iter_num:<5} | {x_val:<12} | {fx_val:<15} | {err_val:<15}")

    print("-" * 55)
    print(f"Resultado final: {result['message']}")
    print("="*60)

if __name__ == "__main__":
    test_secant()