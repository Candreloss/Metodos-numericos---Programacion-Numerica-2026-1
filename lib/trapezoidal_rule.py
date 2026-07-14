"""Regla del Trapecio (simple y compuesta). Ver docs/metodos/trapezoidal_rule.md."""
import copy
import sympy


class TrapezoidalRule:
    """
    Integración numérica con regla del trapecio.
    n=1: Trap(h,f0,f1) = h*(f0+f1)/2
    n>1: Trapm(h,n,f) = h*(f0+2*Σf_i+fn)/2
    provee f_expr para comparación con integral exacta via sympy.
    """
    def __init__(self, x, y, f_expr=None):
        self.x = copy.deepcopy(x)
        self.y = copy.deepcopy(y)
        self.f_expr = f_expr
        self.n = len(x) - 1 if len(x) >= 1 else 0
        self.steps = []

    def _trap_simple(self, h, f0, f1):
        return h * (f0 + f1) / 2.0

    def _trap_composite(self, h, f):
        n = self.n
        sum_val = float(f[0])
        for i in range(1, n):
            sum_val += 2.0 * float(f[i])
        sum_val += float(f[n])
        return h * sum_val / 2.0

    def solve(self):
        self.steps = []

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

        segments = []
        accumulated = 0.0

        for i in range(n):
            x0 = float(self.x[i])
            x1 = float(self.x[i + 1])
            f0 = float(self.y[i])
            f1 = float(self.y[i + 1])
            area_partial = self._trap_simple(h, f0, f1)
            accumulated += area_partial

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

        if n == 1:
            value = self._trap_simple(h, float(self.y[0]), float(self.y[1]))
        else:
            value = self._trap_composite(h, self.y)
        value = float(value)

        if n == 1:
            formula = (
                f"I = h*(f0 + f1)/2 = {h:.6g}*"
                f"({self.y[0]:.6g} + {self.y[1]:.6g})/2 = {value:.6g}"
            )
        else:
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

        exact_value = None
        error_relativo = None
        if self.f_expr:
            try:
                x_sym = sympy.Symbol('x')
                f_sym = sympy.sympify(self.f_expr)
                a = float(self.x[0])
                b = float(self.x[n])
                integral_sym = sympy.integrate(f_sym, (x_sym, a, b))
                exact_value = float(integral_sym)
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
                exact_value = None
                error_relativo = None

        return {
            "success": True,
            "solution": {
                "value": value,
                "h": h,
                "n": n,
                "exact_value": exact_value,
                "error_relativo": error_relativo,
                "segments": segments,
                "formula": formula,
            },
            "steps": self.steps,
            "error_message": None,
        }
