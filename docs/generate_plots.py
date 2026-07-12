import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
import sympy

from lib.lagrange_interpolation import LagrangeInterpolation
from lib.trapezoidal_rule import TrapezoidalRule

# Asegurar que la carpeta docs/img existe
os.makedirs("docs/img", exist_ok=True)

def generate_lagrange():
    print("=== GENERANDO DATOS DE INTERPOLACIÓN DE LAGRANGE ===")
    x_data = [1.0, 2.0, 3.0]
    y_data = [1.0, 4.0, 9.0]
    eval_point = 2.5
    func_str = "x**2"
    
    solver = LagrangeInterpolation(x_data, y_data, eval_point)
    res = solver.solve()
    
    if not res["success"]:
        print("Error:", res["error_message"])
        return
        
    sol = res["solution"]
    print(f"P({eval_point}) = {sol['value']:.8f}")
    print(f"Polinomio expandido: {sol['polynomial']}")
    
    # Crear gráfica
    fig, ax = plt.subplots(figsize=(6, 4))
    x_min, x_max = min(x_data) - 1, max(x_data) + 1
    x_range = np.linspace(x_min, x_max, 300)
    
    # Función original
    x_sym = sympy.Symbol('x')
    f_expr = sympy.sympify(func_str)
    f_callable = sympy.lambdify(x_sym, f_expr, "numpy")
    ax.plot(x_range, f_callable(x_range), "b-", linewidth=1.5, label="Función original f(x) = x²")
    
    # Polinomio interpolante
    poly_expr = sol["polynomial_expr"]
    poly_callable = sympy.lambdify(x_sym, poly_expr, "numpy")
    ax.plot(x_range, poly_callable(x_range), "g--", linewidth=1.5, label="Polinomio Lagrange P(x)")
    
    # Puntos
    ax.plot(x_data, y_data, "or", markersize=8, markerfacecolor="red", label="Puntos de interpolación")
    ax.plot(eval_point, sol["value"], "xc", markersize=10, markeredgewidth=2, label=f"Aprox en x={eval_point} ({sol['value']:.4g})")
    
    ax.set_title("Interpolación de Lagrange (Ejemplo Cuadrático)", fontsize=12, fontweight='bold')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig("docs/img/lagrange_grafica.png", dpi=150)
    plt.close()
    print("Gráfica guardada en docs/img/lagrange_grafica.png\n")
    
    # Retornar los pasos formateados como tabla
    steps_text = ""
    for step in res["steps"]:
        if step["type"] == "initial":
            steps_text += f"{step['description']}\n"
        elif step["type"] == "basis_start":
            steps_text += f"\nCálculo de base L_{step['i']}(x) * y_{step['i']}:\n"
        elif step["type"] == "term":
            steps_text += f"  - {step['description']}\n"
        elif step["type"] == "basis_end":
            steps_text += f"  -> {step['description']}\n"
        elif step["type"] == "sum":
            steps_text += f"\nSuma final:\n  P({eval_point}) = {step['result']:.8f}\n"
    return steps_text

def generate_trapezoidal():
    print("=== GENERANDO DATOS DE LA REGLA DEL TRAPECIO ===")
    x_data = [0.0, 0.5, 1.0, 1.5, 2.0]
    y_data = [xi * xi for xi in x_data]  # f(x) = x^2
    func_str = "x**2"
    
    solver = TrapezoidalRule(x_data, y_data, f_expr=func_str)
    res = solver.solve()
    
    if not res["success"]:
        print("Error:", res["error_message"])
        return
        
    sol = res["solution"]
    print(f"I ~= {sol['value']:.8f}")
    print(f"h = {sol['h']:.6g}, n = {sol['n']} segmentos")
    print(f"Integral exacta = {sol['exact_value']:.8f}")
    print(f"Error relativo = {sol['error_relativo']:.6f}%")
    
    # Crear gráfica
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Dibujar trapecios
    for seg in sol["segments"]:
        poly_x = [seg["x0"], seg["x1"], seg["x1"], seg["x0"]]
        poly_y = [0, 0, seg["f1"], seg["f0"]]
        ax.fill(poly_x, poly_y, alpha=0.25, color="#58A1D3", edgecolor="#0F4C81", linewidth=1.2)
        
    # Función original
    x_sym = sympy.Symbol('x')
    f_expr = sympy.sympify(func_str)
    f_callable = sympy.lambdify(x_sym, f_expr, "numpy")
    x_range = np.linspace(min(x_data), max(x_data), 300)
    ax.plot(x_range, f_callable(x_range), "b-", linewidth=1.5, label="Función original f(x) = x²")
    
    # Nodos
    ax.plot(x_data, y_data, "or", markersize=7, markerfacecolor="red", label="Nodos")
    
    ax.set_title("Integración Numérica: Regla del Trapecio Compuesta (n=4)", fontsize=12, fontweight='bold')
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig("docs/img/trapecio_grafica.png", dpi=150)
    plt.close()
    print("Gráfica guardada en docs/img/trapecio_grafica.png\n")
    
    steps_text = ""
    for step in res["steps"]:
        if step["type"] == "initial":
            steps_text += f"{step['description']}\n"
        elif step["type"] == "segment":
            steps_text += f"  - {step['description']}\n"
        elif step["type"] == "final":
            steps_text += f"\nFórmula final: {step['description']}\n"
        elif step["type"] == "exact":
            steps_text += f"Comparación analítica: {step['description']}\n"
    return steps_text

if __name__ == "__main__":
    lagrange_steps = generate_lagrange()
    trapezoid_steps = generate_trapezoidal()
    
    # Guardar los textos de pasos para usarlos en el informe
    with open("docs/img/lagrange_steps.txt", "w", encoding="utf-8") as f:
        f.write(lagrange_steps)
    with open("docs/img/trapecio_steps.txt", "w", encoding="utf-8") as f:
        f.write(trapezoid_steps)
    print("Pasos guardados en docs/img/lagrange_steps.txt y docs/img/trapecio_steps.txt")
