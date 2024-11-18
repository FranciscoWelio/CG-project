from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def scale_point(point, sx, sy, sz, w):
    # Criação da matriz de identidade de escala 2D
    scale_matrix = np.array([[sx, 0, 0, 0],
                             [0, sy, 0, 0],
                             [0, 0, sz, 0],
                             [0, 0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]],[w]])

    # Aplicando a transformação de escala multiplicando a matriz de escala pelo vetor do ponto
    scaled_point_vector = np.dot(scale_matrix, point_vector)
    
    return (scaled_point_vector[0][0], scaled_point_vector[1][0], scaled_point_vector[2][0])

def realizar_escala(square_points_list, sx, sy, sz): #ajustar

    return [scale_point(point, sx, sy, sz, 1) for point in square_points_list] #ajustar



