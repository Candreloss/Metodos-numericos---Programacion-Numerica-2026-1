import customtkinter as ctk #pyright: ignore
from gui.theme import (
    COLOR_BG, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_LIGHT_CYAN, COLOR_MUTED, COLOR_TEXT,
    get_label_font, get_mono_font
)

class MatrixGrid(ctk.CTkScrollableFrame):
    """
    Componente de UI para ingreso de matriz aumentada [A | b].
    """
    def __init__(self, master, **kwargs):
        super().__init__(
            master, 
            fg_color="transparent", 
            scrollbar_fg_color="transparent",
            scrollbar_button_color=COLOR_INTERACTIVE_BORDER,
            scrollbar_button_hover_color=COLOR_ACCENT,
            **kwargs
        )
        self.label_font = get_label_font()
        self.mono_font = get_mono_font()
        self.entry_A = []
        self.entry_b = []
        self.n_value = 3
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_frame.grid(row=0, column=0, sticky="n")

    def update_grid(self, n):
        self.n_value = n
        
        # Limpiar únicamente los widgets dentro del contenedor central
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        self.entry_A = []
        self.entry_b = []
        
        # Crear etiquetas de cabecera de columna (Alineadas sobre sus respectivas cajas de texto)
        for j in range(n):
            col_lbl = ctk.CTkLabel(
                self.grid_frame, 
                text=f"Columna {j+1}", 
                font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
                text_color=COLOR_LIGHT_CYAN
            )
            col_lbl.grid(row=0, column=2*j + 1, padx=2, pady=5)
            
        col_b_lbl = ctk.CTkLabel(
            self.grid_frame, 
            text="Vector b", 
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
            text_color=COLOR_ACCENT
        )
        col_b_lbl.grid(row=0, column=2*n + 1, padx=5, pady=5)
        
        # Generar filas de inputs
        for i in range(n):
            row_A = []
            
            # Etiqueta indicadora de fila
            row_lbl = ctk.CTkLabel(self.grid_frame, text=f"F{i+1}: ", font=self.label_font, text_color=COLOR_MUTED)
            row_lbl.grid(row=i+1, column=0, padx=(0, 3), pady=3)
            
            for j in range(n):
                # Campo de texto para A[i][j] (con estilos redondeados)
                entry = ctk.CTkEntry(
                    self.grid_frame, 
                    width=55, 
                    fg_color=COLOR_BG, 
                    border_color=COLOR_INTERACTIVE_BORDER, 
                    text_color=COLOR_TEXT,
                    font=self.mono_font,
                    justify="center",
                    corner_radius=6,
                    border_width=1
                )
                
                # Layout
                entry.grid(row=i+1, column=2*j + 1, padx=2, pady=4)
                row_A.append(entry)
                
                # Símbolos matemáticos para guiar al usuario
                if j < n - 1:
                    sym = ctk.CTkLabel(self.grid_frame, text=f"x{j+1} +", font=self.label_font, text_color=COLOR_MUTED)
                else:
                    sym = ctk.CTkLabel(self.grid_frame, text=f"x{j+1} =", font=self.label_font, text_color=COLOR_LIGHT_CYAN)
                sym.grid(row=i+1, column=2*j + 2, padx=1, pady=3)
                
            # Campo de texto para b[i] (borde de color acento para destacar)
            entry_b_i = ctk.CTkEntry(
                self.grid_frame, 
                width=55, 
                fg_color=COLOR_BG, 
                border_color=COLOR_ACCENT, 
                text_color=COLOR_TEXT,
                font=self.mono_font,
                justify="center",
                corner_radius=6,
                border_width=1
            )
            entry_b_i.grid(row=i+1, column=2*n + 1, padx=(4, 4), pady=4)
            
            self.entry_A.append(row_A)
            self.entry_b.append(entry_b_i)

    def clear(self):
        for i in range(self.n_value):
            for j in range(self.n_value):
                self.entry_A[i][j].delete(0, ctk.END)
            self.entry_b[i].delete(0, ctk.END)

    def load_values(self, A_vals, b_vals):
        self.clear()
        for i in range(self.n_value):
            for j in range(self.n_value):
                self.entry_A[i][j].insert(0, str(A_vals[i][j]))
            self.entry_b[i].insert(0, str(b_vals[i]))

    def get_data(self):
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
