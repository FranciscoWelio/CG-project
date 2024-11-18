from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


def translate_point(point, tx, ty, tz, w):
    # Construção da matriz de transformação de translação
    translation_matrix = np.array([[1, 0, 0, tx],
                                    [0, 1, 0, ty],
                                    [0, 0, 1, tz],
                                    [0, 0, 0, 1]], dtype=float)

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]], dtype=float)  # w = 1 para pontos

    # Aplicando a transformação de translação multiplicando a matriz de translação pelo vetor do ponto
    translated_point_vector = np.dot(translation_matrix, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    translated_point = (translated_point_vector[0][0] // translated_point_vector[3][0], 
                        translated_point_vector[1][0] // translated_point_vector[3][0],
                        translated_point_vector[2][0] // translated_point_vector[3][0])
    
    return translated_point


def realizar_translacao(cube_points_list, tx, ty, tz): #ajustar
        
    return [ translate_point(point, tx, ty, tz, 1) for point in cube_points_list]

