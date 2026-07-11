import customtkinter as ctk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.components.sidebar import Sidebar
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_section_font, get_label_font
)
from lib.newton_raphson import NewtonRoots

class NewtonRootsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Rejilla de Máxima Jerarquía: Columna 0 (Sidebar), Columna 1 (Contenido)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Barra Lateral Uniforme de Navegación
        self.sidebar = Sidebar(self, active_method="newton_roots")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # 2. Contenedor del Contenido
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.content_frame.grid_columnconfigure(0, weight=1, minsize=340)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Tipografías del Tema
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        
        # Título de la Sección
        self.title_label = ctk.CTkLabel(
            self.content_frame, 
            text="📐 Cálculo de Raíces: Método de Newton-Raphson", 
            font=self.title_font, 
            text_color=COLOR_LIGHT_CYAN
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # 3. Tarjeta Izquierda: Parámetros de Entrada (Estilo Azul Corp.)
        self.input_card = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=COLOR_PANEL,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=12
        )
        self.input_card.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=0)
        self.setup_inputs()
        
        # 4. Tarjeta Derecha: Pestañas de Resultados (Estilo Azul Corp.)
        self.output_panel = ctk.CTkTabview(
            self.content_frame,
            fg_color=COLOR_PANEL,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=12,
            segmented_button_fg_color=COLOR_BG,
            segmented_button_selected_color=COLOR_ACCENT,
            segmented_button_selected_hover_color=COLOR_ACCENT_HOVER,
            segmented_button_unselected_color=COLOR_BG,
            segmented_button_unselected_hover_color=COLOR_INTERACTIVE_BORDER,
            text_color=COLOR_TEXT
        )
        self.output_panel.grid(row=1, column=1, sticky="nsew", padx=(15, 0), pady=0)
        
        self.tab_res = self.output_panel.add("Resultado")
        self.tab_steps = self.output_panel.add("Paso a Paso")
        self.tab_graph = self.output_panel.add("Evolución Gráfica")
        
        self.setup_outputs()

    def setup_inputs(self):
        card_title = ctk.CTkLabel(
            self.input_card,
            text="PARÁMETROS DE ENTRADA",
            font=self.section_font,
            text_color=COLOR_LIGHT_CYAN
        )
        card_title.pack(anchor="w", padx=15, pady=(15, 10))
        
        fields = [
            ("Función f(x):", "entry_func", "exp(-x) - x"),
            ("Aproximación Inicial (x0):", "entry_x0", "0.0"),
            ("Tolerancia (Tol):", "entry_tol", "1e-5"),
            ("Máx. Iteraciones:", "entry_max", "150"),
            ("Dominio Gráfica Mín (X min):", "entry_xmin", "-2.0"),
            ("Dominio Gráfica Máx (X max):", "entry_xmax", "3.0")
        ]
        
        for label_text, attr_name, default_val in fields:
            lbl = ctk.CTkLabel(self.input_card, text=label_text, font=self.label_font, text_color=COLOR_TEXT)
            lbl.pack(anchor="w", padx=15, pady=(8, 2))
            
            entry = ctk.CTkEntry(
                self.input_card,
                placeholder_text=default_val,
                fg_color=COLOR_BG,
                border_color=COLOR_BORDER,
                text_color=COLOR_TEXT,
                placeholder_text_color=COLOR_MUTED,
                corner_radius=8,
                height=35
            )
            entry.insert(0, default_val)
            entry.pack(fill="x", padx=15, pady=(0, 5))
            setattr(self, attr_name, entry)
            
        self.btn_calc = ctk.CTkButton(
            self.input_card, 
            text="Calcular Raíz", 
            font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            fg_color=COLOR_ACCENT,
            hover_color=COLOR_ACCENT_HOVER,
            text_color="#FFFFFF",
            corner_radius=8,
            height=40,
            command=self.solve_newton
        )
        self.btn_calc.pack(fill="x", padx=15, pady=20)

    def setup_outputs(self):
        self.txt_res = ctk.CTkTextbox(
            self.tab_res, font=self.label_font, fg_color=COLOR_BG,
            border_color=COLOR_BORDER, border_width=1, text_color=COLOR_TEXT, corner_radius=8
        )
        self.txt_res.pack(fill="both", expand=True, padx=15, pady=15)
        self.txt_res.insert("0.0", "Ingrese los parámetros y presione 'Calcular Raíz' para ver el diagnóstico.")
        
        self.txt_steps = ctk.CTkTextbox(
            self.tab_steps, font=ctk.CTkFont(family="Consolas", size=12), fg_color=COLOR_BG,
            border_color=COLOR_BORDER, border_width=1, text_color=COLOR_TEXT, corner_radius=8
        )
        self.txt_steps.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_graph)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        self.apply_graph_theme()

    def apply_graph_theme(self):
        is_dark = (ctk.get_appearance_mode() == "Dark")
        bg_color = COLOR_PANEL[1] if is_dark else COLOR_PANEL[0]
        fg_color = COLOR_TEXT[1] if is_dark else COLOR_TEXT[0]
        grid_color = COLOR_BORDER[1] if is_dark else COLOR_BORDER[0]
        axis_bg = COLOR_BG[1] if is_dark else COLOR_BG[0]
        
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(axis_bg)
        self.ax.title.set_color(fg_color)
        self.ax.xaxis.label.set_color(fg_color)
        self.ax.yaxis.label.set_color(fg_color)
        self.ax.tick_params(colors=fg_color, which='both')
        for spine in self.ax.spines.values():
            spine.set_color(grid_color)
        self.ax.grid(True, linestyle=":", alpha=0.5, color=grid_color)

    def solve_newton(self):
        func_str = self.entry_func.get()
        x0 = self.entry_x0.get()
        tol = self.entry_tol.get()
        max_i = self.entry_max.get()
        
        solver = NewtonRoots(func_str, x0, tol, max_i)
        result = solver.solve()
        
        self.txt_res.delete("0.0", "end")
        self.txt_steps.delete("0.0", "end")
        self.ax.clear()
        self.apply_graph_theme()
        
        if not result["success"]:
            self.txt_res.insert("0.0", f"❌ Error:\n{result['error_message']}")
            self.canvas.draw()
            return
            
        self.txt_res.insert("0.0", f"📊 Resumen de Ejecución:\n\n{result['message']}")
        
        table_header = f"{'Iter':<6} | {'x_i':<14} | {'f(x_i)':<15} | {'Error (%)':<15}\n"
        table_header += "━" * 58 + "\n"
        self.txt_steps.insert("end", table_header)
        
        for step in result["steps"]:
            err_str = f"{step['error']:.6f}" if step["error"] is not None else "---"
            row = f"{step['iter']:<6} | {step['x']:<14.6f} | {step['fx']:<15.2e} | {err_str:<15}\n"
            self.txt_steps.insert("end", row)
            
        try:
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
            x_sym = sp.Symbol('x')
            f_num = sp.lambdify(x_sym, sp.sympify(func_str), 'numpy')
            
            x_curve = np.linspace(xmin, xmax, 500)
            self.ax.plot(x_curve, f_num(x_curve), label="f(x)", color="#58A1D3", lw=2)
            self.ax.axhline(0, color=COLOR_BORDER[1] if ctk.get_appearance_mode() == "Dark" else COLOR_BORDER[0], linestyle="--", linewidth=1)
            
            steps_data = result["steps"]
            if len(steps_data) > 1:
                x_iters = [s["x"] for s in steps_data[:-1]]
                y_iters = [s["fx"] for s in steps_data[:-1]]
                self.ax.scatter(x_iters, y_iters, color="#ff7f0e", marker="o", s=35, label="Iterados", zorder=3)
                self.ax.plot(x_iters, y_iters, color="#ff7f0e", linestyle=":", alpha=0.5)
            
            final_root = steps_data[-1]["x"]
            self.ax.scatter(final_root, steps_data[-1]["fx"], color="#2ca02c", marker="*", s=130, label=f"Raíz ({final_root:.4f})", zorder=4)
            
            is_dark = (ctk.get_appearance_mode() == "Dark")
            legend = self.ax.legend(loc="best")
            if legend:
                legend.get_frame().set_facecolor(COLOR_BG[1] if is_dark else COLOR_BG[0])
                legend.get_frame().set_edgecolor(COLOR_BORDER[1] if is_dark else COLOR_BORDER[0])
                for text in legend.get_texts():
                    text.set_color(COLOR_TEXT[1] if is_dark else COLOR_TEXT[0])
            
            self.ax.set_title("Evolución de los Iterados", fontdict={"size": 11, "weight": "bold"})
        except Exception as ex:
            self.ax.text(0.5, 0.5, f"Error al graficar:\n{str(ex)}", ha="center", va="center")
            
        self.canvas.draw()