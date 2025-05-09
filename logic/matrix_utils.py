from fractions import Fraction
import numpy as np

def format_matrix(A):
    if A is None:
        return "Matriz no disponible."
    return "\n".join(
        ["  ".join(f"{Fraction(x).limit_denominator()}" if x != "|" else "|" for x in fila) for fila in A]
    )

def es_escalonada_reducida(matriz):
    """Verifica si la matriz está en forma escalonada reducida.

    Esta función verifica si una matriz está en forma escalonada reducida (RREF),
    lo que significa que:
    1. El primer elemento no nulo de cada fila es 1 (pivote)
    2. Cada pivote está a la derecha del pivote de la fila anterior
    3. Cada pivote es el único elemento no nulo en su columna
    4. Todas las filas con solo ceros están al final de la matriz

    Args:
        matriz: Matriz numpy a verificar

    Returns:
        bool: True si la matriz está en forma escalonada reducida, False en caso contrario
    """
    filas, columnas = matriz.shape

    # Posición del último pivote encontrado
    ultimo_pivote_col = -1

    for i in range(filas):
        # Encuentra el primer elemento no nulo en la fila actual
        pivote_col = None
        for j in range(columnas):
            if not np.isclose(matriz[i, j], 0):
                pivote_col = j
                break

        # Si la fila es toda ceros, continuamos con la siguiente fila
        if pivote_col is None:
            continue

        # Verificar que el pivote esté a la derecha del pivote anterior
        if pivote_col <= ultimo_pivote_col:
            return False

        # Verificar que el pivote sea 1
        if not np.isclose(matriz[i, pivote_col], 1):
            return False

        # Verificar que el pivote sea el único elemento no nulo en su columna
        for k in range(filas):
            if k != i and not np.isclose(matriz[k, pivote_col], 0):
                return False

        ultimo_pivote_col = pivote_col

    return True
