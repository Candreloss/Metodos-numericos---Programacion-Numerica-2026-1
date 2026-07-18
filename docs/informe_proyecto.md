# INFORME DE PROYECTO: IMPLEMENTACIÓN DE MÉTODOS NUMÉRICOS

**Asignatura:** Programación Numérica (2026-1)  
**Fecha de Entrega:** 15 de Julio de 2026  

---

## INTEGRANTES DEL GRUPO
*   **Integrante 1:** [Nombre del Estudiante 1]
*   **Integrante 2:** [Nombre del Estudiante 2]
*   **Integrante 3:** [Nombre del Estudiante 3]

---

# INTRODUCCIÓN

El análisis numérico constituye una rama fundamental de las matemáticas aplicadas y la computación que se enfoca en el desarrollo y análisis de algoritmos para resolver numéricamente problemas de modelos continuos que no poseen soluciones analíticas o cuyas soluciones exactas resultan imprácticas de calcular. Su aplicación se extiende a áreas críticas de la ingeniería como el diseño estructural, la dinámica de fluidos, la optimización de procesos químicos y la modelación de sistemas eléctricos.

El presente proyecto expone el desarrollo, validación y aplicación de un software modular en lenguaje Python que implementa los algoritmos numéricos clásicos estructurados en tres categorías: cálculo de raíces de ecuaciones no lineales de una variable (Bisección, Newton-Raphson y Secante), resolución de sistemas de ecuaciones lineales acoplados (Eliminación de Gauss con pivoteo parcial por máximo de columna y el método iterativo de Gauss-Seidel), interpolación polinomial de datos discretos (Newton y Lagrange) e integración numérica compuesta (Regla del Trapecio). 

A lo largo de este informe se detalla la reseña histórica y teórica de cada método, se presenta un manual detallado de usuario para el manejo de la interfaz gráfica desarrollada bajo el framework CustomTkinter, y se exponen y analizan los resultados de la resolución de los problemas aplicados tomados de la bibliografía de referencia de Burden & Faires y Chapra & Canale.

---

# CONTENIDO

## 1. RESEÑA DE CADA UNO DE LOS MÉTODOS NUMÉRICOS

### A. Método de Bisección (Cálculo de Raíces)
*   **Origen e Historia:** El método de bisección se fundamenta de forma directa en el *Teorema de Bolzano* (enunciado por el matemático checo Bernard Bolzano en 1817). Es uno de los primeros métodos algorítmicos desarrollados para localizar raíces de funciones continuas debido a su sencillez intuitiva.
*   **Fundamento Matemático:** Si una función $f(x)$ es continua en un intervalo cerrado $[a, b]$ y cumple con que $f(a) \cdot f(b) < 0$ (cambio de signo), existe al menos una raíz real $c \in [a, b]$. El algoritmo divide sucesivamente el intervalo a la mitad mediante $c = (a + b)/2$ y selecciona el subintervalo contiguo que mantenga el cambio de signo para repetir el proceso.
*   **Convergencia:** El método posee convergencia lineal con una tasa constante de $\alpha = 0.5$ (es decir, el intervalo se reduce en un 50% por iteración). Es un método globalmente convergente (siempre encuentra la raíz si está acotada), aunque es lento comparado con métodos basados en derivadas.

### B. Método de Newton-Raphson (Cálculo de Raíces)
*   **Origen e Historia:** Propuesto inicialmente por Isaac Newton en 1669 para aproximar raíces de polinomios, y simplificado y generalizado por Joseph Raphson en 1690 para funciones algebraicas generales utilizando formulaciones iterativas sin recurrir a series infinitas.
*   **Fundamento Matemático:** Se basa en la linealización local de la función mediante el truncamiento de la serie de Taylor de primer grado alrededor de una aproximación inicial $x_i$. La iteración se define como:
    $$x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$$
    Gráficamente representa encontrar la intersección de la recta tangente de $f(x)$ en $x_i$ con el eje horizontal de ordenadas.
*   **Convergencia:** Posee convergencia cuadrática (el error de la iteración actual es proporcional al cuadrado del error anterior, $e_{i+1} \approx C \cdot e_i^2$) para raíces simples, lo que duplica el número de decimales correctos por iteración cerca de la raíz. Sin embargo, requiere conocer $f'(x)$ y es localmente convergente (puede divergir si el valor inicial está lejos de la raíz o cerca de un extremo local).

### C. Método de la Secante (Cálculo de Raíces)
*   **Origen e Historia:** Es un algoritmo antiguo derivado de la regla de la falsa posición (*regula falsi*). Surge como una alternativa al método de Newton para evitar el costo computacional o imposibilidad analítica de calcular la derivada de la función en cada paso.
*   **Fundamento Matemático:** Reemplaza la derivada $f'(x_i)$ en la fórmula de Newton por una aproximación en diferencias finitas basada en los dos iterados anteriores $x_i$ y $x_{i-1}$:
    $$x_{i+1} = x_i - \frac{f(x_i)(x_i - x_{i-1})}{f(x_i) - f(x_{i-1})}$$
