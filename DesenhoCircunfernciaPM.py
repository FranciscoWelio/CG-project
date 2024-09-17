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
   x = 0
   y = r
   d = (5/4)-r
   #d = (1-r)
   pontosCircunferencia(x,y)
   while(y>x):
        if(d<0):
           d = d +(2*x +3)
        else:
            d = d+ (2* (x-y)+5)
            y = y-1
        x = x+1
        pontosCircunferencia(x,y)


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
    linePoli(280)
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
    glutCreateWindow(b"Circunferencia com Ponto Medio no OpenGL")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()