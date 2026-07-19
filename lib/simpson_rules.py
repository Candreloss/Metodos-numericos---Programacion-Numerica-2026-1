"""Reglas de Simpson (1/3, 3/8, compuesta y combinada). Ver docs/pseudocode/simpson_rules.txt."""
import copy

import sympy


class ReglasSimpson:
    """
    Integración numérica con reglas de Simpson.

    metodo:
      "simp13"  — Simpson 1/3 simple (3 puntos, 2 segmentos, h uniforme)
      "simp38"  — Simpson 3/8 simple (4 puntos, 3 segmentos, h uniforme)
      "simp13m" — Simpson 1/3 múltiple (n par >= 2, h uniforme)
      "simpint" — Algoritmo combinado (n>=1, maneja n par/impar, datos desiguales)
      "auto"    — Alias de "simpint" (por defecto)

    provee f_expr para comparación con integral exacta via sympy.
    """

    TOLERANCIA_H = 1e-9

    def __init__(self, x, y, metodo="auto", f_expr=None):
        self.x = copy.deepcopy(x)
        self.y = copy.deepcopy(y)
        self.metodo = metodo.lower().strip()
        if self.metodo == "auto":
            self.metodo = "simpint"
        self.f_expr = f_expr
        self.n = len(x) - 1 if len(x) >= 1 else 0
        self.steps = []

    # --- Validación de entradas (tarea 1.3) ---

    def _validar_entradas(self):
        """Retorna mensaje de error o None si todo es válido."""
        if len(self.x) != len(self.y):
            return (
                f"Dimensiones incompatibles: x tiene "
                f"{len(self.x)} elementos e y tiene "
                f"{len(self.y)} elementos."
            )

        minimos = {
            "simp13": 3,
            "simp38": 4,
            "simp13m": 3,
            "simpint": 2,
        }
        min_pts = minimos.get(self.metodo, 2)
        if len(self.x) < min_pts:
            nombre = {
                "simp13": "Simpson 1/3 simple",
                "simp38": "Simpson 3/8 simple",
                "simp13m": "Simpson 1/3 múltiple",
                "simpint": "Simpson combinado",
            }.get(self.metodo, self.metodo)
            return (
                f"Se requieren al menos {min_pts} puntos para "
                f"{nombre}."
            )

        for i in range(len(self.x) - 1):
            if self.x[i + 1] <= self.x[i]:
                return (
                    f"Los valores de x deben ser estrictamente "
                    f"crecientes. Se encontró x[{i}] = "
                    f"{self.x[i]} >= x[{i + 1}] = {self.x[i + 1]}."
                )

        if self.metodo == "simp13m":
            if self.n % 2 != 0:
                return (
                    f"Simpson 1/3 múltiple requiere n par "
                    f"(se proporcionó n={self.n}). "
                    f"Use 'simpint' para n impar."
                )

        return None

    def _verificar_uniforme(self):
        """Retorna (h, True) si uniforme, (None, False) si no."""
        if len(self.x) < 2:
            return None, False
        h = float(self.x[1]) - float(self.x[0])
        for i in range(len(self.x) - 1):
            h_i = float(self.x[i + 1]) - float(self.x[i])
            if abs(h_i - h) >= self.TOLERANCIA_H:
                return None, False
        return h, True

    # --- Reglas fundamentales (tareas 1.4, 1.5, 1.6) ---

    def _simp13(self, h, f0, f1, f2):
        """Simpson 1/3 simple: 2*h*(f0 + 4*f1 + f2) / 6"""
        return 2.0 * h * (f0 + 4.0 * f1 + f2) / 6.0

    def _simp38(self, h, f0, f1, f2, f3):
        """Simpson 3/8 simple: 3*h*(f0 + 3*(f1 + f2) + f3) / 8"""
        return 3.0 * h * (f0 + 3.0 * (f1 + f2) + f3) / 8.0

    def _simp13m(self, h, n, f):
        """Simpson 1/3 múltiple. Requiere n par. f = lista de n+1 valores."""
        suma = float(f[0])
        for i in range(1, n - 1, 2):
            suma += 4.0 * float(f[i]) + 2.0 * float(f[i + 1])
        suma += 4.0 * float(f[n - 1]) + float(f[n])
        return h * suma / 3.0

    # --- Algoritmo combinado SimpInt (tarea 1.7) ---

    def _simpint(self, a, b, n, f):
        """
        Algoritmo combinado de Chapra (SimpInt):
          n=1          → regla del trapecio
          n impar > 1  → Simp38 últimos 3 segs + Simp13m primeros (n-3) segs
          n par        → Simp13m todos los segmentos
        Retorna (valor, descripcion_aplicaciones).
        """
        h = (b - a) / n
        suma = 0.0
        aplicaciones = []

        if n == 1:
            suma = h * (float(f[0]) + float(f[1])) / 2.0
            aplicaciones.append(("trapecio", 0, 0, suma))
            return suma, aplicaciones

        m = n
        if n % 2 != 0 and n > 1:
            # Últimos 3 segmentos con Simpson 3/8
            v = self._simp38(h, float(f[n - 3]), float(f[n - 2]),
                             float(f[n - 1]), float(f[n]))
            suma += v
            aplicaciones.append(("simp38", n - 3, n, v))
            m = n - 3

        if m > 1:
            v = self._simp13m(h, m, [float(vi) for vi in f[:m + 1]])
            suma += v
            aplicaciones.append(("simp13m", 0, m, v))

        return suma, aplicaciones

    # --- Datos desiguales (tarea 1.8) ---

    def _es_uniforme_sub(self, x_sub):
        """Verifica si subconjunto de x tiene espaciado uniforme."""
        if len(x_sub) < 2:
            return True
        h = x_sub[1] - x_sub[0]
        for i in range(len(x_sub) - 1):
            if abs((x_sub[i + 1] - x_sub[i]) - h) >= self.TOLERANCIA_H:
                return False
        return True

    def _manejar_datos_desiguales(self, x, y, metodo):
        """
        Aplica reglas segmento por segmento para datos con espaciado desigual.
        Agrupa segmentos contiguos con h compatible:
          - 3 pts uniformes (2 segs) → Simpson 1/3
          - 4 pts uniformes (3 segs) → Simpson 3/8
          - 1 segmento aislado       → Trapecio
        Retorna (valor_total, lista_aplicaciones).
        """
        n_segs = len(x) - 1
        aplicaciones = []
        valor_total = 0.0
        i = 0  # índice del segmento actual (0..n_segs-1)

        while i < n_segs:
            restante = n_segs - i

            # Intentar Simpson 3/8 (3 segmentos, 4 puntos)
            if restante >= 3:
                x_sub = [x[i], x[i + 1], x[i + 2], x[i + 3]]
                if self._es_uniforme_sub(x_sub):
                    h = x_sub[1] - x_sub[0]
                    v = self._simp38(h, y[i], y[i + 1], y[i + 2], y[i + 3])
                    aplicaciones.append(("simp38", i, i + 3, v))
                    valor_total += v
                    i += 3
                    continue

            # Intentar Simpson 1/3 (2 segmentos, 3 puntos)
            if restante >= 2:
                x_sub = [x[i], x[i + 1], x[i + 2]]
                if self._es_uniforme_sub(x_sub):
                    h = x_sub[1] - x_sub[0]
                    v = self._simp13(h, y[i], y[i + 1], y[i + 2])
                    aplicaciones.append(("simp13", i, i + 2, v))
                    valor_total += v
                    i += 2
                    continue

            # Fallback: trapecio para 1 segmento
            h = x[i + 1] - x[i]
            v = h * (y[i] + y[i + 1]) / 2.0
            aplicaciones.append(("trapecio", i, i + 1, v))
            valor_total += v
            i += 1

        return valor_total, aplicaciones

    # --- Error relativo (tarea 1.10) ---

    def _calcular_error_relativo(self, valor_aprox, valor_exacto):
        """E_t = |(exacto - aprox) / exacto| * 100"""
        if abs(valor_exacto) < 1e-12:
            return abs(valor_exacto - valor_aprox)
        return abs((valor_exacto - valor_aprox) / valor_exacto) * 100.0

    # --- Solve principal (tarea 1.9) ---

    def solve(self):
        self.steps = []

        error = self._validar_entradas()
        if error:
            return {
                "success": False,
                "solution": None,
                "steps": self.steps,
                "error_message": error,
            }

        x_f = [float(v) for v in self.x]
        y_f = [float(v) for v in self.y]
        n = self.n

        self.steps.append({
            "type": "initial",
            "x": copy.deepcopy(self.x),
            "y": copy.deepcopy(self.y),
            "n": n,
            "metodo": self.metodo,
            "description": (
                f"Datos: {len(self.x)} puntos ({n} segmento{'s' if n != 1 else ''}), "
                f"método: {self.metodo}, intervalo "
                f"[{self.x[0]}, {self.x[n]}]."
            ),
        })

        # --- Ramificación por método ---

        if self.metodo == "simp13":
            return self._resolver_simp13(x_f, y_f)
        elif self.metodo == "simp38":
            return self._resolver_simp38(x_f, y_f)
        elif self.metodo == "simp13m":
            return self._resolver_simp13m(x_f, y_f)
        else:  # simpint
            return self._resolver_simpint(x_f, y_f)

    def _resolver_simp13(self, x_f, y_f):
        n = self.n
        h, uniforme = self._verificar_uniforme()
        if not uniforme:
            return self._error_result(
                "Simpson 1/3 simple requiere nodos uniformemente espaciados."
            )
        if n != 2:
            return self._error_result(
                f"Simpson 1/3 simple requiere exactamente 2 segmentos "
                f"(3 puntos). Se proporcionaron {n} segmentos."
            )

        valor = self._simp13(h, y_f[0], y_f[1], y_f[2])
        self.steps.append({
            "type": "simpson_segment",
            "regla": "simp13",
            "x0": x_f[0], "x2": x_f[2],
            "f0": y_f[0], "f1": y_f[1], "f2": y_f[2],
            "h": h,
            "area": valor,
            "description": (
                f"Simp13 = 2h(f0+4f1+f2)/6 = "
                f"2({h:.6g})({y_f[0]:.6g}+4·{y_f[1]:.6g}+{y_f[2]:.6g})/6 = "
                f"{valor:.6g}"
            ),
        })

        return self._finalizar(valor, "Simpson 1/3 simple", h, n)

    def _resolver_simp38(self, x_f, y_f):
        n = self.n
        h, uniforme = self._verificar_uniforme()
        if not uniforme:
            return self._error_result(
                "Simpson 3/8 simple requiere nodos uniformemente espaciados."
            )
        if n != 3:
            return self._error_result(
                f"Simpson 3/8 simple requiere exactamente 3 segmentos "
                f"(4 puntos). Se proporcionaron {n} segmentos."
            )

        valor = self._simp38(h, y_f[0], y_f[1], y_f[2], y_f[3])
        self.steps.append({
            "type": "simpson_segment",
            "regla": "simp38",
            "x0": x_f[0], "x3": x_f[3],
            "f0": y_f[0], "f1": y_f[1], "f2": y_f[2], "f3": y_f[3],
            "h": h,
            "area": valor,
            "description": (
                f"Simp38 = 3h(f0+3(f1+f2)+f3)/8 = "
                f"3({h:.6g})({y_f[0]:.6g}+3({y_f[1]:.6g}+{y_f[2]:.6g})+"
                f"{y_f[3]:.6g})/8 = {valor:.6g}"
            ),
        })

        return self._finalizar(valor, "Simpson 3/8 simple", h, n)

    def _resolver_simp13m(self, x_f, y_f):
        n = self.n
        h, uniforme = self._verificar_uniforme()
        if not uniforme:
            return self._error_result(
                "Simpson 1/3 múltiple requiere nodos uniformemente espaciados. "
                "Use 'simpint' para datos desiguales."
            )
        if n % 2 != 0:
            return self._error_result(
                f"Simpson 1/3 múltiple requiere n par. Se proporcionó n={n}."
            )
        if n < 2:
            return self._error_result(
                f"Simpson 1/3 múltiple requiere al menos 2 segmentos."
            )

        valor = self._simp13m(h, n, y_f)
        self.steps.append({
            "type": "simpson13m_applied",
            "regla": "simp13m",
            "n": n,
            "h": h,
            "area": valor,
            "description": (
                f"Simp13m = h(f0 + 4Σf_impar + 2Σf_par + fn)/3 = "
                f"{h:.6g} × suma / 3 = {valor:.6g}  "
                f"({n} segmentos, {n // 2} aplicaciones Simpson 1/3)"
            ),
        })

        return self._finalizar(valor, "Simpson 1/3 múltiple", h, n)

    def _resolver_simpint(self, x_f, y_f):
        n = self.n
        h, uniforme = self._verificar_uniforme()

        if uniforme:
            # Datos uniformes: usar algoritmo SimpInt de Chapra
            a, b = x_f[0], x_f[n]
            valor, aplicaciones = self._simpint(a, b, n, y_f)
            for regla, i0, i1, v in aplicaciones:
                nombre = {"simp13m": "Simpson 1/3 múltiple",
                          "simp38": "Simpson 3/8",
                          "trapecio": "Trapecio"}[regla]
                self.steps.append({
                    "type": f"{regla}_applied",
                    "regla": regla,
                    "seg_inicio": i0,
                    "seg_fin": i1,
                    "area": v,
                    "description": (
                        f"{nombre} aplicado a segmentos [{i0}..{i1}] → "
                        f"área = {v:.6g}"
                    ),
                })
            return self._finalizar(valor, "Simpson combinado (SimpInt)", h, n)
        else:
            # Datos desiguales: segmento por segmento
            valor, aplicaciones = self._manejar_datos_desiguales(
                x_f, y_f, self.metodo
            )
            for regla, i0, i1, v in aplicaciones:
                nombre = {"simp13": "Simpson 1/3",
                          "simp38": "Simpson 3/8",
                          "trapecio": "Trapecio"}[regla]
                self.steps.append({
                    "type": f"{regla}_applied",
                    "regla": regla,
                    "seg_inicio": i0,
                    "seg_fin": i1,
                    "area": v,
                    "description": (
                        f"{nombre} en segmentos [{i0}..{i1}] "
                        f"(x={x_f[i0]:.6g}..{x_f[i1]:.6g}) → área = {v:.6g}"
                    ),
                })
            return self._finalizar(
                valor, "Simpson combinado (datos desiguales)", None, n
            )

    # --- Utilidades internas ---

    def _error_result(self, msg):
        self.steps.append({"type": "error", "description": msg})
        return {
            "success": False,
            "solution": None,
            "steps": self.steps,
            "error_message": msg,
        }

    def _finalizar(self, valor, metodo_nombre, h, n):
        """Registra paso final, calcula exacta/error, retorna resultado."""
        valor = float(valor)
        self.steps.append({
            "type": "final",
            "formula": f"I ≈ {valor:.8f}",
            "result": valor,
            "description": f"Resultado ({metodo_nombre}): I ≈ {valor:.8f}",
        })

        exact_value = None
        error_relativo = None
        if self.f_expr:
            try:
                x_sym = sympy.Symbol('x')
                f_sym = sympy.sympify(self.f_expr)
                a = float(self.x[0])
                b = float(self.x[self.n])
                integral_sym = sympy.integrate(f_sym, (x_sym, a, b))
                exact_value = float(integral_sym)
                error_relativo = self._calcular_error_relativo(
                    valor, exact_value
                )
                self.steps.append({
                    "type": "exact",
                    "exact_value": exact_value,
                    "error_relativo": error_relativo,
                    "description": (
                        f"Integral exacta: ∫_{a}^{b} f(x) dx = "
                        f"{exact_value:.8f}  |  E_t = "
                        f"{error_relativo:.6g}%"
                    ),
                })
            except Exception:
                exact_value = None
                error_relativo = None

        return {
            "success": True,
            "solution": {
                "value": valor,
                "h": h,
                "n": n,
                "metodo": metodo_nombre,
                "exact_value": exact_value,
                "error_relativo": error_relativo,
                "segments": [],
            },
            "steps": self.steps,
            "error_message": None,
        }