*   **Convergencia:** Su orden de convergencia es superlineal, con un valor de $\alpha = (1 + \sqrt{5})/2 \approx 1.618$ (la proporción áurea). Es más rápido que la bisección pero ligeramente más lento que Newton, sin requerir derivadas.

### D. Eliminación de Gauss con Pivoteo Parcial por Máximo de Columna
*   **Origen e Historia:** Atribuido a Carl Friedrich Gauss en el siglo XIX para calcular órbitas de asteroides, aunque esquemas idénticos de eliminación se describieron en el antiguo texto matemático chino *Los nueve capítulos sobre el arte matemático* (siglo II a.C.).
*   **Fundamento Matemático:** Consiste en transformar un sistema lineal $A x = b$ en un sistema triangular superior equivalente $U x = d$ a través de operaciones elementales de fila de eliminación hacia adelante. Posteriormente se resuelve por sustitución hacia atrás. El *pivoteo parcial por máximo de columna* consiste en que, al procesar la columna $k$, se busca el elemento de mayor magnitud absoluta en dicha columna entre las filas $k$ a $n$, y se intercambia la fila actual con la fila del máximo. Esto minimiza errores por redondeo numérico causados por divisiones entre números muy pequeños.
*   **Convergencia:** Al ser un método directo, entrega la solución exacta en un número finito de operaciones ($O(n^3)$ operaciones de punto flotante) para sistemas con solución única, sin problemas de convergencia.

### E. Método de Gauss-Seidel
*   **Origen e Historia:** Modificación del método de Jacobi, desarrollada de forma independiente por Carl Friedrich Gauss (en una carta a un estudiante en 1823) y Philipp Ludwig von Seidel en 1874.
*   **Fundamento Matemático:** Es un método iterativo que resuelve cada ecuación $i$ del sistema para la incógnita $x_i$. La iteración calcula el nuevo valor de $x_i$ utilizando inmediatamente los valores más actualizados de las variables en la iteración actual:
    $$x_i^{(k+1)} = \frac{b_i - \sum_{j < i} A_{ij} x_j^{(k+1)} - \sum_{j > i} A_{ij} x_j^{(k)}}{A_{ii}}$$
*   **Convergencia:** Converge linealmente si la matriz $A$ es diagonalmente dominante (es decir, el módulo del elemento diagonal es estrictamente mayor que la suma de los módulos de los demás elementos de su fila) o si es simétrica y definida positiva.

