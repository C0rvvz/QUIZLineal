import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import tkinter as tk
from tkinter import messagebox, simpledialog
from logic.operations import generar_matriz, realizar_operacion, es_transpuesta_correcta, verificar_transpuesta, calcular_inversa, verificar_inversa, calcular_resultado, calcular_determinante
from logic.matrix_utils import format_matrix, es_escalonada_reducida
import numpy as np
from fractions import Fraction

class Linealgame:
    def __init__(self, root):
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
        self.identidad = np.eye(self.n, dtype=object) 

        self.start_frame.pack_forget()
        self.show_game_screen("Gauss Jordan")

    def show_completed_level_1(self):
        """Muestra la matriz completada del nivel 1."""
        if self.matriz is None:
            tk.messagebox.showerror("Error", "La matriz no está definida.")
            return

      
        for widget in self.root.winfo_children():
            widget.destroy()

      
        matriz_texto = format_matrix(self.matriz)
        text_widget = tk.Text(self.root, wrap="none", height=10, width=50)
        text_widget.insert("1.0", matriz_texto)
        text_widget.config(state="disabled")
        text_widget.pack()

       
        tk.Button(self.root, text="Continuar", command=self.next_level).pack()
        tk.Button(self.root, text="Salir", command=self.quit_game).pack()

    def next_level(self):
        """Avanza al siguiente nivel."""
        tk.messagebox.showinfo("Nivel 2", "Aquí comienza el nivel 2.")
        self.start_transpose()

    def start_transpose(self):
        """Start the Transpose level."""
        if self.current_level < 1:
            messagebox.showerror("Error", "Debes completar el Nivel 1 antes de avanzar al Nivel 2.")
            return
        self.n = self.ask_matrix_size() 
        if self.n is None:
            return
        self.matriz = generar_matriz(self.n) 
        self.start_frame.pack_forget()
        self.show_game_screen("Transpuesta")

    def start_inverse(self):
        """Start the Inverse level."""
        if self.current_level < 2:
            messagebox.showerror("Error", "Debes completar el Nivel 2 antes de avanzar al Nivel 3.")
            return
        self.n = 2  
        self.matriz = generar_matriz(self.n) 
        self.determinante = calcular_determinante(self.matriz)
        if self.determinante == 0:
            messagebox.showerror("Error", "La matriz generada no tiene inversa. Intenta nuevamente.")
            self.quit_game()
            return
        self.inversa_correcta = calcular_inversa(self.matriz)
        self.start_frame.pack_forget()
        self.show_game_screen("Inversa")

    def ask_matrix_size(self):
        """Prompt the user to input the size of the matrix (only for level 1)."""
        if self.current_level > 0:
            return self.n 
        try:
            n = int(simpledialog.askstring("Tamaño de la matriz", "Ingresa el tamaño de la matriz cuadrada (2-5):"))
            if n < 2 or n > 5:
                raise ValueError
            return n
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Por favor, ingresa un número válido entre 2 y 5.")
            return None

    def show_game_screen(self, level, disable_controls=False):
        """Display the game screen for the current level."""
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.game_frame.pack()
        tk.Label(self.game_frame, text=f"Nivel: {level}", font=("Arial", 14)).pack(pady=10)

        if level == "Transpuesta":
           
            matriz_texto = format_matrix(self.matriz)
            tk.Label(self.game_frame, text="Matriz Original:", font=("Arial", 12)).pack(pady=5)
            text_widget = tk.Text(self.game_frame, wrap="none", height=10, width=50)
            text_widget.insert("1.0", matriz_texto)
            text_widget.config(state="disabled")
            text_widget.pack(pady=5)

            
            self.entries = []  
            tk.Label(self.game_frame, text="Ingresa la matriz transpuesta:", font=("Arial", 12)).pack(pady=5)
            for i in range(self.n):
                row_entries = []
                row_frame = tk.Frame(self.game_frame)
                row_frame.pack()
                for j in range(self.n):
                    entry = tk.Entry(row_frame, width=5, justify="center")
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.entries.append(row_entries)

            
            tk.Button(self.game_frame, text="Resultado", command=self.mostrar_resultado_transpuesta).pack(pady=5)

           
            tk.Button(self.game_frame, text="Terminar", command=self.verificar_transpuesta).pack(pady=5)

           
            tk.Button(self.game_frame, text="Salir", command=self.salir_nivel).pack(pady=5)

        elif level == "Inversa":
           
            matriz_texto = format_matrix(self.matriz)
            tk.Label(self.game_frame, text="Matriz Original:", font=("Arial", 12)).pack(pady=5)
            text_widget = tk.Text(self.game_frame, wrap="none", height=10, width=50)
            text_widget.insert("1.0", matriz_texto)
            text_widget.config(state="disabled")
            text_widget.pack(pady=5)

           
            self.entries = []  
            tk.Label(self.game_frame, text="Ingresa la matriz inversa:", font=("Arial", 12)).pack(pady=5)
            for i in range(self.n):
                row_entries = []
                row_frame = tk.Frame(self.game_frame)
                row_frame.pack()
                for j in range(self.n):
                    entry = tk.Entry(row_frame, width=5, justify="center")
                    entry.grid(row=i, column=j, padx=5, pady=5)
                    row_entries.append(entry)
                self.entries.append(row_entries)

           
            tk.Button(self.game_frame, text="Resultado", command=self.mostrar_resultado_inversa).pack(pady=5)

           
            tk.Button(self.game_frame, text="Terminar", command=self.verificar_inversa).pack(pady=5)

            
            tk.Button(self.game_frame, text="Salir", command=self.salir_nivel).pack(pady=5)

        elif level == "Gauss Jordan":
            separador = np.array([["|"] for _ in range(self.n)], dtype=object)
            matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  
            matriz_texto = format_matrix(matriz_combinada)
            self.matriz_label = tk.Label(self.game_frame, text=f"Matriz y Resultante:\n{matriz_texto}", font=("Courier", 12))
            self.matriz_label.pack(pady=5)
            self.add_gauss_controls(disable_controls)

    def mostrar_resultado_transpuesta(self):
        """Muestra la matriz transpuesta correcta."""
        try:
            transpuesta = self.matriz.T
            matriz_texto = format_matrix(transpuesta)
            messagebox.showinfo("Resultado", f"Matriz transpuesta:\n{matriz_texto}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def mostrar_resultado_inversa(self):
        """Muestra la matriz inversa correcta y la almacena para validación."""
        try:
            self.inversa_correcta = calcular_inversa(self.matriz)  
            if self.inversa_correcta is None:
                messagebox.showerror("Error", "La matriz no tiene inversa.")
                return
            matriz_texto = format_matrix(self.inversa_correcta)
            messagebox.showinfo("Resultado", f"Matriz inversa:\n{matriz_texto}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def add_gauss_controls(self, disable_controls=False):
        """Add controls for the Gauss Jordan level."""
        if not disable_controls:
            tk.Button(self.game_frame, text="Intercambiar filas", command=self.intercambiar_filas).pack(pady=5)
            tk.Button(self.game_frame, text="Multiplicar fila por un escalar", command=self.multiplicar_fila).pack(pady=5)
            tk.Button(self.game_frame, text="Sumar múltiplo de una fila a otra", command=self.sumar_filas).pack(pady=5)
            tk.Button(self.game_frame, text="Terminar", command=self.terminar_nivel).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.quit_game).pack(pady=5)

    def add_transpose_controls(self):
        """Add controls for the Transpose level."""
        tk.Button(self.game_frame, text="Digitar matriz", command=self.digitar_matriz_transpuesta).pack(pady=5)
        tk.Button(self.game_frame, text="Terminar", command=self.verificar_transpuesta).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.salir_nivel).pack(pady=5)

    def add_inverse_controls(self):
        tk.Button(self.game_frame, text="Terminar", command=self.verificar_inversa).pack(pady=5)
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
            
            f1, f2 = int(partes[0]) - 1, int(partes[1]) - 1  
            factor = float(eval(partes[2]))  

            if f1 < 0 or f1 >= self.n or f2 < 0 or f2 >= self.n:
                raise IndexError("Los índices de las filas están fuera del rango de la matriz.")

           
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
        matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  
        matriz_texto = format_matrix(matriz_combinada)
        self.matriz_label.config(text=f"Matriz y Resultante\n{matriz_texto}")

    def terminar_nivel(self):
        """Valida si la matriz actual es correcta y regresa al menú principal."""
        try:
            if es_escalonada_reducida(self.matriz):
                messagebox.showinfo("¡Correcto!", "¡Has completado el nivel correctamente!")
                self.current_level += 1  
                if self.current_level >= 1:
                    self.level2_button.config(state="normal")  
                if self.current_level >= 2:
                    self.level3_button.config(state="normal")  
                self.quit_game()
            else:
                messagebox.showerror("Incorrecto", "La matriz no está en forma escalonada reducida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def quit_game(self):
        """Regresa al menú principal sin perder el progreso."""
        self.matriz = None  
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.game_frame.pack_forget()
        self.start_frame.pack()

    def digitar_matriz(self):
        """Allow the user to manually input the matrix."""
        try:
            matriz_texto = simpledialog.askstring(
                "Digitar matriz",
                f"Ingresa la matriz fila por fila, separando los elementos con espacios.\n"
                f"Ejemplo para una matriz {self.n}x{self.n}:\n1 2 3\n4 5 6\n7 8 9"
            )
            if not matriz_texto:
                raise ValueError("No se ingresó ninguna matriz.")
            
            filas = matriz_texto.strip().split("\n")
            if len(filas) != self.n:
                raise ValueError(f"Debes ingresar exactamente {self.n} filas.")
            
            matriz = []
            for fila in filas:
                elementos = fila.split()
                if len(elementos) != self.n:
                    raise ValueError(f"Cada fila debe tener exactamente {self.n} elementos.")
                matriz.append([Fraction(eval(x)) for x in elementos]) 
            
            self.matriz = np.array(matriz, dtype=object)
            self.actualizar_matriz()
            messagebox.showinfo("Matriz actualizada", "La matriz fue ingresada correctamente.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def digitar_matriz_transpuesta(self):
        """Allow the user to manually input the transposed matrix using entry widgets."""
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        tk.Label(self.game_frame, text="Ingresa la matriz transpuesta:", font=("Arial", 14)).pack(pady=10)

        
        matriz_texto = format_matrix(self.matriz)
        tk.Label(self.game_frame, text="Matriz Original:", font=("Arial", 12)).pack(pady=5)
        text_widget = tk.Text(self.game_frame, wrap="none", height=10, width=50)
        text_widget.insert("1.0", matriz_texto)
        text_widget.config(state="disabled")
        text_widget.pack(pady=5)

        
        self.entries = []  
        for i in range(self.n):
            row_entries = []
            row_frame = tk.Frame(self.game_frame)
            row_frame.pack()
            for j in range(self.n):
                entry = tk.Entry(row_frame, width=5, justify="center")
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

   
        tk.Button(self.game_frame, text="Guardar", command=self.guardar_matriz_transpuesta).pack(pady=5)
        tk.Button(self.game_frame, text="Terminar", command=self.verificar_transpuesta).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.salir_nivel).pack(pady=5)

    def guardar_matriz_transpuesta(self):
        """Save the manually entered transposed matrix."""
        try:
            matriz_transpuesta = []
            for i in range(self.n):
                row = []
                for j in range(self.n):
                    value = self.entries[i][j].get()
                    row.append(Fraction(eval(value))) 
                matriz_transpuesta.append(row)
            self.matriz_transpuesta = np.array(matriz_transpuesta, dtype=object)
            messagebox.showinfo("Matriz guardada", "La matriz transpuesta fue ingresada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def verificar_transpuesta(self):
        """Verifica si la matriz ingresada coincide con la transpuesta."""
        try:
            matriz_ingresada = self.obtener_matriz_ingresada()
            if np.array_equal(matriz_ingresada, self.matriz.T):
                messagebox.showinfo("¡Correcto!", "¡La matriz ingresada es la transpuesta correcta!")
                self.current_level = 2
                self.level3_button.config(state="normal")
                self.quit_game()
            else:
                messagebox.showerror("Incorrecto", "La matriz ingresada no es la transpuesta correcta.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def verificar_inversa(self):
        """Verifica si la matriz ingresada coincide con la inversa calculada."""
        try:
            
            matriz_ingresada = []
            for i in range(self.n):
                row = []
                for j in range(self.n):
                    value = self.entries[i][j].get()
                    row.append(Fraction(eval(value))) 
                matriz_ingresada.append(row)
            matriz_ingresada = np.array(matriz_ingresada, dtype=object)

            
            if not hasattr(self, 'inversa_correcta'):
                self.inversa_correcta = calcular_inversa(self.matriz)

           
            inversa_correcta_float = self.inversa_correcta.astype(float)
            matriz_ingresada_float = matriz_ingresada.astype(float)

          
            if np.allclose(matriz_ingresada_float, inversa_correcta_float, atol=1e-9):
                messagebox.showinfo("¡Correcto!", "¡La matriz ingresada es la inversa correcta!")
                self.current_level = 3
                self.quit_game()
            else:
                messagebox.showerror("Incorrecto", "La matriz ingresada no coincide con la inversa calculada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def obtener_matriz_ingresada(self):
        """Obtiene la matriz ingresada por el usuario desde los campos de entrada."""
        matriz_ingresada = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                value = self.entries[i][j].get()
                row.append(Fraction(eval(value)))
            matriz_ingresada.append(row)
        return np.array(matriz_ingresada, dtype=object)

    def calcular_resultado(self):
        """Calcula y muestra el resultado de la matriz inversa."""
        try:
            resultado = calcular_resultado(self.matriz, self.determinante)
            matriz_texto = format_matrix(resultado)
            messagebox.showinfo("Resultado", f"Matriz escalada:\n{matriz_texto}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def salir_nivel(self):
        """Reset the matrix and return to the main menu."""
        self.matriz = None
        self.quit_game()

    def reset_to_level_1(self):
        """Reset the game to level 1 and disable higher levels."""
        self.current_level = 0
        self.level2_button.config(state="disabled")
        self.level3_button.config(state="disabled")
        self.salir_nivel()
