import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

    
def rotate_point(point, ang, w):

    rad = np.radians(ang)

    matrizTheta = np.array([[np.cos(rad), - np.sin(rad), 0],
                            [np.sin(rad), np.cos(rad), 0],
                            [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    rotated_point_vector = np.dot(matrizTheta, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    rotated_point = (rotated_point_vector[0][0] / rotated_point_vector[2][0], 
                        rotated_point_vector[1][0] / rotated_point_vector[2][0])
    
    return rotated_point


def realizar_rotacao(square_points_list, angle):

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = rotate_point(point1, angle, 1)
    point2 = rotate_point(point2, angle, 1)
    point3 = rotate_point(point3, angle, 1)
    point4 = rotate_point(point4, angle, 1)

    # retornar os vertices do quadrado após a rotação
    return [point1, point2, point3, point4]