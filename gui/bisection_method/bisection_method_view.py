import customtkinter as ctk #pyright: ignore
from tkinter import messagebox
import numpy as np #pyright: ignore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from lib.bisection_method import BisectionMethod
from gui.components.sidebar import Sidebar
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_section_font, get_label_font, get_mono_font
)


class BisectionMethodView(ctk.CTkFrame):
    """
    Vista del Método de Bisección (búsqueda de raíces).

    Permite al usuario ingresar f(x) (sympy), xl, xu, es (tolerancia),
    imax, y mostrar tres tabs: Resultado (raíz, iteraciones, error),
    Paso a Paso (cada iteración) y Gráfica (curva f(x) + raíz marcada
    + intervalo inicial sombreado).
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
        self.load_preset("cubica")

    def create_layout(self):
        self.sidebar = Sidebar(self, active_method="bisection_method")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.view_container.grid_columnconfigure(0, weight=1)
        self.view_container.grid_rowconfigure(1, weight=1)

        header_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header_frame, text="Método de Bisección",
            font=self.title_font, text_color=COLOR_LIGHT_CYAN
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header_frame,
            text="Hallar raíces de f(x) en [xl, xu] dividiendo el intervalo por mitades. Requiere cambio de signo.",
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

        ctk.CTkLabel(config_frame, text="f(x):", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_func = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                       border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT)
        self.entry_func.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="xl:", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_xl = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                     border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT, width=120)
        self.entry_xl.grid(row=1, column=1, sticky="w", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="xu:", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_xu = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                     border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT, width=120)
        self.entry_xu.grid(row=2, column=1, sticky="w", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="es (%):", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_es = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                     border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT, width=120)
        self.entry_es.insert(0, "0.01")
        self.entry_es.grid(row=3, column=1, sticky="w", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="imax:", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=4, column=0, sticky="w", padx=(0, 8), pady=(0, 6))
        self.entry_imax = ctk.CTkEntry(config_frame, font=self.label_font, fg_color=COLOR_BG,
                                       border_color=COLOR_INTERACTIVE_BORDER, text_color=COLOR_TEXT, width=120)
        self.entry_imax.insert(0, "100")
        self.entry_imax.grid(row=4, column=1, sticky="w", pady=(0, 6))

        ctk.CTkLabel(config_frame, text="Ejemplo:", font=self.label_font, text_color=COLOR_TEXT).grid(
            row=5, column=0, sticky="w", padx=(0, 8))
        self.preset_combo = ctk.CTkComboBox(
            config_frame,
            values=["Manual", "x³−x−2 en [1,2]", "cos(x)−x en [0,1]", "x²−4 en [0,3]"],
            command=self.on_preset,
            fg_color=COLOR_BG, border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER, button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL, dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT, text_color=COLOR_TEXT,
            font=self.label_font, corner_radius=8
        )
        self.preset_combo.set("Manual")
        self.preset_combo.grid(row=5, column=1, sticky="ew")

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
            corner_radius=8, height=38, command=self.solve_bisection
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
            self.tab_result, text="Resultado de la Bisección",
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
            self.tab_steps, text="Iteraciones del Método de Bisección",
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
            "1. xr = (xl + xu)/2 (punto medio)\n"
            "2. ea = |(xr - xrold)/xr| * 100 (error relativo)\n"
            "3. test = f(xl) * f(xr):\n"
            "   - < 0 → xu = xr (raíz en subintervalo inferior)\n"
            "   - > 0 → xl = xr (raíz en subintervalo superior)\n"
            "   - = 0 → raíz exacta encontrada\n"
            "4. Sale cuando ea < es o iter >= imax"
        )
        self.txt_steps.configure(state="disabled")

    def _setup_graph_tab(self):
        self.tab_graph.grid_columnconfigure(0, weight=1)
        self.tab_graph.grid_rowconfigure(0, weight=1)
        self.graph_frame = ctk.CTkFrame(self.tab_graph, fg_color="transparent")
        self.graph_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # --- Lógica de presets ---
    def on_preset(self, value):
        if value == "x³−x−2 en [1,2]":
            self.load_preset("cubica")
        elif value == "cos(x)−x en [0,1]":
            self.load_preset("cosx")
        elif value == "x²−4 en [0,3]":
            self.load_preset("cuadrada")
        if value != "Manual":
            self.preset_combo.set("Manual")

    def load_preset(self, name):
        if name == "cubica":
            func, xl, xu = "x**3 - x - 2", 1.0, 2.0
        elif name == "cosx":
            func, xl, xu = "cos(x) - x", 0.0, 1.0
        elif name == "cuadrada":
            func, xl, xu = "x**2 - 4", 0.0, 3.0
        else:
            return
        self.entry_func.delete(0, "end")
        self.entry_func.insert(0, func)
        self.entry_xl.delete(0, "end")
        self.entry_xl.insert(0, str(xl))
        self.entry_xu.delete(0, "end")
        self.entry_xu.insert(0, str(xu))

    def clear_inputs(self):
        for e in [self.entry_func, self.entry_xl, self.entry_xu, self.entry_es, self.entry_imax]:
            e.delete(0, "end")
        self.entry_es.insert(0, "0.01")
        self.entry_imax.insert(0, "100")
        self.lbl_info.configure(text="")

    # --- Resolución ---
    def solve_bisection(self):
        func_str = self.entry_func.get().strip()
        if func_str == "":
            func_str = None
        try:
            xl = float(self.entry_xl.get().strip())
            xu = float(self.entry_xu.get().strip())
            es = float(self.entry_es.get().strip())
            imax = int(self.entry_imax.get().strip())
        except ValueError:
            messagebox.showerror("Error de entrada", "xl, xu, es deben ser numéricos e imax entero.")
            return

        solver = BisectionMethod(func_str, xl, xu, es=es, imax=imax)
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
            out = f"Raíz ≈ {sol['root']:.8f}\n"
            out += f"Iteraciones = {sol['iterations']}\n"
            out += f"Error (ea) = {sol['error']:.6g}%\n"
            out += f"Convergió = {'Sí' if sol['converged'] else 'No (máx. iteraciones)'}\n"
            out += f"f(raíz) = {sol['f_value']:.6g}\n"
            out += f"Intervalo final: [{sol['xl_final']:.6g}, {sol['xu_final']:.6g}]\n"
            self.txt_result.insert("1.0", out)

            steps_text = ""
            for step in result["steps"]:
                if step["type"] == "initial":
                    steps_text += f"{step['description']}\n\n"
                elif step["type"] == "iteration":
                    sep = "─" * 50
                    if step["iter"] == 1:
                        steps_text += sep + "\n"
                    steps_text += f"  {step['description']}\n"
                elif step["type"] == "final":
                    steps_text += "\n" + "═" * 50 + "\n"
                    steps_text += f"{step['description']}\n"
            self.txt_steps.insert("1.0", steps_text)

            self.lbl_info.configure(
                text=f"Raíz ≈ {sol['root']:.6g} (iter={sol['iterations']}, ea={sol['error']:.4g}%)"
            )

            self._plot(sol, func_str, xl, xu)

        self.txt_result.configure(state="disabled")
        self.txt_steps.configure(state="disabled")

    # --- Gráfica ---
    def _plot(self, solution, func_str, xl_orig, xu_orig):
        for w in self.graph_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 3.5))

        # Intervalo inicial [xl, xu] sombreado (muestra el bracketing).
        ax.axvspan(xl_orig, xu_orig, alpha=0.1, color="#58A1D3",
                   label="Intervalo inicial")

        # Eje y=0 (referencia para la raíz).
        ax.axhline(0, color="k", linewidth=0.8)

        # Curva suave de f(x) si se proveyó una expresión simbólica.
        if func_str:
            try:
                import sympy
                x_sym = sympy.Symbol('x')
                f_expr = sympy.sympify(func_str)
                f_callable = sympy.lambdify(x_sym, f_expr, "numpy")
                margen = 0.2 * (xu_orig - xl_orig)
                a, b = xl_orig - margen, xu_orig + margen
                x_range = np.linspace(a, b, 300)
                y_range = f_callable(x_range)
                if np.isscalar(y_range):
                    y_range = np.full_like(x_range, float(y_range))
                ax.plot(x_range, y_range, "b-", linewidth=1.5,
                        label="f(x)")
                # Extremos del intervalo inicial en la curva.
                ax.plot([xl_orig, xu_orig],
                        [float(f_expr.subs(x_sym, xl_orig)),
                         float(f_expr.subs(x_sym, xu_orig))],
                        "or", markersize=7, label="Extremos [xl,xu]")
            except Exception:
                pass

        # Raíz marcada con 'x' verde sobre y=0.
        ax.plot(solution["root"], 0, "xg", markersize=12,
                markeredgewidth=2, label=f"Raíz ≈ {solution['root']:.4g}")

        ax.set_title("Método de Bisección")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=8)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)