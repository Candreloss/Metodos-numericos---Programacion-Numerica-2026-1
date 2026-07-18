import customtkinter as ctk #pyright: ignore

COLOR_BG = ("#f8fafc", "#06172E")
COLOR_PANEL = ("#ffffff", "#022C50")
COLOR_BORDER = ("#e2e8f0", "#0b253f")
COLOR_INTERACTIVE_BORDER = ("#58A1D3", "#0F4C81")
COLOR_ACCENT = ("#0F4C81", "#58A1D3")
COLOR_ACCENT_HOVER = ("#0b3a63", "#3e87b7")
COLOR_LIGHT_CYAN = ("#022C50", "#B3DEF8")
COLOR_TEXT = ("#1e293b", "#FFFFFF")
COLOR_MUTED = ("#64748b", "#7fa2c7")

def get_title_font():
    return ctk.CTkFont(family="Outfit", size=22, weight="bold")

def get_section_font():
    return ctk.CTkFont(family="Outfit", size=16, weight="bold")

def get_label_font():
    return ctk.CTkFont(family="Inter", size=13)

def get_mono_font():
    return ctk.CTkFont(family="Consolas", size=12)
