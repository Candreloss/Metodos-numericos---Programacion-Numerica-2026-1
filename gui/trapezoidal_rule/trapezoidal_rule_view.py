import customtkinter as ctk #pyright: ignore
from gui.components.sidebar import Sidebar
from gui.theme import COLOR_BG, COLOR_TEXT, get_section_font

class TrapezoidalRuleView(ctk.CTkFrame):
    """
    Vista placeholder para la Regla del Trapecio.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=COLOR_BG, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, active_method="trapezoidal_rule")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Contenido principal
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(0, weight=1)

        label = ctk.CTkLabel(
            content,
            text="🔧  Método en desarrollo",
            font=get_section_font(),
            text_color=COLOR_TEXT
        )
        label.grid(row=0, column=0)
