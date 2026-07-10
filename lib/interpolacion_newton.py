import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp

class NewtonInterpolationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolación de Newton")
        self.root.geometry("900x700")
        
        # Configuración de los paneles Tk
        self.frame_inputs = tk.Frame(self.root, padx=10, pady=10)
        self.frame_inputs.pack(side=tk.TOP, fill=tk.X)
        
        self.frame_results = tk.Frame(self.root, padx=10, pady=10)
        self.frame_results.pack(side=tk.TOP, fill=tk.X)
        
        self.frame_plot = tk.Frame(self.root, padx=10, pady=10)
        self.frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)        
        self._setup_inputs()
        self._setup_table()
        
    def _setup_inputs(self):
        # Etiquetas y campos de entrada
        tk.Label(self.frame_inputs, text="x_list (separados por coma):").grid(row=0, column=0, sticky="w")
        self.entry_xlist = tk.Entry(self.frame_inputs, width=30)
        self.entry_xlist.insert(0, "1, 2, 3, 4, 5")
        self.entry_xlist.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.frame_inputs, text="y_list (separados por coma):").grid(row=1, column=0, sticky="w")
        self.entry_ylist = tk.Entry(self.frame_inputs, width=30)
        self.entry_ylist.insert(0, "1, 4, 9, 16, 25")
        self.entry_ylist.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(self.frame_inputs, text="Grado (n):").grid(row=0, column=2, sticky="w", padx=(15,0))
        self.entry_n = tk.Entry(self.frame_inputs, width=10)
        self.entry_n.insert(0, "4")
        self.entry_n.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(self.frame_inputs, text="Valor a aproximar (x):").grid(row=1, column=2, sticky="w", padx=(15,0))
        self.entry_x = tk.Entry(self.frame_inputs, width=10)
        self.entry_x.insert(0, "2.5")
        self.entry_x.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Label(self.frame_inputs, text="Función original f(x) [Opcional]:").grid(row=2, column=0, sticky="w")
        self.entry_f = tk.Entry(self.frame_inputs, width=30)
        self.entry_f.insert(0, "x**2")
        self.entry_f.grid(row=2, column=1, padx=5, pady=2)
        
        self.btn_calc = tk.Button(self.frame_inputs, text="Calcular y Graficar", command=self.calcular_newton, bg="#4CAF50", fg="white")
        self.btn_calc.grid(row=2, column=2, columnspan=2, pady=10)
        
        self.lbl_resultado = tk.Label(self.frame_inputs, text="Aproximación: --- | Error: ---", font=("Arial", 10, "bold"))
        self.lbl_resultado.grid(row=3, column=0, columnspan=4, pady=5)

    def _setup_table(self):
        # Configuración del Treeview la tabla de pandas
        self.tree = ttk.Treeview(self.frame_results, height=5)
        self.tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        scrollbar = ttk.Scrollbar(self.frame_results, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
    def calcular_newton(self):
        try:
            # 1. Obtener y limpiar datos de entrada
            xlist = np.array([float(i.strip()) for i in self.entry_xlist.get().split(',')])
            ylist = np.array([float(i.strip()) for i in self.entry_ylist.get().split(',')])
            n = int(self.entry_n.get())
            x_aprox = float(self.entry_x.get())
            func_str = self.entry_f.get().strip()
            
            if len(xlist) != len(ylist):
                raise ValueError("Los vectores x_list y y_list deben tener el mismo tamaño.")
            if n >= len(xlist):
                raise ValueError("El grado 'n' debe ser menor que la cantidad de puntos.")
                
            # Truncar las listas según el grado n (se requieren n+1 puntos)
            x_data = xlist[:n+1]
            y_data = ylist[:n+1]
            
            # 2. Algoritmo de Diferencias Divididas
            m = len(x_data)
            tabla = np.zeros((m, m))
            tabla[:, 0] = y_data
            
            for j in range(1, m):
                for i in range(j, m):
                    tabla[i][j] = (tabla[i][j-1] - tabla[i-1][j-1]) / (x_data[i] - x_data[i-j])
            
            # Extraer los coeficientes de la diagonal principal
            coeficientes = np.diag(tabla)
            
            # 3. Evaluar el Polinomio en x_aprox
            x_calc = coeficientes[0]
            prod = 1.0
            for j in range(1, m):
                prod *= (x_aprox - x_data[j-1])
                x_calc += coeficientes[j] * prod
                
            # 4. Cálculo de Error (si existe función f)
            er_str = "Desconocido"
            if func_str:
                x_sym = sp.Symbol('x')
                f_sym = sp.sympify(func_str)
                valor_real = float(f_sym.subs(x_sym, x_aprox))
                if valor_real != 0:
                    er = abs((valor_real - x_calc) / valor_real) * 100
                    er_str = f"{er:.6f}%"
                else:
                    er_str = "División por cero en error"
            
            self.lbl_resultado.config(text=f"Aproximación: {x_calc:.6f} | Error Relativo: {er_str}")
            
            # 5. Estructurar resultados en Pandas y mostrarlos en Tkinter
            df_cols = ['x_i', 'f[x_i]'] + [f'Orden {j}' for j in range(1, m)]
            df_tabla = pd.DataFrame(np.column_stack((x_data, tabla)), columns=df_cols)
            
            # Actualizar Treeview
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(df_tabla.columns)
            self.tree["show"] = "headings"
            for col in df_tabla.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")
                
            for _, row in df_tabla.iterrows():
                # Formatear números para mejor visualización
                valores = [f"{val:.4f}" if val != 0 else "0.0000" for val in row]
                self.tree.insert("", "end", values=valores)
                
            # 6. Graficar con Matplotlib
            self.graficar(xlist, ylist, coeficientes, x_data, x_aprox, x_calc, func_str)
            
        except Exception as e:
            messagebox.showerror("Error de Cálculo", str(e))
            
    def graficar(self, x_total, y_total, coefs, x_data, x_aprox, y_aprox, func_str):
        # Limpiar gráfica anterior si existe
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
            
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Rango para evaluar las curvas
        x_min = min(x_total) - 1
        x_max = max(x_total) + 1
        x_range = np.linspace(x_min, x_max, 200)
        
        # Evaluar el polinomio para todo el rango
        y_range = []
        for val in x_range:
            res = coefs[0]
            prod = 1.0
            for j in range(1, len(coefs)):
                prod *= (val - x_data[j-1])
                res += coefs[j] * prod
            y_range.append(res)
            
        # 1. Graficar función original si existe (Azul continuo)
        if func_str:
            try:
                x_sym = sp.Symbol('x')
                f_sym = sp.sympify(func_str)
                f_lamb = sp.lambdify(x_sym, f_sym, "numpy")
                ax.plot(x_range, f_lamb(x_range), color="blue", linestyle="-", linewidth=1.5, label="Función Original $f(x)$")
            except:
                pass # Si hay error al evaluar la función para el rango, se ignora

        # 2. Polinomio de Newton (Verde discontinuo)
        ax.plot(x_range, y_range, color="green", linestyle="--", linewidth=1.5, label="Polinomio Newton")
        
        # 3. Puntos de interpolación (Rojos circulares)
        ax.plot(x_total, y_total, "or", markersize=8, markerfacecolor="red", label="Puntos Interpolación")
        
        # 4. Punto a aproximar (Cyan con cruz)
        ax.plot(x_aprox, y_aprox, "xc", markersize=10, markeredgewidth=2, label=f"Aproximación x={x_aprox}")
        
        ax.set_title("Interpolación de Newton-Gregory")
        ax.set_xlabel("Eje X")
        ax.set_ylabel("Eje Y")
        ax.grid(True, linestyle=":", alpha=0.7)
        ax.legend()
        
        # Incrustar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = NewtonInterpolationApp(root)
    root.mainloop()