import sympy as sp
import numpy as np

class SecantRoots:
    """
    Clase para el cálculo de raíces mediante el método de la Secante.
    """
    def __init__(self, func_str, x0, x1, tol=1e-5, max_iter=150):
        self.func_str = func_str
        self.x0 = float(x0)
        self.x1 = float(x1)
        self.tol = float(tol)
        self.max_iter = int(max_iter)  # Requisito: parada en max 150 iteraciones 
        self.history = []              # Guardará el paso a paso para la tabla/gráfica
        
    def solve(self):
        x = sp.Symbol('x')
        
        try:
            # Parsear la función ingresada por el usuario
            f_expr = sp.sympify(self.func_str)
            # Convertir a función evaluable de numpy
            f = sp.lambdify(x, f_expr, 'numpy')
            
        except Exception as e:
            return {
                "success": False,
                "solution": None,
                "steps": [],
                "error_message": f"Error al procesar la función: {str(e)}"
            }

        x_prev = self.x0
        x_curr = self.x1
        iter_count = 0
        error = float('inf')
        
        # Evaluar los puntos iniciales
        fx_prev = float(f(x_prev))
        fx_curr = float(f(x_curr))
        
        # Guardar el estado del primer punto inicial para la GUI
        self.history.append({
            "iter": 0,
            "x": x_prev,
            "fx": fx_prev,
            "error": None
        })
        
        while iter_count < self.max_iter:
            iter_count += 1
            
            # Guardar el estado del punto actual
            self.history.append({
                "iter": iter_count,
                "x": x_curr,
                "fx": fx_curr,
                "error": error if iter_count > 1 else None
            })
            
            # Criterio de parada 1: el módulo de f(x) es menor o igual a la tolerancia 
            if abs(fx_curr) <= self.tol:
                break
                
            # Evitar división por cero en la fórmula de la secante
            if (fx_curr - fx_prev) == 0:
                return {
                    "success": False,
                    "solution": None,
                    "steps": self.history,
                    "error_message": f"División por cero en iteración {iter_count}. f(x_i) y f(x_i-1) son iguales."
                }
                
            # Fórmula del método de la Secante
            x_next = x_curr - (fx_curr * (x_curr - x_prev)) / (fx_curr - fx_prev)
            
            # Cálculo del error relativo aproximado 
            if x_next != 0:
                error = abs((x_next - x_curr) / x_next) * 100
            else:
                error = abs(x_next - x_curr)
                
            # Preparar valores para la siguiente iteración
            x_prev = x_curr
            fx_prev = fx_curr
            x_curr = x_next
            fx_curr = float(f(x_curr))
            
            # Criterio de parada 2: el error relativo es menor a la tolerancia 
            if error <= self.tol:
                # Registrar el iterado final que cumplió la condición
                iter_count += 1
                self.history.append({
                    "iter": iter_count,
                    "x": x_curr,
                    "fx": fx_curr,
                    "error": error
                })
                break
                
        # Construir el mensaje de finalización según el requerimiento 
        if iter_count < self.max_iter or error <= self.tol:
            msg = f"Converge por error aceptable. Valor: {x_curr:.6f} (f(x) = {fx_curr:.2e})"
        else:
            msg = f"Alcanzó el máximo de {self.max_iter} iteraciones. Converge a {x_curr:.6f} (f(x) = {fx_curr:.2e})"

        return {
            "success": True,
            "solution": x_curr,
            "steps": self.history,
            "message": msg,
            "error_message": None
        }