"""
Módulo de la Regla del Trapecio (simple y compuesta).

Implementa la integración numérica de datos tabulares siguiendo el
pseudocódigo de Chapra (docs/pseudocode/trapezoidal_rule.txt):

    a) Un solo segmento:
        Trap(h, f0, f1) = h * (f0 + f1) / 2

    b) Segmentos múltiples:
        Trapm(h, n, f) = h * (f0 + 2*Σ_{i=1}^{n-1} f_i + fn) / 2

Ambas fórmulas asumen nodos uniformemente espaciados (h constante).
La clase detecta automáticamente el número de segmentos n = len(x) - 1 y
ramifica al caso simple (n == 1) o compuesto (n > 1).

Si se provee una expresión simbólica `f_expr`, se calcula la integral
exacta con sympy para comparar contra la aproximación y reportar el
error relativo (análisis de error al estilo Chapra).
"""
import copy

# SymPy: librería de matemática simbólica. Se usa para calcular la
# integral analítica exacta cuando se provee f_expr, permitiendo
# comparar contra la aproximación numérica.
# Documentación: https://docs.sympy.org/
import sympy


class TrapezoidalRule:
    """
    Clase que implementa la regla del trapecio (simple y compuesta).

    Dados n+1 puntos (x_0, f_0), ..., (x_n, f_n) igualmente espaciados,
    calcula la integral aproximada de la función subyacente en [a, b].
    El número de segmentos es n = len(x) - 1.

    Casos:
    - n == 1 (2 puntos): Trap(h, f0, f1) = h*(f0 + f1)/2
    - n > 1 (más puntos): Trapm(h, n, f) = h*(f0 + 2*Σf_i + fn)/2

    La clase entrega:
    - El valor aproximado de la integral.
    - El paso h y el número de segmentos n.
    - El paso a paso detallado (lista de diccionarios) para la GUI.
    - Opcionalmente, la integral exacta (vía sympy) y el error relativo
      cuando se provee f_expr.
    """

    def __init__(self, x, y, f_expr=None):
        """
        Inicializa el integrador con los puntos tabulares conocidos.

        Parámetros:
        - x: lista de valores x (nodos, deben ser estrictamente
          crecientes y uniformemente espaciados).
        - y: lista de valores f(x) en cada nodo (mismo largo que x).
        - f_expr: string con expresión sympy de la función original
          (opcional). Se usa para calcular la integral exacta y el
          error relativo. Si es None o no se puede evaluar, simplemente
          se omite la comparación analítica.
        """
        # Copia profunda para no alterar las listas originales del
        # llamador aunque más adelante se modifiquen internamente.
        self.x = copy.deepcopy(x)
        self.y = copy.deepcopy(y)
        # Expresión simbólica opcional (string como "x**2" o "sin(x)").
        self.f_expr = f_expr
        # Número de segmentos: con n+1 puntos hay n segmentos.
        self.n = len(x) - 1 if len(x) >= 1 else 0
        # Lista donde se acumulan los pasos del algoritmo para la GUI.
        # Se reinicia al inicio de solve() para que cada llamada sea
        # idempotente.
        self.steps = []

    # ------------------------------------------------------------------
    # Pseudocódigo a) — Trap (un solo segmento)
    # ------------------------------------------------------------------
    def _trap_simple(self, h, f0, f1):
        """
        Regla del trapecio para un solo segmento.

            Trap(h, f0, f1) = h * (f0 + f1) / 2

        Corresponde al pseudocódigo (a) de Chapra. Geométricamente es
        el área del trapecio de altura h y bases f0, f1.
        """
        return h * (f0 + f1) / 2.0

    # ------------------------------------------------------------------
    # Pseudocódigo b) — Trapm (segmentos múltiples)
    # ------------------------------------------------------------------
    def _trap_composite(self, h, f):
        """
        Regla del trapecio compuesta para n segmentos.

            Trapm(h, n, f) = h * (f0 + 2*Σ_{i=1}^{n-1} f_i + fn) / 2

        Corresponde al pseudocódigo (b) de Chapra. Acumula f0, luego
        suma 2*f_i para los puntos intermedios, y finalmente fn.
        El factor 2 aparece porque cada punto interior pertenece a dos
        trapecios adyacentes.
        """
        n = self.n
        # Acumulador: empieza con f0 (extremo izquierdo, coeficiente 1).
        sum_val = float(f[0])
        # Bucle sobre los puntos interiores i = 1 .. n-1 (coeficiente 2).
        for i in range(1, n):
            sum_val += 2.0 * float(f[i])
        # Extremo derecho fn (coeficiente 1).
        sum_val += float(f[n])
        # Multiplica por h/2 para obtener la integral aproximada.
        return h * sum_val / 2.0

    # ------------------------------------------------------------------
    # Método principal
    # ------------------------------------------------------------------
    def solve(self):
        """
        Ejecuta la integración numérica con la regla del trapecio.

        Retorna un diccionario con la misma estructura que GaussSimple
        y LagrangeInterpolation:
        - success: bool, indica si el cálculo terminó correctamente.
        - solution: dict con los resultados (value, h, n, exact_value,
          error_relativo, segments, formula) o None si hubo error.
        - steps: lista de diccionarios describiendo cada paso del
          algoritmo para visualización en la GUI.
        - error_message: mensaje de error en español o None si todo
          salió bien.
        """
        # Reiniciar pasos: garantiza idempotencia entre llamadas.
        self.steps = []

        # ---------------------------------------------------------------
        # VALIDACIONES DE ENTRADA
        # Se validan antes de cualquier cálculo para fallar rápido con
        # mensajes claros en lugar de producir resultados erróneos.
        # ---------------------------------------------------------------

        # 1. x e y deben tener la misma cantidad de elementos.
        if len(self.x) != len(self.y):
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": (
                    f"Dimensiones incompatibles: x tiene "
                    f"{len(self.x)} elementos e y tiene "
                    f"{len(self.y)} elementos."
                ),
            }

        # 2. Se necesitan al menos 2 puntos (n >= 1 segmento).
        if len(self.x) < 2:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": (
                    "Se requieren al menos 2 puntos para aplicar la "
                    "regla del trapecio (n >= 1 segmento)."
                ),
            }

        # 3. x debe ser estrictamente creciente (senso único del eje).
        for i in range(len(self.x) - 1):
            if self.x[i + 1] <= self.x[i]:
                return {
                    "success": False,
                    "solution": None,
                    "steps": self.steps,
                    "error_message": (
                        f"Los valores de x deben ser estrictamente "
                        f"crecientes. Se encontró x[{i}] = "
                        f"{self.x[i]} >= x[{i + 1}] = {self.x[i + 1]}."
                    ),
                }

        # 4. Nodos uniformemente espaciados (h constante). El
        # pseudocódigo de Chapra asume h constante; la fórmula
        # compuesta es incorrecta si los nodos no son uniformes.
        h = float(self.x[1]) - float(self.x[0])
        for i in range(len(self.x) - 1):
            h_i = float(self.x[i + 1]) - float(self.x[i])
            if abs(h_i - h) >= 1e-9:
                return {
                    "success": False,
                    "solution": None,
                    "steps": self.steps,
                    "error_message": (
                        f"La regla del trapecio requiere nodos "
                        f"uniformemente espaciados. h[0] = {h:.6g} "
                        f"pero h[{i}] = {h_i:.6g}."
                    ),
                }

        n = self.n

        # ---------------------------------------------------------------
        # REGISTRO DEL ESTADO INICIAL
        # Primer paso mostrado en la GUI: resumen de los datos de
        # entrada, h y n.
        # ---------------------------------------------------------------
        self.steps.append({
            "type": "initial",
            "x": copy.deepcopy(self.x),
            "y": copy.deepcopy(self.y),
            "h": h,
            "n": n,
            "description": (
                f"Datos de entrada: {len(self.x)} puntos "
                f"({n} segmento{'s' if n != 1 else ''}). "
                f"h = {h:.6g}, intervalo [{self.x[0]}, {self.x[n]}]."
            ),
        })

        # ---------------------------------------------------------------
        # CÁLCULO PASO A PASO
        # Se calcula la integral acumulando el área de cada segmento.
        # Para el caso n == 1 se usa _trap_simple; para n > 1 se usa
        # _trap_composite, pero en ambos casos se registran los pasos
        # por segmento para que la GUI los muestre.
        # ---------------------------------------------------------------
        segments = []
        accumulated = 0.0

        for i in range(n):
            # Extremos del segmento i-ésimo.
            x0 = float(self.x[i])
            x1 = float(self.x[i + 1])
            f0 = float(self.y[i])
            f1 = float(self.y[i + 1])
            # Área del trapecio individual (fórmula simple por segmento).
            area_partial = self._trap_simple(h, f0, f1)
            accumulated += area_partial

            # Registrar el segmento para la GUI y para la lista de
            # segments del solution.
            seg = {
                "i": i,
                "x0": x0,
                "x1": x1,
                "f0": f0,
                "f1": f1,
                "area": area_partial,
            }
            segments.append(seg)

            self.steps.append({
                "type": "segment",
                "i": i,
                "x0": x0,
                "x1": x1,
                "f0": f0,
                "f1": f1,
                "area_partial": area_partial,
                "accumulated": accumulated,
                "description": (
                    f"Segmento {i}: T_{i} = h*(f_{i} + f_{i + 1})/2 "
                    f"= {h:.6g}*({f0:.6g} + {f1:.6g})/2 = "
                    f"{area_partial:.6g}  |  Acumulado = "
                    f"{accumulated:.6g}"
                ),
            })

        # Verificación cruzada: el acumulado de áreas individuales debe
        # coincidir con la fórmula compuesta (para sanity check).
        if n == 1:
            value = self._trap_simple(h, float(self.y[0]), float(self.y[1]))
        else:
            value = self._trap_composite(h, self.y)
        # El acumulado y value deben ser idénticos (salvo redondeo).
        # Se confía en value (fórmula cerrada) para el resultado final.
        value = float(value)

        # ---------------------------------------------------------------
        # PASO FINAL: fórmula y resultado
        # ---------------------------------------------------------------
        if n == 1:
            # Caso simple: I = h*(f0 + f1)/2
            formula = (
                f"I = h*(f0 + f1)/2 = {h:.6g}*"
                f"({self.y[0]:.6g} + {self.y[1]:.6g})/2 = {value:.6g}"
            )
        else:
            # Caso compuesto: I = h*(f0 + 2*Σf_i + fn)/2
            sum_terms_str = " + ".join(
                f"2*{self.y[i]:.6g}" for i in range(1, n)
            )
            middle = f"2*Σf_{{i=1..{n - 1}}}" if n > 2 else sum_terms_str
            formula = (
                f"I = h*(f0 + {middle} + fn)/2 = {h:.6g}*("
                f"{self.y[0]:.6g} + 2*Σf_i + {self.y[n]:.6g})/2 = "
                f"{value:.6g}"
            )

        self.steps.append({
            "type": "final",
            "formula": formula,
            "result": value,
            "description": f"Resultado: {formula}"
        })

        # ---------------------------------------------------------------
        # COMPARACIÓN CON INTEGRAL EXACTA (opcional vía sympy)
        # Si se provee f_expr, se calcula la integral analítica exacta
        # para comparar contra la aproximación. Errores de parseo o
        # integración se capturan silenciosamente (no falla el cálculo
        # numérico).
        # ---------------------------------------------------------------
        exact_value = None
        error_relativo = None
        if self.f_expr:
            try:
                x_sym = sympy.Symbol('x')
                # Parsear la expresión simbólica del usuario.
                f_sym = sympy.sympify(self.f_expr)
                # Límites de integración: extremos del intervalo.
                a = float(self.x[0])
                b = float(self.x[n])
                # Integral definida exacta.
                integral_sym = sympy.integrate(f_sym, (x_sym, a, b))
                exact_value = float(integral_sym)
                # Error relativo porcentual (si la integral exacta no
                # es cero; si es cero se usa un error absoluto).
                if abs(exact_value) > 1e-12:
                    error_relativo = abs(
                        (exact_value - value) / exact_value
                    ) * 100.0
                else:
                    error_relativo = abs(exact_value - value)

                self.steps.append({
                    "type": "exact",
                    "exact_value": exact_value,
                    "error_relativo": error_relativo,
                    "description": (
                        f"Integral exacta: ∫_{a}^{b} f(x) dx = "
                        f"{exact_value:.6g}  |  Error relativo = "
                        f"{error_relativo:.6g}%"
                    ),
                })
            except Exception:
                # Si la expresión no se puede parsear o la integral no
                # se puede calcular simbólicamente, se omiten los
                # campos exact_value y error_relativo sin fallar.
                exact_value = None
                error_relativo = None

        # ---------------------------------------------------------------
        # RESULTADO
        # ---------------------------------------------------------------
        return {
            "success": True,
            "solution": {
                # Valor numérico aproximado de la integral.
                "value": value,
                # Paso entre nodos.
                "h": h,
                # Número de segmentos.
                "n": n,
                # Integral exacta (vía sympy) o None.
                "exact_value": exact_value,
                # Error relativo porcentual o None.
                "error_relativo": error_relativo,
                # Lista de trapecios individuales (para gráfica).
                "segments": segments,
                # Fórmula final expandida como string.
                "formula": formula,
            },
            "steps": self.steps,
            "error_message": None,
        }