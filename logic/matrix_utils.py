from fractions import Fraction
import numpy as np

def format_matrix(A):
    if A is None:
        return "Matriz no disponible."
    return "\n".join(
        ["  ".join(f"{Fraction(x).limit_denominator()}" if x != "|" else "|" for x in fila) for fila in A]
    )

def es_escalonada_reducida(matriz):
    """Verifica si la matriz está en forma escalonada reducida."""
    filas, columnas = matriz.shape
    for i in range(filas):
        if not np.isclose(matriz[i, i], 1):
            return False
        for j in range(filas):
            if j != i and not np.isclose(matriz[j, i], 0):
                return False
    return True
