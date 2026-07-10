## Métodos Numéricos - Programación Numérica 2026-1

Este proyecto contiene la implementación de diversos métodos numéricos con una interfaz gráfica moderna e interactiva en Python usando **CustomTkinter** y soportando modos Claro y Oscuro.

### Estructura del Proyecto

El proyecto sigue una arquitectura orientada a características (feature-oriented):

*   **`lib/`**: Lógica matemática pura de cada método numérico (sin dependencias de interfaz).
*   **`gui/app.py`**: Contenedor principal de la ventana y barra lateral de navegación.
*   **`gui/theme.py`**: Definición del sistema de diseño (colores dinámicos y tipografías para modos Claro y Oscuro).
*   **`gui/components/`**: Componentes gráficos reutilizables (como `MatrixGrid` para el ingreso de la matriz aumentado [A | b]).
*   **`gui/[método]/`**: Cada método numérico tiene su propia carpeta con su vista y componentes específicos.

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
