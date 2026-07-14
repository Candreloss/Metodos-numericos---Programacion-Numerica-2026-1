"""Newton-Raphson. Ver docs/metodos/newton_raphson.md."""
import sympy as sp
import numpy as np

class NewtonRoots:
    """Cálculo de raíces mediante el método de Newton-Raphson."""
    def __init__(self, func_str, x0, tol=1e-5, max_iter=150):
        self.func_str = func_str
        self.x0 = float(x0)
        self.tol = float(tol)
        self.max_iter = int(max_iter)
        self.history = []

    def solve(self):
        x = sp.Symbol('x')

        try:
            f_expr = sp.sympify(self.func_str)
            df_expr = sp.diff(f_expr, x)
            f = sp.lambdify(x, f_expr, 'numpy')
            df = sp.lambdify(x, df_expr, 'numpy')
        except Exception as e:
            return {
                "success": False,
                "solution": None,
                "steps": [],
                "error_message": f"Error de sintaxis en la función: {str(e)}"
            }

        x_current = self.x0
        iter_count = 0
        error = float('inf')

        try:
            while iter_count < self.max_iter:
                fx_val = f(x_current)
                dfx_val = df(x_current)

                if isinstance(fx_val, complex) or isinstance(dfx_val, complex):
                    raise TypeError("La función evaluó a un número complejo.")

                fx = float(fx_val)
                dfx = float(dfx_val)

                self.history.append({
                    "iter": iter_count,
                    "x": x_current,
                    "fx": fx,
                    "error": error if iter_count > 0 else None
                })

                if abs(fx) <= self.tol:
                    break

                if dfx == 0:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.history,
                        "error_message": f"La derivada se hizo cero en x = {x_current:.6f}. El método falla (división por cero)."
                    }

                x_new = x_current - (fx / dfx)

                if x_new != 0:
                    error = abs((x_new - x_current) / x_new) * 100
                else:
                    error = abs(x_new - x_current)

                x_current = x_new
                iter_count += 1

                if error <= self.tol:
                    self.history.append({
                        "iter": iter_count,
                        "x": x_current,
                        "fx": float(f(x_current)),
                        "error": error
                    })
                    break

            if iter_count < self.max_iter or error <= self.tol:
                msg = f"Converge por error aceptable. Valor: {x_current:.6f} (f(x) = {float(f(x_current)):.2e})"
            else:
                msg = f"Alcanzó el máximo de {self.max_iter} iteraciones sin converger. Mejor aproximación: {x_current:.6f}"

            return {
                "success": True,
                "solution": x_current,
                "steps": self.history,
                "message": msg,
                "error_message": None
            }

        except OverflowError:
            return {
                "success": False,
                "solution": None,
                "steps": self.history,
                "error_message": f"Desbordamiento matemático en iteración {iter_count}.\nLos valores crecieron al infinito (Divergencia)."
            }
        except TypeError as e:
            return {
                "success": False,
                "solution": None,
                "steps": self.history,
                "error_message": f"Error de dominio en iteración {iter_count}.\nPosible salto hacia un dominio indefinido (ej. logaritmos/raíces de negativos)."
            }
        except Exception as e:
            return {
                "success": False,
                "solution": None,
                "steps": self.history,
                "error_message": f"Error matemático inesperado en iteración {iter_count}:\n{str(e)}"
            }
