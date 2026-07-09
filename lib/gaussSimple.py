import copy

class GaussSimple:
    """
    Clase que implementa el método de Eliminación Gaussiana.
    Soporta:
    - Gauss Simple (sin pivoteo)
    - Gauss con Pivoteo Parcial por máximo de columna
    
    Registra detalladamente cada paso para visualización en la interfaz gráfica.
    """
    def __init__(self, A, b, pivoting=True):
        """
        Inicializa el resolutor con la matriz A y el vector b.
        A: lista de listas de tamaño n x n conteniendo los coeficientes.
        b: lista de tamaño n conteniendo los términos independientes.
        pivoting: booleano, indica si se usa pivoteo parcial.
        """
        # Hacer una copia profunda para evitar modificar las listas originales
        self.A = copy.deepcopy(A)
        self.b = copy.deepcopy(b)
        self.pivoting = pivoting
        self.n = len(A)
        self.steps = []
        
    def solve(self):
        """
        Resuelve el sistema Ax = b.
        Retorna un diccionario con:
        - success: bool
        - solution: list (vector x) o None
        - steps: lista de diccionarios describiendo el paso a paso
        - error_message: str o None
        """
        self.steps = []
        n = self.n
        
        # Validaciones de dimensiones
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

        # Construir matriz aumentada [A | b]
        aug = []
        for i in range(n):
            aug.append(self.A[i] + [self.b[i]])
            
        # Registrar estado inicial
        self.steps.append({
            "type": "initial",
            "matrix": copy.deepcopy(aug),
            "description": "Matriz aumentada inicial [A | b]:"
        })

        # Proceso de Eliminación hacia adelante (Forward Elimination)
        for k in range(n - 1):
            self.steps.append({
                "type": "stage_start",
                "matrix": copy.deepcopy(aug),
                "description": f"--- Etapa de eliminación para la columna {k + 1} (k={k}) ---"
            })
            
            # 1. Pivoteo parcial (si está habilitado)
            if self.pivoting:
                pivot_row = k
                max_val = abs(aug[k][k])
                
                # Buscar el elemento máximo en valor absoluto en la columna k debajo de la fila k
                for i in range(k + 1, n):
                    val = abs(aug[i][k])
                    if val > max_val:
                        max_val = val
                        pivot_row = i
                        
                # Si el elemento máximo es extremadamente pequeño, el sistema es singular
                if max_val < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Error: No se puede encontrar un pivote no nulo para la columna {k + 1}. El sistema es singular o tiene soluciones infinitas."
                    }
                
                # Si es necesario, intercambiar filas
                if pivot_row != k:
                    aug[k], aug[pivot_row] = aug[pivot_row], aug[k]
                    self.steps.append({
                        "type": "pivot",
                        "matrix": copy.deepcopy(aug),
                        "description": f"Pivoteo: Intercambio de Fila {k + 1} con Fila {pivot_row + 1} porque |{aug[k][k]:.6g}| es el máximo de la columna {k + 1}.",
                        "details": {"row1": k, "row2": pivot_row}
                    })
            else:
                # Gauss Simple (Sin pivoteo)
                # Verificar si el elemento pivote es cero o extremadamente cercano a cero
                if abs(aug[k][k]) < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Error en la columna {k + 1}: Elemento pivote A[{k + 1}][{k + 1}] es cero o muy cercano a cero. Gauss Simple sin pivoteo falla aquí. Habilite 'Pivoteo Parcial' para resolver este sistema."
                    }

            # 2. Eliminación
            for i in range(k + 1, n):
                factor = aug[i][k] / aug[k][k]
                
                # Modificar los elementos de la fila i
                for j in range(k, n + 1):
                    aug[i][j] = aug[i][j] - factor * aug[k][j]
                
                # Registrar el paso de eliminación para la fila i
                self.steps.append({
                    "type": "elimination_row",
                    "matrix": copy.deepcopy(aug),
                    "description": f"Fila {i + 1} ← Fila {i + 1} - ({factor:.6g}) × Fila {k + 1}",
                    "details": {"source_row": k, "target_row": i, "factor": factor}
                })

        # Verificar si el último elemento diagonal es cero
        if abs(aug[n - 1][n - 1]) < 1e-12:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Error en la última fila: El elemento final en la diagonal principal es muy cercano a cero. El sistema es singular."
            }

        # Registrar matriz resultante de la eliminación
        self.steps.append({
            "type": "elimination_end",
            "matrix": copy.deepcopy(aug),
            "description": "Eliminación hacia adelante completada. Matriz triangular superior obtenida:"
        })

        # Proceso de Sustitución hacia atrás (Back-Substitution)
        x = [0.0] * n
        
        # Última incógnita
        x[n - 1] = aug[n - 1][n] / aug[n - 1][n - 1]
        back_sub_steps = []
        back_sub_steps.append({
            "var_index": n - 1,
            "val": x[n - 1],
            "formula": f"x[{n}] = {aug[n - 1][n]:.6g} / {aug[n - 1][n - 1]:.6g} = {x[n - 1]:.6g}"
        })
        
        # Resolver de n-2 hasta 0
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
