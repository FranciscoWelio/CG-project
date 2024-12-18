from typing import Tuple
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def refXY_point(point, w):

    matrizRef = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, -1, 0],
                            [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    reflection_point = (reflection_point_vector[0][0] / reflection_point_vector[3][0],
                        reflection_point_vector[1][0] / reflection_point_vector[3][0], 
                        reflection_point_vector[2][0] / reflection_point_vector[3][0])
    
    return reflection_point

def refYZ_point(point, w):

    matrizRef = np.array([[-1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    reflection_point = (reflection_point_vector[0][0] / reflection_point_vector[3][0],
                        reflection_point_vector[1][0] / reflection_point_vector[3][0], 
                        reflection_point_vector[2][0] / reflection_point_vector[3][0])
    
    return reflection_point

def refZX_point(point, w):

    matrizRef = np.array([[1, 0, 0, 0],
                            [0, -1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    reflection_point = (reflection_point_vector[0][0] / reflection_point_vector[3][0],
                        reflection_point_vector[1][0] / reflection_point_vector[3][0], 
                        reflection_point_vector[2][0] / reflection_point_vector[3][0])
    
    return reflection_point

def refOrigin_point(point, w):

    matrizRef = np.array([[-1, 0, 0, 0],
                            [0, -1, 0, 0],
                            [0, 0, -1, 0],
                            [0, 0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]],[point[2]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    reflection_point = (reflection_point_vector[0][0] / reflection_point_vector[3][0],
                        reflection_point_vector[1][0] / reflection_point_vector[3][0], 
                        reflection_point_vector[2][0] / reflection_point_vector[3][0])
    
    return reflection_point

def ref45_point(point, w):

    matrizRef = np.array([[0, 1, 0],
                          [1, 0, 0],
                          [0, 0, 1]])
    
    # Convertendo o ponto para um vetor coluna
    point_vector = np.array([[point[0]], [point[1]], [w]])  # w = 1 para pontos

    # Aplicando a transformação de rotação multiplicando a matriz de translação pelo vetor do ponto
    reflection_point_vector = np.dot(matrizRef, point_vector)

    # Normalizando as coordenadas homogêneas resultantes
    reflection_point = (reflection_point_vector[0][0] / reflection_point_vector[2][0], 
                        reflection_point_vector[1][0] / reflection_point_vector[2][0])
    
    return reflection_point


def realizar_reflexaoXY(square_points_list): #ajuste

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = refX_point(point1, 1)
    point2 = refX_point(point2, 1)
    point3 = refX_point(point3, 1)
    point4 = refX_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexaoYZ(square_points_list):#ajuste

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = refY_point(point1, 1)
    point2 = refY_point(point2, 1)
    point3 = refY_point(point3, 1)
    point4 = refY_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexaoZX(square_points_list):#ajuste

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = refY_point(point1, 1)
    point2 = refY_point(point2, 1)
    point3 = refY_point(point3, 1)
    point4 = refY_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexao(eixo: str, cube_points_list: Tuple[int,int,int]):
    if eixo == "em yz":
        return [refYZ_point(point, 1) for point in cube_points_list]
    elif eixo == "em xz":
        return [refZX_point(point, 1) for point in cube_points_list]
    else:
        return [refXY_point(point, 1) for point in cube_points_list]

def realizar_reflexaoOrigem(square_points_list):#ajuste

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = refOrigin_point(point1, 1)
    point2 = refOrigin_point(point2, 1)
    point3 = refOrigin_point(point3, 1)
    point4 = refOrigin_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]

def realizar_reflexao45(square_points_list):

    point1, point2, point3, point4 = square_points_list

    # Rotacionar os pontos
    point1 = ref45_point(point1, 1)
    point2 = ref45_point(point2, 1)
    point3 = ref45_point(point3, 1)
    point4 = ref45_point(point4, 1)

    # retornar os vertices do quadrado após a reflexão
    return [point1, point2, point3, point4]