import customtkinter as ctk #pyright: ignore
from gui.gauss_simple.gauss_simple_view import GaussSimpleView
from gui.gauss_seidel.gauss_seidel_view import GaussSeidelView
from gui.lagrange_interpolation.lagrange_interpolation_view import LagrangeInterpolationView
from gui.newton_interpolation.newton_interpolation_view import NewtonInterpolationView
from gui.bisection_method.bisection_method_view import BisectionMethodView
from gui.trapezoidal_rule.trapezoidal_rule_view import TrapezoidalRuleView
from gui.newton_raphson.newton_rapshon_view import NewtonRootsView
from gui.secante.secante_view import SecantRootsView
from gui.simpson_rules.simpson_rules_view import ReglasSimpsonView
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
        self.title("Métodos Numéricos")
        
        width = 1250
        height = 650
        
        # Calcular posición central basada en las dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(1000, 650)
        self.configure(fg_color=COLOR_BG)

        # Cierre limpio: evita bgerrors de callbacks pendientes de tk after()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Obtener tipografías
        self.title_font = get_title_font()
        self.section_font = get_section_font()
        self.label_font = get_label_font()
        
        # Configurar diseño de rejilla (un solo contenedor que abarca todo)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Crear Contenedor Principal e inyectar la vista
        self.create_main_container()
 
    def create_main_container(self):
        # Contenedor para cargar la vista dinámica (ocupa toda la ventana)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Cargar vista inicial (Gauss Simple)
        self.current_view = GaussSimpleView(self.main_container)
        self.current_view.grid(row=0, column=0, sticky="nsew")
 
    def switch_to_view(self, view_name):
        """Alterna dinámicamente la vista cargada en el contenedor principal."""
        if view_name == "gauss_simple":
            if isinstance(self.current_view, GaussSimpleView):
                return
            self.current_view.destroy()
            self.current_view = GaussSimpleView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        elif view_name == "gauss_seidel":
            if isinstance(self.current_view, GaussSeidelView):
                return
            self.current_view.destroy()
            self.current_view = GaussSeidelView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        elif view_name == "lagrange_interpolation":
            if isinstance(self.current_view, LagrangeInterpolationView):
                return
            self.current_view.destroy()
            self.current_view = LagrangeInterpolationView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        elif view_name == "newton_interpolation":
            if isinstance(self.current_view, NewtonInterpolationView):
                return
            self.current_view.destroy()
            self.current_view = NewtonInterpolationView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        elif view_name == "bisection_method":
            if isinstance(self.current_view, BisectionMethodView):
                return
            self.current_view.destroy()
            self.current_view = BisectionMethodView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")

        elif view_name == "trapezoidal_rule":
            if isinstance(self.current_view, TrapezoidalRuleView):
                return
            self.current_view.destroy()
            self.current_view = TrapezoidalRuleView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        elif view_name == "newton_roots":
            if isinstance(self.current_view, NewtonRootsView):
                return
            self.current_view.destroy()
            self.current_view = NewtonRootsView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")
            
        elif view_name == "secant_roots":
            if isinstance(self.current_view, SecantRootsView):
                return
            self.current_view.destroy()
            self.current_view = SecantRootsView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")

        elif view_name == "simpson_rules":
            if isinstance(self.current_view, ReglasSimpsonView):
                return
            self.current_view.destroy()
            self.current_view = ReglasSimpsonView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew")

    def _on_close(self):
        self.quit()
        self.destroy()
