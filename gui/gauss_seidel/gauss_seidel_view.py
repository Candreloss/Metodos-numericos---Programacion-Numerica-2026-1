# -*- coding: utf-8 -*-
"""
Vista que representa la interfaz de usuario para el método de Gauss-Seidel.
"""

import customtkinter as ctk #pyright: ignore
from tkinter import messagebox
import numpy as np #pyright: ignore
from lib.gauss_seidel import GaussSeidel
from gui.components.matrix_grid import MatrixGrid
from gui.components.sidebar import Sidebar
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_section_font, get_label_font, get_mono_font
)

class GaussSeidelView(ctk.CTkFrame):
    """
    Vista/Pantalla que representa la interfaz del método de Gauss-Seidel.
    Contiene la configuración de parámetros, la estimación inicial, 
    la matriz de coeficientes y el visualizador de resultados en pestañas.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.n_value = 3
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        self.mono_font = get_mono_font()
        
        # Configurar rejilla principal
        self.grid_columnconfigure(0, weight=0) # Sidebar
        self.grid_columnconfigure(1, weight=1) # Contenido principal
        self.grid_rowconfigure(0, weight=1)
        
        self.create_layout()
        
        # Cargar ejemplo inicial por defecto
        self.load_preset("Chapra_Ex")

    def create_layout(self):
        # 1. Instanciar la Barra Lateral Global
        self.sidebar = Sidebar(self, active_method="gauss_seidel")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # 2. Contenedor de contenido de la vista
        self.view_container = ctk.CTkFrame(self, fg_color="transparent")
        self.view_container.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.view_container.grid_columnconfigure(0, weight=1)
        self.view_container.grid_rowconfigure(1, weight=1)
        
        # Cabecera de la sección
        header_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        method_name = ctk.CTkLabel(
            header_frame, 
            text="Método de Gauss-Seidel", 
            font=self.title_font, 
            text_color=COLOR_LIGHT_CYAN
        )
        method_name.grid(row=0, column=0, sticky="w")
        
        method_desc = ctk.CTkLabel(
            header_frame, 
            text="Resuelve sistemas de ecuaciones lineales Ax = b de forma iterativa mediante aproximaciones sucesivas y relajación opcional.", 
            font=self.label_font, 
            text_color=COLOR_MUTED
        )
        method_desc.grid(row=1, column=0, sticky="w", pady=(4, 0))
        
        # Contenido dividido en dos paneles
        content_frame = ctk.CTkFrame(self.view_container, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1) # Panel de entrada
        content_frame.grid_columnconfigure(1, weight=1) # Panel de resultados (igual peso para dar espacio a las pestañas)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # --- PANEL IZQUIERDO: CONFIGURACIÓN, VALORES INICIALES Y MATRIZ ---
        self.left_panel = ctk.CTkFrame(
            content_frame, 
            fg_color=COLOR_PANEL, 
            border_color=COLOR_BORDER, 
            border_width=1, 
            corner_radius=12
        )
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12), pady=0)
        self.left_panel.grid_columnconfigure(0, weight=1)
        self.left_panel.grid_rowconfigure(6, weight=1) # El área de la matriz se expande verticalmente
        
        # 1. Configuración superior del panel izquierdo
        config_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        config_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        config_frame.grid_columnconfigure((1, 3, 5), weight=1)
        
        # Fila 0: Dimensión (n), Decimales y Ejemplos (Presets)
        n_label = ctk.CTkLabel(config_frame, text="Dimensión (n):", font=self.label_font, text_color=COLOR_TEXT)
        n_label.grid(row=0, column=0, sticky="w", padx=(0, 5), pady=(0, 10))
        
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
            text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8
        )
        self.n_combo.set("3")
        self.n_combo.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(0, 10))
        
        dec_label = ctk.CTkLabel(config_frame, text="Decimales:", font=self.label_font, text_color=COLOR_TEXT)
        dec_label.grid(row=0, column=2, sticky="w", padx=(0, 5), pady=(0, 10))
        
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
            text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8
        )
        self.dec_combo.set("4")
        self.dec_combo.grid(row=0, column=3, sticky="ew", padx=(0, 10), pady=(0, 10))
        
        preset_label = ctk.CTkLabel(config_frame, text="Ejemplos:", font=self.label_font, text_color=COLOR_TEXT)
        preset_label.grid(row=0, column=4, sticky="w", padx=(0, 5), pady=(0, 10))
        
        self.preset_combo = ctk.CTkComboBox(
            config_frame, 
            values=["Ejemplo Chapra (3x3)", "Dominante (3x3)", "Divergente (3x3)", "Manual"],
            width=130, 
            command=self.on_preset_selected,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT,
            text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8
        )
        self.preset_combo.set("Ejemplo Chapra (3x3)")
        self.preset_combo.grid(row=0, column=5, sticky="ew", pady=(0, 10))
        
        # Fila 1: Tolerancia (%), Max Iter y Relajación
        tol_label = ctk.CTkLabel(config_frame, text="Tolerancia (%):", font=self.label_font, text_color=COLOR_TEXT)
        tol_label.grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(0, 10))
        
        self.tol_entry = ctk.CTkEntry(
            config_frame,
            width=70,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            text_color=COLOR_TEXT,
            font=self.mono_font,
            corner_radius=8
        )
        self.tol_entry.insert(0, "1e-5")
        self.tol_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 10))
        
        iter_label = ctk.CTkLabel(config_frame, text="Max Iter:", font=self.label_font, text_color=COLOR_TEXT)
        iter_label.grid(row=1, column=2, sticky="w", padx=(0, 5), pady=(0, 10))
        
        self.max_iter_entry = ctk.CTkEntry(
            config_frame,
            width=70,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            text_color=COLOR_TEXT,
            font=self.mono_font,
            corner_radius=8
        )
        self.max_iter_entry.insert(0, "150")
        self.max_iter_entry.grid(row=1, column=3, sticky="ew", padx=(0, 10), pady=(0, 10))
        
        relax_label = ctk.CTkLabel(config_frame, text="Relajación (λ):", font=self.label_font, text_color=COLOR_TEXT)
        relax_label.grid(row=1, column=4, sticky="w", padx=(0, 5), pady=(0, 10))
        
        self.relax_entry = ctk.CTkEntry(
            config_frame,
            width=70,
            fg_color=COLOR_BG,
            border_color=COLOR_INTERACTIVE_BORDER,
            text_color=COLOR_TEXT,
            font=self.mono_font,
            corner_radius=8
        )
        self.relax_entry.insert(0, "1.0")
        self.relax_entry.grid(row=1, column=5, sticky="ew", pady=(0, 10))
        
        # Separador muy delgado
        sep = ctk.CTkFrame(self.left_panel, height=1, fg_color=COLOR_BORDER)
        sep.grid(row=1, column=0, sticky="ew", padx=15, pady=(5, 10))
        
        # 2. Contenedor de Estimación Inicial
        x0_header = ctk.CTkLabel(
            self.left_panel, 
            text="Estimación Inicial x^(0):", 
            font=self.section_font, 
            text_color=COLOR_LIGHT_CYAN
        )
        x0_header.grid(row=2, column=0, sticky="w", padx=15, pady=(0, 5))
        
        self.x0_container = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.x0_container.grid(row=3, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.entry_x0 = []
        self.update_x0_grid(self.n_value)
        
        # Separador
        sep2 = ctk.CTkFrame(self.left_panel, height=1, fg_color=COLOR_BORDER)
        sep2.grid(row=4, column=0, sticky="ew", padx=15, pady=(5, 10))
        
        # 3. Contenedor de la Matriz [A | b]
        matrix_header = ctk.CTkLabel(
            self.left_panel, 
            text="Ingrese los coeficientes del sistema [A | b]:", 
            font=self.section_font, 
            text_color=COLOR_LIGHT_CYAN
        )
        matrix_header.grid(row=5, column=0, sticky="w", padx=15, pady=(5, 8))
        
        self.matrix_grid = MatrixGrid(self.left_panel)
        # Fijar altura de grid para evitar scrollbars infinitas dentro del scroll principal
        self.matrix_grid.grid(row=6, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.matrix_grid.configure(height=260)
        
        # 4. Botones de Acción inferiores
        actions_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        actions_frame.grid(row=7, column=0, sticky="ew", padx=15, pady=(5, 15))
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
            command=self.clear_matrix_and_x0
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
        self.right_panel = ctk.CTkFrame(
            content_frame, 
            fg_color=COLOR_PANEL, 
            border_color=COLOR_BORDER, 
            border_width=1, 
            corner_radius=12
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(12, 0), pady=0)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=1)
        
        self.result_tabs = ctk.CTkTabview(
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
        self.result_tabs.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=12, pady=12)
        
        # Agregar pestañas
        self.tab_solution = self.result_tabs.add("Solución")
        self.tab_steps = self.result_tabs.add("Iteraciones")
        self.tab_pasos = self.result_tabs.add("Paso a Paso")
        self.tab_validation = self.result_tabs.add("Validación")
        
        # Configurar cada pestaña
        self.setup_solution_tab()
        self.setup_steps_tab()
        self.setup_pasos_tab()
        self.setup_validation_tab()

    def setup_solution_tab(self):
        self.tab_solution.grid_columnconfigure(0, weight=1)
        self.tab_solution.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(
            self.tab_solution, 
            text="Vector Solución Iterativo", 
            font=self.section_font, 
            text_color=COLOR_LIGHT_CYAN,
            anchor="w",
            justify="left",
            wraplength=380
        )
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_solution = ctk.CTkTextbox(
            self.tab_solution, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8,
            wrap="none",
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_solution.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_solution.insert("1.0", "Ingrese los datos del sistema y presione 'Resolver'.")
        self.txt_solution.configure(state="disabled")

    def setup_steps_tab(self):
        self.tab_steps.grid_columnconfigure(0, weight=1)
        self.tab_steps.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(
            self.tab_steps, 
            text="Historial de Iteraciones del Método", 
            font=self.section_font, 
            text_color=COLOR_LIGHT_CYAN,
            anchor="w",
            justify="left",
            wraplength=380
        )
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_steps = ctk.CTkTextbox(
            self.tab_steps, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8,
            wrap="none",
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_steps.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_steps.insert(
            "1.0", 
            "Aquí se detallará el comportamiento iterativo del algoritmo:\n"
            "1. Tabla con número de iteración.\n"
            "2. Valores calculados para cada variable (x1, x2, ...).\n"
            "3. Error aproximado porcentual máximo de cada paso."
        )
        self.txt_steps.configure(state="disabled")

    def setup_pasos_tab(self):
        self.tab_pasos.grid_columnconfigure(0, weight=1)
        self.tab_pasos.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(
            self.tab_pasos, 
            text="Desglose Algebraico Paso a Paso", 
            font=self.section_font, 
            text_color=COLOR_LIGHT_CYAN,
            anchor="w",
            justify="left",
            wraplength=380
        )
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_pasos = ctk.CTkTextbox(
            self.tab_pasos, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8,
            wrap="none",
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_pasos.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_pasos.insert(
            "1.0", 
            "Aquí se mostrará el desglose detallado de cada variable e iteración:\n"
            "Ejemplo: x[1] = (b[1] - a12*x2 - a13*x3)/a11 con sus valores numéricos y el error aproximado calculado."
        )
        self.txt_pasos.configure(state="disabled")

    def setup_validation_tab(self):
        self.tab_validation.grid_columnconfigure(0, weight=1)
        self.tab_validation.grid_rowconfigure(1, weight=1)
        
        lbl = ctk.CTkLabel(
            self.tab_validation, 
            text="Verificación: A · x = b y Residuo", 
            font=self.section_font, 
            text_color=COLOR_LIGHT_CYAN,
            anchor="w",
            justify="left",
            wraplength=380
        )
        lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.txt_validation = ctk.CTkTextbox(
            self.tab_validation, 
            fg_color=COLOR_BG, 
            font=self.mono_font, 
            text_color=COLOR_TEXT, 
            border_color=COLOR_BORDER, 
            border_width=1,
            corner_radius=8,
            wrap="none",
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT
        )
        self.txt_validation.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.txt_validation.insert("1.0", "Comprobación matemática del residuo (r = b - A · x) para comprobar la convergencia.")
        self.txt_validation.configure(state="disabled")

    def update_x0_grid(self, n):
        # Limpiar
        for w in self.x0_container.winfo_children():
            w.destroy()
        self.entry_x0 = []
        
        # Generar inputs de forma horizontal
        for j in range(n):
            lbl = ctk.CTkLabel(
                self.x0_container, 
                text=f"x{j+1}^(0):", 
                font=self.label_font, 
                text_color=COLOR_TEXT
            )
            lbl.grid(row=0, column=2*j, padx=(0, 4), pady=5, sticky="w")
            
            entry = ctk.CTkEntry(
                self.x0_container,
                width=50,
                fg_color=COLOR_BG,
                border_color=COLOR_INTERACTIVE_BORDER,
                text_color=COLOR_TEXT,
                font=self.mono_font,
                justify="center",
                corner_radius=6,
                border_width=1
            )
            entry.insert(0, "0.0")
            entry.grid(row=0, column=2*j + 1, padx=(0, 12), pady=5, sticky="w")
            self.entry_x0.append(entry)

    def clear_matrix_and_x0(self):
        self.matrix_grid.clear()
        for entry in self.entry_x0:
            entry.delete(0, ctk.END)
            entry.insert(0, "0.0")

    def on_n_changed(self, value):
        try:
            self.n_value = int(value)
            self.matrix_grid.update_grid(self.n_value)
            self.update_x0_grid(self.n_value)
            self.preset_combo.set("Manual")
        except ValueError:
            pass

    def on_preset_selected(self, value):
        if value == "Ejemplo Chapra (3x3)":
            self.load_preset("Chapra_Ex")
        elif value == "Dominante (3x3)":
            self.load_preset("Dominante_Ex")
        elif value == "Divergente (3x3)":
            self.load_preset("Divergente_Ex")

    def load_preset(self, name):
        if name == "Chapra_Ex":
            self.n_value = 3
            self.n_combo.set("3")
            self.matrix_grid.update_grid(3)
            self.update_x0_grid(3)
            A_vals = [
                [3.0, -0.1, -0.2],
                [0.1, 7.0, -0.3],
                [0.3, -0.2, 10.0]
            ]
            b_vals = [7.85, -19.3, 71.4]
            x0_vals = [0.0, 0.0, 0.0]
            
            self.tol_entry.delete(0, ctk.END)
            self.tol_entry.insert(0, "1e-5")
            self.max_iter_entry.delete(0, ctk.END)
            self.max_iter_entry.insert(0, "150")
            self.relax_entry.delete(0, ctk.END)
            self.relax_entry.insert(0, "1.0")
            
        elif name == "Dominante_Ex":
            self.n_value = 3
            self.n_combo.set("3")
            self.matrix_grid.update_grid(3)
            self.update_x0_grid(3)
            A_vals = [
                [4.0, 1.0, -1.0],
                [1.0, 5.0, 2.0],
                [1.0, 2.0, 6.0]
            ]
            b_vals = [7.0, -8.0, 6.0]
            x0_vals = [0.0, 0.0, 0.0]
            
            self.tol_entry.delete(0, ctk.END)
            self.tol_entry.insert(0, "1e-5")
            self.max_iter_entry.delete(0, ctk.END)
            self.max_iter_entry.insert(0, "150")
            self.relax_entry.delete(0, ctk.END)
            self.relax_entry.insert(0, "1.0")
            
        elif name == "Divergente_Ex":
            self.n_value = 3
            self.n_combo.set("3")
            self.matrix_grid.update_grid(3)
            self.update_x0_grid(3)
            A_vals = [
                [1.0, 2.0, 3.0],
                [4.0, 1.0, 2.0],
                [1.0, 5.0, 1.0]
            ]
            b_vals = [6.0, 7.0, 7.0]
            x0_vals = [0.0, 0.0, 0.0]
            
            self.tol_entry.delete(0, ctk.END)
            self.tol_entry.insert(0, "1e-5")
            self.max_iter_entry.delete(0, ctk.END)
            self.max_iter_entry.insert(0, "150")
            self.relax_entry.delete(0, ctk.END)
            self.relax_entry.insert(0, "1.0")
            
        # Cargar valores en matriz y vector b
        self.matrix_grid.load_values(A_vals, b_vals)
        # Cargar x0
        for j, val in enumerate(x0_vals):
            self.entry_x0[j].delete(0, ctk.END)
            self.entry_x0[j].insert(0, str(val))

    def solve_system(self):
        try:
            A, b = self.matrix_grid.get_data()
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Matriz A o Vector b inválido:\n\n{str(e)}")
            return
            
        # Leer x0
        x0 = []
        for j in range(self.n_value):
            val_str = self.entry_x0[j].get().strip()
            try:
                x0.append(float(val_str) if val_str else 0.0)
            except ValueError:
                messagebox.showerror("Error de Entrada", f"El valor inicial x{j+1}^(0) debe ser numérico.")
                return
                
        # Parámetros numéricos
        try:
            tol_str = self.tol_entry.get().strip()
            tol = float(tol_str)
        except ValueError:
            messagebox.showerror("Error de Entrada", "La tolerancia debe ser un valor decimal válido.")
            return
            
        try:
            max_iter_str = self.max_iter_entry.get().strip()
            max_iter = int(max_iter_str)
        except ValueError:
            messagebox.showerror("Error de Entrada", "El número máximo de iteraciones debe ser un entero válido.")
            return
            
        try:
            relax_str = self.relax_entry.get().strip()
            relax = float(relax_str)
            if relax <= 0.0 or relax >= 2.0:
                messagebox.showwarning("Advertencia", "El factor de relajación λ típicamente debe estar en el rango (0, 2) para converger.")
        except ValueError:
            messagebox.showerror("Error de Entrada", "El factor de relajación debe ser un número decimal válido.")
            return
            
        try:
            precision = int(self.dec_combo.get())
        except ValueError:
            precision = 4
            
        # Instanciar el solver y resolver
        solver = GaussSeidel(A, b, x0=x0, tol=tol, max_iter=max_iter, relax=relax)
        result = solver.solve()
        
        self.txt_solution.configure(state="normal")
        self.txt_steps.configure(state="normal")
        self.txt_pasos.configure(state="normal")
        self.txt_validation.configure(state="normal")
        
        self.txt_solution.delete("1.0", ctk.END)
        self.txt_steps.delete("1.0", ctk.END)
        self.txt_pasos.delete("1.0", ctk.END)
        self.txt_validation.delete("1.0", ctk.END)
        
        # Imprimir diagnóstico de dominancia diagonal
        diag_dominant_str = "SÍ" if result["diag_dominant"] else "NO"
        dominance_text = f"Matriz diagonalmente dominante: {diag_dominant_str}\n\nDetalle por Fila:\n"
        for detail in result["dominant_details"]:
            symbol = "≥" if detail["ok"] else "<"
            dominance_text += f"  • Fila {detail['row']}: |{detail['diag']:.4g}| {symbol} (Suma de otros: {detail['row_sum']:.4g}) ➔ {detail['status']}\n"
            
        if not result["success"]:
            err_msg = f"❌ ERROR EN LA RESOLUCIÓN:\n\n{result['error_message']}\n\n"
            err_msg += dominance_text
            self.txt_solution.insert("1.0", err_msg)
            self.txt_validation.insert("1.0", "Imposible verificar: El método falló debido a inestabilidad o división por cero.")
            
            # Tabla de iteraciones lograda antes de la falla
            steps_txt = "ITERACIONES REALIZADAS ANTES DE LA FALLA:\n\n"
            steps_txt += self.format_steps_table(result["steps"], precision)
            self.txt_steps.insert("1.0", steps_txt)
            
            # Desglose algebraico logrado antes de la falla
            pasos_txt = "PASOS ALGEBRAICOS DETALLADOS LOGRADOS ANTES DE LA FALLA:\n\n"
            pasos_txt += self.format_pasos_detail(result["steps"], precision, relax)
            self.txt_pasos.insert("1.0", pasos_txt)
            
            self.result_tabs.set("Solución")
        else:
            sol = result["solution"]
            sol_text = "✅ ¡Sistema resuelto con éxito!\n\n"
            sol_text += f"Configuración: Gauss-Seidel con λ = {relax}\n"
            sol_text += f"Dimensión: {self.n_value} x {self.n_value}\n"
            sol_text += f"Tolerancia configurada: {tol} %\n"
            sol_text += f"Iteraciones finales: {len(result['steps'])-1}\n\n"
            
            sol_text += "RESULTADOS DE LAS INCÓGNITAS:\n"
            sol_text += "━" * 40 + "\n"
            for i, val in enumerate(sol):
                sol_text += f"  x[{i+1}] = {val:.{precision}f}\n"
            sol_text += "━" * 40 + "\n\n"
            
            # Agregar información de dominancia al final de la pestaña solución
            sol_text += dominance_text
            self.txt_solution.insert("1.0", sol_text)
            
            # Tabla de todas las iteraciones
            steps_text = f"SEGUIMIENTO PASO A PASO DEL PROCESO ITERATIVO (Aprox. con {precision} decimales):\n\n"
            steps_text += self.format_steps_table(result["steps"], precision)
            self.txt_steps.insert("1.0", steps_text)
            
            # Desglose de cálculos estilo Chapra
            pasos_text = f"DESGLOSE DE CÁLCULOS ITERACIÓN POR ITERACIÓN (ESTILO CHAPRA):\n\n"
            pasos_text += self.format_pasos_detail(result["steps"], precision, relax)
            self.txt_pasos.insert("1.0", pasos_text)
            
            # Validación matemática: Ax = b
            A_arr = np.array(A)
            b_arr = np.array(b)
            x_arr = np.array(sol)
            calc_b = np.dot(A_arr, x_arr)
            residual = b_arr - calc_b
            norm_res = np.linalg.norm(residual)
            
            val_text = "COMPROBACIÓN DEL SISTEMA Ax = b:\n"
            val_text += "━" * 60 + "\n"
            val_text += f"{'Fila':<8}{'b original':<15}{'A · x calculado':<20}{'Residuo (Error)':<15}\n"
            val_text += "━" * 60 + "\n"
            for i in range(self.n_value):
                val_text += f"F{i+1:<7}{b[i]:<15.{precision}f}{calc_b[i]:<20.{precision}f}{residual[i]:<15.3e}\n"
            val_text += "━" * 60 + "\n\n"
            val_text += f"Norma Euclidiana del residuo ||r||_2: {norm_res:.3e}\n\n"
            
            if norm_res < 1e-10:
                val_text += "✓ La solución obtenida es exacta con un residuo numérico insignificante."
            elif norm_res < 1e-3:
                val_text += "⚠ El residuo es muy pequeño y aceptable (convergencia estable)."
            else:
                val_text += "❌ El residuo de la solución es elevado. La aproximación iterativa no alcanzó exactitud suficiente."
            self.txt_validation.insert("1.0", val_text)
            self.result_tabs.set("Solución")
            
        self.txt_solution.configure(state="disabled")
        self.txt_steps.configure(state="disabled")
        self.txt_pasos.configure(state="disabled")
        self.txt_validation.configure(state="disabled")

    def format_steps_table(self, steps, precision):
        """Formatea el historial de pasos de iteración como una tabla ASCII legible."""
        if not steps:
            return "No se realizaron iteraciones."
            
        # Calcular ancho dinámico de columnas basándonos en variables
        table_width = 8 + (self.n_value * 16) + 16
        sep_line = "━" * table_width + "\n"
        
        # Encabezado
        header = f"{'Iter':^6}│"
        for j in range(self.n_value):
            header += f"{f'x[{j+1}]':^15} │"
        header += f"{'Error Max (%)':^15}\n"
        
        table = sep_line + header + sep_line
        
        for step in steps:
            it = step["iter"]
            x_vals = step["x"]
            max_err = step["max_error"]
            
            row = f" {it:^4} │"
            for val in x_vals:
                row += f" {val:^13.{precision}f} │"
            
            if it == 0:
                row += f" {'---':^13} \n"
            else:
                row += f" {max_err:^13.{precision}f} \n"
            table += row
            
        table += sep_line
        return table

    def format_pasos_detail(self, steps, precision, relax):
        """Formatea el desglose algebraico detallado de cada iteración paso a paso."""
        if not steps:
            return "No se realizaron iteraciones."
            
        pasos_text = "═" * 85 + "\n"
        
        for step in steps:
            it = step["iter"]
            if it == 0:
                pasos_text += f"📍 Iteración 0 (Aproximación Inicial):\n"
                for idx, val in enumerate(step["x"]):
                    pasos_text += f"  x[{idx+1}]^(0) = {val:.{precision}f}\n"
                pasos_text += "═" * 85 + "\n\n"
                continue
            
            pasos_text += f"📍 Iteración {it}:\n"
            pasos_text += "─" * 40 + "\n"
            for detail in step["var_details"]:
                v = detail["var"]
                pasos_text += f"  • Variable x[{v}]:\n"
                pasos_text += f"    Fórmula con sustitución numérica:\n"
                pasos_text += f"      {detail['formula']}\n"
                
                if abs(relax - 1.0) > 1e-6:
                    pasos_text += f"    Aplicando relajación (λ = {relax:.6g}):\n"
                    pasos_text += f"      {detail['relax']}\n"
                else:
                    pasos_text += f"    Valor resultante:\n"
                    pasos_text += f"      x[{v}]^({it}) = {detail['val']:.{precision}f}\n"
                    
                pasos_text += f"    Error relativo aproximado:\n"
                pasos_text += f"      {detail['error']}\n\n"
                
            pasos_text += f"  ➔ Error máximo de esta iteración: {step['max_error']:.{precision}f} %\n"
            pasos_text += "═" * 85 + "\n\n"
            
        return pasos_text
