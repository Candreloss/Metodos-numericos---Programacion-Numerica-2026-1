"""Interpolación de Lagrange. Ver docs/metodos/lagrange_interpolation.md."""
import copy
import sympy


class LagrangeInterpolation:
    """
    Interpolación de Lagrange.
    Construye polinomio de grado n que pasa por n+1 puntos usando bases L_i(x).
    Retorna P(x) evaluado, expresión simbólica expandida y paso a paso.
    """
    def __init__(self, x, y, eval_point):
        self.x = copy.deepcopy(x)
        self.y = copy.deepcopy(y)
        self.eval_point = eval_point
        self.n = len(x)
        self.steps = []

    def solve(self):
        self.steps = []

        if len(self.x) != len(self.y):
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": f"Dimensiones incompatibles: x tiene {len(self.x)} elementos e y tiene {len(self.y)} elementos.",
            }

        if self.n < 2:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Se requieren al menos 2 puntos para construir el polinomio de interpolación.",
            }

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if abs(self.x[i] - self.x[j]) < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Los valores de x deben ser distintos. Se encontró un valor duplicado: x[{i}] = x[{j}] = {self.x[i]}.",
                    }

        self.steps.append({
            "type": "initial",
            "x": copy.deepcopy(self.x),
            "y": copy.deepcopy(self.y),
            "eval_point": self.eval_point,
            "description": f"Datos de entrada: {self.n} puntos. Punto de evaluación x = {self.eval_point}."
        })

        x_sym = sympy.Symbol('x')
        poly_expr = 0
        basis_exprs = []

        for i in range(self.n):
            numerator = 1
            denominator = 1
            for j in range(self.n):
                if i != j:
                    numerator *= (x_sym - self.x[j])
                    denominator *= (self.x[i] - self.x[j])
            L_i = numerator / denominator
            basis_exprs.append(L_i)
            poly_expr += self.y[i] * L_i

        poly_expanded = sympy.expand(poly_expr)
        poly_str = str(poly_expanded)

        sum_val = 0.0

        for i in range(self.n):
            product = float(self.y[i])
            self.steps.append({
                "type": "basis_start",
                "i": i,
                "description": f"Cálculo de L_{i}(x) · y_{i}:"
            })

            for j in range(self.n):
                if i != j:
                    factor_num = (self.eval_point - self.x[j])
                    factor_den = (self.x[i] - self.x[j])
                    term_val = factor_num / factor_den
                    product *= term_val
                    self.steps.append({
                        "type": "term",
                        "i": i,
                        "j": j,
                        "term": f"(x - {self.x[j]}) / ({self.x[i]} - {self.x[j]})",
                        "term_value": term_val,
                        "product_so_far": product,
                        "description": f"Término j={j}: ({self.eval_point} - {self.x[j]}) / ({self.x[i]} - {self.x[j]}) = {term_val:.6g}"
                    })

            li_value = float(product) / float(self.y[i]) if float(self.y[i]) != 0 else 0.0
            self.steps.append({
                "type": "basis_end",
                "i": i,
                "li_value": li_value,
                "product_value": product,
                "description": f"L_{i}({self.eval_point}) = {li_value:.6g} | y_{i} · L_{i} = {product:.6g}"
            })
            sum_val += product

        self.steps.append({
            "type": "sum",
            "description": f"Suma de todos los términos: P({self.eval_point}) = Σ y_i · L_i({self.eval_point})",
            "result": sum_val
        })

        self.steps.append({
            "type": "polynomial",
            "polynomial": poly_str,
            "description": "Polinomio de Lagrange expandido:"
        })

        symbolic_eval = float(poly_expanded.subs(x_sym, self.eval_point))

        return {
            "success": True,
            "solution": {
                "value": sum_val,
                "symbolic_value": symbolic_eval,
                "polynomial": poly_str,
                "polynomial_expr": poly_expanded,
                "basis": basis_exprs,
            },
            "steps": self.steps,
            "error_message": None
        }
