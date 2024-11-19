import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def shear_pointZ(point, a, b, w):

    matrizCis = np.array([[1, a, 0, 0],
                            [0, 1, b, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    shear_point_vector = np.dot(matrizCis, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (shear_point_vector[0][0] / shear_point_vector[3][0], 
                   shear_point_vector[1][0] / shear_point_vector[3][0],
                        shear_point_vector[2][0] / shear_point_vector[3][0])
    
    return shear_point

def shear_pointX(point, a, b, w):

    matrizCis = np.array([[1, 0, 0, 0],
                            [a, 1, 0, 0],
                            [b, 0, 1, 0],
                            [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    shear_point_vector = np.dot(matrizCis, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (shear_point_vector[0][0] / shear_point_vector[3][0], 
                   shear_point_vector[1][0] / shear_point_vector[3][0],
                        shear_point_vector[2][0] / shear_point_vector[3][0])
    
    return shear_point

def shear_pointY(point, a, b, w):

    matrizCis = np.array([[1, a, 0, 0],
                            [0, 1, 0, 0],
                            [0, b, 1, 0],
                            [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    shear_point_vector = np.dot(matrizCis, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (shear_point_vector[0][0] / shear_point_vector[3][0], 
                   shear_point_vector[1][0] / shear_point_vector[3][0],
                        shear_point_vector[2][0] / shear_point_vector[3][0])
    
    return shear_point

def shear_pointGeral(point, a, b, c, d, e, f, w):

    matrizCis = np.array([[1, c, e, 0],
                            [a, 1, f, 0],
                            [b, d, 1, 0],
                            [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    shear_point_vector = np.dot(matrizCis, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    shear_point = (shear_point_vector[0][0] / shear_point_vector[3][0], 
                   shear_point_vector[1][0] / shear_point_vector[3][0],
                        shear_point_vector[2][0] / shear_point_vector[3][0])
    
    return shear_point
def realizar_cisalhamento(cube_points_list, a, b, c, d, e, f):
    # retornar os vertices do quadrado após o cisalhamento
    return [shear_pointGeral(point, a, b, c, d, e, f, 1) for point in cube_points_list]