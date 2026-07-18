import customtkinter as ctk #pyright: ignore
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_label_font
)

class Sidebar(ctk.CTkFrame):
    """
    Componente reutilizable de la Barra Lateral (Sidebar).
    Puede ser instanciado en cualquier vista para mantener la navegación global uniforme.
    """
    def __init__(self, master, active_method="gauss_simple", **kwargs):
        super().__init__(
            master, 
            width=240, 
            corner_radius=0, 
            fg_color=COLOR_PANEL, 
            border_color=COLOR_BORDER, 
            border_width=1,
            **kwargs
        )
        self.active_method = active_method
        self.title_font = get_title_font()
        self.label_font = get_label_font()
        
        self.grid_rowconfigure(11, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Título del software (Centrado horizontalmente)
        title_label = ctk.CTkLabel(
            self, 
            text="Programación\nNumérica", 
            font=self.title_font, 
            text_color=COLOR_LIGHT_CYAN,
            justify="center",
            anchor="center"
        )
        title_label.grid(row=0, column=0, padx=24, pady=(35, 25), sticky="ew")
        
        # Separador muy delgado
        sep = ctk.CTkFrame(self, height=1, fg_color=COLOR_BORDER)
        sep.grid(row=1, column=0, sticky="ew", padx=24, pady=0)
        
        # Sección de selección de métodos
        method_title = ctk.CTkLabel(
            self, 
            text="MÉTODOS", 
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
            text_color=COLOR_MUTED
        )
        method_title.grid(row=2, column=0, padx=24, pady=(25, 12), sticky="w")
        
        # Menú de Métodos (Botones expandidos de borde a borde, con corner_radius=0 y altura de 44px)
        sidebar_font = ctk.CTkFont(family="Inter", size=13, weight="bold")
        
        self.btn_gauss_simple = ctk.CTkButton(
            self, 
            text="      📊   Gauss Simple", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_gauss_simple_click
        )
        self.btn_gauss_simple.grid(row=3, column=0, padx=0, pady=2, sticky="ew")
        
        self.btn_gauss_seidel = ctk.CTkButton(
            self, 
            text="      📊   Gauss-Seidel", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_gauss_seidel_click
        )
        self.btn_gauss_seidel.grid(row=4, column=0, padx=0, pady=2, sticky="ew")
        
        self.btn_lagrange = ctk.CTkButton(
            self, 
            text="      📈   Lagrange", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_lagrange_click
        )
        self.btn_lagrange.grid(row=5, column=0, padx=0, pady=2, sticky="ew")
        
        self.btn_newton_interp = ctk.CTkButton(
            self, 
            text="      📈   Newton (Interp.)", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_newton_interp_click
        )
        self.btn_newton_interp.grid(row=6, column=0, padx=0, pady=2, sticky="ew")

        self.btn_newton_roots = ctk.CTkButton(
            self, 
            text="      📐   Newton (Raíces)", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_newton_roots_click
        )
        self.btn_newton_roots.grid(row=7, column=0, padx=0, pady=2, sticky="ew")

        self.btn_secant_roots = ctk.CTkButton(
            self, 
            text="      📐   Secante (Raíces)", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_secant_click
        )
        self.btn_secant_roots.grid(row=8, column=0, padx=0, pady=2, sticky="ew")
        
        self.btn_bisection = ctk.CTkButton(
            self, 
            text="      📐   Bisección", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_bisection_click
        )
        self.btn_bisection.grid(row=9, column=0, padx=0, pady=2, sticky="ew")
        
        self.btn_trapecio = ctk.CTkButton(
            self, 
            text="      📐   Trapecio", 
            fg_color="transparent", 
            text_color=COLOR_TEXT,
            hover_color=COLOR_INTERACTIVE_BORDER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w",
            command=self.on_trapecio_click
        )
        self.btn_trapecio.grid(row=10, column=0, padx=0, pady=2, sticky="ew")

        # Selector de Tema
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.grid(row=12, column=0, padx=24, pady=24, sticky="ew")
        
        theme_lbl = ctk.CTkLabel(
            theme_frame, 
            text="🎨  Tema", 
            font=sidebar_font, 
            text_color=COLOR_TEXT
        )
        theme_lbl.pack(anchor="w", pady=(0, 10))
        
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["Oscuro", "Claro", "Sistema"],
            command=self.change_appearance_mode,
            fg_color=COLOR_BG,
            button_color=COLOR_INTERACTIVE_BORDER,
            button_hover_color=COLOR_ACCENT,
            dropdown_fg_color=COLOR_PANEL,
            dropdown_hover_color=COLOR_BORDER,
            dropdown_text_color=COLOR_TEXT,
            text_color=COLOR_TEXT,
            font=self.label_font,
            corner_radius=8,
            height=36
        )
        self.theme_menu.pack(fill="x")
        
        # Sincronizar el valor actual del OptionMenu con el modo actual de CTK
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            self.theme_menu.set("Oscuro")
        elif current_mode == "Light":
            self.theme_menu.set("Claro")
        else:
            self.theme_menu.set("Sistema")

    def change_appearance_mode(self, mode):
        if mode == "Claro":
            ctk.set_appearance_mode("light")
        elif mode == "Oscuro":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("system")

    # --- EVENTOS DE RUTEO ---
    def on_gauss_simple_click(self):
        if self.active_method == "gauss_simple":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("gauss_simple")

    def on_gauss_seidel_click(self):
        if self.active_method == "gauss_seidel":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("gauss_seidel")

    def on_lagrange_click(self):
        if self.active_method == "lagrange_interpolation":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("lagrange_interpolation")

    def on_newton_interp_click(self):
        if self.active_method == "newton_interpolation":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("newton_interpolation")

    def on_newton_roots_click(self):
        if self.active_method == "newton_roots":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("newton_roots")

    def on_secant_click(self):
        if self.active_method == "secant_roots":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("secant_roots")

    def on_bisection_click(self):
        if self.active_method == "bisection_method":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("bisection_method")

    def on_trapecio_click(self):
        if self.active_method == "trapezoidal_rule":
            return
        app = self.winfo_toplevel()
        if hasattr(app, "switch_to_view"):
            app.switch_to_view("trapezoidal_rule")
