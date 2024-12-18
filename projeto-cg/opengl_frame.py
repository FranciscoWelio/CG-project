'''
    Classe que renderiza o OpenGl na tela
'''
from tkinter import Tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from transformations import (
    Rotacao,
    Translacao,
    Escala,
    Cisalhamento,
    Reflexao,
    Rotacao3D,
    Translacao3D,
    Escala3D,
    Cisalhamento3D,
    Reflexao3D
)
import math


class AppOgl(OpenGLFrame):
    def __init__(self, frame: Tk, *args, width=700, height=600, threed=False, **kwargs):
        super().__init__(frame, *args,  width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.animate = 0
        self.frame = frame
        self.points = []
        self.square_points_list = []
        self.relative_movements = [
            (35, 0),
            (25,50),
            (25,-200),
            (15, 300),
            (20, -150),
        ]
        self.current_pos = [-300, 0]
        self.threed = threed
        self.rotated = False
        self.context_initialized = False
        self._is_current = False

    def make_current(self):
        """Garante que este contexto OpenGL seja o atual"""
        if not self._is_current:
            if not hasattr(self, 'context'):
                self.context = self.tk.call('winfo', 'id', self._w)
            self.tk.call('winfo', 'id', self._w)
            self._is_current = True

    def release_current(self):
        """Libera o contexto atual"""
        self._is_current = False

    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        self.make_current()
        try:
            self._after_id = None
            if not self.threed:
                glClearColor(0.7, 0.7, 0.7, 0.0)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                gluOrtho2D(-self.winfo_reqwidth()/2, self.winfo_reqwidth()/2, 
                          -self.winfo_reqheight()/2, self.winfo_reqheight()/2)
            else:
                glClearColor(0.7, 0.7, 0.7, 0.0)
                glMatrixMode(GL_PROJECTION)
                glLoadIdentity()
                glFrustum(-10.0, 10.0, -10.0, 10.0, 20, 3000.0)
                glTranslatef(0.0, 0.0, -500.0)
                glPointSize(1.0)
            self.points = []
            self.square_points_list = []
            self.context_initialized = True
        finally:
            self.release_current()# Lista de pontos para armazenar os vértices do quadrado

    def redraw(self):
        """Redesenha a cena OpenGL"""
        self.make_current()
        try:
            if self.threed:
                self.draw_scene3D()
            else:
                self.draw_scene()
        finally:
            self.release_current()

    def draw_scene(self, red = 1, green=0, blue=0):
        """Redesenha a cena OpenGL para que os objetos etc. fiquem na tela"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_axes(self.winfo_reqwidth(), self.winfo_reqheight()) #Desenhar eixos X e Y

        # Desenha os pontos armazenados na lista
        glBegin(GL_POINTS)
        glColor3f(red, green, blue)
        for point in self.points:
            glVertex2f(point[0], point[1])
        glEnd()

        self.update()

    def draw_scene3D(self):
        """Redesenha a cena OpenGL para que os objetos etc. fiquem na tela"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if not self.rotated:
            glRotatef(45, 1.0, 0, 0)  # Rotação em X
            glRotatef(-45, 0.0, 1.0, 0.0)  # Rotação em Y
            self.rotated = True
        self.draw_axes3d((self.winfo_reqwidth()*2)//1, (self.winfo_reqheight()*2.5)//1, ((self.winfo_reqwidth() + self.winfo_reqheight())*2)//2) #Desenhar eixos X, Y e Z

        # Desenha os pontos armazenados na lista
        glBegin(GL_POINTS)
        glColor3f(0.627, 0.125, 0.941)
        for point in self.points:
            glVertex3f(point[0], point[1], point[2])
        glEnd()

        self.update()
    def draw_axes(self, width, height): #Desenhar eixos X e Y 
        glBegin(GL_LINES)
        glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo x
        glVertex3f(-width/2, 0.0, 0.0)
        glVertex3f(width/2, 0.0, 0.0)
        glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo y
        glVertex3f(0.0, -height/2, 0.0)
        glVertex3f(0.0, height/2, 0.0)
        glEnd()

    def draw_axes3d(self, width, height, depth):
        glBegin(GL_LINES)
        # Eixo X (vermelho)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-width/2, 0.0, 0.0)
        glVertex3f(width/2, 0.0, 0.0)
        
        # Eixo Y (verde)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, -height/2, 0.0)
        glVertex3f(0.0, height/2, 0.0)
        
        # Eixo Z (azul)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, -depth/2)
        glVertex3f(0.0, 0.0, depth/2)
        
        glEnd()

    def draw_pixel(self, dc_x, dc_y):
        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(dc_x, dc_y) 
        glEnd()

    def DDA(self, x0, y0, xEnd, yEnd):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        dx = xEnd - x0
        dy = yEnd - y0
        steps = max(abs(dx), abs(dy))
        xIncrement = dx / (steps or 1) # evita divisão por 0
        yIncrement = dy / (steps or 1) # evita divisão por 0
        x = x0
        y = y0
        #self.draw_pixel(round(x), round(y))
        for k in range(int(steps)):
            x += xIncrement
            y += yIncrement
            self.points.append((round(x), round(y)))

    def square_points3D(self, size):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa a tela antes de desenhar o quadrado
        self.points = []
        self.square_points_list = []

        # Define os pontos do quadrado
        x = size
        y = size

        # Desenha o quadrado com o vértice inferior esquerdo na origem
        self.DDA2(0, 0, x, 0)        # Linha inferior
        self.DDA2(x, 0, x, y)        # Linha direita
        self.DDA2(x, y, 0, y)        # Linha superior
        self.DDA2(0, y, 0, 0)        # Linha esquerda

        # Lista de pontos do quadrado com ponto inferior esquerdo na origem
        self.square_points_list = [(0, 0), (x, 0), (x, y), (0, y)]

        return (0, 0), (x, 0), (x, y), (0, y)

    def DDA3D(self, x0, y0, z0, xEnd, yEnd, zEnd):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        dx = xEnd - x0
        dy = yEnd - y0
        dz = zEnd - z0
        
        # Determine the number of steps based on the largest distance
        steps = max(abs(dx), abs(dy), abs(dz))
        
        # Calculate increments for each axis
        xIncrement = dx / (steps or 1)
        yIncrement = dy / (steps or 1)
        zIncrement = dz / (steps or 1)
        
        x = x0
        y = y0
        z = z0
        
        # Store points in 3D
        for k in range(int(steps)):
            x += xIncrement
            y += yIncrement
            z += zIncrement
            self.points.append((round(x), round(y), round(z)))

    def PontoMedio(self, x0, y0, xEnd, yEnd):
        dx = abs(xEnd - x0)
        dy = abs(yEnd - y0)

        if dx >= dy and x0 <= xEnd and y0 <= yEnd:# Verifica se a linha está no primeiro oitante
            print("1 oitante")
            ds = 2 * dy - dx
            incE = 2 * dy
            incNE = 2 * (dy - dx)
            x, y = 0, 0
            if x0 > xEnd:
                x, y = xEnd, yEnd
                xEnd = x0
            else:
                x, y = x0, y0
                
            self.points.append((round(x), round(y)))
            
            while x < xEnd:
                x += 1
                if ds < 0:
                    ds += incE
                else:
                    y += 1
                    ds += incNE
                self.points.append((round(x), round(y)))
            self.update()
            return 
        elif dx >= dy and x0 >= xEnd and y0 <= yEnd: # 4 oitante
            print("4 oitante")
            ds = 2 * dy - dx
            incE = 2 * dy
            incNE = 2 * (dy - dx)
            x, y = x0, y0
                
            self.points.append((round(x), round(y)))
            
            while x > xEnd:
                x -= 1
                if ds < 0:
                    ds += incE
                else:
                    y += 1
                    ds += incNE
                self.points.append((round(x), round(y)))
            self.update()
            return 
        elif dy >= dx and x0 <= xEnd and y0 <= yEnd: # 2 oitante 
            print("2 oitante")
            ds = 2 * dx - dy  # Ajustado para (y, x)
            incE = 2 * dx     # Ajustado para incremento E
            incNE = 2 * (dx - dy)  # Ajustado para incremento NE
            x, y = x0, y0
                
            self.points.append((round(x), round(y)))
            
            while y < yEnd:
                y += 1
                if ds < 0:
                    ds += incE
                else:
                    x += 1
                    ds += incNE
                self.points.append((round(x), round(y)))
            self.update()
            return

        elif (dy >= dx) and x0 >= xEnd and y0 <= yEnd: # 3 oitante
            print("3 oitante")
            ds = 2 * dx - dy  # Ajustado para (y, x)
            incE = 2 * dx     # Ajustado para incremento E
            incNE = 2 * (dx - dy)  # Ajustado para incremento NE
            x, y = x0, y0
                
            self.points.append((round(x), round(y)))
            
            while x > xEnd:
                y += 1
                if ds < 0:
                    ds += incE
                else:
                    x -= 1
                    ds += incNE
                self.points.append((round(x), round(y)))
            self.update()
            return 
        elif(dx>=dy) and x0 >= xEnd and y0 >= yEnd: # 5 oitante
            print("5 oitante")
            ds = 2 * -dy + dx
            incE = 2 * -dy
            incNE = 2 * (-dy + dx) # Ajustado para incremento NE
            x, y = x0, y0

            self.points.append((round(x), round(y)))


            while x > xEnd:  
                x -= 1
                if ds < 0:
                    ds += -incE
                else:
                    y -= 1
                    ds += -incNE
                self.points.append((round(x), round(y)))

            self.update()
            return
        elif(dy>=dx) and x0 >= xEnd and y0 >= yEnd: # 6 oitante
            print("6 oitante")
            dx, dy =  dy, dx
            ds = 2 * -dy + dx
            incE = 2 * -dy
            incNE = 2 * (-dy + dx) # Ajustado para incremento NE
            x, y = x0, y0

            self.points.append((round(x), round(y)))


            while y > yEnd:
                y -= 1
                if ds < 0:
                    ds += -incE
                else:
                    x -= 1
                    ds += -incNE
                self.points.append((round(x), round(y)))

            self.update()
            return
        elif(dy>=dx) and xEnd >= x0 and y0 >= yEnd: # 7 oitante
            print("7 oitante")
            dx, dy =  dy, dx
            ds = 2 * -dy + dx
            incE = 2 * -dy
            incNE = 2 * (-dy + dx) # Ajustado para incremento NE
            x, y = x0, y0

            self.points.append((round(x), round(y)))


            while y > yEnd:
                y -= 1
                if ds < 0:
                    ds += -incE
                else:
                    x += 1
                    ds += -incNE
                self.points.append((round(x), round(y)))

            self.update()
            return
        elif(dx>=dy) and x0 <= xEnd and y0 >= yEnd: # 8 oitante
            print("8 oitante")
            ds = 2 * -dy + dx
            incE = 2 * -dy
            incNE = 2 * (-dy + dx) # Ajustado para incremento NE
            x, y = x0, y0

            self.points.append((round(x), round(y)))


            while x < xEnd:
                x += 1
                print(ds, incE, incNE)
                if ds < 0:
                    ds += -incE
                else:
                    y -= 1
                    ds += -incNE
                self.points.append((round(x), round(y)))

            self.update()
            return
    # Método para desenhar quadrado com o ponto inferior esquerdo na origem
    def square_points(self, size):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa a tela antes de desenhar o quadrado
        self.points = []
        self.square_points_list = []

        # Define os pontos do quadrado
        x = size
        y = size

        # Desenha o quadrado com o vértice inferior esquerdo na origem
        self.DDA(0, 0, x, 0)        # Linha inferior
        self.DDA(x, 0, x, y)        # Linha direita
        self.DDA(x, y, 0, y)        # Linha superior
        self.DDA(0, y, 0, 0)        # Linha esquerda

        # Lista de pontos do quadrado com ponto inferior esquerdo na origem
        self.square_points_list = [(0, 0), (x, 0), (x, y), (0, y)]

        return (0, 0), (x, 0), (x, y), (0, y)
    
    def cube_points(self, size):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # self.cube_points_list = []

        # Define dimensões do cubo
        x = size
        y = size
        z = size

        # Face frontal
        self.DDA3D(0, 0, 0, x, 0, 0)
        self.DDA3D(x, 0, 0, x, y, 0)
        self.DDA3D(x, y, 0, 0, y, 0)
        self.DDA3D(0, y, 0, 0, 0, 0)

        # Face traseira
        self.DDA3D(0, 0, z, x, 0, z)
        self.DDA3D(x, 0, z, x, y, z)
        self.DDA3D(x, y, z, 0, y, z)
        self.DDA3D(0, y, z, 0, 0, z)

        # Arestas conectoras
        self.DDA3D(0, 0, 0, 0, 0, z)
        self.DDA3D(x, 0, 0, x, 0, z)
        self.DDA3D(x, y, 0, x, y, z)
        self.DDA3D(0, y, 0, 0, y, z)

        self.cube_points_list = [(0, 0, 0), (x, 0, 0), (x, y, 0), (0, y, 0),
                                 (0, 0, z), (x, 0, z), (x, y, z), (0, y, z),]

        # Lista de vértices do cubo
        return [
            (0, 0, 0), (x, 0, 0), (x, y, 0), (0, y, 0),
            (0, 0, z), (x, 0, z), (x, y, z), (0, y, z)
        ]

    def linePoliExpli(self, r):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.redraw()
        x=0
        xEnd = r/math.sqrt(2)
        RR = r**2
        while(x<=xEnd):
            XX = x**2
            y = math.sqrt(RR-XX)
            self.pontosCircunferencia(x,y)
            x = x+1

    def linePoliTrig(self, r):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.redraw()
        theta = 0
        thetaEnd = 45
        while(theta<=thetaEnd):
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            self.pontosCircunferencia(x,y)
            theta = theta+ 0.3

    def linePoliPM(self, r):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.redraw()
        x = 0
        y = r
        d = (5/4)-r
        #d = (1-r)
        self.pontosCircunferencia(x,y)
        while(y>x):
            if(d<0):
                d = d +(2*x +3)
            else:
                d = d+ (2* (x-y)+5)
                y = y-1
            x = x+1
            self.pontosCircunferencia(x,y)

    def linePoliElip(self, rx, ry, centrox, centroy):
        x = 0
        y = ry
        # Inicializa o parâmetro de decisão para a Região 1
        d1 = (ry**2) - (rx**2 * ry) + (0.25 * rx**2)
        dx = 2 * ry**2 * x
        dy = 2 * rx**2 * y

        self.pontosElipse(x, y, centrox, centroy)  # Plota o primeiro ponto

        # Região 1
        while dx < dy:
            if d1 < 0:
                d1 += dx + (ry**2)
            else:
                y -= 1
                dy -= 2 * (rx**2)
                d1 += dx - dy + (ry**2)
            x += 1
            dx += 2 * (ry**2)
            self.pontosElipse(x, y, centrox, centroy)

        # Inicializa o parâmetro de decisão para a Região 2
        d2 = ((ry**2) * ((x + 0.5)**2)) + ((rx**2) * ((y - 1)**2)) - (rx**2 * ry**2)

        # Região 2
        while y > 0:
            if d2 > 0:
                d2 += (rx**2) - dy
            else:
                x += 1
                dx += 2 * (ry**2)
                d2 += dx - dy + (rx**2)
            y -= 1
            dy -= 2 * (rx**2)
            self.pontosElipse(x, y, centrox, centroy)


    def pontosElipse(self, x, y,centrox, centroy):
        cx= centrox
        cy = centroy  # O centro da elipse
        self.points.append((cx + x, cy + y))
        self.points.append((cx - x, cy + y))
        self.points.append((cx + x, cy - y))
        self.points.append((cx - x, cy - y))

    def pontosCircunferencia(self, x, y):
        self.points.append((round(x), round(y)))
        self.points.append((round(x), round(-y)))
        self.points.append((round(-x), round(y)))
        self.points.append((round(-x), round(-y)))
        self.points.append((round(y), round(x)))
        self.points.append((round(y), round(-x)))
        self.points.append((round(-y), round(x)))
        self.points.append((round(-y), round(-x)))


    #Método para desenhar quadrado após a transformação
    def draw_square(self, point1, point2, point3, point4):
        self.DDA(point1[0], point1[1], point2[0], point2[1])
        self.DDA(point2[0], point2[1], point3[0], point3[1])
        self.DDA(point3[0], point3[1], point4[0], point4[1])
        self.DDA(point4[0], point4[1], point1[0], point1[1])


    #Transformações no Quadrado
    def escala(self, sx, sy):
        #Passa os pontos do quadrado desenhado para a função de escala que retorna os novos pontos do quadrado
        self.square_points_list = Escala.realizar_escala(self.square_points_list, sx, sy)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado
        self.draw_square(*self.square_points_list) #passa os parametros da função ao desempacotar a lista (p1, p2, etc.)

    def escala3D(self, sx, sy, sz):
        #Passa os pontos do quadrado desenhado para a função de escala que retorna os novos pontos do quadrado

        #Remove o quadrado anterior
        # self.points = Escala.realizar_escala3D(self.points, sx, sy, sz)
        self.cube_points_list = Escala3D.realizar_escala(self.cube_points_list, sx, sy, sz)
        
        #Remove o quadrado anterior
        self.points = []

        self.draw_cube(*self.cube_points_list)
        

        #Desenha o novo quadrado
        #self.draw_square(*self.square_points_list) 

    def translacao(self, tx, ty):
        
        self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado transladado
        self.draw_square(*self.square_points_list)
    
    def translacao3D(self, tx, ty, tz):
        #Passa os pontos do quadrado desenhado para a função de escala que retorna os novos pontos do quadrado

        #Remove o quadrado anterior
        # self.points = Escala.realizar_escala3D(self.points, sx, sy, sz)
        self.cube_points_list = Translacao3D.realizar_translacao(self.cube_points_list, tx, ty, tz)
        
        #Remove o quadrado anterior
        self.points = []

        self.draw_cube(*self.cube_points_list)

    def rotacao(self, angle):
        
        self.square_points_list = Rotacao.realizar_rotacao(self.square_points_list, angle)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def rotacaoReta(self, angle, angle2):
        
        self.square_points_list = Rotacao.realizar_rotacaoReta(self.square_points_list, angle, angle2)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def rotacao3D(self, eixo: str, angle: int):
        self.cube_points_list = Rotacao3D.realizar_rotacao(eixo, self.cube_points_list, angle)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_cube(*self.cube_points_list)
    
    def cisalhamento(self, a, b):

        self.square_points_list = Cisalhamento.realizar_cisalhamento(self.square_points_list, a, b)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def cisalhamento3D(self, a, c, e):
        b = a
        d = c
        f = e

        self.cube_points_list = Cisalhamento3D.realizar_cisalhamento(self.cube_points_list, a, b, c, d, e, f)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_cube(*self.cube_points_list)
    
    def reflexao3D(self, eixo: str):

        self.cube_points_list = Reflexao3D.realizar_reflexao(eixo, self.cube_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_cube(*self.cube_points_list)

    def reflexaoX(self):

        self.square_points_list = Reflexao.realizar_reflexaoX(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def reflexaoY(self):

        self.square_points_list = Reflexao.realizar_reflexaoY(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def reflexaoOrigem(self):

        self.square_points_list = Reflexao.realizar_reflexaoOrigem(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)

    def reflexao45(self):

        self.square_points_list = Reflexao.realizar_reflexao45(self.square_points_list)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    #def RetaPM(self):
    def draw_cube(self, point1, point2, point3, point4, point5, point6, point7, point8):
        self.DDA3D(point1[0], point1[1], point1[2], point2[0], point2[1], point2[2])
        self.DDA3D(point2[0], point2[1], point2[2], point3[0], point3[1], point3[2])
        self.DDA3D(point3[0], point3[1], point3[2], point4[0], point4[1], point4[2])
        self.DDA3D(point4[0], point4[1], point4[2], point1[0], point1[1], point1[2])

        self.DDA3D(point1[0], point1[1], point1[2], point5[0], point5[1], point5[2])
        self.DDA3D(point2[0], point2[1], point2[2], point6[0], point6[1], point6[2])
        self.DDA3D(point3[0], point3[1], point3[2], point7[0], point7[1], point7[2])
        self.DDA3D(point4[0], point4[1], point4[2], point8[0], point8[1], point8[2])
        
        self.DDA3D(point5[0], point5[1], point5[2], point6[0], point6[1], point6[2])
        self.DDA3D(point6[0], point6[1], point6[2], point7[0], point7[1], point7[2])
        self.DDA3D(point7[0], point7[1], point7[2], point8[0], point8[1], point8[2])
        self.DDA3D(point8[0], point8[1], point8[2], point5[0], point5[1], point5[2])


    def desenhar_batimento(self):
        """
        Desenha uma linha de batimento cardíaco (ECG)
        Padrão básico de ECG: linha base - pico P - complexo QRS - onda T
        """

        #self.points = [(point[0]-1, point[1]) for point in self.points if point[0]>-100]
        x_init, y_init = self.current_pos
        x_final, y_final = self.relative_movements.pop(0)
        if x_init > 350:
            x_init = -350
        self.PontoMedio(x_init, y_init, x_init+x_final, y_init+y_final)
        self.relative_movements.append([x_final, y_final])
        self.points = [(point[0] - 700,point[1]) if point[0] > 350 else point for point in self.points]
        self.points = self.points[-3500:]
        self.current_pos = self.points[-1]

    def display(self):
        # glClear(GL_COLOR_BUFFER_BIT)
        # glLoadIdentity()
        
        # Draw heart
        self.desenhar_batimento()
        self.frame.update_idletasks()
        self.frame.update()

    def update_animation(self):
        if self.animate:
            # self.time += 0.1
            self.display()
            # Schedule next update using Tkinter's after method
            self.frame.after(500, self.update_animation)

    def destroy(self):
        self.make_current()
        try:
            self.animate = 0
            if hasattr(self, '_after_id') and self._after_id:
                try:
                    self.after_cancel(self._after_id)
                except ValueError:
                    pass
            self.update_idletasks()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        finally:
            self.release_current()
            super().destroy()       
        
    


