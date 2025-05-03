import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to sys.pathorts
import tkinter as tk
from tkinter import messagebox, simpledialog
from logic.operations import generar_matriz, realizar_operacion
from logic.matrix_utils import format_matrix, es_escalonada_reducida
import numpy as np
from fractions import Fraction

class GaussGameApp:
    def __init__(self, root):
        """Initialize the GaussGameApp with the main Tkinter root."""
        self.root = root
        self.root.title("🎯 Desafío Matemático 🎯")
        self.matriz = None
        self.n = 0
        self.current_level = 0

        self.start_frame = tk.Frame(root)
        self.start_frame.pack()

        tk.Label(self.start_frame, text="🎯 Bienvenido al Desafío Matemático 🎯", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.start_frame, text="Elige un nivel:").pack(pady=5)

        self.level1_button = tk.Button(self.start_frame, text="Nivel 1: Gauss Jordan", command=self.start_gauss)
        self.level1_button.pack(pady=5)

        self.level2_button = tk.Button(self.start_frame, text="Nivel 2: Transpuesta", command=self.start_transpose, state="disabled")
        self.level2_button.pack(pady=5)

        self.level3_button = tk.Button(self.start_frame, text="Nivel 3: Inversa", command=self.start_inverse, state="disabled")
        self.level3_button.pack(pady=5)

        self.game_frame = tk.Frame(root)

    def start_gauss(self):
        """Start the Gauss Jordan level."""
        self.n = self.ask_matrix_size()
        if self.n is None:
            return
        self.matriz = generar_matriz(self.n)
        self.identidad = np.eye(self.n, dtype=object)  # Initialize identity matrix
        self.start_frame.pack_forget()
        self.show_game_screen("Gauss Jordan")

    def start_transpose(self):
        if self.current_level < 1:
            messagebox.showerror("Error", "Debes completar el Nivel 1 antes de avanzar al Nivel 2.")
            return
        self.n = self.ask_matrix_size()
        if self.n is None:
            return
        self.matriz = np.zeros((self.n, self.n), dtype=object)  
        self.start_frame.pack_forget()
        self.show_game_screen("Transpuesta")

    def start_inverse(self):
        if self.current_level < 2:
            messagebox.showerror("Error", "Debes completar el Nivel 2 antes de avanzar al Nivel 3.")
            return
        self.n = self.ask_matrix_size()
        if self.n is None:
            return
        self.matriz = generar_matriz(self.n)
        self.start_frame.pack_forget()
        self.show_game_screen("Inversa")

    def ask_matrix_size(self):
        """Prompt the user to input the size of the matrix."""
        try:
            n = int(simpledialog.askstring("Tamaño de la matriz", "Ingresa el tamaño de la matriz cuadrada (2-5):"))
            if n < 2 or n > 5:
                raise ValueError
            return n
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Por favor, ingresa un número válido entre 2 y 5.")
            return None

    def show_game_screen(self, level):
        """Display the game screen for the current level."""
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.game_frame.pack()
        tk.Label(self.game_frame, text=f"Nivel: {level}", font=("Arial", 14)).pack(pady=10)

        # Create a vertical separator as a column of "|"
        separador = np.array([["|"] for _ in range(self.n)], dtype=object)
        matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  # Combine matrices with separator
        matriz_texto = format_matrix(matriz_combinada)
        self.matriz_label = tk.Label(self.game_frame, text=f"Matriz y Resultante:\n{matriz_texto}", font=("Courier", 12))
        self.matriz_label.pack(pady=5)

        if level == "Gauss Jordan":
            self.add_gauss_controls()
        elif level == "Transpuesta":
            self.add_transpose_controls()
        elif level == "Inversa":
            self.add_inverse_controls()

    def add_gauss_controls(self):
        tk.Button(self.game_frame, text="Intercambiar filas", command=self.intercambiar_filas).pack(pady=5)
        tk.Button(self.game_frame, text="Multiplicar fila por un escalar", command=self.multiplicar_fila).pack(pady=5)
        tk.Button(self.game_frame, text="Sumar múltiplo de una fila a otra", command=self.sumar_filas).pack(pady=5)
        tk.Button(self.game_frame, text="Terminar", command=self.terminar_nivel).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.quit_game).pack(pady=5)

    def add_transpose_controls(self):
        tk.Button(self.game_frame, text="Digitar matriz", command=self.digitar_matriz).pack(pady=5)
        tk.Button(self.game_frame, text="Terminar", command=self.terminar_nivel).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.quit_game).pack(pady=5)

    def add_inverse_controls(self):
        tk.Button(self.game_frame, text="Terminar", command=self.terminar_nivel).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.quit_game).pack(pady=5)

    def intercambiar_filas(self):
        try:
            entrada = simpledialog.askstring("Intercambiar filas", "Ingresa las filas a intercambiar (ej: 1 2):")
            if not entrada:
                raise ValueError("No se ingresó ninguna entrada.")
            f1, f2 = map(int, entrada.split())
            f1, f2 = f1 - 1, f2 - 1  
            self.matriz, self.identidad = realizar_operacion(self.matriz, "intercambio", f1, f2, B=self.identidad)
            self.actualizar_matriz()
            messagebox.showinfo("Operación realizada", f"Se intercambiaron las filas {f1 + 1} y {f2 + 1}.")
        except Exception:
            messagebox.showerror("Error", "Entrada inválida. Asegúrate de ingresar dos números separados por un espacio.")

    def multiplicar_fila(self):
        try:
            entrada = simpledialog.askstring("Multiplicar fila", "Ingresa la fila y el factor de multiplicación (ej: 1 1/2):")
            if not entrada:
                raise ValueError("No se ingresó ninguna entrada.")
            f1, factor = entrada.split()
            f1 = int(f1) - 1  
            factor = float(eval(factor))  
            if f1 < 0 or f1 >= self.n:
                raise IndexError("El índice de la fila está fuera del rango de la matriz.")
            self.matriz, self.identidad = realizar_operacion(self.matriz, "multiplicacion", f1, factor=factor, B=self.identidad)
            self.actualizar_matriz()
            factor_formateado = Fraction(factor).limit_denominator() if factor != int(factor) else factor
            messagebox.showinfo("Operación realizada", f"La fila {f1 + 1} fue multiplicada por {factor_formateado}.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida: {ve}")
        except IndexError as ie:
            messagebox.showerror("Error", f"Índice fuera de rango: {ie}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")

    def sumar_filas(self):
        """Suma un múltiplo de una fila a otra, modificando solo la fila destino."""
        try:
            entrada = simpledialog.askstring(
                "Sumar filas", 
                "Ingresa la fila fuente, la fila destino y el factor (ej: 1 2 -3):"
            )
            if not entrada:
                raise ValueError("No se ingresó ninguna entrada.")
            partes = entrada.split()
            if len(partes) != 3:
                raise ValueError("Debes ingresar exactamente tres valores separados por espacios.")
            
            f1, f2 = int(partes[0]) - 1, int(partes[1]) - 1  # Convert to zero-based index
            factor = float(eval(partes[2]))  # Evaluate the factor (e.g., fractions)

            if f1 < 0 or f1 >= self.n or f2 < 0 or f2 >= self.n:
                raise IndexError("Los índices de las filas están fuera del rango de la matriz.")

            # Multiply the source row by the factor and add it to the target row
            self.matriz[f2] = [
                Fraction(x) + Fraction(factor) * Fraction(y) 
                for x, y in zip(self.matriz[f2], self.matriz[f1])
            ]
            if self.identidad is not None:
                self.identidad[f2] = [
                    Fraction(x) + Fraction(factor) * Fraction(y) 
                    for x, y in zip(self.identidad[f2], self.identidad[f1])
                ]

            self.actualizar_matriz()
            messagebox.showinfo(
                "Operación realizada", 
                f"Se sumó {factor} veces la fila {f1 + 1} a la fila {f2 + 1}."
            )
        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida: {ve}")
        except IndexError as ie:
            messagebox.showerror("Error", f"Índice fuera de rango: {ie}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")

    def actualizar_matriz(self):
        """Actualiza la visualización de la matriz y la matriz identidad juntas con una línea separadora."""
        separador = np.array([["|"] for _ in range(self.n)], dtype=object)
        matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  # Combine matrices with separator
        matriz_texto = format_matrix(matriz_combinada)
        self.matriz_label.config(text=f"Matriz y Resultante\n{matriz_texto}")

    def terminar_nivel(self):
        """Valida si la matriz actual es correcta y regresa al menú principal si no lo es."""
        try:
            if es_escalonada_reducida(self.matriz):
                messagebox.showinfo("¡Correcto!", "¡Has completado el nivel correctamente!")
                self.current_level = 1  # Update the current level
                self.level2_button.config(state="normal")  # Enable the next level button
            else:
                messagebox.showerror("Incorrecto", "La matriz no está en forma escalonada reducida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def quit_game(self):
        """Return to the main menu and clear the current matrix."""
        self.matriz = None
        if hasattr(self, 'matriz_label'):
            self.matriz_label.config(text="")

        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.game_frame.pack_forget()
        self.start_frame.pack()
