"""
Módulo del Método de Bisección (búsqueda de raíces de funciones).

Implementa el algoritmo Bisect(xl, xu, es, imax) siguiendo el
pseudocódigo de Chapra (docs/pseudocode/bisection.txt) y el algoritmo
paso a paso (docs/pseudocode/bisection_algo.md):

    FUNCTION Bisect(xl, xu, es, imax, xr, iter, ea)
        iter = 0
        DO
            xrold = xr
            xr = (xl + xu) / 2
            iter = iter + 1
            IF xr != 0 THEN
                ea = ABS((xr - xrold) / xr) * 100
            END IF
            test = f(xl) * f(xr)
            IF test < 0 THEN
                xu = xr
            ELSE IF test > 0 THEN
                xl = xr
            ELSE
                ea = 0       # raíz exacta encontrada
            END IF
            IF ea < es OR iter >= imax EXIT
        END DO
        Bisect = xr
    END Bisect

Requisito: f(xl) * f(xu) < 0 (cambio de signo en el intervalo). Si un
extremo ya es raíz (f(xl)==0 o f(xu)==0), se retorna éxito inmediato.
La función f se provee como expresión simbólica (string sympy) y se
evalúa con sympy en cada iteración.
"""
import copy

# SymPy: librería de matemática simbólica. Se usa para parsear la
# expresión f(x) del usuario y evaluarla en xl, xu, xr cada iteración.
# Documentación: https://docs.sympy.org/
import sympy


