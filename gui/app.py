import customtkinter as ctk #pyright: ignore
from gui.views.gauss_simple_view import GaussSimpleView
from gui.theme import (
    COLOR_BG, COLOR_PANEL, COLOR_BORDER, COLOR_INTERACTIVE_BORDER,
    COLOR_ACCENT, COLOR_ACCENT_HOVER, COLOR_LIGHT_CYAN, COLOR_TEXT, COLOR_MUTED,
    get_title_font, get_section_font, get_label_font
)

class GaussSimpleApp(ctk.CTk):
    """
    Contenedor principal de la aplicación.
    Administra la ventana, la barra lateral de navegación y la carga de vistas dinámicas.
    """
    def __init__(self):
        super().__init__()
        
        # Apariencia por defecto
        ctk.set_appearance_mode("dark")
        
        # Configurar ventana principal y centrado en pantalla
        self.title("Métodos Numéricos - Eliminación Gaussiana")
        
        width = 1200
        height = 650
        
        # Calcular posición central basada en las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(1000, 650)
        self.configure(fg_color=COLOR_BG)
        
        # Obtener tipografías
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        
        # Configurar diseño de rejilla
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Crear Barra Lateral (Sidebar)
        self.create_sidebar()
        
        # 2. Crear Contenedor Principal e inyectar la vista
        self.create_main_container()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLOR_PANEL, border_color=COLOR_BORDER, border_width=1)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_rowconfigure(5, weight=1)
        
        # Título del software (Centrado horizontalmente en la barra lateral)
        title_label = ctk.CTkLabel(
            sidebar, 
            text="Programación\nNumérica", 
            font=self.title_font, 
            text_color=COLOR_LIGHT_CYAN,
            justify="center",
            anchor="center"
        )
        title_label.grid(row=0, column=0, padx=24, pady=(35, 25), sticky="ew")
        
        # Separador muy delgado
        sep = ctk.CTkFrame(sidebar, height=1, fg_color=COLOR_BORDER)
        sep.grid(row=1, column=0, sticky="ew", padx=24, pady=0)
        
        # Sección de selección de métodos
        method_title = ctk.CTkLabel(
            sidebar, 
            text="MÉTODOS", 
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"), 
            text_color=COLOR_MUTED
        )
        method_title.grid(row=2, column=0, padx=24, pady=(25, 12), sticky="w")
        
        # Menú de Métodos (Botones expandidos de borde a borde, con corner_radius=0 y altura de 44px)
        sidebar_font = ctk.CTkFont(family="Inter", size=13, weight="bold")
        
        self.btn_gauss_simple = ctk.CTkButton(
            sidebar, 
            text="      📊   Gauss Simple", 
            fg_color=COLOR_ACCENT, 
            text_color=("#ffffff", "#06172E"),
            hover_color=COLOR_ACCENT_HOVER,
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w"
        )
        self.btn_gauss_simple.grid(row=3, column=0, padx=0, pady=2, sticky="ew")
        
        self.btn_gauss_seidel = ctk.CTkButton(
            sidebar, 
            text="      🔒   Gauss-Seidel (Prox.)", 
            fg_color="transparent", 
            text_color=COLOR_MUTED,
            state="disabled",
            font=sidebar_font,
            corner_radius=0,
            height=44,
            anchor="w"
        )
        self.btn_gauss_seidel.grid(row=4, column=0, padx=0, pady=2, sticky="ew")
        
        # Selector de Tema (Rediseñado según la referencia visual)
        theme_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        theme_frame.grid(row=6, column=0, padx=24, pady=24, sticky="ew")
        
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
        self.theme_menu.set("Oscuro")

    def change_appearance_mode(self, mode):
        if mode == "Claro":
            ctk.set_appearance_mode("light")
        elif mode == "Oscuro":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("system")

    def create_main_container(self):
        # Contenedor para cargar la vista dinámica
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Cargar vista inicial (Gauss Simple)
        self.current_view = GaussSimpleView(self.main_container)
        self.current_view.grid(row=0, column=0, sticky="nsew")
