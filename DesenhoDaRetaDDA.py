from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def draw_pixel(x, y):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex2i(x, y)  
    glEnd()
    glFlush()

def lineDDA(x0, y0, xEnd, yEnd):
    dx = xEnd - x0
    dy = yEnd - y0
    steps = max(abs(dx), abs(dy))
    xIncrement = dx / steps
    yIncrement = dy / steps
    x = x0
    y = y0
    draw_pixel(round(x), round(y))
    for k in range(steps):
        x += xIncrement
        y += yIncrement
        imprimeCoordenadasDaLinha(x,y)
        draw_pixel(round(x), round(y))

def imprimeCoordenadasDaLinha(x,y):
    print(f"Setar coordenadas: [x = {round(x)}, y = {round(y)}]")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Cor branca
    #lineDDA(-250,250,250,250)
    lineDDA(30,14,250,300)
    #lineDDA(250,0,0,0)
    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Cor de fundo preta
    gluOrtho2D(-500, 500, -500, 500)  # Define o sistema de coordenadas


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Linha com DDA no OpenGL")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()

