from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def cponto_medio(raio):
    x = 0
    y = raio
    d = 1 - raio
    ponto_circulo(x, y)
    imprimeCoordenadasDaLinha(x,y)
    
    while y > x:
        if d < 0:  # escolhe E
            d += 2.0 * x + 3.0
        else:  # escolhe SE
            d += 2.0 * (x - y) + 5
            y -= 1
        x += 1
        imprimeCoordenadasDaLinha(x,y)
        ponto_circulo(x, y)

def ponto_circulo(x, y):
    draw_pixel(x, y)
    draw_pixel(y, x)
    draw_pixel(y, -x)
    draw_pixel(x, -y)
    draw_pixel(-x, -y)
    draw_pixel(-y, -x)
    draw_pixel(-y, x)
    draw_pixel(-x, y)

def draw_pixel(x, y):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex2d(x,y)
    glEnd()
    glFlush()

def imprimeCoordenadasDaLinha(x,y):
    print(f"Setar coordenadas: [x = {x}, y = {y}]")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  
    cponto_medio(400)
    #cponto_medio(150)
    #cponto_medio(50)
    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Cor de fundo preta
    gluOrtho2D(-500, 500, -500, 500)  # Define o sistema de coordenadas


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Circulo com Ponto Medio no OpenGL")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
