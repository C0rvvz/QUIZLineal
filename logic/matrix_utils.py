from fractions import Fraction
import numpy as np

def format_matrix(A):
    if A is None:
        return "Matriz no disponible."
    return "\n".join(
        ["  ".join(f"{Fraction(x).limit_denominator()}" if x != "|" else "|" for x in fila) for fila in A]
    )

def es_escalonada_reducida(matriz):
    filas, columnas = matriz.shape

    ultimo_pivote_col = -1

    for i in range(filas):
        pivote_col = None
        for j in range(columnas):
            if not np.isclose(matriz[i, j], 0):
                pivote_col = j
                break

        if pivote_col is None:
            continue

        if pivote_col <= ultimo_pivote_col:
            return False

        if not np.isclose(matriz[i, pivote_col], 1):
            return False

        for k in range(filas):
            if k != i and not np.isclose(matriz[k, pivote_col], 0):
                return False

        ultimo_pivote_col = pivote_col

    return True
