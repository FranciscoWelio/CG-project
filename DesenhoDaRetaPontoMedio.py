from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

def draw_pixel(x, y):
    glPointSize(0.5)
    glBegin(GL_POINTS)
    glVertex2i(x, y)  
    glEnd()
    glFlush()

def linePM(x0, y0, xEnd, yEnd):
    dx = abs(xEnd - x0)
    dy = abs(yEnd - y0)
    p = 2 * dy - dx
    twoDy = 2 * dy
    twoDyMinusDx = 2 * (dy - dx)
    x, y = 0, 0

    # Verifica se a linha está no primeiro oitante
    if dy > dx:
        print("Reta não se situa no 1º oitante")
        return
    
    if x0 > xEnd:
        x, y = xEnd, yEnd
        xEnd = x0
    else:
        x, y = x0, y0
        
    imprimeCoordenadasDaLinha(x,y)
    draw_pixel(x, y)
    
    while x < xEnd:
        x += 1
        if p < 0:
            p += twoDy
        else:
            y += 1
            p += twoDyMinusDx
        imprimeCoordenadasDaLinha(x, y)
        draw_pixel(x, y)

def imprimeCoordenadasDaLinha(x,y):
    print(f"Setar coordenadas: [x = {round(x)}, y = {round(y)}]")

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  # Cor branca
    linePM(200,250,351,330)
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
    glutCreateWindow(b"Linha com Ponto Medio no OpenGL")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()