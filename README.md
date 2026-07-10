## Métodos Numéricos - Programación Numérica 2026-1

Este proyecto contiene la implementación de diversos métodos numéricos con una interfaz gráfica moderna e interactiva en Python usando **CustomTkinter** y soportando modos Claro y Oscuro.

### Estructura del Proyecto

El proyecto sigue una arquitectura limpia de separación de capas (Lógica y Vista):

*   **`src/logic/`**: Contiene la lógica matemática pura de cada método numérico (sin dependencias de interfaz).
*   **`src/gui/app.py`**: Contenedor principal de la ventana y barra lateral de navegación.
*   **`src/gui/theme.py`**: Definición del sistema de diseño (colores dinámicos y tipografías para modos Claro y Oscuro).
*   **`src/gui/components/`**: Componentes gráficos reutilizables (como `MatrixGrid` para el ingreso de la matriz aumentado [A | b]).
*   **`src/gui/views/`**: Formularios y visualización de resultados paso a paso para cada método.

### Métodos a Elaborar e Integrar

1. **Métodos para cálculo de raíces**
    *   Newton y Secante (Carlos Paradas)
    *   Bisección (Raimir Linarez)
2. **Métodos para resolución de ecuaciones lineales**
    *   Gauss Simple con pivoteo parcial por columna (Alondra León) [**Implementado**]
    *   Gauss-Seidel (Próximamente)
3. **Otros Métodos Numéricos**
    *   Interpolación de Newton (Ricardo Pérez)
    *   Interpolación de Lagrange (Hanuman Sánchez)
    *   Regla del trapecio (Colaborativo)
