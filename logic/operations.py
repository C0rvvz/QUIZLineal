import numpy as np
from fractions import Fraction

def crear_matriz_aleatoria(n):
    """
    Genera una matriz aleatoria cuadrada de tamaño n×n.

    Parámetros:
    - n: dimensión de la matriz cuadrada

    Retorna:
    - Matriz con números enteros aleatorios entre -10 y 10
      para facilitar los cálculos manuales
    """
    return np.random.randint(-10, 10, (n, n))

# ==================== NIVEL 1: TRANSPUESTA ====================
# En álgebra lineal, la transpuesta de una matriz A es una nueva matriz A^T
# donde las filas de A se convierten en columnas de A^T y viceversa.
# Matemáticamente: (A^T)_ij = A_ji para todo i,j

def comparar_con_transpuesta(matriz, matriz_transpuesta):
    """
    Verifica si una matriz es la transpuesta correcta de otra.

    Fundamento matemático:
    - Una matriz es la transpuesta de otra si y solo si A_ij = (A^T)_ji
      para todos los elementos.

    Implementación:
    - Aprovechamos NumPy que ofrece la propiedad .T para calcular
      la transpuesta y array_equal para comparación exacta
    """
    try:
        return np.array_equal(matriz_transpuesta, matriz.T)
    except Exception as e:
        raise ValueError(f"Error al verificar la transpuesta: {e}")


def evaluar_entrada_transpuesta(matriz, entries):
    """
    Evalúa si la matriz ingresada por el usuario es la transpuesta correcta.

    Proceso:
    1. Convierte las entradas de la interfaz gráfica a valores numéricos
    2. Construye la matriz con estos valores
    3. Compara con la transpuesta esperada (matriz.T)

    Utilizamos Fraction para manejar entradas como fracciones o decimales,
    manteniendo precisión exacta.
    """
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


# ==================== NIVEL 2: GAUSS-JORDAN ====================
# El método Gauss-Jordan utiliza operaciones elementales por filas
# para transformar una matriz a su forma escalonada reducida.
# Este método es fundamental para resolver sistemas de ecuaciones lineales.

def aplicar_operacion_elemental(A, tipo, fila1, fila2=None, factor=1, B=None):
    """
    Realiza las tres operaciones elementales por filas en matrices.

    Fundamentos matemáticos:
    1. Intercambio de filas: Fi ↔ Fj
    2. Multiplicación por escalar: Fi → k·Fi (k≠0)
    3. Suma de múltiplo: Fi → Fi + k·Fj (i≠j)

    Estas operaciones preservan el espacio de soluciones del sistema lineal.

    Parámetros adicionales:
    - B: matriz opcional que sufrirá las mismas transformaciones
      (crucial para calcular inversas mediante Gauss-Jordan)

    Utilizamos Fraction para mantener precisión exacta en cálculos
    con fracciones, evitando errores de redondeo.
    """
    A = A.astype(object)  # Asegura compatibilidad con Fraction
    if B is not None:
        B = B.astype(object)

    if tipo == "intercambio":
        # Implementación vectorizada del intercambio de filas
        A[[fila1, fila2]] = A[[fila2, fila1]]
        if B is not None:
            B[[fila1, fila2]] = B[[fila2, fila1]]

    elif tipo == "multiplicacion":
        # Multiplica cada elemento por un factor (k≠0)
        A[fila1] = [Fraction(x) * Fraction(factor) for x in A[fila1]]
        if B is not None:
            B[fila1] = [Fraction(x) * Fraction(factor) for x in B[fila1]]

    elif tipo == "suma":
        # Operación Fi → Fi + k·Fj
        # Usamos comprensión de listas con zip para operar elemento a elemento
        A[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y)
                    for x, y in zip(A[fila1], A[fila2])]
        if B is not None:
            B[fila1] = [Fraction(x) + Fraction(factor) * Fraction(y)
                        for x, y in zip(B[fila1], B[fila2])]

    return A, B  # Retorna ambas matrices modificadas


# ==================== NIVEL 3: MATRIZ INVERSA ====================
# La matriz inversa A⁻¹ de una matriz A satisface: A·A⁻¹ = A⁻¹·A = I
# donde I es la matriz identidad. No todas las matrices tienen inversa.
# Una matriz tiene inversa si y solo si su determinante es no nulo.

def verificar_producto_es_identidad(matriz_original, matriz_inversa):
    """
    Verifica si el producto de dos matrices es la matriz identidad,
    lo que confirma que una matriz es la inversa de la otra.

    Fundamento matemático:
    - Si A·B = I, entonces B es la inversa por derecha de A
    - Si A es cuadrada y tiene inversa, entonces A⁻¹ es única

    Implementación:
    1. Convertimos matrices a punto flotante para cálculos numéricos
    2. Calculamos el producto matricial con np.dot
    3. Comparamos con la identidad usando np.allclose con tolerancia 10⁻⁹
       para manejar pequeños errores de redondeo

    Esta función es crucial para verificar si la matriz calculada
    mediante Gauss-Jordan es realmente la inversa.
    """
    try:
        # Convertimos a float para cálculos numéricos
        matriz_float = np.array(matriz_original, dtype=float)
        matriz_inversa_float = np.array(matriz_inversa, dtype=float)

        # Creamos matriz identidad del tamaño adecuado
        identidad = np.eye(matriz_original.shape[0], dtype=float)

        # Calculamos A·B
        producto = np.dot(matriz_float, matriz_inversa_float)

        # Verificamos si el producto es aproximadamente la identidad
        # usando tolerancia para manejar errores de redondeo
        if np.allclose(producto, identidad, atol=1e-9):
            return True, "¡La matriz ingresada es la inversa correcta!"
        else:
            return False, "La matriz ingresada no es la inversa correcta."
    except Exception as e:
        return False, f"Error al verificar la inversa: {e}"
