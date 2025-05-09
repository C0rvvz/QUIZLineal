from fractions import Fraction
import numpy as np

def format_matrix(A):
    # Formatea matriz para mostrar
    if A is None:
        return "Matriz no disponible."
    return "\n".join(
        ["  ".join(f"{Fraction(x).limit_denominator()}" if x != "|" else "|" for x in fila) for fila in A]
    )

def es_escalonada_reducida(matriz):
    # Verifica si la matriz está en forma escalonada reducida
    filas, columnas = matriz.shape

    ultimo_pivote_col = -1

    for i in range(filas):
        # Busca primer elemento no cero
        pivote_col = None
        for j in range(columnas):
            if not np.isclose(matriz[i, j], 0):
                pivote_col = j
                break

        # Fila de ceros
        if pivote_col is None:
            continue

        # Pivote a la derecha del anterior
        if pivote_col <= ultimo_pivote_col:
            return False

        # Pivote debe ser 1
        if not np.isclose(matriz[i, pivote_col], 1):
            return False

        # Único no-cero en columna
        for k in range(filas):
            if k != i and not np.isclose(matriz[k, pivote_col], 0):
                return False

        ultimo_pivote_col = pivote_col

    return True
