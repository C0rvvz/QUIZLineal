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


# NIVEL 3: SOLO FUNCIONES RELEVANTES PARA INVERSA POR OPERACIONES ELEMENTALES

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