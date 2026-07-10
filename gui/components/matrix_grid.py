import customtkinter as ctk
from gui.theme import (
    COLOR_BG, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_LIGHT_CYAN, COLOR_MUTED, COLOR_TEXT,
    get_label_font, get_mono_font
)

class MatrixGrid(ctk.CTkScrollableFrame):
    """
    Componente de UI reutilizable para el ingreso y administración
    de la matriz aumentada [A | b] del sistema de ecuaciones.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.label_font = get_label_font()
        self.mono_font = get_mono_font()
        self.entry_A = []
        self.entry_b = []
        self.n_value = 3

    def update_grid(self, n):
        self.n_value = n
        
        # Limpiar widgets previos
        for widget in self.winfo_children():
            widget.destroy()
            
        self.entry_A = []
        self.entry_b = []
        
        # Crear etiquetas de cabecera de columna
        for j in range(n):
            col_lbl = ctk.CTkLabel(
                self, 
                text=f"Columna {j+1}", 
                font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
                text_color=COLOR_LIGHT_CYAN
            )
            col_lbl.grid(row=0, column=2*j, padx=2, pady=5)
            
        col_b_lbl = ctk.CTkLabel(
            self, 
            text="Vector b", 
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
            text_color=COLOR_ACCENT
        )
        col_b_lbl.grid(row=0, column=2*n, padx=5, pady=5)
        
        # Generar filas de inputs
        for i in range(n):
            row_A = []
            
            # Etiqueta indicadora de fila
            row_lbl = ctk.CTkLabel(self, text=f"F{i+1}: ", font=self.label_font, text_color=COLOR_MUTED)
            row_lbl.grid(row=i+1, column=0, padx=(0, 5), pady=3)
            
            for j in range(n):
                # Campo de texto para A[i][j] (con estilos redondeados)
                entry = ctk.CTkEntry(
                    self, 
                    width=65, 
                    fg_color=COLOR_BG, 
                    border_color=COLOR_INTERACTIVE_BORDER, 
                    text_color=COLOR_TEXT,
                    font=self.mono_font,
                    justify="center",
                    corner_radius=6,
                    border_width=1
                )
                
                # Layout
                entry.grid(row=i+1, column=2*j + 1, padx=3, pady=4)
                row_A.append(entry)
                
                # Símbolos matemáticos para guiar al usuario
                if j < n - 1:
                    sym = ctk.CTkLabel(self, text=f"x{j+1} +", font=self.label_font, text_color=COLOR_MUTED)
                else:
                    sym = ctk.CTkLabel(self, text=f"x{j+1} =", font=self.label_font, text_color=COLOR_LIGHT_CYAN)
                sym.grid(row=i+1, column=2*j + 2, padx=2, pady=3)
                
            # Campo de texto para b[i] (borde de color acento para destacar)
            entry_b_i = ctk.CTkEntry(
                self, 
                width=65, 
                fg_color=COLOR_BG, 
                border_color=COLOR_ACCENT, 
                text_color=COLOR_TEXT,
                font=self.mono_font,
                justify="center",
                corner_radius=6,
                border_width=1
            )
            entry_b_i.grid(row=i+1, column=2*n + 1, padx=(5, 5), pady=4)
            
            self.entry_A.append(row_A)
            self.entry_b.append(entry_b_i)

    def clear(self):
        """Limpia el texto de todas las celdas."""
        for i in range(self.n_value):
            for j in range(self.n_value):
                self.entry_A[i][j].delete(0, ctk.END)
            self.entry_b[i].delete(0, ctk.END)

    def load_values(self, A_vals, b_vals):
        """Carga valores predefinidos en la matriz."""
        self.clear()
        for i in range(self.n_value):
            for j in range(self.n_value):
                self.entry_A[i][j].insert(0, str(A_vals[i][j]))
            self.entry_b[i].insert(0, str(b_vals[i]))

    def get_data(self):
        """Lee y valida los datos ingresados."""
        n = self.n_value
        A = []
        b = []
        
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
