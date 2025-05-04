import numpy as np
from fractions import Fraction

def generar_matriz(n):
    """Genera una matriz cuadrada aleatoria de tamaño n x n."""
    return np.random.randint(-10, 10, (n, n))

def realizar_operacion(A, tipo, fila1, fila2=None, factor=1, B=None):
    """
    Aplica una operación de fila sobre la matriz usando fracciones.
    Esto es parte del método de Gauss-Jordan para reducir matrices.

    :param A: Matriz principal (numpy array).
    :param tipo: Tipo de operación ("intercambio", "multiplicacion", "suma").
    :param fila1: Índice de la primera fila involucrada.
    :param fila2: Índice de la segunda fila (solo para "intercambio" o "suma").
    :param factor: Escalar usado en "multiplicacion" o "suma".
    :param B: Matriz adicional para operaciones simultáneas.
    :return: Las matrices A y B modificadas.
    """
    A = A.astype(object)
    if B is not None:
        B = B.astype(object)
    if tipo == "intercambio":
        # Intercambia las filas fila1 y fila2.
        A[[fila1, fila2]] = A[[fila2, fila1]]
        if B is not None:
            B[[fila1, fila2]] = B[[fila2, fila1]]
    elif tipo == "multiplicacion":
        # Multiplica todos los elementos de fila1 por un factor.
        A[fila1] = [Fraction(x) * Fraction(factor) for x in A[fila1]]
        if B is not None:
            B[fila1] = [Fraction(x) * Fraction(factor) for x in B[fila1]]
    elif tipo == "suma":
        # Suma fila2 escalada por un factor a fila1.
        A[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y) for x, y in zip(A[fila1], A[fila2])]
        if B is not None:
            B[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y) for x, y in zip(B[fila1], B[fila2])]
    return A, B

def es_transpuesta_correcta(matriz, matriz_transpuesta):
    """
    Verifica si la matriz_transpuesta es la transpuesta correcta de la matriz original.

    :param matriz: Matriz original (numpy array).
    :param matriz_transpuesta: Matriz ingresada como transpuesta (numpy array).
    :return: True si es la transpuesta correcta, False en caso contrario.
    """
    try:
        return np.array_equal(matriz_transpuesta, matriz.T)
    except Exception as e:
        raise ValueError(f"Error al verificar la transpuesta: {e}")

def verificar_transpuesta(matriz, entries):
    """
    Verifica si la matriz ingresada por el usuario es la transpuesta correcta.
    La transpuesta se obtiene intercambiando filas por columnas.

    :param matriz: Matriz original (numpy array).
    :param entries: Lista de listas de widgets Entry con los valores ingresados por el usuario.
    :return: (bool, str) Una tupla con un booleano indicando si es correcta y un mensaje.
    """
    try:
        # Convertimos los valores ingresados por el usuario en una matriz.
        matriz_transpuesta = []
        for i in range(len(entries)):
            row = []
            for j in range(len(entries[i])):
                value = entries[i][j].get()  # Obtenemos el valor del widget Entry.
                row.append(Fraction(eval(value)))  # Convertimos a fracción.
            matriz_transpuesta.append(row)
        matriz_transpuesta = np.array(matriz_transpuesta, dtype=object)

        # Comparamos la matriz ingresada con la transpuesta real.
        if np.array_equal(matriz_transpuesta, matriz.T):
            return True, "¡Has completado el nivel correctamente!"
        else:
            return False, "La matriz ingresada no es la transpuesta correcta."
    except Exception as e:
        return False, f"Error al verificar la transpuesta: {e}"

def calcular_determinante(matriz):
    """
    Calcula el determinante de una matriz cuadrada 2x2.
    :param matriz: Matriz cuadrada (numpy array).
    :return: Determinante de la matriz.
    """
    n = matriz.shape[0]
    if n == 2:
        return matriz[0, 0] * matriz[1, 1] - matriz[0, 1] * matriz[1, 0]
    
def calcular_adjunta(matriz):
    """
    Calcula la matriz adjunta de una matriz cuadrada.
    :param matriz: Matriz cuadrada (numpy array).
    :return: Matriz adjunta (numpy array).
    """
    cofactores = np.zeros_like(matriz, dtype=object)
    n = matriz.shape[0]
    for i in range(n):
        for j in range(n):
            submatriz = np.delete(np.delete(matriz, i, axis=0), j, axis=1)
            determinante_submatriz = calcular_determinante(submatriz)
            signo = (-1) ** (i + j)
            cofactores[i, j] = signo * determinante_submatriz
    return cofactores.T

def calcular_inversa(matriz):
    """
    Calcula la inversa de una matriz cuadrada de 2x2.
    La inversa se calcula como la transpuesta de la matriz de cofactores dividida por el determinante.

    :param matriz: Matriz cuadrada (numpy array).
    :return: Matriz inversa (numpy array) o None si no tiene inversa.
    """
    determinante = calcular_determinante(matriz)  # Calcula el determinante.
    if determinante == 0:
        return None  # Si el determinante es 0, la matriz no tiene inversa.

    # Calculamos la transpuesta manualmente.
    transpuesta = []
    for i in range(matriz.shape[1]):  # Iteramos por columnas.
        row = []
        for j in range(matriz.shape[0]):  # Iteramos por filas.
            value = matriz[j, i]  # Intercambiamos filas y columnas.
            row.append(Fraction(value))  # Usamos fracciones para precisión.
        transpuesta.append(row)
    transpuesta = np.array(transpuesta, dtype=object)

    # Dividimos cada elemento de la transpuesta por el determinante.
    inversa = transpuesta / Fraction(determinante)
    return inversa

def calcular_resultado(matriz, determinante):
    """
    Calcula el resultado de la matriz inversa: (1/determinante) * Transpuesta.
    :param matriz: Matriz original (numpy array).
    :param determinante: Determinante de la matriz original.
    :return: Matriz escalada (numpy array).
    """
    if determinante == 0:
        raise ValueError("El determinante es 0, la matriz no tiene inversa.")
    traspuesta = matriz.T
    return traspuesta / determinante

def verificar_inversa(matriz, matriz_ingresada):
    """
    Verifica si la matriz ingresada es la inversa correcta de la matriz original.
    :param matriz: Matriz original (numpy array).
    :param matriz_ingresada: Matriz ingresada por el usuario (numpy array).
    :return: (bool, str) Una tupla con un booleano indicando si es correcta y un mensaje.
    """
    try:
        matriz_float = np.array(matriz, dtype=float)
        matriz_ingresada_float = np.array(matriz_ingresada, dtype=float)

        identidad = np.eye(matriz.shape[0], dtype=float)

        producto = np.dot(matriz_float, matriz_ingresada_float)

        if np.allclose(producto, identidad, atol=1e-9):
            return True, "¡La matriz ingresada es la inversa correcta!"
        else:
            return False, "La matriz ingresada no es la inversa correcta."
    except Exception as e:
        return False, f"Error al verificar la inversa: {e}"
