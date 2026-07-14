"""Método de Bisección. Ver docs/metodos/bisection.md."""
import copy
import sympy


class BisectionMethod:
    """
    Método de bisección para hallar raíces de funciones.
    Dado [xl, xu] con f(xl)*f(xu) < 0, divide el intervalo por
    mitades hasta que ea < es o iter >= imax.
    """
    def __init__(self, f_expr, xl, xu, es=0.01, imax=100):
        self.xl = float(xl)
        self.xu = float(xu)
        self.es = float(es)
        self.imax = int(imax)
        self.f_expr = f_expr
        self.steps = []

    def solve(self):
        self.steps = []

        if self.f_expr is None or (isinstance(self.f_expr, str)
                                   and self.f_expr.strip() == ""):
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": "Se requiere una función f(x) para aplicar el método de bisección.",
            }

        x_sym = sympy.Symbol('x')
        try:
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

        xl = self.xl
        xu = self.xu
        xr = xl
        iter_count = 0
        ea = 100.0
        converged = False
        reason = "max_iter"

        while True:
            xrold = xr
            xr = (xl + xu) / 2.0
            iter_count += 1

            if xr != 0:
                ea = abs((xr - xrold) / xr) * 100.0

            f_xl_cur = float(f_sym.subs(x_sym, xl))
            f_xr_cur = float(f_sym.subs(x_sym, xr))
            test = f_xl_cur * f_xr_cur

            if test < 0:
                xu = xr
                action = "xu = xr"
            elif test > 0:
                xl = xr
                action = "xl = xr"
            else:
                ea = 0.0
                action = "raiz_exacta"

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

            if action == "raiz_exacta":
                converged = True
                reason = "raiz_exacta"
                break
            if ea < self.es or abs(f_xr_cur) <= self.es:
                converged = True
                reason = "tolerancia"
                break
            if iter_count >= self.imax:
                converged = False
                reason = "max_iter"
                break

        f_xr_final = float(f_sym.subs(x_sym, xr))

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

        return {
            "success": True,
            "solution": {
                "root": xr,
                "iterations": iter_count,
                "error": ea,
                "converged": converged,
                "f_value": f_xr_final,
                "xl_final": xl,
                "xu_final": xu,
            },
            "steps": self.steps,
            "error_message": None,
        }
