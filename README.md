# Métodos Numéricos — Programación Numérica 2026-1

Implementación de métodos numéricos con interfaz gráfica moderna en Python
usando **CustomTkinter** (modos Claro/Oscuro) y **Matplotlib** para gráficas.

## Instalación y ejecución

```bash
# 1. Clonar
git clone git@github.com:Candreloss/Metodos-numericos---Programacion-Numerica-2026-1.git
cd Metodos-numericos---Programacion-Numerica-2026-1

# 2. Entorno virtual + dependencias
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 3. Ejecutar la aplicación
.venv/bin/python main.py
```

## Tests

```bash
.venv/bin/python -m lib.lagrange_interpolation_test
.venv/bin/python -m lib.newton_interpolation_test
```

## Estructura del proyecto

```
main.py                          ← entrypoint
lib/                             ← lógica pura (sin dependencias de UI)
├── __init__.py
├── gauss_simple.py
├── lagrange_interpolation.py
├── lagrange_interpolation_test.py
├── newton_interpolation.py
└── newton_interpolation_test.py
gui/                             ← interfaz gráfica (customtkinter)
├── __init__.py
├── app.py                       ← ventana principal + routing de vistas
├── theme.py                     ← colores y tipografías (claro/oscuro)
├── components/
│   ├── __init__.py
│   ├── sidebar.py               ← barra lateral de navegación
│   └── matrix_grid.py           ← widget de matriz aumentada
├── gauss_simple/
│   ├── __init__.py
│   └── gauss_simple_view.py
├── lagrange_interpolation/
│   ├── __init__.py
│   └── lagrange_interpolation_view.py
└── newton_interpolation/
    ├── __init__.py
    └── newton_interpolation_view.py
```

## Métodos implementados

| Método | Categoría | Autor | Estado |
|--------|-----------|-------|--------|
| Gauss Simple (pivoteo parcial) | Ecuaciones lineales | Alondra León | ✅ |
| Interpolación de Lagrange | Interpolación | Hanuman Sánchez | ✅ |
| Interpolación de Newton | Interpolación | Ricardo Pérez | ✅ |
| Bisección | Raíces | Raimir Linarez | 🔜 |
| Newton (raíces) | Raíces | Carlos Paradas | 🔜 |
| Secante | Raíces | Carlos Paradas | 🔜 |
| Gauss-Seidel | Ecuaciones lineales | — | 🔜 |
| Regla del Trapecio | Integración | Colaborativo | 🔜 |
| Regla de Simpson | Integración | — | 🔜 |

## Cómo agregar un nuevo método numérico

### 1. Crear la clase de lógica (`lib/<metodo>.py`)

El constructor recibe los parámetros del método y `solve()` retorna
un diccionario estándar:

```python
class MiMetodo:
    def __init__(self, parametros...):
        self.steps = []   # paso a paso para la GUI

    def solve(self):
        # Validaciones...
        # Algoritmo...
        return {
            "success": bool,
            "solution": ...,          # resultado (depende del método)
            "steps": self.steps,      # lista de dicts con type + description
            "error_message": str | None
        }
```

Ver `lib/gauss_simple.py` o `lib/lagrange_interpolation.py` como referencia.

### 2. Crear tests (`lib/<metodo>_test.py`)

Ejecutar con:
```bash
.venv/bin/python -m lib.<metodo>_test
```

### 3. Crear la vista GUI (`gui/<metodo>/`)

La vista es un `CTkFrame` que sigue el patrón de `gauss_simple_view.py`:
- `gui/<metodo>/__init__.py` con docstring descriptivo
- `gui/<metodo>/<metodo>_view.py` con:
  - Sidebar (`Sidebar(self, active_method="<metodo>")`)
  - `view_container` con header y dos paneles (inputs izq, resultados der)
  - `CTkTabview` con tabs (Resultado, Paso a Paso, Gráfica si aplica)
  - Método `solve_*()` que instancia la clase de `lib/`, procesa `result["steps"]` y actualiza los textboxes y gráficas

### 4. Registrar la vista

En **`gui/app.py`**:
```python
from gui.<metodo>.<metodo>_view import MiMetodoView

def switch_to_view(self, view_name):
    # ...
    elif view_name == "<metodo>":
        if isinstance(self.current_view, MiMetodoView): return
        self.current_view.destroy()
        self.current_view = MiMetodoView(self.main_container)
        self.current_view.grid(row=0, column=0, sticky="nsew")
```

En **`gui/components/sidebar.py`**:
```python
self.btn_<metodo> = ctk.CTkButton(
    self, text="      📐   Mi Método",
    command=self.on_<metodo>_click, ...
)

def on_<metodo>_click(self):
    if self.active_method == "<metodo>": return
    app = self.winfo_toplevel()
    if hasattr(app, "switch_to_view"):
        app.switch_to_view("<metodo>")
```

### 5. Probar

```bash
.venv/bin/python main.py
```

## Dependencias

`requirements.txt`: customtkinter, numpy, pandas, matplotlib, sympy

## Estilo

- UI, comentarios y docstrings en **español**
- Cada directorio (`lib/`, `gui/`, `gui/components/`, `gui/<metodo>/`) tiene `__init__.py`
- Tipografías: Outfit (títulos), Inter (labels), Consolas (código monoespaciado)
- Colores en `gui/theme.py` como tuplas `(claro, oscuro)`
- `#pyright: ignore` en imports de customtkinter (problemas conocidos de type stubs)
