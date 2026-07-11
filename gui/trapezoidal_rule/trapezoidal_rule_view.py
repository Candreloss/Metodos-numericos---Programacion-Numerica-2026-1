import customtkinter as ctk #pyright: ignore
from tkinter import messagebox
import numpy as np #pyright: ignore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from lib.trapezoidal_rule import TrapezoidalRule
from gui.components.sidebar import Sidebar
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_section_font, get_label_font, get_mono_font
)


class TrapezoidalRuleView(ctk.CTkFrame):
    """
    Vista del método de la Regla del Trapecio.

    Permite al usuario ingresar los nodos x,y (comas) y una expresión
    opcional f(x) para comparar contra la integral exacta. Muestra tres
    tabs: Resultado (valor aproximado, h, n, error), Paso a Paso (cada
    segmento y fórmula final) y Gráfica (trapecios rellenos + curva).
    """

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
        self.load_preset("cuadratico")

    def create_layout(self):
        self.sidebar = Sidebar(self, active_method="trapezoidal_rule")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.view_container.grid_columnconfigure(0, weight=1)
        self.view_container.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header_frame, text="Regla del Trapecio",
            font=self.title_font, text_color=COLOR_LIGHT_CYAN
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header_frame,
            text="Integra datos tabulares con nodos uniformes. Simple (n=1) o compuesta (n>1) — automático.",
            font=self.label_font, text_color=COLOR_MUTED
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        content_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=5)
        content_frame.grid_columnconfigure(1, weight=5)
        content_frame.grid_rowconfigure(0, weight=1)

        self._setup_left_panel(content_frame)
        self._setup_right_panel(content_frame)

    def _setup_left_panel(self, parent):
        self.left_panel = ctk.CTkFrame(
            parent, fg_color=COLOR_PANEL, border_color=COLOR_BORDER,
            border_width=1, corner_radius=12
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        self.left_panel.grid_columnconfigure(0, weight=1)

        config_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        config_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        config_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(config_frame, text="x (comas):", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_x = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                    border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT)
        self.entry_x.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="f(x) (comas):", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_y = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                    border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT)
        self.entry_y.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="f(x) opcional:", font=self.label_font, text_color=COLOR_MUTED).grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_func = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                       border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT)
        self.entry_func.grid(row=2, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="Ejemplo:", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=3, column=0, sticky="w", padx=(0, 8))
        self.preset_combo = ctk.CTkComboBox(
            config_frame,
            values=["Manual", "Lineal (2 pts)", "Constante (3 pts)", "x² (5 pts)", "sen(x) (5 pts)"],
            command=self.on_preset,
            fg_color=COLOR_BG, border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER, button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL, dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT, text_color=COLOR_TEXT,
            font=self.label_font, corner_radius=8
        )
        self.preset_combo.set("Manual")
        self.preset_combo.grid(row=3, column=1, sticky="ew")

        actions_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            actions_frame, text="Limpiar",
            fg_color="transparent", hover_color=COLOR_BORDER,
            border_color=COLOR_INTERACTIVE_BORDER, border_width=1,
            text_color=COLOR_LIGHT_CYAN, font=self.label_font,
            corner_radius=8, height=38, command=self.clear_inputs
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            actions_frame, text="Calcular y Graficar",
            fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_BG,
            font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            corner_radius=8, height=38, command=self.solve_integration
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

        info_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        info_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.lbl_info = ctk.CTkLabel(
            info_frame, text="", font=self.label_font, text_color=COLOR_MUTED, wraplength=320)
        self.lbl_info.grid(row=0, column=0, sticky="w")

    def _setup_right_panel(self, parent):
        self.right_panel = ctk.CTkFrame(
            parent, fg_color=COLOR_PANEL, border_color=COLOR_BORDER,
            border_width=1, corner_radius=12
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=0)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)

        self.result_tabs = ctk.CTkTabview(
            self.right_panel, fg_color=COLOR_PANEL,
            segmented_button_fg_color=COLOR_BG,
            segmented_button_selected_color=("#58A1D3", "#0F4C81"),
            segmented_button_selected_hover_color=("#3e87b7", "#0b3a63"),
            segmented_button_unselected_color=COLOR_BG,
            segmented_button_unselected_hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT, corner_radius=8
        )
        self.result_tabs.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=12, pady=12)

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
            font=self.section_font, text_color=COLOR_LIGHT_CYAN
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.txt_result = ctk.CTkTextbox(
            self.tab_result, fg_color=COLOR_BG, font=self.mono_font,
            text_color=COLOR_TEXT, border_color=COLOR_BORDER, border_width=1,
            corner_radius=8,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_result.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_result.insert("1.0", "Ingrese datos y presione 'Calcular y Graficar'.")
        self.txt_result.configure(state="disabled")

    def _setup_steps_tab(self):
        self.tab_steps.grid_columnconfigure(0, weight=1)
        self.tab_steps.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(
            self.tab_steps, text="Cálculo de la Regla del Trapecio",
            font=self.section_font, text_color=COLOR_LIGHT_CYAN
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.txt_steps = ctk.CTkTextbox(
            self.tab_steps, fg_color=COLOR_BG, font=self.mono_font,
            text_color=COLOR_TEXT, border_color=COLOR_BORDER, border_width=1,
            corner_radius=8,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_steps.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_steps.insert(
            "1.0",
            "Paso a paso:\n"
            "1. Para cada segmento i: T_i = h*(f_i + f_{i+1})/2\n"
            "2. Se acumulan las áreas de todos los segmentos\n"
            "3. Si n=1: I = h*(f0 + f1)/2 (simple)\n"
            "4. Si n>1: I = h*(f0 + 2*Σf_i + fn)/2 (compuesta)"
        )
        self.txt_steps.configure(state="disabled")

    def _setup_graph_tab(self):
        self.tab_graph.grid_columnconfigure(0, weight=1)
        self.tab_graph.grid_rowconfigure(0, weight=1)
        self.graph_frame = ctk.CTkFrame(self.tab_graph, fg_color="transparent")
        self.graph_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # --- Lógica de presets ---
    def on_preset(self, value):
        if value == "Lineal (2 pts)":
            self.load_preset("lineal")
        elif value == "Constante (3 pts)":
            self.load_preset("constante")
        elif value == "x² (5 pts)":
            self.load_preset("cuadratico")
        elif value == "sen(x) (5 pts)":
            self.load_preset("seno")
        if value != "Manual":
            self.preset_combo.set("Manual")

    def load_preset(self, name):
        if name == "lineal":
            x, y, func = [0.0, 2.0], [0.0, 4.0], "2*x"
        elif name == "constante":
            x, y, func = [1.0, 2.0, 3.0], [5.0, 5.0, 5.0], "5"
        elif name == "cuadratico":
            x = [0.0, 0.5, 1.0, 1.5, 2.0]
            y = [xi * xi for xi in x]
            func = "x**2"
        elif name == "seno":
            import math
            n = 4
            x = [i * math.pi / n for i in range(n + 1)]
            y = [math.sin(xi) for xi in x]
            func = "sin(x)"
        else:
            return
        self.entry_x.delete(0, "end")
        self.entry_x.insert(0, ", ".join(str(v) for v in x))
        self.entry_y.delete(0, "end")
        self.entry_y.insert(0, ", ".join(str(v) for v in y))
        self.entry_func.delete(0, "end")
        self.entry_func.insert(0, func)

    def clear_inputs(self):
        for e in [self.entry_x, self.entry_y, self.entry_func]:
            e.delete(0, "end")
        self.lbl_info.configure(text="")

    # --- Resolución ---
    def solve_integration(self):
        try:
            x = [float(v.strip()) for v in self.entry_x.get().split(",")]
            y = [float(v.strip()) for v in self.entry_y.get().split(",")]
        except ValueError:
            messagebox.showerror("Error de entrada", "Los campos x e y deben ser numéricos (separados por comas).")
            return

        func_str = self.entry_func.get().strip()
        if func_str == "":
            func_str = None
        solver = TrapezoidalRule(x, y, f_expr=func_str)
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
            out = f"I ≈ {sol['value']:.8f}\n"
            out += f"h = {sol['h']:.6g}\n"
            out += f"n = {sol['n']} segmento(s)\n\n"
            if sol["exact_value"] is not None:
                out += f"Integral exacta = {sol['exact_value']:.8f}\n"
                out += f"Error relativo = {sol['error_relativo']:.6g}%\n\n"
            out += f"Fórmula:\n{sol['formula']}\n"
            self.txt_result.insert("1.0", out)

            steps_text = ""
            for step in result["steps"]:
                if step["type"] == "initial":
                    steps_text += f"{step['description']}\n\n"
                elif step["type"] == "segment":
                    sep = "─" * 50
                    if step["i"] == 0:
                        steps_text += sep + "\n"
                    steps_text += f"  {step['description']}\n"
                elif step["type"] == "final":
                    steps_text += "\n" + "═" * 50 + "\n"
                    steps_text += f"{step['description']}\n"
                    steps_text += f"  I = {step['result']:.8f}\n"
                elif step["type"] == "exact":
                    steps_text += "\n" + "─" * 50 + "\n"
                    steps_text += f"{step['description']}\n"
            self.txt_steps.insert("1.0", steps_text)

            self.lbl_info.configure(
                text=f"I ≈ {sol['value']:.6g} (n={sol['n']}, h={sol['h']:.4g})"
            )

            self._plot(sol, func_str, x, y)

        self.txt_result.configure(state="disabled")
        self.txt_steps.configure(state="disabled")

    # --- Gráfica ---
    def _plot(self, solution, func_str, x_data, y_data):
        for w in self.graph_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 3.5))

        # Trapecios rellenos semitransparentes (uno por segmento).
        for seg in solution["segments"]:
            xs = [seg["x0"], seg["x1"]]
            # Área del trapecio: vertices (x0,0), (x1,0), (x1,f1), (x0,f0).
            poly_x = [seg["x0"], seg["x1"], seg["x1"], seg["x0"]]
            poly_y = [0, 0, seg["f1"], seg["f0"]]
            ax.fill(poly_x, poly_y, alpha=0.25, color="#58A1D3",
                    edgecolor="#0F4C81", linewidth=1.2)

        # Curva suave de f(x) si se proveyó una expresión simbólica.
        if func_str:
            try:
                import sympy
                x_sym = sympy.Symbol('x')
                f_expr = sympy.sympify(func_str)
                f_callable = sympy.lambdify(x_sym, f_expr, "numpy")
                a, b = min(x_data), max(x_data)
                x_range = np.linspace(a, b, 300)
                y_range = f_callable(x_range)
                # Asegurar que sea 1D (lambdify a veces devuelve escalar).
                if np.isscalar(y_range):
                    y_range = np.full_like(x_range, float(y_range))
                ax.plot(x_range, y_range, "b-", linewidth=1.5,
                        label="f(x) original")
            except Exception:
                pass

        # Nodos (puntos tabulares).
        ax.plot(x_data, y_data, "or", markersize=7, markerfacecolor="red",
                label="Nodos")

        ax.set_title("Regla del Trapecio")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)