import numpy as np
from fractions import Fraction

def generar_matriz(n):
    """Genera una matriz cuadrada aleatoria de tamaño n x n."""
    return np.random.randint(-10, 10, (n, n))

def realizar_operacion(A, tipo, fila1, fila2=None, factor=1, B=None):
    """Aplica una operación de fila sobre la matriz usando fracciones."""
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
