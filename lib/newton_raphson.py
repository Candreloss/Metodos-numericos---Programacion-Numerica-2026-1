import sympy as sp
import numpy as np

class NewtonRoots:
    """
    Clase para el cálculo de raíces mediante el método de Newton-Raphson.
    """
    def __init__(self, func_str, x0, tol=1e-5, max_iter=150):
        self.func_str = func_str
        self.x0 = float(x0)
        self.tol = float(tol)
        self.max_iter = int(max_iter)  # Requisito: parada en max 150 iteraciones
        self.history = []              # Guardará el paso a paso para la tabla/gráfica
        
    def solve(self):
        x = sp.Symbol('x')
        
        try:
            # Parsear la función y calcular su derivada simbólicamente
            f_expr = sp.sympify(self.func_str)
            df_expr = sp.diff(f_expr, x)
            
            # Convertir a funciones evaluables de numpy para mayor velocidad
            f = sp.lambdify(x, f_expr, 'numpy')
            df = sp.lambdify(x, df_expr, 'numpy')
            
        except Exception as e:
            return {
                "success": False,
                "solution": None,
                "steps": [],
                "error_message": f"Error al procesar la función: {str(e)}"
            }

        x_current = self.x0
        iter_count = 0
        error = float('inf')
        
        while iter_count < self.max_iter:
            fx = float(f(x_current))
            dfx = float(df(x_current))
            
            # Guardar el estado actual para la GUI
            self.history.append({
                "iter": iter_count,
                "x": x_current,
                "fx": fx,
                "error": error if iter_count > 0 else None
            })
            
            # Criterio de parada 1: f(x) es suficientemente cercano a 0
            if abs(fx) <= self.tol:
                break
                
            # Evitar división por cero
            if dfx == 0:
                return {
                    "success": False,
                    "solution": None,
                    "steps": self.history,
                    "error_message": f"La derivada se hizo cero en x = {x_current}. El método falla."
                }
                
            # Fórmula de Newton-Raphson
            x_new = x_current - (fx / dfx)
            
            # Cálculo del error relativo (evitando división por cero)
            if x_new != 0:
                error = abs((x_new - x_current) / x_new) * 100
            else:
                error = abs(x_new - x_current)
                
            x_current = x_new
            iter_count += 1
            
            # Criterio de parada 2: Error relativo menor a la tolerancia
            if error <= self.tol:
                # Registrar la última iteración exitosa
                self.history.append({
                    "iter": iter_count,
                    "x": x_current,
                    "fx": float(f(x_current)),
                    "error": error
                })
                break
                
        # Construir el mensaje de finalización según el requisito del PDF
        if iter_count < self.max_iter or error <= self.tol:
            msg = f"Converge por error aceptable. Valor: {x_current:.6f} (f(x) = {float(f(x_current)):.2e})"
        else:
            msg = f"Alcanzó el máximo de {self.max_iter} iteraciones. Converge a {x_current:.6f} (f(x) = {float(f(x_current)):.2e})"

        return {
            "success": True,
            "solution": x_current,
            "steps": self.history,
            "message": msg,
            "error_message": None
        }