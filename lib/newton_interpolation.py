import copy
import numpy as np
import sympy


class NewtonInterpolation:
    """
    Clase que implementa el método de Interpolación de Newton (diferencias
    divididas).  Construye el polinomio de grado n-ésimo que pasa por todos
    los puntos (x, y) dados usando la tabla de diferencias divididas.

    Fórmula:
        P(x) = f[x_0] + f[x_0,x_1]·(x - x_0)
              + f[x_0,x_1,x_2]·(x - x_0)(x - x_1) + ...
    donde f[x_0,...,x_k] son las diferencias divididas extraídas de la
    diagonal de la tabla.
    """

    def __init__(self, x, y, eval_point, degree=None):
        """
        Inicializa el interpolador.

        x: lista de valores x (abscisas).
        y: lista de valores y (ordenadas).
        eval_point: valor donde evaluar P(x).
        degree: grado del polinomio (opcional). Si none, usa todos los
                puntos. Si se especifica, trunca a los primeros degree+1.
        """
        self.x_full = copy.deepcopy(x)
        self.y_full = copy.deepcopy(y)
        self.eval_point = eval_point
        self.degree = degree
        self.func_str = None
        self.steps = []

    def solve(self):
        self.steps = []
        m = len(self.x_full)

        if len(self.x_full) != len(self.y_full):
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": f"Dimensiones incompatibles: x tiene {len(self.x_full)} elementos e y tiene {len(self.y_full)}.",
            }
        if m < 2:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Se requieren al menos 2 puntos para interpolar.",
            }
        for i in range(m):
            for j in range(i + 1, m):
                if abs(self.x_full[i] - self.x_full[j]) < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Valores x duplicados: x[{i}] = x[{j}] = {self.x_full[i]}.",
                    }

        n = self.degree if self.degree is not None else m - 1
        n = min(n, m - 1)
        if n < 1:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "El grado debe ser al menos 1.",
            }

        x_data = copy.deepcopy(self.x_full[: n + 1])
        y_data = copy.deepcopy(self.y_full[: n + 1])
        n_points = len(x_data)

        self.steps.append({
            "type": "initial",
            "x": copy.deepcopy(x_data),
            "y": copy.deepcopy(y_data),
            "eval_point": self.eval_point,
            "degree": n,
            "description": f"Datos: {n_points} puntos. Grado {n}. Evalúa en x = {self.eval_point}.",
        })

        table = np.zeros((n_points, n_points))
        table[:, 0] = y_data
        self.steps.append({
            "type": "table_col",
            "col": 0,
            "table_snapshot": copy.deepcopy(table),
            "description": "Columna 0 de la tabla = valores de y (f[x_i]).",
        })

        for j in range(1, n_points):
            for i in range(j, n_points):
                table[i, j] = (table[i, j - 1] - table[i - 1, j - 1]) / (x_data[i] - x_data[i - j])
            self.steps.append({
                "type": "table_col",
                "col": j,
                "table_snapshot": copy.deepcopy(table),
                "description": f"Columna {j}: diferencias divididas de orden {j}.",
            })

        coefficients = list(np.diag(table))
        self.steps.append({
            "type": "coefficients",
            "coefficients": copy.deepcopy(coefficients),
            "description": f"Coeficientes extraídos de la diagonal: {[f'{c:.6g}' for c in coefficients]}",
        })

        result = coefficients[0]
        prod = 1.0
        eval_steps_rows = []
        for j in range(1, n_points):
            prod *= (self.eval_point - x_data[j - 1])
            term = coefficients[j] * prod
            result += term
            eval_steps_rows.append({
                "j": j,
                "coef": coefficients[j],
                "prod": prod,
                "term": term,
                "accumulated": result,
                "description": f"Sumando: {coefficients[j]:.6g} × {prod:.6g} = {term:.6g}  →  acum = {result:.6g}",
            })
        self.steps.append({
            "type": "evaluation",
            "rows": eval_steps_rows,
            "description": f"Evaluación progresiva. Resultado final: P({self.eval_point}) = {result:.6g}",
        })

        x_sym = sympy.Symbol('x')
        poly_expr = coefficients[0]
        prod_sym = 1
        for j in range(1, n_points):
            prod_sym *= (x_sym - x_data[j - 1])
            poly_expr += coefficients[j] * prod_sym
        poly_expanded = sympy.expand(poly_expr)
        poly_str = str(poly_expanded)

        self.steps.append({
            "type": "polynomial",
            "polynomial": poly_str,
            "description": "Polinomio de Newton expandido:",
        })

        symbolic_eval = float(poly_expanded.subs(x_sym, self.eval_point))

        return {
            "success": True,
            "solution": {
                "value": result,
                "symbolic_value": symbolic_eval,
                "polynomial": poly_str,
                "polynomial_expr": poly_expanded,
                "coefficients": coefficients,
                "table": table.tolist(),
            },
            "steps": self.steps,
            "error_message": None,
        }
