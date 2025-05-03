import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add parent directory to sys.pathfrom logic.operations import generar_matriz, realizar_operacionfrom logic.matrix_utils import format_matrix, es_escalonada_reducida