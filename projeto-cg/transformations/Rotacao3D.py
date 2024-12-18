from typing import Tuple
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

    
def rotate_pointZ(point, ang, w):

    rad = np.radians(ang)

    matrizTheta = np.array([[np.cos(rad), - np.sin(rad), 0,0],
                            [np.sin(rad), np.cos(rad), 0,0],
                            [0, 0, 1,0],
                            [0, 0, 0,1]
    ])
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    rotated_point_vector = np.dot(matrizTheta, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    rotated_point = (rotated_point_vector[0][0] / rotated_point_vector[3][0], 
                     rotated_point_vector[1][0] / rotated_point_vector[3][0], 
                        rotated_point_vector[2][0] / rotated_point_vector[3][0])
    
    return rotated_point
def rotate_pointY(point, ang, w):

    rad = np.radians(ang)

    matrizTheta = np.array([[np.cos(rad), 0 , np.sin(rad),0],
                            [0, 1, 0,0],
                            [-np.sin(rad), 0, np.cos(rad),0],
                            [0, 0, 0,1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    rotated_point_vector = np.dot(matrizTheta, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    rotated_point = (rotated_point_vector[0][0] / rotated_point_vector[3][0], 
                     rotated_point_vector[1][0] / rotated_point_vector[3][0], 
                        rotated_point_vector[2][0] / rotated_point_vector[3][0])
    
    return rotated_point
def rotate_pointX(point, ang, w):

    rad = np.radians(ang)

    matrizTheta = np.array([[1, 0 , 0,0],
                            [0, np.cos(rad), -np.sin(rad),0],
                            [0, np.sin(rad), np.cos(rad),0],
                            [0, 0, 0,1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    rotated_point_vector = np.dot(matrizTheta, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    rotated_point = (rotated_point_vector[0][0] / rotated_point_vector[3][0], 
                     rotated_point_vector[1][0] / rotated_point_vector[3][0], 
                        rotated_point_vector[2][0] / rotated_point_vector[3][0])
    
    return rotated_point

def realizar_rotacao(eixo: str, cube_points_list: Tuple[int,int,int], angle: int):

    if eixo == "em x":
        return [rotate_pointX(point, angle, 1) for point in cube_points_list]
    elif eixo == "em y":
        return [rotate_pointY(point, angle, 1) for point in cube_points_list]
    else:
        return [rotate_pointZ(point, angle, 1) for point in cube_points_list]
