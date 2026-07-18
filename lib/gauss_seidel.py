"""Gauss-Seidel. Ver docs/metodos/gauss_seidel.md."""
import copy
import numpy as np #pyright: ignore

class GaussSeidel:
    """
    Método iterativo de Gauss-Seidel con factor de relajación.
    Resuelve Ax = b y registra cada paso.
    """
    def __init__(self, A, b, x0=None, tol=1e-5, max_iter=150, relax=1.0):
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.n = len(A)
        if x0 is None:
            self.x0 = np.zeros(self.n, dtype=float)
        else:
            self.x0 = np.array(x0, dtype=float)
        self.tol = float(tol)
        self.max_iter = int(max_iter)
        self.relax = float(relax)
        self.steps = []

    def check_diagonal_dominance(self):
        details = []
        is_dominant = True

        for i in range(self.n):
            diag = abs(self.A[i][i])
            row_sum = sum(abs(self.A[i][j]) for j in range(self.n) if j != i)

            row_ok = diag >= row_sum
            if not row_ok:
                is_dominant = False

            details.append({
                "row": i + 1,
                "diag": diag,
                "row_sum": row_sum,
                "ok": row_ok,
                "status": "✓ Dominante" if row_ok else "❌ No dominante"
            })

        return is_dominant, details

    def solve(self):
        self.steps = []
        n = self.n

        if len(self.b) != n:
            return {
                "success": False,
                "solution": None,
                "steps": [],
                "error_message": f"Dimensiones incompatibles: A es {n}x{n} y b tiene longitud {len(self.b)}.",
                "diag_dominant": False,
                "dominant_details": []
            }

        for i in range(n):
            if len(self.A[i]) != n:
                return {
                    "success": False,
                    "solution": None,
                    "steps": [],
                    "error_message": f"La fila {i+1} de la matriz A no tiene longitud {n} (no es cuadrada).",
                    "diag_dominant": False,
                    "dominant_details": []
                }
            if abs(self.A[i][i]) < 1e-12:
                return {
                    "success": False,
                    "solution": None,
                    "steps": [],
                    "error_message": f"Error en elemento diagonal A[{i+1}][{i+1}]: Es cero o sumamente cercano a cero. Gauss-Seidel no puede continuar sin un pivote no nulo.",
                    "diag_dominant": False,
                    "dominant_details": []
                }

        is_dominant, dominant_details = self.check_diagonal_dominance()

        x_old = np.copy(self.x0)
        x_new = np.copy(x_old)

        self.steps.append({
            "iter": 0,
            "x": x_old.tolist(),
            "errors": [0.0] * n,
            "max_error": 0.0,
            "description": "Aproximación inicial x^(0):"
        })

        converged = False

        try:
            for k in range(1, self.max_iter + 1):
                errors = []
                var_details = []

                for i in range(n):
                    sum1_terms = []
                    sum1 = 0.0
                    for j in range(i):
                        sum1 += self.A[i][j] * x_new[j]
                        sum1_terms.append(f"({self.A[i][j]:+.6g} × {x_new[j]:.6g})")

                    sum2_terms = []
                    sum2 = 0.0
                    for j in range(i + 1, n):
                        sum2 += self.A[i][j] * x_old[j]
                        sum2_terms.append(f"({self.A[i][j]:+.6g} × {x_old[j]:.6g})")

                    x_calc = (self.b[i] - sum1 - sum2) / self.A[i][i]

                    x_new[i] = self.relax * x_calc + (1.0 - self.relax) * x_old[i]

                    if abs(x_new[i]) > 1e-12:
                        ea = abs((x_new[i] - x_old[i]) / x_new[i]) * 100.0
                    else:
                        ea = abs(x_new[i] - x_old[i]) * 100.0
                    errors.append(ea)

                    terms_str = ""
                    for term in sum1_terms + sum2_terms:
                        if term.startswith("(+"):
                            terms_str += f" - {term[2:-1]}"
                        elif term.startswith("(-"):
                            terms_str += f" + {term[2:-1]}"
                        else:
                            terms_str += f" - {term[1:-1]}"

                    formula_str = f"({self.b[i]:.6g}{terms_str}) / {self.A[i][i]:.6g}"

                    if abs(self.relax - 1.0) > 1e-6:
                        relax_str = f"{self.relax:.6g} × {x_calc:.6g} + (1 - {self.relax:.6g}) × {x_old[i]:.6g} = {x_new[i]:.6g}"
                    else:
                        relax_str = f"{x_calc:.6g}"

                    if k == 1 and np.all(self.x0 == 0.0):
                        error_str = "100.0000%"
                    else:
                        if abs(x_new[i]) > 1e-12:
                            error_str = f"|({x_new[i]:.6g} - {x_old[i]:.6g}) / {x_new[i]:.6g}| × 100% = {ea:.6g}%"
                        else:
                            error_str = f"|{x_new[i]:.6g} - {x_old[i]:.6g}| × 100% = {ea:.6g}%"

                    var_details.append({
                        "var": i + 1,
                        "formula": formula_str,
                        "relax": relax_str,
                        "error": error_str,
                        "val": x_new[i],
                        "val_calc": x_calc
                    })

                max_err = max(errors)

                self.steps.append({
                    "iter": k,
                    "x": x_new.tolist(),
                    "errors": errors,
                    "max_error": max_err,
                    "description": f"Iteración {k}:",
                    "var_details": var_details
                })

                if max_err <= self.tol:
                    converged = True
                    break

                if np.isnan(x_new).any() or np.isinf(x_new).any() or max_err > 1e12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Se ha detectado divergencia en la iteración {k}. El error máximo es excesivo o se encontraron valores NaN/Inf. Compruebe si la matriz cumple con la dominancia diagonal.",
                        "diag_dominant": is_dominant,
                        "dominant_details": dominant_details
                    }

                x_old = np.copy(x_new)

            if converged:
                return {
                    "success": True,
                    "solution": x_new.tolist(),
                    "steps": self.steps,
                    "error_message": None,
                    "diag_dominant": is_dominant,
                    "dominant_details": dominant_details,
                    "message": f"Converge por error aceptable. Iteraciones realizadas: {k}"
                }
            else:
                return {
                    "success": True,
                    "solution": x_new.tolist(),
                    "steps": self.steps,
                    "error_message": f"Se alcanzó el límite máximo de {self.max_iter} iteraciones sin converger por debajo del error de tolerancia de {self.tol}%.",
                    "diag_dominant": is_dominant,
                    "dominant_details": dominant_details,
                    "message": f"Alcanzó el máximo de {self.max_iter} iteraciones sin converger."
                }

        except OverflowError:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Error de desbordamiento (Overflow) durante el cálculo. La aproximación divergió rápidamente al infinito.",
                "diag_dominant": is_dominant,
                "dominant_details": dominant_details
            }
        except Exception as e:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": f"Error inesperado durante la ejecución: {str(e)}",
                "diag_dominant": is_dominant,
                "dominant_details": dominant_details
            }
