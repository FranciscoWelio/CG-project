from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def draw_pixel(x, y):
    glPointSize(0.5)
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))  
    glEnd()
    glFlush()


def linePoli(r):
    theta = 0
    thetaEnd = 45
    while(theta<=thetaEnd):
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        pontosCircunferencia(x,y)
        theta = theta+ 0.3

def pontosCircunferencia(x, y):
    draw_pixel(x, y)
    draw_pixel(x, -y)
    draw_pixel(-x, y)
    draw_pixel(-x, -y)
    draw_pixel(y, x)
    draw_pixel(y, -x)
    draw_pixel(-y, x)
    draw_pixel(-y, -x)

def imprimeCoordenadasDaLinha(x,y):
    return print(f"Setar coordenadas: [x = {round(x)}, y = {round(y)}]")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Cor branca
    linePoli(480)
    #linePM(0,0,250,250)
    #linePM(0,0,250,359)
    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Cor de fundo preta
    gluOrtho2D(-500, 500, -500, 500)  # Define o sistema de coordenadas

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Circunferencia Trigonometrica no OpenGL")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()