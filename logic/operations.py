import numpy as np
from fractions import Fraction


# NIVEL 1: FUNCIONES PARA TRANSPUESTA

def crear_matriz_aleatoria(n):
    # Genera matriz aleatoria nxn
    return np.random.randint(-10, 10, (n, n))


def comparar_con_transpuesta(matriz, matriz_transpuesta):
    # Verifica si una matriz es la transpuesta correcta de otra
    try:
        return np.array_equal(matriz_transpuesta, matriz.T)
    except Exception as e:
        raise ValueError(f"Error al verificar la transpuesta: {e}")


def evaluar_entrada_transpuesta(matriz, entries):
    # Evalúa si la matriz ingresada por el usuario es la transpuesta correcta
    try:
        matriz_transpuesta = []
        for i in range(len(entries)):
            row = []
            for j in range(len(entries[i])):
                value = entries[i][j].get()
                row.append(Fraction(eval(value)))
            matriz_transpuesta.append(row)
        matriz_transpuesta = np.array(matriz_transpuesta, dtype=object)

        if np.array_equal(matriz_transpuesta, matriz.T):
            return True, "¡Has completado el nivel correctamente!"
        else:
            return False, "La matriz ingresada no es la transpuesta correcta."
    except Exception as e:
        return False, f"Error al verificar la transpuesta: {e}"


# NIVEL 2: FUNCIONES PARA GAUSS-JORDAN

def aplicar_operacion_elemental(A, tipo, fila1, fila2=None, factor=1, B=None):
    # Realiza operaciones elementales de fila en matrices
    A = A.astype(object)
    if B is not None:
        B = B.astype(object)
    if tipo == "intercambio":
        # Intercambia filas
        A[[fila1, fila2]] = A[[fila2, fila1]]
        if B is not None:
            B[[fila1, fila2]] = B[[fila2, fila1]]
    elif tipo == "multiplicacion":
        # Multiplica fila por escalar
        A[fila1] = [Fraction(x) * Fraction(factor) for x in A[fila1]]
        if B is not None:
            B[fila1] = [Fraction(x) * Fraction(factor) for x in B[fila1]]
    elif tipo == "suma":
        # Suma múltiplo de una fila a otra
        A[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y) for x, y in zip(A[fila1], A[fila2])]
        if B is not None:
            B[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y) for x, y in zip(B[fila1], B[fila2])]
    return A, B


# NIVEL 3: FUNCIONES PARA MATRIZ INVERSA

def obtener_submatriz(matriz, fila, columna):
    """
    Obtiene la submatriz que resulta de eliminar una fila y una columna específicas.
    """
    # Copiamos la matriz para no modificar la original
    submatriz = matriz.copy()
    # Eliminamos la fila y columna indicadas
    submatriz = np.delete(submatriz, fila, axis=0)
    submatriz = np.delete(submatriz, columna, axis=1)
    return submatriz


def determinante_cofactores(matriz):
    """
    Calcula el determinante de una matriz usando el método de expansión por cofactores.
    """
    n = matriz.shape[0]

    # Caso base: matriz 1x1
    if n == 1:
        return matriz[0, 0]

    # Caso base: matriz 2x2
    if n == 2:
        return matriz[0, 0] * matriz[1, 1] - matriz[0, 1] * matriz[1, 0]

    determinante = 0
    # Expandimos por la primera fila
    for j in range(n):
        # Calculamos el cofactor: (-1)^(i+j) * determinante de la submatriz
        cofactor = (-1) ** j * matriz[0, j] * determinante_cofactores(obtener_submatriz(matriz, 0, j))
        determinante += cofactor

    return determinante


def obtener_determinante(matriz):
    # Calcula el determinante de una matriz
    filas, columnas = matriz.shape
    if filas != columnas:
        raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")

    if filas == 2:
        return matriz[0, 0] * matriz[1, 1] - matriz[0, 1] * matriz[1, 0]
    elif filas == 3:
        # Implementación manual para matrices 3x3 usando la regla de Sarrus
        a, b, c = matriz[0, 0], matriz[0, 1], matriz[0, 2]
        d, e, f = matriz[1, 0], matriz[1, 1], matriz[1, 2]
        g, h, i = matriz[2, 0], matriz[2, 1], matriz[2, 2]

        # Diagonal principal y sus paralelas
        diag1 = a * e * i
        diag2 = b * f * g
        diag3 = c * d * h

        # Diagonal secundaria y sus paralelas
        diag4 = c * e * g
        diag5 = a * f * h
        diag6 = b * d * i

        # Determinante = suma de productos de diagonales principales - suma de productos de diagonales secundarias
        return diag1 + diag2 + diag3 - diag4 - diag5 - diag6
    elif filas == 4:
        # Para matrices 4x4, usamos el método de expansión por cofactores
        return determinante_cofactores(matriz)

    # Para matrices de tamaño mayor a 4x4, usamos la función de NumPy por eficiencia
    return np.linalg.det(matriz.astype(float))


def obtener_matriz_inversa(matriz):
    # Calcula la matriz inversa
    filas, columnas = matriz.shape

    determinante = obtener_determinante(matriz)
    if determinante == 0:
        return None

    if filas == 2:
        a, b = matriz[0, 0], matriz[0, 1]
        c, d = matriz[1, 0], matriz[1, 1]

        inversa = np.array([
            [Fraction(d), Fraction(-b)],
            [Fraction(-c), Fraction(a)]
        ], dtype=object)

        inversa = inversa / Fraction(determinante)
        return inversa

    try:
        matriz_float = matriz.astype(float)
        inversa_float = np.linalg.inv(matriz_float)

        inversa = np.array([[Fraction(float(x)).limit_denominator() for x in fila] for fila in inversa_float],
                           dtype=object)
        return inversa
    except np.linalg.LinAlgError:
        return None


def calcular_matriz_escalada(matriz, determinante):
    # Calcula matriz escalada (utilizada para inversa)
    if determinante == 0:
        raise ValueError("El determinante es 0, la matriz no tiene inversa.")
    traspuesta = matriz.T
    return traspuesta / determinante


def verificar_producto_es_identidad(matriz_original, matriz_inversa):
    # Verifica si el producto de dos matrices es la identidad (comprueba inversa)
    try:
        matriz_float = np.array(matriz_original, dtype=float)
        matriz_inversa_float = np.array(matriz_inversa, dtype=float)

        identidad = np.eye(matriz_original.shape[0], dtype=float)

        producto = np.dot(matriz_float, matriz_inversa_float)

        if np.allclose(producto, identidad, atol=1e-9):
            return True, "¡La matriz ingresada es la inversa correcta!"
        else:
            return False, "La matriz ingresada no es la inversa correcta."
    except Exception as e:
        return False, f"Error al verificar la inversa: {e}"