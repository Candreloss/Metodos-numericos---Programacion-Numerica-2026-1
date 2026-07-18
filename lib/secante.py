"""Método de la Secante. Ver docs/metodos/secante.md."""
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


class SecantRoots:
    """Cálculo de raíces mediante el método de la Secante."""
    def __init__(self, func_str, x0, x1, tol=1e-5, max_iter=150):
        self.func_str = func_str
        self.x0 = float(x0)
        self.x1 = float(x1)
        self.tol = float(tol)
        self.max_iter = int(max_iter)
        self.history = []

    def solve(self):
        x = sp.Symbol('x')

        try:
            f_expr = _parse_expression(self.func_str)
            f = sp.lambdify(x, f_expr, 'numpy')
        except Exception as e:
            err_msg = str(e)
            if "could not parse" in err_msg:
                msg = "Error de sintaxis en la función. Asegúrese de usar '*' para multiplicaciones (ej. '2*x' en lugar de '2x')."
            else:
                msg = f"Error al procesar la función matemática: {err_msg}"
            return {"success": False, "solution": None, "steps": [], "error_message": msg}

        x_prev = self.x0
        x_curr = self.x1
        iter_count = 0
        error = float('inf')

        try:
            fx_prev_val = f(x_prev)
            fx_curr_val = f(x_curr)

            # VALIDACIÓN DE INDETERMINACIONES EN PUNTOS INICIALES
            if np.isnan(fx_prev_val) or np.isnan(fx_curr_val) or np.isinf(fx_prev_val) or np.isinf(fx_curr_val) or isinstance(fx_prev_val, complex) or isinstance(fx_curr_val, complex):
                raise TypeError("Uno o ambos puntos iniciales (x0 o x1) no pertenecen al dominio real de la función.")

            fx_prev = float(fx_prev_val)
            fx_curr = float(fx_curr_val)

            self.history.append({
                "iter": 0,
                "x": x_prev,
                "fx": fx_prev,
                "error": None
            })

            while iter_count < self.max_iter:
                iter_count += 1

                self.history.append({
                    "iter": iter_count,
                    "x": x_curr,
                    "fx": fx_curr,
                    "error": error if iter_count > 1 else None
                })

                if abs(fx_curr) <= self.tol:
                    break

                if (fx_curr - fx_prev) == 0:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.history,
                        "error_message": f"División por cero en iteración {iter_count}. f(x_curr) y f(x_prev) son idénticos."
                    }

                x_next = x_curr - (fx_curr * (x_curr - x_prev)) / (fx_curr - fx_prev)

                if x_next != 0:
                    error = abs((x_next - x_curr) / x_next) * 100
                else:
                    error = abs(x_next - x_curr)

                x_prev = x_curr
                fx_prev = fx_curr
                x_curr = x_next

                fx_curr_val = f(x_curr)
                
                # VALIDACIÓN CONTINUA DE INDETERMINACIONES
                if np.isnan(fx_curr_val) or np.isinf(fx_curr_val) or isinstance(fx_curr_val, complex):
                    raise TypeError("El método divergió o saltó hacia un punto fuera del dominio real de la función.")
                    
                fx_curr = float(fx_curr_val)

                if error <= self.tol:
                    iter_count += 1
                    self.history.append({
                        "iter": iter_count,
                        "x": x_curr,
                        "fx": fx_curr,
                        "error": error
                    })
                    break

            if iter_count < self.max_iter or error <= self.tol:
                msg = f"Converge por error aceptable. Valor: {x_curr:.6f} (f(x) = {fx_curr:.2e})"
            else:
                msg = f"Alcanzó el máximo de {self.max_iter} iteraciones sin converger. Mejor aproximación: {x_curr:.6f}"

            return {
                "success": True,
                "solution": x_curr,
                "steps": self.history,
                "message": msg,
                "error_message": None
            }

        except NameError as ne:
            return {
                "success": False,
                "solution": None,
                "steps": self.history,
                "error_message": f"Función no reconocida o mal declarada.\nRecuerde usar la sintaxis matemática internacional estándar:\nsin(x), cos(x), tan(x), exp(x), log(x)."
            }
        except OverflowError:
            return {
                "success": False,
                "solution": None,
                "steps": self.history,
                "error_message": f"Desbordamiento matemático en iteración {iter_count}.\nLos puntos divergieron con valores que tienden al infinito."
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
                "error_message": f"Error imprevisto en la ejecución (Iteración {iter_count}):\n{str(e)}"
            }