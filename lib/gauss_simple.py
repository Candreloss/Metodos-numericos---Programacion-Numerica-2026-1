"""Eliminación Gaussiana. Ver docs/metodos/gauss_simple.md."""
import copy

class GaussSimple:
    """
    Eliminación Gaussiana. Soporta pivoteo parcial opcional.
    """
    def __init__(self, A, b, pivoting=True):
        self.A = copy.deepcopy(A)
        self.b = copy.deepcopy(b)
        self.pivoting = pivoting
        self.n = len(A)
        self.steps = []

    def solve(self):
        self.steps = []
        n = self.n

        if len(self.b) != n:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": f"Dimensiones incompatibles: A es {n}x{n} y b tiene longitud {len(self.b)}."
            }

        for i, row in enumerate(self.A):
            if len(row) != n:
                return {
                    "success": False,
                    "solution": None,
                    "steps": self.steps,
                    "error_message": f"La fila {i} de la matriz A no tiene longitud {n} (no es cuadrada)."
                }

        aug = []
        for i in range(n):
            aug.append(self.A[i] + [self.b[i]])

        self.steps.append({
            "type": "initial",
            "matrix": copy.deepcopy(aug),
            "description": "Matriz aumentada inicial [A | b]:"
        })

        for k in range(n - 1):
            self.steps.append({
                "type": "stage_start",
                "matrix": copy.deepcopy(aug),
                "description": f"--- Etapa de eliminación para la columna {k + 1} (k={k}) ---"
            })

            if self.pivoting:
                pivot_row = k
                max_val = abs(aug[k][k])
                for i in range(k + 1, n):
                    val = abs(aug[i][k])
                    if val > max_val:
                        max_val = val
                        pivot_row = i

                if max_val < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Error: No se puede encontrar un pivote no nulo para la columna {k + 1}. El sistema es singular o tiene soluciones infinitas."
                    }

                if pivot_row != k:
                    aug[k], aug[pivot_row] = aug[pivot_row], aug[k]
                    self.steps.append({
                        "type": "pivot",
                        "matrix": copy.deepcopy(aug),
                        "description": f"Pivoteo: Intercambio de Fila {k + 1} con Fila {pivot_row + 1} porque |{aug[k][k]:.6g}| es el máximo de la columna {k + 1}.",
                        "details": {"row1": k, "row2": pivot_row}
                    })
            else:
                if abs(aug[k][k]) < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Error en la columna {k + 1}: Elemento pivote A[{k + 1}][{k + 1}] es cero o muy cercano a cero. Gauss Simple sin pivoteo falla aquí. Habilite 'Pivoteo Parcial' para resolver este sistema."
                    }

            for i in range(k + 1, n):
                factor = aug[i][k] / aug[k][k]
                for j in range(k, n + 1):
                    aug[i][j] = aug[i][j] - factor * aug[k][j]

                self.steps.append({
                    "type": "elimination_row",
                    "matrix": copy.deepcopy(aug),
                    "description": f"Fila {i + 1} ← Fila {i + 1} - ({factor:.6g}) × Fila {k + 1}",
                    "details": {"source_row": k, "target_row": i, "factor": factor}
                })

        if abs(aug[n - 1][n - 1]) < 1e-12:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Error en la última fila: El elemento final en la diagonal principal es muy cercano a cero. El sistema es singular."
            }

        self.steps.append({
            "type": "elimination_end",
            "matrix": copy.deepcopy(aug),
            "description": "Eliminación hacia adelante completada. Matriz triangular superior obtenida:"
        })

        x = [0.0] * n
        x[n - 1] = aug[n - 1][n] / aug[n - 1][n - 1]
        back_sub_steps = []
        back_sub_steps.append({
            "var_index": n - 1,
            "val": x[n - 1],
            "formula": f"x[{n}] = {aug[n - 1][n]:.6g} / {aug[n - 1][n - 1]:.6g} = {x[n - 1]:.6g}"
        })

        for i in range(n - 2, -1, -1):
            sum_terms = 0.0
            formula_terms = []
            for j in range(i + 1, n):
                sum_terms += aug[i][j] * x[j]
                formula_terms.append(f"({aug[i][j]:.6g} × {x[j]:.6g})")

            x[i] = (aug[i][n] - sum_terms) / aug[i][i]

            formula_str = f"x[{i + 1}] = ({aug[i][n]:.6g} - " + " - ".join(formula_terms) + f") / {aug[i][i]:.6g} = {x[i]:.6g}"
            back_sub_steps.append({
                "var_index": i,
                "val": x[i],
                "formula": formula_str
            })

        self.steps.append({
            "type": "back_substitution",
            "matrix": copy.deepcopy(aug),
            "description": "Sustitución hacia atrás:",
            "back_sub_steps": back_sub_steps
        })

        return {
            "success": True,
            "solution": x,
            "steps": self.steps,
            "error_message": None
        }
