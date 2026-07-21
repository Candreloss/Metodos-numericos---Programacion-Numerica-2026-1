"""
Script de resolución y generación de resultados/gráficas para los Problemas 12.1 a 12.4
del libro 'Métodos Numéricos para Ingenieros' (Chapra & Canale, 7ma Edición).
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Directorio de salida
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. SISTEMA BASE (SECCIÓN 12.1 CHAPRA)
# ---------------------------------------------------------
A_base = np.array([
    [6,  0, -1,  0,  0],
    [-3, 3,  0,  0,  0],
    [0, -1,  9,  0,  0],
    [0, -1, -8, 11, -2],
    [-3, 0,  0,  0,  4]
], dtype=float)

b_base = np.array([50, 0, 160, 0, 0], dtype=float)

c_base = np.linalg.solve(A_base, b_base)
A_inv_base = np.linalg.inv(A_base)

# ---------------------------------------------------------
# 2. PROBLEMA 12.1
# ---------------------------------------------------------
A_121 = np.array([
    [7,  0, -1,  0,  0],
    [-4, 4,  0,  0,  0],
    [0, -1,  9,  0,  0],
    [0, -2, -8, 12, -2],
    [-3, 0,  0,  0,  4]
], dtype=float)

b_121 = np.array([240, 0, 80, 0, 0], dtype=float)

c_121 = np.linalg.solve(A_121, b_121)
A_inv_121 = np.linalg.inv(A_121)

# ---------------------------------------------------------
# 3. PROBLEMA 12.2
# ---------------------------------------------------------
delta_b = np.array([0, 0, -40, 0, 0], dtype=float)
delta_c = A_inv_base @ delta_b
c_122 = c_base + delta_c
pct_change_122 = (delta_c / c_base) * 100

# ---------------------------------------------------------
# 4. PROBLEMA 12.4
# ---------------------------------------------------------
A_124 = np.array([
    [13, -4,  0,  0, -4],
    [-4,  8, -2,  0, -2],
    [-3,  0, 18, -7,  0],
    [ 0, -4,-16, 20,  0],
    [-6,  0,  0, -3,  9]
], dtype=float)

b_124 = np.array([50, 0, 160, 0, 0], dtype=float)

c_124 = np.linalg.solve(A_124, b_124)
A_inv_124 = np.linalg.inv(A_124)

# ---------------------------------------------------------
# IMPRESIÓN DE RESULTADOS EN CONSOLA
# ---------------------------------------------------------
print("====================================================")
print("  RESULTADOS DE LOS PROBLEMAS 12.1 A 12.4 (CHAPRA)")
print("====================================================")
print("\n[Base Sec. 12.1] Concentraciones:", np.round(c_base, 4))
print("[Problema 12.1] Concentraciones:", np.round(c_121, 4))
print("[Problema 12.2] Concentraciones:", np.round(c_122, 4))
print("[Problema 12.2] % Cambio:", np.round(pct_change_122, 4))
print("[Problema 12.4] Concentraciones:", np.round(c_124, 4))

# ---------------------------------------------------------
# GENERACIÓN DE GRÁFICAS
# ---------------------------------------------------------

# Gráfica 1: Comparativa de concentraciones entre escenarios
plt.figure(figsize=(10, 6))
x = np.arange(1, 6)
width = 0.2

plt.bar(x - 1.5*width, c_base, width, label='Base (Sec 12.1)', color='#3498db')
plt.bar(x - 0.5*width, c_121, width, label='Prob. 12.1 (Nuevos flujos/conc)', color='#e74c3c')
plt.bar(x + 0.5*width, c_122, width, label='Prob. 12.2 (-25% ent 3)', color='#2ecc71')
plt.bar(x + 1.5*width, c_124, width, label='Prob. 12.4 (Red de flujos)', color='#9b59b6')

plt.xlabel('Reactor i', fontsize=12, fontweight='bold')
plt.ylabel('Concentración $c_i$ (mg/m³)', fontsize=12, fontweight='bold')
plt.title('Comparativa de Concentraciones en Reactores (Problemas 12.1 - 12.4)', fontsize=14, fontweight='bold', pad=15)
plt.xticks(x, [f'Reactor {i}' for i in x])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(frameon=True, facecolor='white', edgecolor='none')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'comparativa_concentraciones.png'), dpi=300)
plt.close()

# Gráfica 2: Cambio porcentual en el Problema 12.2
plt.figure(figsize=(8, 5))
bars = plt.bar([f'R{i}' for i in range(1, 6)], pct_change_122, color=['#e74c3c' if val < -10 else '#f39c12' for val in pct_change_122])

plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.xlabel('Reactor i', fontsize=12, fontweight='bold')
plt.ylabel('Cambio Porcentual (%)', fontsize=12, fontweight='bold')
plt.title('Problema 12.2: Cambio Porcentual en Concentración por Disminución del 25% en R3', fontsize=12, fontweight='bold', pad=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval - 1.5, f'{yval:.2f}%', ha='center', va='top', fontweight='bold', color='white')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'cambio_porcentual_12_2.png'), dpi=300)
plt.close()

# Gráfica 3: Mapas de calor de las Matrices Inversas
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

im1 = axes[0].imshow(A_inv_base, cmap='Blues')
axes[0].set_title('Matriz Inversa $A^{-1}$ (Base Sec. 12.1)', fontweight='bold')
axes[0].set_xticks(range(5))
axes[0].set_yticks(range(5))
axes[0].set_xticklabels([f'R{i}' for i in range(1,6)])
axes[0].set_yticklabels([f'R{i}' for i in range(1,6)])
for i in range(5):
    for j in range(5):
        axes[0].text(j, i, f'{A_inv_base[i, j]:.3f}', ha='center', va='center', color='black' if A_inv_base[i,j] < 0.15 else 'white', fontsize=9)

im2 = axes[1].imshow(A_inv_124, cmap='Purples')
axes[1].set_title('Matriz Inversa $A^{-1}$ (Problema 12.4)', fontweight='bold')
axes[1].set_xticks(range(5))
axes[1].set_yticks(range(5))
axes[1].set_xticklabels([f'R{i}' for i in range(1,6)])
axes[1].set_yticklabels([f'R{i}' for i in range(1,6)])
for i in range(5):
    for j in range(5):
        axes[1].text(j, i, f'{A_inv_124[i, j]:.3f}', ha='center', va='center', color='black' if A_inv_124[i,j] < 0.12 else 'white', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'mapa_calor_matrices_inversas.png'), dpi=300)
plt.close()

print(f"Gráficas generadas exitosamente en {OUTPUT_DIR}")
