import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def shear_point(point, a, b, w):

    matrizCis = np.array([[1, a, 0],
                          [b, 1, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    shear_point_vector = np.dot(matrizCis, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (shear_point_vector[0][0] / shear_point_vector[2][0], 
                        shear_point_vector[1][0] / shear_point_vector[2][0])
    
    return shear_point


def realizar_cisalhamento(square_points_list, a, b):

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = shear_point(point1, a, b, 1)
    point2 = shear_point(point2, a, b, 1)
    point3 = shear_point(point3, a, b, 1)
    point4 = shear_point(point4, a, b, 1)

    # retornar os vertices do quadrado após o cisalhamento
    return [point1, point2, point3, point4]