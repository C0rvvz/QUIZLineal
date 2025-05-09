import numpy as np
from fractions import Fraction

def generar_matriz(n):
    return np.random.randint(-10, 10, (n, n))

def realizar_operacion(A, tipo, fila1, fila2=None, factor=1, B=None):
    A = A.astype(object)
    if B is not None:
        B = B.astype(object)
    if tipo == "intercambio":
        A[[fila1, fila2]] = A[[fila2, fila1]]
        if B is not None:
            B[[fila1, fila2]] = B[[fila2, fila1]]
    elif tipo == "multiplicacion":
        A[fila1] = [Fraction(x) * Fraction(factor) for x in A[fila1]]
        if B is not None:
            B[fila1] = [Fraction(x) * Fraction(factor) for x in B[fila1]]
    elif tipo == "suma":
        A[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y) for x, y in zip(A[fila1], A[fila2])]
        if B is not None:
            B[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y) for x, y in zip(B[fila1], B[fila2])]
    return A, B

def es_transpuesta_correcta(matriz, matriz_transpuesta):
    try:
        return np.array_equal(matriz_transpuesta, matriz.T)
    except Exception as e:
        raise ValueError(f"Error al verificar la transpuesta: {e}")

def verificar_transpuesta(matriz, entries):
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

def calcular_determinante(matriz):
    filas, columnas = matriz.shape
    if filas != columnas:
        raise ValueError("La matriz debe ser cuadrada para calcular su determinante.")

    if filas == 2:
        return matriz[0, 0] * matriz[1, 1] - matriz[0, 1] * matriz[1, 0]

    return np.linalg.det(matriz.astype(float))

def calcular_adjunta(matriz):
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
    filas, columnas = matriz.shape
    if filas != columnas:
        raise ValueError("La matriz debe ser cuadrada para calcular su inversa.")

    determinante = calcular_determinante(matriz)
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

        inversa = np.array([[Fraction(float(x)).limit_denominator() for x in fila] for fila in inversa_float], dtype=object)
        return inversa
    except np.linalg.LinAlgError:
        return None

def calcular_resultado(matriz, determinante):
    if determinante == 0:
        raise ValueError("El determinante es 0, la matriz no tiene inversa.")
    traspuesta = matriz.T
    return traspuesta / determinante

def verificar_inversa(matriz, matriz_ingresada):
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
