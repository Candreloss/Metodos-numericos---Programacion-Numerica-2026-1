import customtkinter as ctk  # pyright: ignore
from tkinter import messagebox
import numpy as np  # pyright: ignore
from lib.gaussSimple import GaussSimple

# Configuración del tema y colores según la paleta del usuario
COLOR_BG = "#011C40"          # Fondo principal
COLOR_PANEL = "#023859"       # Fondo de tarjetas/paneles
COLOR_BORDER = "#26658C"      # Bordes y elementos secundarios
COLOR_ACCENT = "#54ACBF"      # Botones principales y resaltados
COLOR_LIGHT_CYAN = "#A7EBF2"  # Títulos y textos destacados
COLOR_TEXT = "#FFFFFF"        # Texto estándar
COLOR_MUTED = "#B0BEC5"       # Texto secundario

class GaussSimpleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurar ventana principal
        self.title("Métodos Numéricos - Eliminación Gaussian")
        self.geometry("1100x750")
        self.minsize(1000, 650)
        self.configure(fg_color=COLOR_BG)
        
        # Estado de la aplicación
        self.n_value = 3
        self.entry_A = []  # Matriz de CTkEntry
        self.entry_b = []  # Vector de CTkEntry
        
        # Cargar fuentes predeterminadas elegantes
        self.title_font = ctk.CTkFont(family="Outfit", size=22, weight="bold")
        self.section_font = ctk.CTkFont(family="Outfit", size=16, weight="bold")
        self.label_font = ctk.CTkFont(family="Inter", size=13)
        self.mono_font = ctk.CTkFont(family="Consolas", size=12)
        
        # Configurar diseño de rejilla (Grid)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Crear Barra Lateral (Sidebar)
        self.create_sidebar()
        
        # 2. Crear Contenedor Principal
        self.create_main_container()
        
        # Dibujar la cuadrícula inicial de 3x3
        self.update_matrix_grid()
        
        # Cargar el primer ejemplo por defecto
        self.load_preset("Chapra_Ex")

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLOR_PANEL, border_color=COLOR_BORDER, border_width=1)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(5, weight=1)
        
        # Título del software
        title_label = ctk.CTkLabel(sidebar, text="PROGRAMACIÓN\nNUMÉRICA", font=self.title_font, text_color=COLOR_LIGHT_CYAN)
        title_label.grid(row=0, column=0, padx=20, pady=30)
        
        # Separador
        sep = ctk.CTkFrame(sidebar, height=2, fg_color=COLOR_BORDER)
        sep.grid(row=1, column=0, sticky="ew", padx=20, pady=0)
        
        # Sección de selección de métodos
        method_title = ctk.CTkLabel(sidebar, text="MÉTODOS", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        method_title.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Menú de Métodos (Botón activo para Gauss Simple, otros inactivos para el grupo)
        self.btn_gauss_simple = ctk.CTkButton(
            sidebar, 
            text="Gauss Simple", 
            fg_color=COLOR_BORDER, 
            text_color=COLOR_LIGHT_CYAN,
            hover_color=COLOR_BORDER,
            font=self.label_font,
            anchor="w"
        )
        self.btn_gauss_simple.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_gauss_seidel = ctk.CTkButton(
            sidebar, 
            text="Gauss-Seidel (Prox.)", 
            fg_color="transparent", 
            text_color=COLOR_MUTED,
            state="disabled",
            font=self.label_font,
            anchor="w"
        )
        self.btn_gauss_seidel.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # Firma/Info del Proyecto en el fondo de la barra lateral
        info_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        info_frame.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        
        lib_label = ctk.CTkLabel(info_frame, text="Libro: Chapra & Canale", font=ctk.CTkFont(family="Inter", size=11, slant="italic"), text_color=COLOR_MUTED)
        lib_label.pack(anchor="w")
        
        author_label = ctk.CTkLabel(info_frame, text="Desarrollado por: Alondra León", font=ctk.CTkFont(family="Inter", size=11), text_color=COLOR_MUTED)
        author_label.pack(anchor="w", pady=(2, 0))

    def create_main_container(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Cabecera de la sección
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_frame.grid_columnconfigure(0, weight=1)
        
        method_name = ctk.CTkLabel(header_frame, text="Método de Gauss Simple (Eliminación Gaussiana)", font=self.title_font, text_color=COLOR_LIGHT_CYAN)
        method_name.grid(row=0, column=0, sticky="w")
        
        method_desc = ctk.CTkLabel(header_frame, text="Resuelve sistemas de ecuaciones lineales Ax = b mediante eliminación hacia adelante y sustitución hacia atrás.", font=self.label_font, text_color=COLOR_MUTED)
        method_desc.grid(row=1, column=0, sticky="w", pady=(2, 0))
        
        # Contenido Dividido en dos paneles: Entrada (Izquierda) y Resultados (Derecha)
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=6) # Panel de entrada
        content_frame.grid_columnconfigure(1, weight=5) # Panel de resultados
        content_frame.grid_rowconfigure(0, weight=1)
        
        # --- PANEL IZQUIERDO: CONFIGURACIÓN Y MATRIZ ---
        self.left_panel = ctk.CTkFrame(content_frame, fg_color=COLOR_PANEL, border_color=COLOR_BORDER, border_width=1)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(2, weight=1) # El área de la matriz se expande
        
        # 1. Configuración superior del panel izquierdo
        config_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        config_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        # Tamaño de matriz (n)
        n_label = ctk.CTkLabel(config_frame, text="Dimensión (n):", font=self.label_font, text_color=COLOR_LIGHT_CYAN)
        n_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.n_combo = ctk.CTkComboBox(config_frame, values=["2", "3", "4", "5", "6", "7"], width=70, command=self.on_n_changed)
        self.n_combo.set("3")
        self.n_combo.grid(row=0, column=1, sticky="w", padx=(0, 15))
        
        # Selector de ejemplos predefinidos
        preset_label = ctk.CTkLabel(config_frame, text="Ejemplos:", font=self.label_font, text_color=COLOR_LIGHT_CYAN)
        preset_label.grid(row=0, column=2, sticky="w", padx=(0, 5))
        
        self.preset_combo = ctk.CTkComboBox(
            config_frame, 
            values=["Ejemplo Chapra (3x3)", "Requiere Pivoteo (3x3)", "Sistema Pequeño (2x2)", "Sistema Grande (5x5)"],
            width=200, 
            command=self.on_preset_selected
        )
        self.preset_combo.set("Ejemplo Chapra (3x3)")
        self.preset_combo.grid(row=0, column=3, sticky="w")
        
        # 2. Opciones de cálculo
        options_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        options_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        
        # Checkbox Pivoteo
        self.pivot_var = ctk.BooleanVar(value=True)
        self.pivot_switch = ctk.CTkSwitch(
            options_frame, 
            text="Pivoteo Parcial por Columna", 
            variable=self.pivot_var,
            progress_color=COLOR_ACCENT,
            text_color=COLOR_TEXT,
            font=self.label_font
        )
        self.pivot_switch.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        # Selección de decimales
        dec_label = ctk.CTkLabel(options_frame, text="Decimales:", font=self.label_font, text_color=COLOR_TEXT)
        dec_label.grid(row=0, column=1, sticky="w", padx=(0, 5))
        
        self.dec_combo = ctk.CTkComboBox(options_frame, values=["2", "4", "6", "8"], width=70)
        self.dec_combo.set("4")
        self.dec_combo.grid(row=0, column=2, sticky="w")
        
        # 3. Contenedor de la Matriz (Scrollable)
        matrix_header = ctk.CTkLabel(self.left_panel, text="Ingrese los coeficientes del sistema [A | b]:", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        matrix_header.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 5))
        
        self.matrix_scroll = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.matrix_scroll.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # 4. Botones de Acción inferiores
        actions_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        actions_frame.grid(row=4, column=0, sticky="ew", padx=15, pady=15)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)
        
        self.btn_clear = ctk.CTkButton(
            actions_frame, 
            text="Limpiar Matriz", 
            fg_color="transparent", 
            hover_color=COLOR_BORDER,
            border_color=COLOR_BORDER,
            border_width=1,
            text_color=COLOR_LIGHT_CYAN,
            font=self.label_font,
            command=self.clear_matrix
        )
        self.btn_clear.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_solve = ctk.CTkButton(
            actions_frame, 
            text="Resolver Sistema", 
            fg_color=COLOR_ACCENT, 
            hover_color="#3fa2b5",
            text_color="#011C40",
            font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
            command=self.solve_system
        )
        self.btn_solve.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # --- PANEL DERECHO: RESULTADOS ---
        self.right_panel = ctk.CTkFrame(content_frame, fg_color=COLOR_PANEL, border_color=COLOR_BORDER, border_width=1)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        # Pestañas de Resultados
        self.result_tabs = ctk.CTkTabview(
            self.right_panel, 
            fg_color=COLOR_PANEL, 
            segmented_button_fg_color=COLOR_BG,
            segmented_button_selected_color=COLOR_BORDER,
            segmented_button_selected_hover_color=COLOR_ACCENT,
            segmented_button_unselected_color=COLOR_BG,
            segmented_button_unselected_hover_color=COLOR_BORDER,
            text_color=COLOR_TEXT
        )
        self.result_tabs.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        
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
        
        # Título interior
        lbl = ctk.CTkLabel(self.tab_solution, text="Vector Solución Obtenido", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # TextBox para la solución
        self.txt_solution = ctk.CTkTextbox(self.tab_solution, fg_color=COLOR_BG, font=self.mono_font, text_color=COLOR_TEXT, border_color=COLOR_BORDER, border_width=1)
        self.txt_solution.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_solution.insert("1.0", "Ingrese los datos del sistema y presione 'Resolver'.")
        self.txt_solution.configure(state="disabled")

    def setup_steps_tab(self):
        self.tab_steps.grid_columnconfigure(0, weight=1)
        self.tab_steps.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(self.tab_steps, text="Detalle de Operaciones de Eliminación", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_steps = ctk.CTkTextbox(self.tab_steps, fg_color=COLOR_BG, font=self.mono_font, text_color=COLOR_TEXT, border_color=COLOR_BORDER, border_width=1)
        self.txt_steps.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_steps.insert("1.0", "Aquí se mostrará el paso a paso del método:\n1. Estados de la matriz aumentada.\n2. Pivoteo parcial si se realiza.\n3. Multiplicadores y operaciones por fila.\n4. Fórmulas de la sustitución hacia atrás.")
        self.txt_steps.configure(state="disabled")

    def setup_validation_tab(self):
        self.tab_validation.grid_columnconfigure(0, weight=1)
        self.tab_validation.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(self.tab_validation, text="Verificación Matemática: A · x = b", font=self.section_font, text_color=COLOR_LIGHT_CYAN)
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_validation = ctk.CTkTextbox(self.tab_validation, fg_color=COLOR_BG, font=self.mono_font, text_color=COLOR_TEXT, border_color=COLOR_BORDER, border_width=1)
        self.txt_validation.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_validation.insert("1.0", "Comprobación del error residual (r = b - A·x) para certificar la precisión del método.")
        self.txt_validation.configure(state="disabled")

    def update_matrix_grid(self):
        """Reconstruye dinámicamente la cuadrícula de inputs de la matriz según N."""
        # Limpiar widgets previos
        for widget in self.matrix_scroll.winfo_children():
            widget.destroy()
            
        self.entry_A = []
        self.entry_b = []
        
        # Configurar pesos de columnas en la rejilla del scrollable frame
        n = self.n_value
        
        # Crear etiquetas de cabecera de columna
        for j in range(n):
            col_lbl = ctk.CTkLabel(self.matrix_scroll, text=f"Columna {j+1}", font=ctk.CTkFont(family="Inter", size=11, weight="bold"), text_color=COLOR_LIGHT_CYAN)
            col_lbl.grid(row=0, column=2*j, padx=2, pady=5)
            
        col_b_lbl = ctk.CTkLabel(self.matrix_scroll, text="Vector b", font=ctk.CTkFont(family="Inter", size=11, weight="bold"), text_color=COLOR_ACCENT)
        col_b_lbl.grid(row=0, column=2*n, padx=5, pady=5)
        
        # Generar filas de inputs
        for i in range(n):
            row_A = []
            
            # Etiqueta indicadora de fila
            row_lbl = ctk.CTkLabel(self.matrix_scroll, text=f"F{i+1}: ", font=self.label_font, text_color=COLOR_MUTED)
            row_lbl.grid(row=i+1, column=0, padx=(0, 5), pady=3)
            
            for j in range(n):
                # Campo de texto para A[i][j]
                entry = ctk.CTkEntry(
                    self.matrix_scroll, 
                    width=60, 
                    fg_color=COLOR_BG, 
                    border_color=COLOR_BORDER, 
                    text_color=COLOR_TEXT,
                    font=self.mono_font,
                    justify="center"
                )
                
                # Layout
                # Col 2*j + 1 es el Entry, Col 2*j + 2 es el símbolo
                entry.grid(row=i+1, column=2*j + 1, padx=2, pady=3)
                row_A.append(entry)
                
                # Símbolos matemáticos para guiar al usuario
                if j < n - 1:
                    sym = ctk.CTkLabel(self.matrix_scroll, text=f"x{j+1} +", font=self.label_font, text_color=COLOR_MUTED)
                else:
                    sym = ctk.CTkLabel(self.matrix_scroll, text=f"x{j+1} =", font=self.label_font, text_color=COLOR_LIGHT_CYAN)
                sym.grid(row=i+1, column=2*j + 2, padx=2, pady=3)
                
            # Campo de texto para b[i]
            entry_b_i = ctk.CTkEntry(
                self.matrix_scroll, 
                width=65, 
                fg_color=COLOR_BG, 
                border_color=COLOR_ACCENT, 
                text_color=COLOR_TEXT,
                font=self.mono_font,
                justify="center"
            )
            entry_b_i.grid(row=i+1, column=2*n + 1, padx=(5, 5), pady=3)
            
            self.entry_A.append(row_A)
            self.entry_b.append(entry_b_i)

    def on_n_changed(self, value):
        try:
            self.n_value = int(value)
            self.update_matrix_grid()
            # Limpiar la selección de presets para no confundir al usuario
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
            self.update_matrix_grid()
            
            # Datos del Chapra pág. 248
            A_vals = [
                [3.0, -0.1, -0.2],
                [0.1, 7.0, -0.3],
                [0.3, -0.2, 10.0]
            ]
            b_vals = [7.85, -19.3, 71.4]
            
        elif name == "Pivoteo_Ex":
            self.n_value = 3
            self.n_combo.set("3")
            self.update_matrix_grid()
            
            # Requiere pivoteo por tener 0 en la diagonal inicial
            A_vals = [
                [0.0, 2.0, 1.0],
                [1.0, -2.0, -3.0],
                [5.0, -1.0, 3.0]
            ]
            b_vals = [5.0, -4.0, 14.0]
            
        elif name == "Pequeño_Ex":
            self.n_value = 2
            self.n_combo.set("2")
            self.update_matrix_grid()
            
            A_vals = [
                [2.0, 1.0],
                [1.0, -3.0]
            ]
            b_vals = [8.0, -3.0]
            
        elif name == "Grande_Ex":
            self.n_value = 5
            self.n_combo.set("5")
            self.update_matrix_grid()
            
            A_vals = [
                [4.0, -1.0, 0.0, 1.0, 0.0],
                [-1.0, 4.0, -1.0, 0.0, 1.0],
                [0.0, -1.0, 4.0, -1.0, 0.0],
                [1.0, 0.0, -1.0, 4.0, -1.0],
                [0.0, 1.0, 0.0, -1.0, 4.0]
            ]
            b_vals = [10.0, 5.0, 15.0, 0.0, 8.0]
            
        # Rellenar inputs
        for i in range(self.n_value):
            for j in range(self.n_value):
                self.entry_A[i][j].insert(0, str(A_vals[i][j]))
            self.entry_b[i].insert(0, str(b_vals[i]))

    def clear_matrix(self):
        for i in range(self.n_value):
            for j in range(self.n_value):
                self.entry_A[i][j].delete(0, ctk.END)
            self.entry_b[i].delete(0, ctk.END)

    def get_matrix_data(self):
        """Lee y parsea la información de la matriz A y el vector b de los inputs."""
        n = self.n_value
        A = []
        b = []
        
        try:
            for i in range(n):
                row = []
                for j in range(n):
                    val_str = self.entry_A[i][j].get().strip()
                    if not val_str:
                        raise ValueError(f"Celda A[{i+1}][{j+1}] vacía.")
                    row.append(float(val_str))
                A.append(row)
                
                val_b_str = self.entry_b[i].get().strip()
                if not val_b_str:
                    raise ValueError(f"Celda b[{i+1}] vacía.")
                b.append(float(val_b_str))
                
            return A, b
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Todos los valores deben ser números válidos.\n\nDetalle: {str(e)}")
            return None, None

    def format_matrix_to_string(self, matrix, precision):
        """Genera una representación bonita en texto monoespaciado de la matriz aumentada."""
        lines = []
        n = len(matrix)
        
        # Encontrar el ancho máximo de cada columna para formatear de forma tabulada
        col_widths = []
        num_cols = len(matrix[0])
        
        for col_idx in range(num_cols):
            max_w = 0
            for row in matrix:
                val = row[col_idx]
                val_str = f"{val:.{precision}f}"
                # Quitar ceros redundantes a la derecha si es float limpio
                if precision > 2 and val_str.endswith("0"):
                    val_str = f"{val:.{precision}g}"
                max_w = max(max_w, len(val_str))
            col_widths.append(max_w)
            
        for i in range(n):
            row_str = "│ "
            for j in range(num_cols - 1):
                val_str = f"{matrix[i][j]:.{precision}f}"
                # Ajustar al ancho máximo
                row_str += val_str.rjust(col_widths[j]) + "  "
            # Separador de la matriz aumentada
            row_str += "║ "
            val_b_str = f"{matrix[i][-1]:.{precision}f}"
            row_str += val_b_str.rjust(col_widths[-1]) + " │"
            lines.append(row_str)
            
        return "\n".join(lines)

    def solve_system(self):
        # 1. Obtener datos
        A, b = self.get_matrix_data()
        if A is None:
            return
            
        pivoting = self.pivot_var.get()
        
        try:
            precision = int(self.dec_combo.get())
        except ValueError:
            precision = 4
            
        # 2. Ejecutar método
        solver = GaussSimple(A, b, pivoting=pivoting)
        result = solver.solve()
        
        # 3. Mostrar resultados en pestañas
        self.txt_solution.configure(state="normal")
        self.txt_steps.configure(state="normal")
        self.txt_validation.configure(state="normal")
        
        self.txt_solution.delete("1.0", ctk.END)
        self.txt_steps.delete("1.0", ctk.END)
        self.txt_validation.delete("1.0", ctk.END)
        
        if not result["success"]:
            # Caso de error (singular, división entre cero)
            err_msg = f"❌ ERROR EN LA RESOLUCIÓN:\n\n{result['error_message']}"
            self.txt_solution.insert("1.0", err_msg)
            self.txt_validation.insert("1.0", "Imposible verificar: El sistema no tiene una solución única.")
            
            # Poner los pasos acumulados hasta la falla en la pestaña de pasos
            steps_txt = "PASOS REALIZADOS ANTES DE LA FALLA:\n\n"
            for idx, step in enumerate(result["steps"]):
                steps_txt += f"Paso {idx + 1}: {step['description']}\n"
                steps_txt += self.format_matrix_to_string(step["matrix"], precision) + "\n\n"
            self.txt_steps.insert("1.0", steps_txt)
            
            # Mover a la pestaña de solución para mostrar el error
            self.result_tabs.set("Solución")
            
        else:
            # Caso exitoso
            sol = result["solution"]
            
            # --- PESTAÑA 1: SOLUCIÓN ---
            sol_text = "✅ ¡Sistema resuelto con éxito!\n\n"
            sol_text += f"Configuración: {'Con Pivoteo Parcial' if pivoting else 'Sin Pivoteo (Gauss Simple)'}\n"
            sol_text += f"Dimensión: {self.n_value} x {self.n_value}\n\n"
            sol_text += "RESULTADOS DE LAS INCÓGNITAS:\n"
            sol_text += "━" * 40 + "\n"
            for i, val in enumerate(sol):
                sol_text += f"  x[{i+1}] = {val:.{precision}f}\n"
            sol_text += "━" * 40 + "\n"
            
            self.txt_solution.insert("1.0", sol_text)
            
            # --- PESTAÑA 2: PASO A PASO ---
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
            
            # --- PESTAÑA 3: VALIDACIÓN (A·x = b) ---
            # Calcular residuo usando numpy
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
            
            # Cambiar a la pestaña de solución
            self.result_tabs.set("Solución")
            
        self.txt_solution.configure(state="disabled")
        self.txt_steps.configure(state="disabled")
        self.txt_validation.configure(state="disabled")
