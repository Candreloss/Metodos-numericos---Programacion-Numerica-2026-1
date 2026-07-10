# Módulo de copia profunda para evitar modificar las listas origiciales que
# entrega el llamador. Se usa copy.deepcopy porque las listas pueden contener
# valores anidados (matrices) y deepcopy replica de forma recursiva.
import copy

# SymPy: librería de matemática simbólica. Permite construir el polinomio
# de Lagrange como expresión algebraica (no solo numérica), expandirlo a su
# forma estándar de potencias y evaluarlo en cualquier punto.
# Documentación: https://docs.sympy.org/
import sympy


class LagrangeInterpolation:
    """
    Clase que implementa el método de Interpolación de Lagrange.

    Dados n+1 puntos (x_0,y_0),...,(x_n,y_n) construye el único polinomio de
    grado n que pasa por todos ellos. La fórmula es:

        P(x) = Σ_{i=0}^{n} y_i · L_i(x)

    donde cada L_i(x) es la i-ésima base de Lagrange:

        L_i(x) = Π_{j=0, j≠i}^{n} (x - x_j) / (x_i - x_j)

    Propiedades de la base: L_i(x_i) = 1 y L_i(x_j) = 0 para i ≠ j, lo que
    garantiza que P(x_i) = y_i (el polinomio pasa por todos los datos).

    La clase entrega:
    - El polinomio expandido como expresión simbólica de sympy.
    - La evaluación numérica del polinomio en un punto específico.
    - El paso a paso detallado (lista de diccionarios) para visualización
      posterior en la interfaz gráfica.
    """

    def __init__(self, x, y, eval_point):
        """
        Inicializa el interpolador con los puntos conocidos y el punto a evaluar.

        Parámetros:
        - x: lista de valores x (puntos conocidos, abscisas).
        - y: lista de valores y (puntos conocidos, ordenadas).
        - eval_point: valor numérico donde se evaluará el polinomio P(x).
        """
        # Copia profunda de las listas para no alterar las originales del
        # llamador aunque más adelante se modifiquen internamente.
        self.x = copy.deepcopy(x)
        self.y = copy.deepcopy(y)
        # Punto de evaluación (escalar, no requiere copia profunda).
        self.eval_point = eval_point
        # Número de puntos de datos. El polinomio resultante será de grado n-1.
        self.n = len(x)
        # Lista donde se acumulan los pasos del algoritmo para la GUI.
        # Se reinicia al inicio de solve() para que cada llamada sea idempotente.
        self.steps = []

    def solve(self):
        """
        Ejecuta la interpolación de Lagrange.

        Retorna un diccionario con la misma estructura que GaussSimple:
        - success: bool, indica si el cálculo terminó correctamente.
        - solution: dict con los resultados (value, symbolic_value, polynomial,
          polynomial_expr, basis) o None si hubo error.
        - steps: lista de diccionarios describiendo cada paso del algoritmo.
        - error_message: mensaje de error en español o None si todo salió bien.
        """
        # Reiniciar pasos: garantiza que llamadas repetidas a solve() partan
        # de cero y no acumulen pasos de ejecuciones anteriores.
        self.steps = []

        # ---------------------------------------------------------------
        # VALIDACIONES DE ENTRADA
        # Se validan antes de any cálculo para fallar rápido con mensajes
        # claros en lugar de producir excepciones crípticas más adelante.
        # ---------------------------------------------------------------

        # 1. x e y deben tener la misma cantidad de elementos.
        # Sin esto, no se puede formar un conjunto coherente de puntos (x,y).
        if len(self.x) != len(self.y):
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": f"Dimensiones incompatibles: x tiene {len(self.x)} elementos e y tiene {len(self.y)} elementos.",
            }

        # 2. Se necesitan al menos 2 puntos: con 1 punto no se puede definir
        # un polinomio interpolante (grado mínimo 1 = recta con 2 puntos).
        if self.n < 2:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Se requieren al menos 2 puntos para construir el polinomio de interpolación.",
            }

        # 3. Los valores de x deben ser distintos entre sí.
        # Si existiera un valor x duplicado, el denominador (x_i - x_j) sería
        # cero y se generaría una división indeterminada => error matemático.
        # Se usa una tolerancia 1e-12 para comparar floats por posibles
        # errores de redondeo.
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if abs(self.x[i] - self.x[j]) < 1e-12:
                    return {
                        "success": False,
                        "solution": None,
                        "steps": self.steps,
                        "error_message": f"Los valores de x deben ser distintos. Se encontró un valor duplicado: x[{i}] = x[{j}] = {self.x[i]}.",
                    }

        # ---------------------------------------------------------------
        # REGISTRO DEL ESTADO INICIAL
        # Primer paso mostrado en la GUI: resumen de los datos de entrada.
        # Se copian de nuevo las listas para que la GUI muestre los datos
        # tal cual entraron y no una referencia mutable.
        # ---------------------------------------------------------------
        self.steps.append({
            "type": "initial",
            "x": copy.deepcopy(self.x),
            "y": copy.deepcopy(self.y),
            "eval_point": self.eval_point,
            "description": f"Datos de entrada: {self.n} puntos. Punto de evaluación x = {self.eval_point}."
        })

        # ---------------------------------------------------------------
        # CONSTRUCCIÓN SIMBÓLICA DEL POLINOMIO
        # Se construye P(x) usando sympy para obtener una expresión algebraica
        # que la GUI puede mostrar como texto (ej: "x**2 + 2*x - 1").
        # ---------------------------------------------------------------

        # Símbolo de variable: representa x en la expresión simbólica.
        # Se usará en los productos (x - x_j) de cada base L_i.
        x_sym = sympy.Symbol('x')
        # Acumulador de la expresión simbólica del polinomio completo.
        # Parte de 0 y se le suman y_i * L_i(x).
        poly_expr = 0
        # Lista donde se guardan las n bases L_i(x) por separado (expresiones
        # sympy sin simplificar). Servirá para que la GUI muestre cada base.
        basis_exprs = []

        # Para cada punto i, construir su base L_i(x) y sumar y_i*L_i al total.
        for i in range(self.n):
            # Numerador: Π_{j≠i} (x - x_j). Empieza en 1 (elemento neutro del
            # producto) y se van multiplicando los términos lineales.
            numerator = 1
            # Denominador: Π_{j≠i} (x_i - x_j). Es una constante (no depende de
            # x) que normaliza la base para que L_i(x_i) = 1.
            denominator = 1
            for j in range(self.n):
                # Se excluye j=i porque (x_i - x_i) = 0 haría el producto cero.
                if i != j:
                    numerator *= (x_sym - self.x[j])
                    denominator *= (self.x[i] - self.x[j])
            # Base de Lagrange L_i(x) = numerador / denominador.
            L_i = numerator / denominator
            # Guardar la base para referencia externa (GUI/tests).
            basis_exprs.append(L_i)
            # Acumular el término y_i * L_i(x) en el polinomio total.
            poly_expr += self.y[i] * L_i

        # Expandir el polinomio: sympy lo reorganiza a la forma estándar de
        # potencias de x (ej: del producto (x-1)(x-2) pasa a x**2 - 3*x + 2).
        # Esto facilita la lectura por el usuario y la comparación con un
        # polinomio esperado.
        poly_expanded = sympy.expand(poly_expr)
        # Representación en texto para mostrar en la GUI / logs.
        poly_str = str(poly_expanded)

        # ---------------------------------------------------------------
        # EVALUACIÓN NUMÉRICA PASO A PASO
        # Sigue el pseudocódigo Lagrng(x, y, n, x) provisto en
        # docs/pseudocode/lagrange_interpolation.txt.
        # Se calcula P(eval_point) con doble bucle: para cada i se calcula el
        # producto de y_i por todos los cocientes (eval_point - x_j)/(x_i - x_j),
        # y luego se suman todos esos productos.
        # Cada subpaso se registra en self.steps para que la GUI lo muestre.
        # ---------------------------------------------------------------

        # Acumulador de la suma total Σ y_i * L_i(eval_point).
        sum_val = 0.0

        # Bucle exterior: recorre cada base i.
        for i in range(self.n):
            # product arranca en y_i (el coeficiente del término actual).
            # Observación: en el pseudocódigo "product = yi" porque el
            # producto empieza valiendo y_i y luego se multiplica por los
            # cocientes correspondientes.
            product = float(self.y[i])
            # Registrar el inicio del cálculo de la base i-ésima.
            self.steps.append({
                "type": "basis_start",
                "i": i,
                "description": f"Cálculo de L_{i}(x) · y_{i}:"
            })

            # Bucle interior: recorre cada j para multiplicar el cociente
            # correspondiente al término (x - x_j)/(x_i - x_j) con j ≠ i.
            for j in range(self.n):
                if i != j:
                    # Numerador del cociente: (eval_point - x_j).
                    factor_num = (self.eval_point - self.x[j])
                    # Denominador del cociente: (x_i - x_j) (constante).
                    factor_den = (self.x[i] - self.x[j])
                    # Valor del cociente completo.
                    term_val = factor_num / factor_den
                    # Acumular el cociente en el producto del término i.
                    product *= term_val
                    # Registrar detalle del término j para la GUI.
                    self.steps.append({
                        "type": "term",
                        "i": i,
                        "j": j,
                        "term": f"(x - {self.x[j]}) / ({self.x[i]} - {self.x[j]})",
                        "term_value": term_val,
                        "product_so_far": product,
                        "description": f"Término j={j}: ({self.eval_point} - {self.x[j]}) / ({self.x[i]} - {self.x[j]}) = {term_val:.6g}"
                    })

            # Fin del cálculo de la base i: product = y_i * L_i(eval_point).
            # li_value aísla L_i(eval_point) dividiendo product por y_i
            # (salvo cuando y_i = 0, en cuyo caso L_i es 0 por convención).
            self.steps.append({
                "type": "basis_end",
                "i": i,
                "li_value": float(product) / float(self.y[i]) if float(self.y[i]) != 0 else 0.0,
                "product_value": product,
                "description": f"L_{i}({self.eval_point}) = {float(product) / float(self.y[i]):.6g} | y_{i} · L_{i} = {product:.6g}"
            })
            # Acumular el término en la suma total.
            sum_val += product

        # ---------------------------------------------------------------
        # PASO FINAL: suma y presentación del polinomio
        # ---------------------------------------------------------------

        # Registrar la suma final con el resultado numérico.
        self.steps.append({
            "type": "sum",
            "description": f"Suma de todos los términos: P({self.eval_point}) = Σ y_i · L_i({self.eval_point})",
            "result": sum_val
        })

        # Registrar el polinomio expandido como texto para la GUI.
        self.steps.append({
            "type": "polynomial",
            "polynomial": poly_str,
            "description": "Polinomio de Lagrange expandido:"
        })

        # ---------------------------------------------------------------
        # VERIFICACIÓN SIMBÓLICA
        # Se reevalúa el polinomio expandido con sympy en el mismo punto
        # usando subs(). Sirve como verificación cruzada: el valor obtenido
        # por la ruta numérica (sum_val) debe coincidir con el de la ruta
        # simbólica (symbolic_eval). Si difieren, hay un bug en la lógica.
        # ---------------------------------------------------------------
        symbolic_eval = float(poly_expanded.subs(x_sym, self.eval_point))

        # ---------------------------------------------------------------
        # RESULTADO
        # ---------------------------------------------------------------
        return {
            "success": True,
            "solution": {
                # Valor numérico calculado paso a paso (ruta pseudocódigo).
                "value": sum_val,
                # Valor numérico calculado desde la expresión simbólica.
                "symbolic_value": symbolic_eval,
                # Polinomio expandido como string legible.
                "polynomial": poly_str,
                # Expresión sympy cruda (objeto Expr) para uso avanzado.
                "polynomial_expr": poly_expanded,
                # Lista con las n bases L_i(x) como expresiones sympy.
                "basis": basis_exprs,
            },
            "steps": self.steps,
            "error_message": None
        }