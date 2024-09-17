from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

def scale_point(point, sx, sy, w):
    # Criação da matriz de identidade de escala 2D
    scale_matrix = np.array([[sx, 0, 0],
                             [0, sy, 0],
                             [0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[w]])

    # Aplicando a transformação de escala multiplicando a matriz de escala pelo vetor do ponto
    scaled_point_vector = np.dot(scale_matrix, point_vector)
    
    return (scaled_point_vector[0][0], scaled_point_vector[1][0])

def realizar_escala(square_points_list, sx, sy):
    
    point1, point2, point3, point4 = square_points_list

    point1 = scale_point(point1, sx, sy, 1)
    point2 = scale_point(point2, sx, sy, 1)
    point3 = scale_point(point3, sx, sy, 1)
    point4 = scale_point(point4, sx, sy, 1)

    return [point1, point2, point3, point4]


