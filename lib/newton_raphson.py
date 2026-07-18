"""Newton-Raphson. Ver docs/metodos/newton_raphson.md."""
import re
import sympy as sp
import numpy as np


def _parse_expression(func_str):
    """Normaliza expresiones matemáticas escritas en notación común."""
    cleaned = func_str.strip()
    cleaned = cleaned.replace('sen(', 'sin(')
    cleaned = cleaned.replace('ln(', 'log(')
    cleaned = re.sub(r'(?<![A-Za-z0-9_])e(?![A-Za-z0-9_])', 'E', cleaned)
    cleaned = cleaned.replace('^', '**')
    return sp.sympify(
        cleaned,
        locals={
            'E': sp.E,
            'pi': sp.pi,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'exp': sp.exp,
            'log': sp.log,
        },
    )


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
            f_expr = _parse_expression(self.func_str)
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

                # BLINDAJE CONTRA INDETERMINACIONES (NaN, Inf, Complejos)
                if np.isnan(fx_val) or np.isnan(dfx_val) or np.isinf(fx_val) or np.isinf(dfx_val) or isinstance(fx_val, complex) or isinstance(dfx_val, complex):
                    raise TypeError("La función o su derivada no están definidas matemáticamente en este punto (Resultado no real, NaN o Infinito).")

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
                    # Validar también el último punto calculado
                    fx_final = f(x_current)
                    if np.isnan(fx_final) or isinstance(fx_final, complex):
                        raise TypeError("El punto de convergencia final cayó en una zona indefinida de la función.")
                    
                    self.history.append({
                        "iter": iter_count,
                        "x": x_current,
                        "fx": float(fx_final),
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
                "error_message": f"Error de dominio en iteración {iter_count}.\n{str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "solution": None,
                "steps": self.history,
                "error_message": f"Error matemático inesperado en iteración {iter_count}:\n{str(e)}"
            }