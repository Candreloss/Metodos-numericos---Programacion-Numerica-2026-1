import customtkinter as ctk #pyright: ignore

# Paleta de colores dinámica para Modo Claro y Modo Oscuro (Formato: (Claro, Oscuro))
COLOR_BG = ("#f8fafc", "#06172E")                  # Fondo principal
COLOR_PANEL = ("#ffffff", "#022C50")               # Fondo de tarjetas/paneles
COLOR_BORDER = ("#e2e8f0", "#0b253f")              # Bordes muy sutiles
COLOR_INTERACTIVE_BORDER = ("#58A1D3", "#0F4C81")  # Bordes de celdas y comboboxes (Vibrante en claro, Classic Blue en oscuro)
COLOR_ACCENT = ("#0F4C81", "#58A1D3")              # Acento principal (Classic Blue en claro, Blue Gray en oscuro)
COLOR_ACCENT_HOVER = ("#0b3a63", "#3e87b7")        # Hover para acento
COLOR_LIGHT_CYAN = ("#022C50", "#B3DEF8")          # Títulos y destacados (Blue Slate en claro, Powder Blue en oscuro)
COLOR_TEXT = ("#1e293b", "#FFFFFF")                # Texto estándar
COLOR_MUTED = ("#64748b", "#7fa2c7")               # Texto secundario/silenciado

def get_title_font():
    return ctk.CTkFont(family="Outfit", size=22, weight="bold")

def get_section_font():
    return ctk.CTkFont(family="Outfit", size=16, weight="bold")

def get_label_font():
    return ctk.CTkFont(family="Inter", size=13)

def get_mono_font():
    return ctk.CTkFont(family="Consolas", size=12)