### F. Interpolación Polinomial de Newton (Diferencias Divididas)
*   **Origen e Historia:** Desarrollada por Isaac Newton. Representa una de las formulaciones más potentes para construir polinomios interpolantes a partir de puntos discretos.
*   **Fundamento Matemático:** El polinomio interpolante de grado $n$ se escribe en términos de diferencias divididas:
    $$P_n(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \dots$$
    donde las diferencias divididas se calculan recursivamente mediante:
    $$f[x_0, x_1, \dots, x_k] = \frac{f[x_1, \dots, x_k] - f[x_0, \dots, x_{k-1}]}{x_k - x_0}$$
*   **Convergencia/Propiedades:** La ventaja principal es que si se añade un punto base adicional, no es necesario recalcular todos los coeficientes previos del polinomio; únicamente se añade una fila a la tabla de diferencias divididas.

### G. Interpolación Polinomial de Lagrange
*   **Origen e Historia:** Formulada originalmente por Edward Waring en 1779 y redescubierta de forma independiente por Joseph-Louis Lagrange en 1795.
*   **Fundamento Matemático:** Expresa el polinomio interpolante como una combinación lineal de las ordenadas $y_i$ y polinomios base de Lagrange $L_i(x)$:
    $$P_n(x) = \sum_{i=0}^n y_i L_i(x), \quad L_i(x) = \prod_{j \neq i} \frac{x - x_j}{x_i - x_j}$$
    El polinomio base $L_i(x)$ toma el valor de 1 en $x_i$ y 0 en cualquier otro punto de soporte.
*   **Propiedades:** Es teóricamente muy elegante e ideal para demostraciones analíticas e integraciones numéricas, pero es computacionalmente costosa de actualizar si se añaden nuevos puntos base.

### H. Regla del Trapecio (Integración Numérica)
*   **Origen e Historia:** Una de las fórmulas de Newton-Cotes. Su origen es clásico y representa la aproximación del área bajo la curva mediante segmentos de recta.
*   **Fundamento Matemático:** Aproxima la integral de una función $f(x)$ en $[a, b]$ dividiendo el dominio en $n$ subintervalos de tamaño de paso $h = (b - a)/n$. En cada subintervalo se aproxima la curva por una recta, lo que resulta en la regla compuesta:
    $$\int_a^b f(x) dx \approx \frac{h}{2} \left[ f(a) + 2\sum_{i=1}^{n-1} f(a + ih) + f(b) \right]$$
*   **Convergencia:** Posee un error global proporcional a $O(h^2)$. Si la función posee derivada segunda continua, el error es proporcional a $-\frac{b-a}{12} h^2 f''(\xi)$.

---

## 2. MANUAL DE USUARIO PARA LA EJECUCIÓN DE LOS PROGRAMAS

La aplicación modular está desarrollada en **Python** con una interfaz gráfica moderna utilizando **CustomTkinter** y **Matplotlib**. 

### A. Ejecución e Inicio de la Aplicación
Para ejecutar el software desde la terminal en el directorio raíz del proyecto:
1.  Active el entorno virtual:
    ```bash
    .venv/bin/activate  # (Linux/macOS)
    .venv\Scripts\activate  # (Windows)
    ```
2.  Inicie el punto de entrada principal:
    ```bash
    python main.py
    ```

La ventana se abrirá centrada en pantalla con un diseño oscuro elegante ("dark mode").

### B. Estructura de la Interfaz
La pantalla principal consta de tres secciones:
1.  **Barra Lateral de Navegación (Sidebar):** Permite cambiar con un solo clic entre las distintas herramientas de cálculo (Bisección, Newton-Raphson, Secante, Gauss Simple, Gauss-Seidel, Interpolación de Newton, Interpolación de Lagrange, Regla del Trapecio).
2.  **Panel de Entrada de Parámetros (Izquierda):** Contiene campos de texto interactivos para ingresar las ecuaciones (sintaxis algebraica de Python/Sympy, ej. `x**3 - x - 2`), los intervalos, puntos iniciales, tolerancias y rangos de graficación. Incluye un botón para calcular.
3.  **Panel de Resultados (Derecha):** Un contenedor de pestañas (Tabs):
    *   *Resultado:* Muestra el diagnóstico de convergencia final, la raíz encontrada y la evaluación de la función.
    *   *Paso a Paso:* Muestra una tabla detallada con el registro numérico de cada iteración (iteración, valores calculados, error estimado).
    *   *Evolución Gráfica (o Gráfica):* Muestra el gráfico interactivo de la función, con el marcaje de los puntos iterados intermedios y la raíz final encontrada de forma visual.

---

## 3. TABLA DE COMANDOS ORIGINALES DEL SOFTWARE UTILIZADO (PYTHON / SCIPY / NUMPY)

En la práctica del desarrollo con Python para el cálculo científico, se suelen utilizar las bibliotecas especializadas de código abierto **SciPy**, **NumPy** y **SymPy** para llevar a cabo estos cálculos numéricos de forma directa y optimizada.

| Categoría Matemática | Comando/Función en Python (SciPy / NumPy) | Sintaxis de Ejemplo | Descripción |
|---|---|---|---|
| **Cálculo de Raíces** | `scipy.optimize.bisect` | `r = bisect(lambda x: x**3-x-2, 1, 2)` | Encuentra la raíz de una función no lineal en un intervalo utilizando el método de bisección con alta tolerancia. |
| | `scipy.optimize.newton` | `r = newton(lambda x: exp(-x)-x, 0)` | Encuentra la raíz utilizando el método de Newton-Raphson. Si no se provee la derivada, implementa automáticamente el método de la secante. |
| **Sistemas Lineales** | `numpy.linalg.solve` | `x = np.linalg.solve(A, b)` | Resuelve un sistema de ecuaciones lineales $A x = b$ mediante descomposición LU con pivoteo parcial de manera exacta y eficiente. |
| **Interpolación** | `scipy.interpolate.lagrange` | `poly = lagrange(x, y)` | Construye el polinomio interpolante de Lagrange a partir de un conjunto de puntos discretos $x$ e $y$. |
| | `numpy.polyfit` | `p = np.polyfit(x, y, deg)` | Ajusta un polinomio de grado `deg` por mínimos cuadrados o interpolación exacta si el grado es $n-1$. |
| **Integración Numérica**| `scipy.integrate.trapezoid` | `area = trapezoid(y, x)` | Integra datos tabulados discretos $x$ e $y$ aplicando de forma compuesta la regla del trapecio. |
| | `numpy.trapz` | `area = np.trapz(y, x)` | Comando heredado de NumPy para integración compuesta trapezoidal en un arreglo de puntos discretos. |

---

# REFERENCIAS BIBLIOGRÁFICAS

1.  **Burden, R. L., & Faires, J. D. (2002).** *Análisis Numérico* (7ma Edición). Thomson Learning. México.
2.  **Chapra, S. C., & Canale, R. P. (2015).** *Métodos Numéricos para Ingenieros* (7ma Edición). McGraw-Hill Education. México.
3.  **SymPy Development Team. (2026).** *SymPy: Python Library for Symbolic Mathematics*. Disponible en: [https://www.sympy.org/](https://www.sympy.org/)
4.  **CustomTkinter GitHub Repository.** *Modern GUI library for Tkinter in Python*. Disponible en: [https://github.com/tomschimansky/CustomTkinter](https://github.com/tomschimansky/CustomTkinter)
