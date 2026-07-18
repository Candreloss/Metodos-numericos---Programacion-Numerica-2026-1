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
from lib.secante import SecantRoots

class SecantRootsView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.sidebar = Sidebar(self, active_method="secant_roots")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.content_frame.grid_columnconfigure(0, weight=1, minsize=340)
        self.content_frame.grid_columnconfigure(1, weight=2)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        
        self.title_label = ctk.CTkLabel(
            self.content_frame, 
            text="📐 Cálculo de Raíces: Método de la Secante", 
            font=self.title_font, 
            text_color=COLOR_LIGHT_CYAN
        )
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        self.input_card = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=COLOR_PANEL,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=12,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.input_card.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=0)
        self.setup_inputs()
        
        self.right_panel = ctk.CTkFrame(
            self.content_frame,
            fg_color=COLOR_PANEL,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=12
        )
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(15, 0), pady=0)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(0, weight=1)
        
        self.output_panel = ctk.CTkTabview(
            self.right_panel,
            fg_color=COLOR_PANEL,
            segmented_button_fg_color=COLOR_BG,
            segmented_button_selected_color=("#58A1D3", "#0F4C81"),
            segmented_button_selected_hover_color=("#3e87b7", "#0b3a63"),
            segmented_button_unselected_color=COLOR_BG,
            segmented_button_unselected_hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            corner_radius=8
        )
        self.output_panel.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        
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
            ("Aproximación Inicial x0:", "entry_x0", "0.0"),
            ("Aproximación Inicial x1:", "entry_x1", "1.0"),
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
            text_color=COLOR_BG,
            corner_radius=8,
            height=40,
            command=self.solve_secant
        )
        self.btn_calc.pack(fill="x", padx=15, pady=20)

    def setup_outputs(self):
        self.txt_res = ctk.CTkTextbox(
            self.tab_res, font=self.label_font, fg_color=COLOR_BG,
            border_color=COLOR_BORDER, border_width=1, text_color=COLOR_TEXT, corner_radius=8,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_res.pack(fill="both", expand=True, padx=15, pady=15)
        self.txt_res.insert("0.0", "Ingrese los parámetros y presione 'Calcular Raíz' para ver el diagnóstico.")
        
        self.txt_steps = ctk.CTkTextbox(
            self.tab_steps, font=ctk.CTkFont(family="Consolas", size=12), fg_color=COLOR_BG,
            border_color=COLOR_BORDER, border_width=1, text_color=COLOR_TEXT, corner_radius=8,
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
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

    def solve_secant(self):
        func_str = self.entry_func.get()
        
        try:
            x0 = float(self.entry_x0.get())
            x1 = float(self.entry_x1.get())
            tol = float(self.entry_tol.get())
            max_i = int(self.entry_max.get())
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
            
            if max_i <= 0:
                raise ValueError("Las iteraciones máximas deben ser un entero positivo mayor a 0.")
            if tol <= 0:
                raise ValueError("La tolerancia debe ser un valor positivo (ej. 1e-5).")
            if x0 == x1:
                raise ValueError("Las aproximaciones iniciales x0 y x1 no pueden ser iguales para iniciar la Secante.")
            if xmin >= xmax:
                raise ValueError("El dominio de la gráfica es inválido (X min debe ser estrictamente menor a X max).")
                
        except ValueError as e:
            err_msg = str(e)
            if "could not convert" in err_msg or "invalid literal" in err_msg:
                err_msg = "Asegúrese de que los puntos, Tolerancia, Iteraciones y el Dominio contengan únicamente números."

            self.txt_res.configure(state="normal")
            self.txt_res.delete("0.0", "end")
            self.txt_res.insert("0.0", f"❌ Error de Entrada:\n{err_msg}")
            self.txt_res.configure(state="disabled")
            return

        solver = SecantRoots(func_str, x0, x1, tol, max_i)
        result = solver.solve()

        self.txt_res.configure(state="normal")
        self.txt_steps.configure(state="normal")

        self.txt_res.delete("0.0", "end")
        self.txt_steps.delete("0.0", "end")
        self.ax.clear()
        self.apply_graph_theme()

        if not result["success"]:
            self.txt_res.insert("0.0", f"❌ Error:\n{result['error_message']}")

            if result["steps"]:
                table_header = f"{'Iter':<6} | {'x_i':<14} | {'f(x_i)':<15} | {'Error (%)':<15}\n"
                table_header += "━" * 58 + "\n"
                self.txt_steps.insert("end", table_header)
                for step in result["steps"]:
                    err_str = f"{step['error']:.6f}" if step["error"] is not None else "---"
                    row = f"{step['iter']:<6} | {step['x']:<14.6f} | {step['fx']:<15.2e} | {err_str:<15}\n"
                    self.txt_steps.insert("end", row)

            self.txt_res.configure(state="disabled")
            self.txt_steps.configure(state="disabled")
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
            
        self.txt_res.configure(state="disabled")
        self.txt_steps.configure(state="disabled")
        
        try:
            xmin = float(self.entry_xmin.get())
            xmax = float(self.entry_xmax.get())
            x_sym = sp.Symbol('x')
            cleaned_str = func_str.replace('sen(', 'sin(')
            f_num = sp.lambdify(x_sym, sp.sympify(cleaned_str), 'numpy')
            
            x_curve = np.linspace(xmin, xmax, 500)
            
            with np.errstate(divide='ignore', invalid='ignore'):
                y_curve = f_num(x_curve)
                if np.isscalar(y_curve):
                    y_curve = np.full_like(x_curve, y_curve)

            if np.isnan(y_curve).all():
                raise ValueError("La función es compleja o\nindefinida en este dominio.")
                
            self.ax.plot(x_curve, y_curve, label="f(x)", color="#58A1D3", lw=2)
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
            is_dark = (ctk.get_appearance_mode() == "Dark")
            txt_color = COLOR_TEXT[1] if is_dark else COLOR_TEXT[0]
            self.ax.text(0.5, 0.5, f"⚠ Gráfica no disponible:\n{str(ex)}", 
                         ha="center", va="center", transform=self.ax.transAxes, 
                         color=txt_color, weight="bold")
            
        self.canvas.draw()