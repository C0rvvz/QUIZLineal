import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import tkinter as tk
from tkinter import messagebox, simpledialog
from logic.operations import crear_matriz_aleatoria, aplicar_operacion_elemental, evaluar_entrada_transpuesta, verificar_producto_es_identidad
from logic.matrix_utils import formatear_matriz_para_mostrar, verificar_forma_escalonada_reducida
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

        self.level1_button = tk.Button(self.start_frame, text="Nivel 1: Transpuesta", command=self.start_transpose)
        self.level1_button.pack(pady=5)

        self.level2_button = tk.Button(self.start_frame, text="Nivel 2: Gauss Jordan", command=self.start_gauss, state="disabled")
        self.level2_button.pack(pady=5)

        self.level3_button = tk.Button(self.start_frame, text="Nivel 3: Inversa", command=self.start_inverse, state="disabled")
        self.level3_button.pack(pady=5)

        self.game_frame = tk.Frame(root)

    def start_gauss(self):
        # Inicia nivel Gauss Jordan
        if self.current_level < 1:
            messagebox.showerror("Error", "Debes completar el Nivel 1 (Transpuesta) antes de avanzar al Nivel 2.")
            return
        self.n = self.ask_matrix_size()
        if self.n is None:
            return
        self.matriz = crear_matriz_aleatoria(self.n)  
        # Crear una matriz aleatoria de 2x1 en lugar de la matriz identidad
        self.identidad = np.random.randint(-10, 10, (self.n, 1)).astype(object)
    
        self.start_frame.pack_forget()
        self.show_game_screen("Gauss Jordan")
    
    def show_completed_level_1(self):
        # Muestra matriz completada nivel 1
        if self.matriz is None:
            tk.messagebox.showerror("Error", "La matriz no está definida.")
            return
    
    
        for widget in self.root.winfo_children():
            widget.destroy()
    
    
        matriz_texto = formatear_matriz_para_mostrar(self.matriz)
        text_widget = tk.Text(self.root, wrap="none", height=10, width=50)
        text_widget.insert("1.0", matriz_texto)
        text_widget.config(state="disabled")
        text_widget.pack()
    
    
        tk.Button(self.root, text="Continuar al Nivel 2 (Gauss Jordan)", command=self.next_level).pack()
        tk.Button(self.root, text="Salir", command=self.quit_game).pack()
    
    def next_level(self):
        # Avanza al siguiente nivel
        tk.messagebox.showinfo("Nivel 2", "Aquí comienza el nivel 2.")
        self.start_gauss()
    
    def start_transpose(self):
        """Start the Transpose level (Level 1)."""
        self.n = self.ask_matrix_size()
        if self.n is None:
            return
        self.matriz = crear_matriz_aleatoria(self.n) 
        self.start_frame.pack_forget()
        self.show_game_screen("Transpuesta")

    def start_inverse(self):
        # Inicia nivel de inversa
        if self.current_level < 2:
            messagebox.showerror("Error", "Debes completar el Nivel 2 (Gauss Jordan) antes de avanzar al Nivel 3.")
            return

        self.n = self.ask_matrix_size()
        if self.n is None:
            return

        # Crea matriz identidad y guarda matriz original

        self.identidad = np.eye(self.n, dtype=object)
        self.matriz = crear_matriz_aleatoria(self.n)
        # Asegúrate de que self.matriz no sea None antes de copiar
        if self.matriz is None:
            self.msg_label = tk.Label(self.frame, text="Error: No se pudo crear la matriz.", fg="red")
            self.msg_label.grid(row=0, column=0)
            return
        self.matriz_original = self.matriz.copy()

        self.start_frame.pack_forget()
        self.show_game_screen("Inversa")

    def ask_matrix_size(self):
        # Solicita tamaño de matriz
        try:
            n = int(simpledialog.askstring("Tamaño de la matriz", "Ingresa el tamaño de la matriz cuadrada (2-5):"))
            if n < 2 or n > 5:
                raise ValueError
            return n
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Por favor, ingresa un número válido entre 2 y 5.")
            return None

    def show_game_screen(self, level, disable_controls=False):
        # Muestra pantalla de juego
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.game_frame.pack()
        tk.Label(self.game_frame, text=f"Nivel: {level}", font=("Arial", 14)).pack(pady=10)

        if level == "Transpuesta":

            matriz_texto = formatear_matriz_para_mostrar(self.matriz)
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
            separador = np.array([["|"] for _ in range(self.n)], dtype=object)
            matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  
            matriz_texto = formatear_matriz_para_mostrar(matriz_combinada)
            self.matriz_label = tk.Label(self.game_frame, text=f"Matriz:\n{matriz_texto}", font=("Courier", 12))
            self.matriz_label.pack(pady=5)
            self.add_inverse_controls(disable_controls)
        
        elif level == "Gauss Jordan":
            separador = np.array([["|"] for _ in range(self.n)], dtype=object)
            # La identidad ahora tiene solo una columna
            matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  
            matriz_texto = formatear_matriz_para_mostrar(matriz_combinada)
            self.matriz_label = tk.Label(self.game_frame, text=f"Matriz:\n{matriz_texto}", font=("Courier", 12))
            self.matriz_label.pack(pady=5)
            self.add_gauss_controls(disable_controls)

    def mostrar_resultado_transpuesta(self):
        # Muestra matriz transpuesta
        try:
            transpuesta = self.matriz.T
            matriz_texto = formatear_matriz_para_mostrar(transpuesta)
            messagebox.showinfo("Resultado", f"Matriz transpuesta:\n{matriz_texto}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def mostrar_resultado_inversa(self):
        # Muestra matriz inversa
        try:
            self.inversa_correcta = obtener_matriz_inversa(self.matriz)  
            if self.inversa_correcta is None:
                messagebox.showerror("Error", "La matriz no tiene inversa.")
                return
            matriz_texto = formatear_matriz_para_mostrar(self.inversa_correcta)
            messagebox.showinfo("Resultado", f"Matriz inversa:\n{matriz_texto}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def add_gauss_controls(self, disable_controls=False):
        # Agrega controles nivel Gauss
        if not disable_controls:
            tk.Button(self.game_frame, text="Intercambiar filas", command=self.intercambiar_filas).pack(pady=5)
            tk.Button(self.game_frame, text="Multiplicar fila por un escalar", command=self.multiplicar_fila).pack(pady=5)
            tk.Button(self.game_frame, text="Sumar múltiplo de una fila a otra", command=self.sumar_filas).pack(pady=5)
            tk.Button(self.game_frame, text="Terminar", command=self.terminar_nivel).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.quit_game).pack(pady=5)

    def add_transpose_controls(self):
        # Agrega controles nivel Transpuesta
        tk.Button(self.game_frame, text="Digitar matriz", command=self.digitar_matriz_transpuesta).pack(pady=5)
        tk.Button(self.game_frame, text="Terminar", command=self.verificar_transpuesta).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.salir_nivel).pack(pady=5)

    def add_inverse_controls(self, disable_controls=False):
        if not disable_controls:
            tk.Button(self.game_frame, text="Intercambiar filas", command=self.intercambiar_filas_inversa).pack(pady=5)
            tk.Button(self.game_frame, text="Multiplicar fila por un escalar", command=self.multiplicar_fila_inversa).pack(pady=5)
            tk.Button(self.game_frame, text="Sumar múltiplo de una fila a otra", command=self.sumar_filas_inversa).pack(pady=5)
            tk.Button(self.game_frame, text="Terminar", command=self.terminar_nivel_inversa).pack(pady=5)
        tk.Button(self.game_frame, text="Salir", command=self.quit_game).pack(pady=5)

    def intercambiar_filas(self):
        try:
            entrada = simpledialog.askstring("Intercambiar filas", "Ingresa las filas a intercambiar (ej: 1 2):")
            if not entrada:
                raise ValueError("No se ingresó ninguna entrada.")
                
            # Validar el formato de entrada
            partes = entrada.split()
            if len(partes) != 2:
                raise ValueError("Debes ingresar exactamente dos números separados por un espacio.")
                
            try:
                f1, f2 = map(int, partes)
            except ValueError:
                raise ValueError("Debes ingresar números enteros válidos.")
                
            # Validar rango de filas
            if f1 < 1 or f1 > self.n or f2 < 1 or f2 > self.n:
                raise ValueError(f"Los índices de fila deben estar entre 1 y {self.n}.")
                
            f1, f2 = f1 - 1, f2 - 1  
            # Solo intercambiar las filas en la matriz principal
            self.matriz, _ = aplicar_operacion_elemental(self.matriz, "intercambio", f1, f2)
            # Generar nuevos valores aleatorios para la matriz derecha
            self.identidad = np.random.randint(-10, 10, (self.n, 1)).astype(object)
            self.actualizar_matriz()
            messagebox.showinfo("Operación realizada", f"Se intercambiaron las filas {f1 + 1} y {f2 + 1}.")
        except ValueError as ve:
            messagebox.showerror("Error", f"{ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
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
            # Solo aplicar la operación a la matriz principal
            self.matriz, _ = aplicar_operacion_elemental(self.matriz, "multiplicacion", f1, factor=factor)
            # Generar nuevos valores aleatorios para la matriz derecha
            self.identidad = np.random.randint(-10, 10, (self.n, 1)).astype(object)
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
        # Suma múltiplo de fila a otra
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
    
            # Solo aplicar la operación a la matriz principal
            self.matriz, _ = aplicar_operacion_elemental(self.matriz, "suma", f2, f1, factor)

            # Generar nuevos valores aleatorios para la matriz derecha
            self.identidad = np.random.randint(-10, 10, (self.n, 1)).astype(object)

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
        # Actualiza visualización de matriz
        separador = np.array([["|"] for _ in range(self.n)], dtype=object)
        matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  
        matriz_texto = formatear_matriz_para_mostrar(matriz_combinada)
        self.matriz_label.config(text=f"Matriz y Resultante\n{matriz_texto}")

    def terminar_nivel(self):
        # Valida matriz y finaliza nivel
        try:
            if verificar_forma_escalonada_reducida(self.matriz):
                messagebox.showinfo("¡Correcto!", "¡Has completado el nivel correctamente!")
                self.current_level = 2  
                self.level3_button.config(state="normal")  
                self.quit_game()
            else:
                messagebox.showerror("Incorrecto", "La matriz no está en forma escalonada reducida.")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def quit_game(self):
        # Vuelve al menú principal
        self.matriz = None  
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        self.game_frame.pack_forget()
        self.start_frame.pack()

    def digitar_matriz(self):
        # Permite ingresar matriz manualmente
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


        matriz_texto = formatear_matriz_para_mostrar(self.matriz)
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
        try:
            matriz_transpuesta = []
            for i in range(self.n):
                row = []
                for j in range(self.n):
                    value = self.entries[i][j].get()
                    if not value.strip():  # Verifica si está vacío
                        raise ValueError(f"El campo en fila {i+1}, columna {j+1} está vacío.")
                    try:
                        # Intenta convertir el valor a fracción
                        row.append(Fraction(eval(value)))
                    except Exception:
                        raise ValueError(f"Valor inválido en fila {i+1}, columna {j+1}: '{value}'")
                matriz_transpuesta.append(row)
            self.matriz_transpuesta = np.array(matriz_transpuesta, dtype=object)
            messagebox.showinfo("Matriz guardada", "La matriz transpuesta fue ingresada correctamente.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def verificar_transpuesta(self):
        """Verifica si la matriz ingresada coincide con la transpuesta."""
        try:
            exito, mensaje = evaluar_entrada_transpuesta(self.matriz, self.entries)
            if exito:
                messagebox.showinfo("¡Correcto!", mensaje)
                self.current_level = 1
                self.level2_button.config(state="normal")
                self.quit_game()
            else:
                messagebox.showerror("Incorrecto", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def intercambiar_filas_inversa(self):
        # Intercambia filas en nivel inversa
        try:
            entrada = simpledialog.askstring("Intercambiar filas", "Ingresa las filas a intercambiar (ej: 1 2):")
            if not entrada:
                raise ValueError("No se ingresó ninguna entrada.")
            f1, f2 = map(int, entrada.split())
            f1, f2 = f1 - 1, f2 - 1  
            self.matriz, self.identidad = aplicar_operacion_elemental(self.matriz, "intercambio", f1, f2, B=self.identidad)
            self.actualizar_matriz_inversa()
            messagebox.showinfo("Operación realizada", f"Se intercambiaron las filas {f1 + 1} y {f2 + 1}.")
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
    
    def multiplicar_fila_inversa(self):
        # Multiplica fila por escalar en nivel inversa
        try:
            entrada = simpledialog.askstring("Multiplicar fila", "Ingresa la fila y el factor de multiplicación (ej: 1 1/2):")
            if not entrada:
                raise ValueError("No se ingresó ninguna entrada.")
            f1, factor = entrada.split()
            f1 = int(f1) - 1  
            factor = float(eval(factor))  
            if f1 < 0 or f1 >= self.n:
                raise IndexError("El índice de la fila está fuera del rango de la matriz.")
            self.matriz, self.identidad = aplicar_operacion_elemental(self.matriz, "multiplicacion", f1, factor=factor, B=self.identidad)
            self.actualizar_matriz_inversa()
            factor_formateado = Fraction(factor).limit_denominator() if factor != int(factor) else factor
            messagebox.showinfo("Operación realizada", f"La fila {f1 + 1} fue multiplicada por {factor_formateado}.")
        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida: {ve}")
        except IndexError as ie:
            messagebox.showerror("Error", f"Índice fuera de rango: {ie}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")
    
    def sumar_filas_inversa(self):
        # Suma múltiplo de fila a otra en nivel inversa
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
    
            self.matriz, self.identidad = aplicar_operacion_elemental(self.matriz, "suma", f2, f1, factor, B=self.identidad)
            self.actualizar_matriz_inversa()
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

    def actualizar_matriz_inversa(self):
        # Actualiza visualización de matriz inversa
        separador = np.array([["|"] for _ in range(self.n)], dtype=object)
        matriz_combinada = np.hstack((self.matriz, separador, self.identidad))  
        matriz_texto = formatear_matriz_para_mostrar(matriz_combinada)
        self.matriz_label.config(text=f"Matriz y Identidad\n{matriz_texto}")

    def terminar_nivel_inversa(self):
        # Verifica matriz inversa y finaliza nivel
        try:
            # Verificamos tamaño de matriz
            if self.matriz.shape[0] != self.n or self.matriz.shape[1] != self.n:
                messagebox.showerror("Error", f"La matriz no tiene el tamaño correcto ({self.n}x{self.n}).")
                return
                
            # Primero, verificamos si la matriz izquierda es la identidad
            identidad_esperada = np.eye(self.n, dtype=float)
            matriz_float = self.matriz.astype(float)
    
            if not np.allclose(matriz_float, identidad_esperada, atol=1e-9):
                messagebox.showerror("Incorrecto", "La matriz izquierda debe ser la matriz identidad.")
                return
    
            # Ahora verificamos si la matriz derecha es la inversa de la matriz original
            matriz_original_float = self.matriz_original.astype(float)
            identidad_float = self.identidad.astype(float)
    
            # Verificamos que la matriz de identidad tenga dimensiones adecuadas
            if identidad_float.shape[0] != self.n:
                messagebox.showerror("Error", "La matriz de transformación no tiene las dimensiones correctas.")
                return
    
            # Verificar si A * B = I (la matriz original multiplicada por la calculada es identidad)
            try:
                producto = np.dot(matriz_original_float, identidad_float)
                
                if np.allclose(producto, identidad_esperada, atol=1e-9):
                    messagebox.showinfo("¡Correcto!", "¡Has calculado correctamente la matriz inversa!")
                    self.current_level = 3
                    self.quit_game()
                else:
                    messagebox.showerror("Incorrecto", "La matriz derecha no es la inversa de la matriz original.")
            except ValueError:
                messagebox.showerror("Error", "No se puede realizar el producto matricial. Verifica las dimensiones.")
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
                    if not value.strip():  # Verifica si el campo está vacío
                        raise ValueError("Todos los campos deben estar completos")
                    row.append(Fraction(eval(value)))
                matriz_ingresada.append(row)
            matriz_ingresada = np.array(matriz_ingresada, dtype=object)
            
            # Verificar directamente si es la inversa correcta usando la función especializada
            exito, mensaje = verificar_producto_es_identidad(self.matriz, matriz_ingresada)
            
            if exito:
                messagebox.showinfo("¡Correcto!", mensaje)
                self.current_level = 3
                self.quit_game()
            else:
                messagebox.showerror("Incorrecto", mensaje)
        except ValueError as ve:
            messagebox.showerror("Error", f"Entrada inválida: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")

    def obtener_matriz_ingresada(self):
        """Obtiene la matriz ingresada por el usuario desde los campos de entrada."""
        matriz_ingresada = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                value = self.entries[i][j].get()
                if not value.strip():  # Verifica si está vacío
                    raise ValueError(f"El campo en fila {i+1}, columna {j+1} está vacío.")
                try:
                    # Intenta convertir el valor a fracción
                    row.append(Fraction(eval(value)))
                except Exception:
                    raise ValueError(f"Valor inválido en fila {i+1}, columna {j+1}: '{value}'")
            matriz_ingresada.append(row)
        return np.array(matriz_ingresada, dtype=object)

    def calcular_resultado(self):
        # Calcula y muestra el resultado de la matriz inversa
        try:
            resultado = calcular_matriz_escalada(self.matriz, self.determinante)
            matriz_texto = formatear_matriz_para_mostrar(resultado)
            messagebox.showinfo("Resultado", f"Matriz escalada:\n{matriz_texto}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error: {e}")
    
    def salir_nivel(self):
        # Sale del nivel actual
        self.matriz = None
        self.quit_game()

    def reset_to_level_1(self):
        # Reinicia al nivel 1
        self.current_level = 0
        self.level2_button.config(state="disabled")
        self.level3_button.config(state="disabled")
        self.salir_nivel()
