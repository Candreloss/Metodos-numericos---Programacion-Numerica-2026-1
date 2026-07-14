# -*- coding: utf-8 -*-
"""
Test del método de Gauss-Seidel.
Ejecutar desde la raíz del proyecto con: python -m lib.gauss_seidel_test
"""

from lib.gauss_seidel import GaussSeidel

def test_gauss_seidel():
    print("="*65)
    print("   TEST: MÉTODO DE GAUSS-SEIDEL (CHAPRA EX)")
    print("="*65)
    
    # Sistema de ecuaciones de ejemplo
    A = [
        [3.0, -0.1, -0.2],
        [0.1, 7.0, -0.3],
        [0.3, -0.2, 10.0]
    ]
    b = [7.85, -19.3, 71.4]
    x0 = [0.0, 0.0, 0.0]
    tol = 1e-5 # tolerancia en %
    max_iter = 150
    relax = 1.0
    
    print("Matriz A:")
    for row in A:
        print("  ", row)
    print("Vector b:", b)
    print("Aproximación inicial x0:", x0)
    print("Tolerancia:", tol, "%")
    print("Relajación lambda:", relax)
    print()
    
    solver = GaussSeidel(A, b, x0=x0, tol=tol, max_iter=max_iter, relax=relax)
    result = solver.solve()
    
    if not result["success"]:
        print(f"Error en la ejecución: {result['error_message']}")
        return
        
    print(f"Dominancia diagonal de A: {'SÍ' if result['diag_dominant'] else 'NO'}")
    for detail in result["dominant_details"]:
        print(f"  Fila {detail['row']}: {detail['status']} (Diag: {detail['diag']:.4g}, Suma otros: {detail['row_sum']:.4g})")
    print()
    
    # Imprimir tabla de resultados
    headers = f"{'Iter':^5} │ "
    for j in range(len(x0)):
        headers += f"{f'x[{j+1}]':^14} │ "
    headers += f"{'Error Max (%)':^15}"
    print(headers)
    print("─" * len(headers))
    
    for step in result["steps"]:
        it = step["iter"]
        x_vals = step["x"]
        max_err = step["max_error"]
        
        row_str = f" {it:^3}  │ "
        for val in x_vals:
            row_str += f"{val:^14.6f} │ "
        
        if it == 0:
            row_str += f"{'---':^15}"
        else:
            row_str += f"{max_err:^15.3e}"
        print(row_str)
        
    print("─" * len(headers))
    print(f"Resultado final: {result['message']}")
    print("Vector solución obtenido:", [round(x, 6) for x in result["solution"]])
    print("="*65)

if __name__ == "__main__":
    test_gauss_seidel()
