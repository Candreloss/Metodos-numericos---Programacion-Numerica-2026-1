# AGENTS.md

## Setup & Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

No test suite, no linter, no type checker, no CI. Verify changes by launching the GUI.

## Architecture

Feature-oriented layout. Each method is a self-contained folder under `gui/`.

```
main.py                       ← entrypoint
lib/                          ← pure math implementations (no UI deps)
  gauss_simple.py
gui/
  app.py                      ← main window + view routing
  theme.py                    ← design tokens (light/dark tuples)
  components/                 ← reusable UI widgets
    sidebar.py
    matrix_grid.py
  gauss_simple/               ← one folder per method
    gauss_simple_view.py
  [future_method]/
    [method]_view.py
```

## Adding a New Numerical Method

1. Create `lib/<method>.py` with a class matching `GaussSimple` — constructor takes inputs, `solve()` returns `{"success": bool, "solution": ..., "steps": [...], "error_message": ...}`
2. Create `gui/<method>/<method>_view.py` as a `CTkFrame` subclass following `gauss_simple_view.py` layout
3. Register in `gui/app.py`: import the view, add a case to `switch_to_view()`, add a sidebar button in `gui/components/sidebar.py`
4. All UI text in Spanish. All comments/docstrings in Spanish.

## Dependencies

`requirements.txt`: customtkinter, numpy, pandas, matplotlib, sympy. Only customtkinter and numpy are currently used. pandas/matplotlib/sympy are likely planned for future methods.

## Style

- No `__init__.py` files anywhere — imports rely on CWD being the project root
- All UI strings, comments, and docstrings in Spanish
- Colors defined as `(light_hex, dark_hex)` tuples in `theme.py`; use `ctk` appearance mode to switch
- Fonts: Outfit (titles/sections), Inter (labels/UI), Consolas (monospace/code output)
- `#pyright: ignore` on all customtkinter imports (known type stub issues)
