import customtkinter as ctk  # pyright: ignore
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np  # pyright: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.components.sidebar import Sidebar
from gui.theme import (
    COLOR_ACCENT,
    COLOR_ACCENT_HOVER,
    COLOR_BG,
    COLOR_BORDER,
    COLOR_INTERACTIVE_BORDER,
    COLOR_LIGHT_CYAN,
    COLOR_MUTED,
    COLOR_PANEL,
    COLOR_TEXT,
    get_label_font,
    get_mono_font,
    get_section_font,
    get_title_font,
)
from lib.simpson_rules import ReglasSimpson


class ReglasSimpsonView(ctk.CTkFrame):
    """
    Vista del método de las Reglas de Simpson.

    Permite al usuario ingresar nodos x,y (comas), elegir el método
    (Simpson 1/3, 3/8, 1/3 múltiple, combinado/auto) y una expresión
    opcional f(x) para comparar contra la integral exacta. Muestra tres
    tabs: Resultado, Paso a Paso y Gráfica (segmentos Simpson + curva).
    """

    METODOS = ["Auto", "Simpson 1/3", "Simpson 3/8",
               "Simpson 1/3 Múltiple", "Combinado"]
    MAPA_METODO = {
        "Auto": "auto",
        "Simpson 1/3": "simp13",
        "Simpson 3/8": "simp38",
        "Simpson 1/3 Múltiple": "simp13m",
        "Combinado": "simpint",
    }

    PRESETS = [
        "Manual",
        "Ejercicio 21.13",
        "Parábola (5 pts)",
        "sen(x) (5 pts)",
        "sen(x) (7 pts)",
    ]

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        self.mono_font = get_mono_font()
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_layout()
        self.load_preset("ejercicio")

    # --- Layout ---

    def create_layout(self):
        self.sidebar = Sidebar(self, active_method="simpson_rules")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.grid(
            row=0, column=1, sticky="nsew", padx=24, pady=24
        )
        self.view_container.grid_columnconfigure(0, weight=1)
        self.view_container.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header_frame, text="Reglas de Simpson",
            font=self.title_font, text_color=COLOR_LIGHT_CYAN,
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header_frame,
            text=(
                "Integra datos tabulares con Simpson 1/3, 3/8, múltiple o "
                "combinado. Acepta nodos uniformes y desiguales."
            ),
            font=self.label_font, text_color=COLOR_MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        content_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=5)
        content_frame.grid_columnconfigure(1, weight=5)
        content_frame.grid_rowconfigure(0, weight=1)

        self._setup_left_panel(content_frame)
        self._setup_right_panel(content_frame)

    # --- Panel izquierdo (tarea 2.4) ---

    def _setup_left_panel(self, parent):
        self.left_panel = ctk.CTkFrame(
            parent, fg_color=COLOR_PANEL, border_color=COLOR_BORDER,
            border_width=1, corner_radius=12,
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.left_panel.grid_columnconfigure(0, weight=1)

        config_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        config_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        config_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            config_frame, text="x (comas):", font=self.label_font,
            text_color=COLOR_TEXT,
        ).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_x = ctk.CTkEntry(
            config_frame, font=self.label_font, fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT,
        )
        self.entry_x.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(
            config_frame, text="f(x) (comas):", font=self.label_font,
            text_color=COLOR_TEXT,
        ).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_y = ctk.CTkEntry(
            config_frame, font=self.label_font, fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT,
        )
        self.entry_y.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(
            config_frame, text="f(x) opcional:", font=self.label_font,
            text_color=COLOR_MUTED,
        ).grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_func = ctk.CTkEntry(
            config_frame, font=self.label_font, fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT,
        )
        self.entry_func.grid(row=2, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(
            config_frame, text="Método:", font=self.label_font,
            text_color=COLOR_TEXT,
        ).grid(row=3, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.metodo_combo = ctk.CTkComboBox(
            config_frame, values=self.METODOS,
            fg_color=COLOR_BG, border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT, text_color=COLOR_TEXT,
            font=self.label_font, corner_radius=8,
        )
        self.metodo_combo.set("Auto")
        self.metodo_combo.grid(row=3, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(
            config_frame, text="Ejemplo:", font=self.label_font,
            text_color=COLOR_TEXT,
        ).grid(row=4, column=0, sticky="w", padx=(0, 8))
        self.preset_combo = ctk.CTkComboBox(
            config_frame, values=self.PRESETS, command=self.on_preset,
            fg_color=COLOR_BG, border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT, text_color=COLOR_TEXT,
            font=self.label_font, corner_radius=8,
        )
        self.preset_combo.set("Manual")
        self.preset_combo.grid(row=4, column=1, sticky="ew")

        actions_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            actions_frame, text="Limpiar",
            fg_color="transparent", hover_color=COLOR_BORDER,
            border_color=COLOR_INTERACTIVE_BORDER, border_width=1,
            text_color=COLOR_LIGHT_CYAN, font=self.label_font,
            corner_radius=8, height=38, command=self.clear_inputs,
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            actions_frame, text="Calcular y Graficar",
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_BG,
            font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            corner_radius=8, height=38, command=self._calcular,
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        info_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        info_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.lbl_info = ctk.CTkLabel(
            info_frame, text="", font=self.label_font,
            text_color=COLOR_MUTED, wraplength=320,
        )
        self.lbl_info.grid(row=0, column=0, sticky="w")

    # --- Panel derecho: pestañas (tarea 2.6) ---

    def _setup_right_panel(self, parent):
        self.right_panel = ctk.CTkFrame(
            parent, fg_color=COLOR_PANEL, border_color=COLOR_BORDER,
            border_width=1, corner_radius=12,
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        self.result_tabs = ctk.CTkTabview(
            self.right_panel, fg_color=COLOR_PANEL,
            segmented_button_fg_color=COLOR_BG,
            segmented_button_selected_color=("#58A1D3", "#0F4C81"),
            segmented_button_selected_hover_color=("#3e87b7", "#0b3a63"),
            segmented_button_unselected_color=COLOR_BG,
            segmented_button_unselected_hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT, corner_radius=8,
        )
        self.result_tabs.grid(
            row=0, column=0, rowspan=2, sticky="nsew", padx=12, pady=12
        )

        self.tab_result = self.result_tabs.add("Resultado")
        self.tab_steps = self.result_tabs.add("Paso a Paso")
        self.tab_graph = self.result_tabs.add("Gráfica")
        self._setup_result_tab()
        self._setup_steps_tab()
        self._setup_graph_tab()

    def _setup_result_tab(self):
        self.tab_result.grid_columnconfigure(0, weight=1)
        self.tab_result.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(
            self.tab_result, text="Resultado de la Integración",
            font=self.section_font, text_color=COLOR_LIGHT_CYAN,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.txt_result = ctk.CTkTextbox(
            self.tab_result, fg_color=COLOR_BG, font=self.mono_font,
            text_color=COLOR_TEXT, border_color=COLOR_BORDER,
            border_width=1, corner_radius=8,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT,
        )
        self.txt_result.grid(row=1, column=0, sticky="nsew", padx=10,
                             pady=(0, 10))
        self.txt_result.insert(
            "1.0", "Ingrese datos y presione 'Calcular y Graficar'."
        )
        self.txt_result.configure(state="disabled")

    def _setup_steps_tab(self):
        self.tab_steps.grid_columnconfigure(0, weight=1)
        self.tab_steps.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(
            self.tab_steps, text="Cálculo Paso a Paso",
            font=self.section_font, text_color=COLOR_LIGHT_CYAN,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.txt_steps = ctk.CTkTextbox(
            self.tab_steps, fg_color=COLOR_BG, font=self.mono_font,
            text_color=COLOR_TEXT, border_color=COLOR_BORDER,
            border_width=1, corner_radius=8,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT,
        )
        self.txt_steps.grid(row=1, column=0, sticky="nsew", padx=10,
                            pady=(0, 10))
        self.txt_steps.insert(
            "1.0",
            "Reglas de Simpson:\n"
            "• Simp13  = 2h(f0+4f1+f2)/6     (2 segmentos)\n"
            "• Simp38  = 3h(f0+3(f1+f2)+f3)/8 (3 segmentos)\n"
            "• Simp13m = h(f0+4Σimpar+2Σpar+fn)/3 (n par)\n"
            "• SimpInt = combinación automática según n"
        )
        self.txt_steps.configure(state="disabled")

    def _setup_graph_tab(self):
        self.tab_graph.grid_columnconfigure(0, weight=1)
        self.tab_graph.grid_rowconfigure(0, weight=1)
        self.graph_frame = ctk.CTkFrame(self.tab_graph, fg_color="transparent")
        self.graph_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # --- Presets (tarea 2.5) ---

    def on_preset(self, value):
        if value == "Ejercicio 21.13":
            self.load_preset("ejercicio")
        elif value == "Parábola (5 pts)":
            self.load_preset("parabola")
        elif value == "sen(x) (5 pts)":
            self.load_preset("seno5")
        elif value == "sen(x) (7 pts)":
            self.load_preset("seno7")
        if value != "Manual":
            self.preset_combo.set("Manual")

    def load_preset(self, name):
        if name == "ejercicio":
            x = [0, 0.05, 0.15, 0.25, 0.35, 0.475, 0.6]
            y = [2, 1.8555, 1.5970, 1.3746, 1.1831, 0.9808, 0.8131]
            func = "2*exp(-1.5*x)"
            metodo = "Auto"
        elif name == "parabola":
            x = [0.0, 0.5, 1.0, 1.5, 2.0]
            y = [xi * xi for xi in x]
            func = "x**2"
            metodo = "Auto"
        elif name == "seno5":
            import math
            n = 4
            x = [i * math.pi / n for i in range(n + 1)]
            y = [math.sin(xi) for xi in x]
            func = "sin(x)"
            metodo = "Auto"
        elif name == "seno7":
            import math
            n = 6
            x = [i * math.pi / n for i in range(n + 1)]
            y = [math.sin(xi) for xi in x]
            func = "sin(x)"
            metodo = "Auto"
        else:
            return
        self.entry_x.delete(0, "end")
        self.entry_x.insert(0, ", ".join(str(v) for v in x))
        self.entry_y.delete(0, "end")
        self.entry_y.insert(0, ", ".join(str(v) for v in y))
        self.entry_func.delete(0, "end")
        self.entry_func.insert(0, func)
        self.metodo_combo.set(metodo)

    def clear_inputs(self):
        for e in [self.entry_x, self.entry_y, self.entry_func]:
            e.delete(0, "end")
        self.lbl_info.configure(text="")

    # --- Resolución (tarea 2.10) ---

    def _calcular(self):
        try:
            x = [float(v.strip()) for v in self.entry_x.get().split(",")]
            y = [float(v.strip()) for v in self.entry_y.get().split(",")]
        except ValueError:
            messagebox.showerror(
                "Error de entrada",
                "Los campos x e y deben ser numéricos (separados por comas).",
            )
            return

        func_str = self.entry_func.get().strip()
        if func_str == "":
            func_str = None

        metodo_ui = self.metodo_combo.get()
        metodo = self.MAPA_METODO.get(metodo_ui, "auto")

        solver = ReglasSimpson(x, y, metodo=metodo, f_expr=func_str)
        result = solver.solve()

        self.txt_result.configure(state="normal")
        self.txt_steps.configure(state="normal")
        self.txt_result.delete("1.0", "end")
        self.txt_steps.delete("1.0", "end")

        if not result["success"]:
            err = f"ERROR\n{result['error_message']}"
            self.txt_result.insert("1.0", err)
            self.txt_steps.insert("1.0", err)
            self.lbl_info.configure(text="")
        else:
            sol = result["solution"]
            out = f"Método: {sol['metodo']}\n"
            out += f"I ≈ {sol['value']:.8f}\n"
            if sol["h"] is not None:
                out += f"h = {sol['h']:.6g}\n"
            out += f"n = {sol['n']} segmento(s)\n\n"
            if sol["exact_value"] is not None:
                out += f"Integral exacta = {sol['exact_value']:.8f}\n"
                out += f"Error relativo = {sol['error_relativo']:.6g}%\n"
            self.txt_result.insert("1.0", out)

            steps_text = ""
            for step in result["steps"]:
                if step["type"] == "initial":
                    steps_text += f"{step['description']}\n\n"
                elif step["type"] in (
                    "simpson_segment", "simp13_applied",
                    "simp38_applied", "simp13m_applied",
                    "trapecio_applied",
                ):
                    steps_text += f"  {step['description']}\n"
                elif step["type"] == "final":
                    steps_text += "\n" + "═" * 50 + "\n"
                    steps_text += f"{step['description']}\n"
                elif step["type"] == "exact":
                    steps_text += "\n" + "─" * 50 + "\n"
                    steps_text += f"{step['description']}\n"
            self.txt_steps.insert("1.0", steps_text)

            self.lbl_info.configure(
                text=f"I ≈ {sol['value']:.6g} ({sol['metodo']})"
            )
            self._plot(sol, func_str, x, y)

        self.txt_result.configure(state="disabled")
        self.txt_steps.configure(state="disabled")

    # --- Gráfica (tarea 2.9) ---

    def _plot(self, solution, func_str, x_data, y_data):
        for w in self.graph_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 3.5))

        # Sombrear segmentos entre nodos.
        n = len(x_data) - 1
        for i in range(n):
            xs = [x_data[i], x_data[i + 1]]
            poly_x = [xs[0], xs[1], xs[1], xs[0]]
            poly_y = [0, 0, y_data[i + 1], y_data[i]]
            ax.fill(
                poly_x, poly_y, alpha=0.20, color="#58A1D3",
                edgecolor="#0F4C81", linewidth=0.8,
            )

        # Curva suave si hay expresión analítica.
        if func_str:
            try:
                import sympy
                x_sym = sympy.Symbol('x')
                f_expr = sympy.sympify(func_str)
                f_call = sympy.lambdify(x_sym, f_expr, "numpy")
                a, b = min(x_data), max(x_data)
                x_r = np.linspace(a, b, 300)
                y_r = f_call(x_r)
                if np.isscalar(y_r):
                    y_r = np.full_like(x_r, float(y_r))
                ax.plot(
                    x_r, y_r, "b-", linewidth=1.5, label="f(x) original"
                )
            except Exception:
                pass

        ax.plot(
            x_data, y_data, "or", markersize=7,
            markerfacecolor="red", label="Nodos",
        )
        ax.set_title(f"Reglas de Simpson — {solution['metodo']}")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
