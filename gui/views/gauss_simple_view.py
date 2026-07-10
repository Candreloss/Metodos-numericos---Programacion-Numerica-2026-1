import customtkinter as ctk #pyright: ignore
from tkinter import messagebox
import numpy as np #pyright: ignore
from logic.gauss_simple import GaussSimple
from gui.components.matrix_grid import MatrixGrid
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_section_font, get_label_font, get_mono_font
)

class GaussSimpleView(ctk.CTkFrame):
    """
    Vista/Pantalla que representa la interfaz del método de Gauss Simple.
    Contiene los parámetros del método, el ingreso de matriz y la pestaña de resultados.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.n_value = 3
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        self.mono_font = get_mono_font()
        
        # Configurar rejilla principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_layout()
        
        # Cargar ejemplo inicial por defecto
        self.load_preset("Chapra_Ex")

    def create_layout(self):
        # Cabecera de la sección
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        method_name = ctk.CTkLabel(header_frame, text="Método de Gauss Simple (Eliminación Gaussiana)", font=self.title_font, text_color=COLOR_LIGHT_CYAN)
        method_name.grid(row=0, column=0, sticky="w")
        
        method_desc = ctk.CTkLabel(header_frame, text="Resuelve sistemas de ecuaciones lineales Ax = b mediante eliminación hacia adelante y sustitución hacia atrás.", font=self.label_font, text_color=COLOR_MUTED)
        method_desc.grid(row=1, column=0, sticky="w", pady=(4, 0))
        
        # Contenido Dividido en dos paneles: Entrada (Izquierda) y Resultados (Derecha)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=6) # Panel de entrada
        content_frame.grid_columnconfigure(1, weight=5) # Panel de resultados
        content_frame.grid_rowconfigure(0, weight=1)
        
        # --- PANEL IZQUIERDO: CONFIGURACIÓN Y MATRIZ ---
        self.left_panel = ctk.CTkFrame(content_frame, fg_color=COLOR_PANEL, border_color=COLOR_BORDER, border_width=1, corner_radius=12)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(2, weight=1) # El área de la matriz se expande
        
        # 1. Configuración superior del panel izquierdo (Reorganizado en filas para evitar desbordamiento)
        config_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        config_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_columnconfigure(3, weight=1)
        
        # Fila 0: Dimensión (n) y Decimales
        n_label = ctk.CTkLabel(config_frame, text="Dimensión (n):", font=self.label_font, text_color=COLOR_TEXT)
        n_label.grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 10))
        
        self.n_combo = ctk.CTkComboBox(
            config_frame, 
            values=["2", "3", "4", "5", "6", "7"], 
            width=70, 
            command=self.on_n_changed,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8
        )
        self.n_combo.set("3")
        self.n_combo.grid(row=0, column=1, sticky="w", padx=(0, 20), pady=(0, 10))
        
        dec_label = ctk.CTkLabel(config_frame, text="Decimales:", font=self.label_font, text_color=COLOR_TEXT)
        dec_label.grid(row=0, column=2, sticky="w", padx=(0, 8), pady=(0, 10))
        
        self.dec_combo = ctk.CTkComboBox(
            config_frame, 
            values=["2", "4", "6", "8"], 
            width=70,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8
        )
        self.dec_combo.set("4")
        self.dec_combo.grid(row=0, column=3, sticky="w", pady=(0, 10))
        
        # Fila 1: Ejemplos (Presets) - Expansión completa usando columnspan
        preset_label = ctk.CTkLabel(config_frame, text="Ejemplos:", font=self.label_font, text_color=COLOR_TEXT)
        preset_label.grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 10))
        
        self.preset_combo = ctk.CTkComboBox(
            config_frame, 
            values=["Ejemplo Chapra (3x3)", "Requiere Pivoteo (3x3)", "Sistema Pequeño (2x2)", "Sistema Grande (5x5)"],
            width=260, 
            command=self.on_preset_selected,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8
        )
        self.preset_combo.set("Ejemplo Chapra (3x3)")
        self.preset_combo.grid(row=1, column=1, columnspan=3, sticky="ew", pady=(0, 10))
        
        # Fila 2: Opciones de cálculo (Pivoteo Switch)
        self.pivot_var = ctk.BooleanVar(value=True)
        self.pivot_switch = ctk.CTkSwitch(
            config_frame, 
            text="Pivoteo Parcial por Columna", 
            variable=self.pivot_var,
            progress_color=COLOR_ACCENT,
            fg_color=COLOR_BG,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            text_color=COLOR_TEXT,
            font=self.label_font
        )
        self.pivot_switch.grid(row=2, column=0, columnspan=4, sticky="w", pady=(5, 0))
        
        # 3. Contenedor de la Matriz [A | b]
        matrix_header = ctk.CTkLabel(self.left_panel, text="Ingrese los coeficientes del sistema [A | b]:", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        matrix_header.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 8))
        
        self.matrix_grid = MatrixGrid(self.left_panel)
        self.matrix_grid.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # 4. Botones de Acción inferiores
        actions_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        actions_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=20)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        self.btn_clear = ctk.CTkButton(
            actions_frame, 
            text="Limpiar Matriz", 
            fg_color="transparent", 
            hover_color=COLOR_BORDER,
            border_color=COLOR_INTERACTIVE_BORDER,
            border_width=1,
            text_color=COLOR_LIGHT_CYAN,
            font=self.label_font,
            corner_radius=8,
            height=38,
            command=self.matrix_grid.clear
        )
        self.btn_clear.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        
        self.btn_solve = ctk.CTkButton(
            actions_frame, 
            text="Resolver Sistema", 
            fg_color=COLOR_ACCENT, 
            hover_color=COLOR_ACCENT_HOVER,
            text_color=COLOR_BG,
            font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            corner_radius=8,
            height=38,
            command=self.solve_system
        )
        self.btn_solve.grid(row=0, column=1, padx=(6, 0), sticky="ew")
        
        # --- PANEL DERECHO: RESULTADOS ---
        self.right_panel = ctk.CTkFrame(content_frame, fg_color=COLOR_PANEL, border_color=COLOR_BORDER, border_width=1, corner_radius=12)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=0)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        # Pestañas de Resultados
        self.result_tabs = ctk.CTkTabview(
            self.right_panel, 
            fg_color=COLOR_PANEL, 
            segmented_button_fg_color=COLOR_BG,
            segmented_button_selected_color=COLOR_ACCENT,
            segmented_button_selected_hover_color=COLOR_ACCENT_HOVER,
            segmented_button_unselected_color=COLOR_BG,
            segmented_button_unselected_hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            corner_radius=8
        )
        self.result_tabs.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=12, pady=12)
        
        # Agregar pestañas
        self.tab_solution = self.result_tabs.add("Solución")
        self.tab_steps = self.result_tabs.add("Paso a Paso")
        self.tab_validation = self.result_tabs.add("Validación")
        
        # Configurar cada pestaña
        self.setup_solution_tab()
        self.setup_steps_tab()
        self.setup_validation_tab()

    def setup_solution_tab(self):
        self.tab_solution.grid_columnconfigure(0, weight=1)
        self.tab_solution.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(self.tab_solution, text="Vector Solución Obtenido", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_solution = ctk.CTkTextbox(
            self.tab_solution, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8
        )
        self.txt_solution.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_solution.insert("1.0", "Ingrese los datos del sistema y presione 'Resolver'.")
        self.txt_solution.configure(state="disabled")

    def setup_steps_tab(self):
        self.tab_steps.grid_columnconfigure(0, weight=1)
        self.tab_steps.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(self.tab_steps, text="Detalle de Operaciones de Eliminación", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_steps = ctk.CTkTextbox(
            self.tab_steps, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8
        )
        self.txt_steps.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_steps.insert("1.0", "Aquí se mostrará el paso a paso del método:\n1. Estados de la matriz aumentada.\n2. Pivoteo parcial si se realiza.\n3. Multiplicadores y operaciones por fila.\n4. Fórmulas de la sustitución hacia atrás.")
        self.txt_steps.configure(state="disabled")

    def setup_validation_tab(self):
        self.tab_validation.grid_columnconfigure(0, weight=1)
        self.tab_validation.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(self.tab_validation, text="Verificación Matemática: A · x = b", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_validation = ctk.CTkTextbox(
            self.tab_validation, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8
        )
        self.txt_validation.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_validation.insert("1.0", "Comprobación del error residual (r = b - A·x) para certificar la precisión del método.")
        self.txt_validation.configure(state="disabled")

    def on_n_changed(self, value):
        try:
            self.n_value = int(value)
            self.matrix_grid.update_grid(self.n_value)
            self.preset_combo.set("Manual")
        except ValueError:
            pass

    def on_preset_selected(self, value):
        if value == "Ejemplo Chapra (3x3)":
            self.load_preset("Chapra_Ex")
        elif value == "Requiere Pivoteo (3x3)":
            self.load_preset("Pivoteo_Ex")
        elif value == "Sistema Pequeño (2x2)":
            self.load_preset("Pequeño_Ex")
        elif value == "Sistema Grande (5x5)":
            self.load_preset("Grande_Ex")

    def load_preset(self, name):
        if name == "Chapra_Ex":
            self.n_value = 3
            self.n_combo.set("3")
            self.matrix_grid.update_grid(3)
            A_vals = [
                [3.0, -0.1, -0.2],
                [0.1, 7.0, -0.3],
                [0.3, -0.2, 10.0]
            ]
            b_vals = [7.85, -19.3, 71.4]
        elif name == "Pivoteo_Ex":
            self.n_value = 3
            self.n_combo.set("3")
            self.matrix_grid.update_grid(3)
            A_vals = [
                [0.0, 2.0, 1.0],
                [1.0, -2.0, -3.0],
                [5.0, -1.0, 3.0]
            ]
            b_vals = [5.0, -4.0, 14.0]
        elif name == "Pequeño_Ex":
            self.n_value = 2
            self.n_combo.set("2")
            self.matrix_grid.update_grid(2)
            A_vals = [
                [2.0, 1.0],
                [1.0, -3.0]
            ]
            b_vals = [8.0, -3.0]
        elif name == "Grande_Ex":
            self.n_value = 5
            self.n_combo.set("5")
            self.matrix_grid.update_grid(5)
            A_vals = [
                [4.0, -1.0, 0.0, 1.0, 0.0],
                [-1.0, 4.0, -1.0, 0.0, 1.0],
                [0.0, -1.0, 4.0, -1.0, 0.0],
                [1.0, 0.0, -1.0, 4.0, -1.0],
                [0.0, 1.0, 0.0, -1.0, 4.0]
            ]
            b_vals = [10.0, 5.0, 15.0, 0.0, 8.0]
            
        self.matrix_grid.load_values(A_vals, b_vals)

    def format_matrix_to_string(self, matrix, precision):
        lines = []
        n = len(matrix)
        col_widths = []
        num_cols = len(matrix[0])
        
        for col_idx in range(num_cols):
            max_w = 0
            for row in matrix:
                val = row[col_idx]
                val_str = f"{val:.{precision}f}"
                if precision > 2 and val_str.endswith("0"):
                    val_str = f"{val:.{precision}g}"
                max_w = max(max_w, len(val_str))
            col_widths.append(max_w)
            
        for i in range(n):
            row_str = "│ "
            for j in range(num_cols - 1):
                val_str = f"{matrix[i][j]:.{precision}f}"
                row_str += val_str.rjust(col_widths[j]) + "  "
            row_str += "║ "
            val_b_str = f"{matrix[i][-1]:.{precision}f}"
            row_str += val_b_str.rjust(col_widths[-1]) + " │"
            lines.append(row_str)
            
        return "\n".join(lines)

    def solve_system(self):
        try:
            A, b = self.matrix_grid.get_data()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Todos los valores deben ser números válidos.\n\nDetalle: {str(e)}")
            return
            
        pivoting = self.pivot_var.get()
        try:
            precision = int(self.dec_combo.get())
        except ValueError:
            precision = 4
            
        solver = GaussSimple(A, b, pivoting=pivoting)
        result = solver.solve()
        
        self.txt_solution.configure(state="normal")
        self.txt_steps.configure(state="normal")
        self.txt_validation.configure(state="normal")
        
        self.txt_solution.delete("1.0", ctk.END)
        self.txt_steps.delete("1.0", ctk.END)
        self.txt_validation.delete("1.0", ctk.END)
        
        if not result["success"]:
            err_msg = f"❌ ERROR EN LA RESOLUCIÓN:\n\n{result['error_message']}"
            self.txt_solution.insert("1.0", err_msg)
            self.txt_validation.insert("1.0", "Imposible verificar: El sistema no tiene una solución única.")
            
            steps_txt = "PASOS REALIZADOS ANTES DE LA FALLA:\n\n"
            for idx, step in enumerate(result["steps"]):
                steps_txt += f"Paso {idx + 1}: {step['description']}\n"
                steps_txt += self.format_matrix_to_string(step["matrix"], precision) + "\n\n"
            self.txt_steps.insert("1.0", steps_txt)
            self.result_tabs.set("Solución")
        else:
            sol = result["solution"]
            sol_text = "✅ ¡Sistema resuelto con éxito!\n\n"
            sol_text += f"Configuración: {'Con Pivoteo Parcial' if pivoting else 'Sin Pivoteo (Gauss Simple)'}\n"
            sol_text += f"Dimensión: {self.n_value} x {self.n_value}\n\n"
            sol_text += "RESULTADOS DE LAS INCÓGNITAS:\n"
            sol_text += "━" * 40 + "\n"
            for i, val in enumerate(sol):
                sol_text += f"  x[{i+1}] = {val:.{precision}f}\n"
            sol_text += "━" * 40 + "\n"
            self.txt_solution.insert("1.0", sol_text)
            
            steps_text = f"PASO A PASO DETALLADO (Precisión mostrada: {precision} decimales):\n\n"
            for step in result["steps"]:
                if step["type"] == "stage_start":
                    steps_text += "═" * 60 + "\n"
                    steps_text += f"{step['description']}\n"
                    steps_text += "═" * 60 + "\n\n"
                elif step["type"] == "back_substitution":
                    steps_text += "━" * 60 + "\n"
                    steps_text += f"{step['description']}\n"
                    steps_text += "━" * 60 + "\n"
                    for sub_step in step["back_sub_steps"]:
                        steps_text += f"  • {sub_step['formula']}\n"
                    steps_text += "\n"
                else:
                    steps_text += f"👉 {step['description']}\n"
                    steps_text += self.format_matrix_to_string(step["matrix"], precision) + "\n\n"
            self.txt_steps.insert("1.0", steps_text)
            
            A_arr = np.array(A)
            b_arr = np.array(b)
            x_arr = np.array(sol)
            calc_b = np.dot(A_arr, x_arr)
            residual = b_arr - calc_b
            norm_res = np.linalg.norm(residual)
            
            val_text = "COMPROBACIÓN DEL SISTEMA Ax = b:\n"
            val_text += "━" * 50 + "\n"
            val_text += f"{'Fila':<8}{'b original':<15}{'A · x calculado':<20}{'Residuo (Error)':<15}\n"
            val_text += "━" * 50 + "\n"
            for i in range(self.n_value):
                val_text += f"F{i+1:<7}{b[i]:<15.{precision}f}{calc_b[i]:<20.{precision}f}{residual[i]:<15.3e}\n"
            val_text += "━" * 50 + "\n\n"
            val_text += f"Norma Euclidiana del residuo ||r||_2: {norm_res:.3e}\n\n"
            if norm_res < 1e-10:
                val_text += "✓ La solución es matemática y numéricamente exacta (error residual insignificante)."
            elif norm_res < 1e-4:
                val_text += "⚠ La solución tiene un residuo pequeño pero aceptable (posible mal condicionamiento)."
            else:
                val_text += "❌ El residuo es elevado. Verifique si el sistema está muy mal condicionado."
            self.txt_validation.insert("1.0", val_text)
            self.result_tabs.set("Solución")
            
        self.txt_solution.configure(state="disabled")
        self.txt_steps.configure(state="disabled")
        self.txt_validation.configure(state="disabled")