class BisectionMethod:
    """
    Clase que implementa el método de bisección para hallar raíces.

    Dado un intervalo [xl, xu] donde f(xl)*f(xu) < 0 (cambio de signo),
    divide el intervalo por mitades sucesivas hasta que el error
    relativo aproximado ea sea menor que la tolerancia es o se alcance
    el máximo de iteraciones imax.

    La clase entrega:
    - La raíz aproximada xr y el número de iteraciones.
    - El error relativo final y si convergió (ea < es).
    - El valor |f(xr)| para verificar qué tan cerca de cero está.
    - El paso a paso detallado (lista de diccionarios) para la GUI.
    """

    def __init__(self, f_expr, xl, xu, es=0.01, imax=100):
        """
        Inicializa el solucionador con la función y el intervalo.

        Parámetros:
        - f_expr: string con la expresión sympy de f(x), por ejemplo
          "x**3 - x - 2" o "cos(x) - x". Se parsea con sympy.sympify.
          Si es None, vacío o no se puede parsear, solve() retorna
          error.
        - xl: extremo inferior del intervalo (float).
        - xu: extremo superior del intervalo (float). Debe cumplir
          xl < xu.
        - es: tolerancia del error relativo aproximado en porcentaje
          (float). Default 0.01 (%). El bucle se detiene cuando
          ea < es.
        - imax: máximo número de iteraciones (int). Default 100. El
          bucle se detiene cuando iter >= imax.
        """
        # Copia de los extremos del intervalo para no alterar los
        # originales del llamador.
        self.xl = float(xl)
        self.xu = float(xu)
        self.es = float(es)
        self.imax = int(imax)
        # Expresión simbólica de la función (string crudo). Se parsea
        # en solve() para detectar errores de sintaxis allí y reportar
        # un mensaje claro.
        self.f_expr = f_expr
        # Lista donde se acumulan los pasos del algoritmo para la GUI.
        # Se reinicia al inicio de solve() para idempotencia.
        self.steps = []

    def solve(self):
        """
        Ejecuta el método de bisección.

        Retorna un diccionario con la misma estructura que los otros
        métodos (GaussSimple, LagrangeInterpolation, TrapezoidalRule):
        - success: bool, indica si el cálculo terminó correctamente.
        - solution: dict con los resultados (root, iterations, error,
          converged, f_value, xl_final, xu_final) o None si hubo error.
        - steps: lista de diccionarios describiendo cada iteración
          para visualización en la GUI.
        - error_message: mensaje de error en español o None si todo
          salió bien.
        """
        # Reiniciar pasos para idempotencia entre llamadas.
        self.steps = []

        # ---------------------------------------------------------------
        # VALIDACIÓN DE f_expr
        # La función es obligatoria y debe ser parseable por sympy.
        # ---------------------------------------------------------------
        if self.f_expr is None or (isinstance(self.f_expr, str)
                                   and self.f_expr.strip() == ""):
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Se requiere una función f(x) para aplicar el método de bisección.",
            }

        # Símbolo de la variable x para las evaluaciones con sympy.
        x_sym = sympy.Symbol('x')
        try:
            # Parsear la expresión del usuario.
            f_sym = sympy.sympify(self.f_expr)
        except Exception:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": (
                    f"No se pudo evaluar la expresión f(x) = "
                    f"'{self.f_expr}'. Verifique la sintaxis."
                ),
            }

        # ---------------------------------------------------------------
        # VALIDACIÓN DEL INTERVALO
        # xl debe ser estrictamente menor que xu.
        # ---------------------------------------------------------------
        if self.xl >= self.xu:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": (
                    f"El extremo inferior xl ({self.xl}) debe ser menor "
                    f"que el extremo superior xu ({self.xu})."
                ),
            }

        # ---------------------------------------------------------------
        # EVALUACIÓN DE f EN LOS EXTREMOS
        # Se necesita f(xl) y f(xu) para verificar el cambio de signo.
        # ---------------------------------------------------------------
        try:
            f_xl = float(f_sym.subs(x_sym, self.xl))
            f_xu = float(f_sym.subs(x_sym, self.xu))
        except Exception:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": (
                    "No se pudo evaluar la función en los extremos del "
                    "intervalo. Verifique que f(x) sea válida."
                ),
            }

        # ---------------------------------------------------------------
        # CASO ESPECIAL: raíz exacta en un extremo
        # Si f(xl)==0 o f(xu)==0, ya tenemos la raíz sin iterar.
        # ---------------------------------------------------------------
        if abs(f_xl) < 1e-12:
            root = self.xl
            self.steps.append({
                "type": "initial",
                "xl": self.xl, "xu": self.xu,
                "es": self.es, "imax": self.imax,
                "f_expr": self.f_expr,
                "f_xl": f_xl, "f_xu": f_xu,
                "description": (
                    f"Datos de entrada: f(x) = {self.f_expr}, "
                    f"intervalo [{self.xl}, {self.xu}], "
                    f"es = {self.es}%, imax = {self.imax}. "
                    f"f(xl) = {f_xl:.6g} (raíz exacta en xl)."
                ),
            })
            self.steps.append({
                "type": "final",
                "root": root, "iterations": 0, "error": 0.0,
                "converged": True, "reason": "raiz_exacta",
                "description": (
                    f"Raíz exacta encontrada en xl = {root:.6g}. "
                    f"iter = 0, ea = 0%."
                ),
            })
            return {
                "success": True,
                "solution": {
                    "root": root,
                    "iterations": 0,
                    "error": 0.0,
                    "converged": True,
                    "f_value": f_xl,
                    "xl_final": self.xl,
                    "xu_final": self.xu,
                },
                "steps": self.steps,
                "error_message": None,
            }

        if abs(f_xu) < 1e-12:
            root = self.xu
            self.steps.append({
                "type": "initial",
                "xl": self.xl, "xu": self.xu,
                "es": self.es, "imax": self.imax,
                "f_expr": self.f_expr,
                "f_xl": f_xl, "f_xu": f_xu,
                "description": (
                    f"Datos de entrada: f(x) = {self.f_expr}, "
                    f"intervalo [{self.xl}, {self.xu}], "
                    f"es = {self.es}%, imax = {self.imax}. "
                    f"f(xu) = {f_xu:.6g} (raíz exacta en xu)."
                ),
            })
            self.steps.append({
                "type": "final",
                "root": root, "iterations": 0, "error": 0.0,
                "converged": True, "reason": "raiz_exacta",
                "description": (
                    f"Raíz exacta encontrada en xu = {root:.6g}. "
                    f"iter = 0, ea = 0%."
                ),
            })
            return {
                "success": True,
                "solution": {
                    "root": root,
                    "iterations": 0,
                    "error": 0.0,
                    "converged": True,
                    "f_value": f_xu,
                    "xl_final": self.xl,
                    "xu_final": self.xu,
                },
                "steps": self.steps,
                "error_message": None,
            }

        # ---------------------------------------------------------------
        # VERIFICACIÓN DE CAMBIO DE SIGNO
        # Requerimiento del algoritmo (paso 1 de bisection_algo.md).
        # ---------------------------------------------------------------
        test_sign = f_xl * f_xu
        if test_sign > 0:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": (
                    f"No hay cambio de signo en el intervalo: "
                    f"f({self.xl}) = {f_xl:.6g} y f({self.xu}) = "
                    f"{f_xu:.6g} tienen el mismo signo. La bisección "
                    f"requiere f(xl)*f(xu) < 0."
                ),
            }

        # ---------------------------------------------------------------
        # REGISTRO DEL ESTADO INICIAL
        # ---------------------------------------------------------------
        self.steps.append({
            "type": "initial",
            "xl": self.xl, "xu": self.xu,
            "es": self.es, "imax": self.imax,
            "f_expr": self.f_expr,
            "f_xl": f_xl, "f_xu": f_xu,
            "description": (
                f"Datos de entrada: f(x) = {self.f_expr}, "
                f"intervalo [{self.xl}, {self.xu}], "
                f"es = {self.es}%, imax = {self.imax}. "
                f"f(xl) = {f_xl:.6g}, f(xu) = {f_xu:.6g} "
                f"(cambio de signo verificado)."
            ),
        })

        # ---------------------------------------------------------------
        # BUCLE PRINCIPAL (pseudocódigo Bisect)
        # Pre-loop: xr = xl (convención, ver D2 del design.md). En la
        # primera iteración xrold = xl y el primer xr es el midpoint.
        # ---------------------------------------------------------------
        xl = self.xl
        xu = self.xu
        xr = xl       # convención pre-loop
        iter_count = 0
        ea = 100.0    # error inicial grande para no salir en iter 1
        converged = False
        reason = "max_iter"

        while True:
            # Guardar el xr anterior y calcular el nuevo midpoint.
            xrold = xr
            xr = (xl + xu) / 2.0
            iter_count += 1

            # Error relativo aproximado (saltar si xr == 0).
            if xr != 0:
                ea = abs((xr - xrold) / xr) * 100.0

            # Evaluar f(xl) (ya teníamos f_xl pero xl puede cambiar)
            # y f(xr) en este punto del bucle.
            f_xl_cur = float(f_sym.subs(x_sym, xl))
            f_xr_cur = float(f_sym.subs(x_sym, xr))
            test = f_xl_cur * f_xr_cur

            # Ramificación según el signo de test = f(xl)*f(xr).
            if test < 0:
                # Raíz en el subintervalo inferior → mover xu.
                xu = xr
                action = "xu = xr"
            elif test > 0:
                # Raíz en el subintervalo superior → mover xl.
                xl = xr
                action = "xl = xr"
            else:
                # test == 0: raíz exacta en xr.
                ea = 0.0
                action = "raiz_exacta"

            # Registrar la iteración para la GUI.
            self.steps.append({
                "type": "iteration",
                "iter": iter_count,
                "xl": xl, "xu": xu,
                "xr": xr, "xrold": xrold,
                "ea": ea, "test": test,
                "action": action,
                "f_xl": f_xl_cur, "f_xr": f_xr_cur,
                "description": (
                    f"iter {iter_count}: xr = ({xl:.6g} + "
                    f"{xu:.6g})/2 = {xr:.6g}  |  ea = {ea:.6g}%  "
                    f"|  test = f({xl:.6g})*f({xr:.6g}) = "
                    f"{test:.6g}  →  {action}"
                ),
            })

            # Criterios de salida del pseudocódigo.
            if action == "raiz_exacta":
                converged = True
                reason = "raiz_exacta"
                break
            if ea < self.es:
                converged = True
                reason = "tolerancia"
                break
            if iter_count >= self.imax:
                converged = False
                reason = "max_iter"
                break

        # ---------------------------------------------------------------
        # VALOR f(xr) FINAL
        # Para reportar qué tan cerca de cero está la raíz hallada.
        # ---------------------------------------------------------------
        f_xr_final = float(f_sym.subs(x_sym, xr))

        # ---------------------------------------------------------------
        # PASO FINAL
        # ---------------------------------------------------------------
        self.steps.append({
            "type": "final",
            "root": xr, "iterations": iter_count, "error": ea,
            "converged": converged, "reason": reason,
            "description": (
                f"Resultado: raíz = {xr:.6g}  |  iter = "
                f"{iter_count}  |  ea = {ea:.6g}%  |  "
                f"converged = {converged}  |  razón = "
                f"{'tolerancia alcanzada' if reason == 'tolerancia' else 'raíz exacta' if reason == 'raiz_exacta' else 'máximo de iteraciones'}"
            ),
        })

        # ---------------------------------------------------------------
        # RESULTADO
        # ---------------------------------------------------------------
        return {
            "success": True,
            "solution": {
                # Raíz aproximada hallada.
                "root": xr,
                # Número de iteraciones realizadas.
                "iterations": iter_count,
                # Error relativo aproximado final (%).
                "error": ea,
                # True si salió por tolerancia o raíz exacta.
                "converged": converged,
                # |f(xr)| — qué tan cerca de cero está la raíz.
                "f_value": f_xr_final,
                # Intervalo final [xl, xu] después de iterar.
                "xl_final": xl,
                "xu_final": xu,
            },
            "steps": self.steps,
            "error_message": None,
        }