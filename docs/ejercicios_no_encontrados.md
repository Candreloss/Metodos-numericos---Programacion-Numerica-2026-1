# Reporte: Ejercicios No Resueltos por Indeterminación de Datos

Este documento registra los ejercicios especificados en la pauta del proyecto que **no pudieron ser resueltos ni estudiados** debido a la falta de especificación y ambigüedad de los enunciados en las distintas ediciones de la bibliografía de referencia.

---

## 1. Análisis Numérico (Burden & Faires) - Sección 2.1, Ejercicio 7 (Método de Bisección)

### Causa de Omisión
La pauta indica únicamente *"Ejercicio 7, de la sección 2.1 del libro Análisis Numérico - Burden & Faires - 7ma Edición"*. Sin embargo, al contrastar esta referencia con las distintas ediciones del libro y solucionarios académicos, se detectaron las siguientes inconsistencias:

1. **Variación de Edición**: Dependiendo de la edición del libro, la sección 2.1 (Método de Bisección) tiene diferentes distribuciones de problemas. En la **9ma y 10ma edición**, el Ejercicio 7 de la sección 2.1 es un problema de demostración teórica relacionado con el **Teorema de Punto Fijo** (que corresponde a la sección 2.2), pidiendo demostrar la existencia y unicidad de un punto fijo para una función como $g(x) = \pi + 0.5 \sin(x/2)$, lo cual no es aplicable directamente al algoritmo de Bisección programado en la aplicación.
2. **Multiplicidad de Funciones**: En las ediciones donde el Ejercicio 7 sí corresponde a Bisección, el problema se divide en múltiples sub-apartados independientes (a, b, c, d), cada uno con una función trascendente y un intervalo distinto:
   *   *(a)* $x - 2^{-x} = 0$ en $[0, 1]$
   *   *(b)* $x + 1 - 2\sin(\pi x) = 0$ en $[0, 0.5]$ y $[0.5, 1]$
   *   *(c)* $e^x - x^2 + 3x - 2 = 0$ en $[0, 1]$
   *   *(d)* $x\cos x - 2x^2 + 3x - 1 = 0$ en $[0.2, 0.3]$ y $[1.2, 1.3]$
   
Al no estar especificado cuál de estos incisos correspondía al trabajo del grupo, y para evitar la introducción de datos arbitrarios ajenos a la evaluación, se ha omitido la resolución del mismo.

---

## 2. Análisis Numérico (Burden & Faires) - Sección 2.3, Ejercicio 6 (Métodos de Newton y Secante)

### Causa de Omisión
La pauta indica *"Ejercicio 6, de la sección 2.3 del libro Análisis Numérico - Burden & Faires - 7ma Edición"* y luego para el método de la Secante *"repita las funciones que se le asignó en el ítem anterior"*. 

De igual forma que el problema anterior:
1. En la sección 2.3 (dedicada a Newton y sus extensiones) de varias ediciones del Burden, el Ejercicio 6 es una comparación de convergencia o una cota de error teórica que requiere la aplicación del método de la secante y la regla de la falsa posición sobre ecuaciones complejas, sin definir una única función para el cálculo directo de raíces.
2. En otras versiones, el problema 6 consta de varios sub-apartados con funciones polinómicas y trigonométricas de alta frecuencia donde no se especifica la tolerancia de parada ni la aproximación inicial exacta que el docente deseaba evaluar.

---

### Solución Alternativa Implementada
Para garantizar que se evalúe correctamente la funcionalidad de los algoritmos de **Bisección**, **Newton-Raphson** y **Secante** del programa, se ha realizado el estudio exhaustivo del **Problema del Abrevadero Semicircular** (ejercicio aplicado de la guía de bisección) y de los ejercicios del libro de **Chapra & Canale** (capítulos 12 y 18) cuyos datos, ecuaciones y flujos de red de reactores sí están definidos de forma explícita e inequívoca en los requerimientos del proyecto.
