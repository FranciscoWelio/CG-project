from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import*

def draw_pixel(x, y):
    glPointSize(1.0)
    glBegin(GL_POINTS)
    glVertex2d(x,y)
    glEnd()
    glFlush()

def display(ndcx,ndcy):
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0) 
    glBegin(GL_LINES)
    glEnd()
    draw_pixel(ndcx,ndcy)
    glFlush()

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    gluOrtho2D(-1, 1, -1, 1) 

#Do dispositivo para normalização 
def input_to_ndc(ndh,ndv,dcx,dcy):
    limite_inferiorx = (dcx - 0.5) / (ndh - 1)
    limite_superiorx = (dcx + 0.5) / (ndh - 1)

    limite_inferiory = (dcy - 0.5) / (ndv - 1)
    limite_superiory = (dcy + 0.5) / (ndv - 1)

    return limite_inferiorx, limite_superiorx,limite_inferiory,limite_superiory 

#Normalização para o dispositivo
def ndc_to_dc(ndcx,ndcy,ndh,ndv):
    dcx = round(ndcx * (ndh-1))
    dcy = round(ndcy * (ndv-1))
    return dcx, dcy

#Normalização para usuário
def ndc_to_user(ndcx,ndcy,xmax,xmin,ymax,ymin):
    x = (ndcx+1)*xmax+(1-ndcx)*xmin/2
    y = (ndcy+1)*ymax+(1-ymax)*ymin/2

    return x, y

#Do usuário para normalização
def user_to_ndc(x, y, xmax, xmin, ymax, ymin):
    ndcx = 2*(x-xmin)/(xmax-xmin) -1
    ndcy = 2*(y-ymin)/(ymax-ymin) -1
    return ndcx, ndcy

def main():
    #ndh = int(input("ndh: "))
    #ndv = int(input("ndv: "))
    x = float(input("x: "))
    xmax = 500
    xmin = -500
    y = float(input("y: "))
    ymax = 500
    ymin = -500

    print()
    print("-"*100)
    print("                                           RESULTADOS")
    print("-"*100)
    print()

    ndcx,ndcy = user_to_ndc(x, y, xmax, xmin, ymax, ymin)
    dcx,dcy = ndc_to_dc(ndcx,ndcy,ndh=500,ndv=500)

    print("ndcx = ", "{:.6f}".format(ndcx))
    print("ndcy = ", "{:.6f}".format(ndcy))
    print("dcx = ", dcx)
    print("dcy = ", dcy)

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500,500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Pixel")
    glutDisplayFunc(lambda: display(ndcx, ndcy))  
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
