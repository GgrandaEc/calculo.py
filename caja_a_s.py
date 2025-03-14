#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aplicación para Cálculo de Caja Sin Tapa con Volumen Fijo
--------------------------------------------------------

Esta aplicación calcula las dimensiones óptimas de una caja sin tapa
con un volumen fijo, utilizando cálculo diferencial para minimizar
la cantidad de material utilizado (área superficial).

Incluye:
- Cálculo de dimensiones óptimas
- Visualización 3D de la caja resultante
- Explicación del proceso matemático
- Presentación detallada de resultados

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class CajaSinTapaApp:
    """
    Clase principal que implementa la aplicación de cálculo de
    dimensiones óptimas para una caja sin tapa con volumen fijo.
    """
    
    def __init__(self, root):
        """
        Inicializa la aplicación con la interfaz gráfica.
        
        Args:
            root: La ventana principal de Tkinter
        """
        self.root = root
        self.root.title("Cálculo de Caja Sin Tapa - Optimización")
        self.root.geometry("950x700")
        self.root.configure(bg="#e8f5e9")  # Fondo verde claro como en tu imagen
        
        # Variables para almacenar los datos
        self.volumen_var = tk.StringVar()
        self.resultados = None
        
        # Configuración de estilo
        self.configurar_estilo()
        
        # Crear los widgets de la interfaz
        self.crear_interfaz()
    
    def configurar_estilo(self):
        """
        Configura el estilo visual de la aplicación para mantener
        la gama de colores verde que se muestra en la imagen de referencia.
        """
        self.style = ttk.Style()
        
        # Configuración de colores principales
        self.colores = {
            'bg_principal': '#e8f5e9',       # Fondo principal (verde muy claro)
            'bg_header': '#4caf50',          # Fondo del encabezado (verde medio)
            'bg_form': '#ffffff',            # Fondo del formulario (blanco)
            'bg_resultados': '#f1f8e9',      # Fondo de resultados (verde pálido)
            'fg_principal': '#212121',       # Texto principal (casi negro)
            'fg_header': '#ffffff',          # Texto del encabezado (blanco)
            'accent': '#2e7d32',             # Color de acento (verde oscuro)
            'border': '#81c784',             # Color de bordes (verde claro)
            'error': '#d32f2f'               # Color de error (rojo)
        }
        
        # Estilo para los frames
        self.style.configure('Header.TFrame', background=self.colores['bg_header'])
        self.style.configure('Form.TFrame', background=self.colores['bg_form'])
        self.style.configure('Results.TFrame', background=self.colores['bg_resultados'])
        
        # Estilo para las etiquetas
        self.style.configure('Header.TLabel', 
                            background=self.colores['bg_header'],
                            foreground=self.colores['fg_header'],
                            font=('Arial', 16, 'bold'))
        
        self.style.configure('Title.TLabel', 
                            background=self.colores['bg_form'],
                            foreground=self.colores['fg_principal'],
                            font=('Arial', 12, 'bold'))
                            
        self.style.configure('Normal.TLabel', 
                            background=self.colores['bg_form'],
                            foreground=self.colores['fg_principal'],
                            font=('Arial', 10))
        
        # Estilo para los botones
        self.style.configure('Calculate.TButton', 
                            background=self.colores['accent'],
                            foreground=self.colores['fg_header'],
                            font=('Arial', 10, 'bold'))
        
        self.style.map('Calculate.TButton',
                      background=[('active', self.colores['accent'])])
                      
    def crear_interfaz(self):
        """
        Crea todos los elementos de la interfaz gráfica.
        """
        # Frame principal que contendrá toda la aplicación
        main_frame = ttk.Frame(self.root, padding="10", style='Form.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== Encabezado =====
        header_frame = ttk.Frame(main_frame, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="Visualización de la Caja sin Tapa", 
                style='Header.TLabel').pack(pady=10)
        
        # ===== Frame para entrada de datos =====
        input_frame = ttk.Frame(main_frame, style='Form.TFrame')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Entrada de Datos", 
                style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=5)
        
        # Frame para el formulario
        form_frame = ttk.Frame(input_frame, style='Form.TFrame')
        form_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Entrada para el volumen
        ttk.Label(form_frame, text="Volumen de la caja (u³):", 
                style='Normal.TLabel').grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        volume_entry = ttk.Entry(form_frame, textvariable=self.volumen_var, width=15)
        volume_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Botón de cálculo
        calculate_button = ttk.Button(form_frame, text="Calcular Dimensiones Óptimas", 
                                    command=self.calcular_dimensiones, style='Calculate.TButton')
        calculate_button.grid(row=0, column=2, padx=15, pady=5)
        
        # ===== Frame para resultados y visualización =====
        self.results_frame = ttk.Frame(main_frame, style='Results.TFrame')
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Inicialmente este frame está vacío, se llenará al calcular
        
    def calcular_dimensiones(self):
        """
        Calcula las dimensiones óptimas de la caja sin tapa.
        Utiliza cálculo diferencial para minimizar el área superficial
        manteniendo un volumen constante.
        """
        try:
            # Obtener y validar el volumen
            volumen = float(self.volumen_var.get())
            if volumen <= 0:
                messagebox.showerror("Error", "El volumen debe ser un número positivo.")
                return
                
            # Cálculo de dimensiones óptimas usando derivadas
            # Para una caja sin tapa con volumen fijo, la solución es:
            # x = y = cbrt(2*V), h = V/(x*y) = V/(x²)
            x = (2 * volumen) ** (1/3)
            y = x  # Para una caja óptima, x = y (base cuadrada)
            h = volumen / (x * y)
            
            # Cálculo del área superficial mínima
            area = x * y + 2 * x * h + 2 * y * h
            
            # Almacenar resultados
            self.resultados = {
                'volumen': volumen,
                'x': x,
                'y': y,
                'h': h,
                'area': area
            }
            
            # Mostrar resultados
            self.mostrar_resultados()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico válido para el volumen.")
    
    def mostrar_resultados(self):
        """
        Muestra los resultados calculados y la visualización 3D.
        """
        # Limpiar el frame de resultados
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        # Crear un notebook (pestañas) para organizar la información
        notebook = ttk.Notebook(self.results_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== Pestaña de resultados numéricos =====
        results_tab = ttk.Frame(notebook, style='Results.TFrame')
        notebook.add(results_tab, text="Resultados")
        
        results_text = f"""
        Dimensiones Óptimas:
        
        • Ancho (x) = {self.resultados['x']:.4f} u
        • Largo (y) = {self.resultados['y']:.4f} u
        • Altura (h) = {self.resultados['h']:.4f} u
        
        • Área mínima = {self.resultados['area']:.4f} u²
        • Volumen = {self.resultados['volumen']:.4f} u³
        
        La caja con estas dimensiones minimiza la cantidad 
        de material necesario (área superficial) para el 
        volumen especificado.
        """
        
        results_label = ttk.Label(results_tab, text=results_text, 
                                style='Normal.TLabel', justify=tk.LEFT)
        results_label.pack(padx=20, pady=20, anchor=tk.W)
        
        # ===== Pestaña de visualización 3D =====
        visual_tab = ttk.Frame(notebook, style='Results.TFrame')
        notebook.add(visual_tab, text="Visualización 3D")
        
        # Crear la figura 3D
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
        
        # Dibujar la caja sin tapa
        self.dibujar_caja_3d(ax)
        
        # Colocar la figura en la interfaz
        canvas = FigureCanvasTkAgg(fig, visual_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # ===== Pestaña de proceso matemático =====
        process_tab = ttk.Frame(notebook, style='Results.TFrame')
        notebook.add(process_tab, text="Proceso Matemático")
        
        # Texto con la explicación del proceso
        process_text = f"""
        Proceso Matemático para Minimizar el Área:
        
        1. Planteamiento del problema:
           • Volumen fijo: V = {self.resultados['volumen']} u³
           • Base rectangular: x × y
           • Altura: h
           • Área a minimizar: A = xy + 2xh + 2yh (base + 4 paredes)
        
        2. Como el volumen es fijo: V = xyh
           Despejamos h: h = V/(xy)
        
        3. Sustituimos en la función de área:
           A(x,y) = xy + 2x·V/(xy) + 2y·V/(xy)
           A(x,y) = xy + 2V/y + 2V/x
        
        4. Tomamos derivadas parciales e igualamos a cero:
           ∂A/∂x = y - 2V/x² = 0
           ∂A/∂y = x - 2V/y² = 0
        
        5. De la primera ecuación:
           y = 2V/x²
        
        6. De la segunda ecuación:
           x = 2V/y²
        
        7. Sustituyendo en la segunda ecuación:
           x = 2V/(2V/x²)² = x⁴/(2V)
           2V = x³
           x = ∛(2V) = {self.resultados['x']:.4f}
        
        8. Por simetría del problema: y = x = {self.resultados['y']:.4f}
        
        9. La altura: h = V/(x·y) = V/{self.resultados['x']*self.resultados['y']:.4f} = {self.resultados['h']:.4f}
        
        10. El área mínima: A = xy + 2xh + 2yh = {self.resultados['area']:.4f} u²
        """
        
        # Crear un widget de texto con scrollbar para la explicación matemática
        text_frame = ttk.Frame(process_tab)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                            bg=self.colores['bg_resultados'],
                            fg=self.colores['fg_principal'],
                            font=('Arial', 10))
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        text_widget.insert(tk.END, process_text)
        text_widget.config(state='disabled')  # Hacer el texto no editable
    
    def dibujar_caja_3d(self, ax):
        """
        Dibuja la caja sin tapa en 3D.
        
        Args:
            ax: El eje 3D de Matplotlib donde se dibujará la caja
        """
        x, y, h = self.resultados['x'], self.resultados['y'], self.resultados['h']
        
        # Definir los vértices de la caja (sin la tapa superior)
        vertices = np.array([
            [0, 0, 0],  # v0
            [x, 0, 0],  # v1
            [x, y, 0],  # v2
            [0, y, 0],  # v3
            [0, 0, h],  # v4
            [x, 0, h],  # v5
            [x, y, h],  # v6
            [0, y, h]   # v7
        ])
        
        # Definir las caras de la caja (base y 4 paredes)
        caras = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # base
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # pared frontal
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # pared derecha
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # pared trasera
            [vertices[3], vertices[0], vertices[4], vertices[7]]   # pared izquierda
        ]
        
        # Colores para las diferentes caras (tonos de verde como en la imagen)
        colores = [
            '#81c784',  # base (verde claro)
            '#4caf50',  # pared frontal (verde medio)
            '#4caf50',  # pared derecha (verde medio)
            '#4caf50',  # pared trasera (verde medio)
            '#4caf50'   # pared izquierda (verde medio)
        ]
        
        # Crear la colección de polígonos 3D
        caja = Poly3DCollection(caras, alpha=0.7, linewidths=1, edgecolors='black')
        caja.set_facecolor(colores)
        ax.add_collection3d(caja)
        
        # Configurar los límites de los ejes
        ax.set_xlim(0, x*1.2)
        ax.set_ylim(0, y*1.2)
        ax.set_zlim(0, h*1.2)
        
        # Etiquetas de los ejes
        ax.set_xlabel('Ancho (x)')
        ax.set_ylabel('Largo (y)')
        ax.set_zlabel('Altura (h)')
        
        # Título del gráfico
        ax.set_title(f'Caja Sin Tapa Óptima (V={self.resultados["volumen"]:.2f} u³)')
        
        # Agregar etiquetas con las dimensiones
        ax.text(x/2, 0, 0, f'x={x:.2f}', color='black')
        ax.text(x, y/2, 0, f'y={y:.2f}', color='black')
        ax.text(0, 0, h/2, f'h={h:.2f}', color='black')
        
        # Configurar la vista
        ax.view_init(elev=30, azim=30)

# Función principal para iniciar la aplicación
def main():
    """
    Función principal que inicia la aplicación.
    """
    root = tk.Tk()
    app = CajaSinTapaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()