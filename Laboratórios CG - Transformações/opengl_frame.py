'''
    Classe que renderiza o OpenGl na tela
'''
from tkinter import Tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from Transformações import Rotacao
from Transformações import Translacao
from Transformações import Escala
from Transformações import Cisalhamento
from Transformações import Reflexao
import math


class AppOgl(OpenGLFrame):
    def __init__(self, frame: Tk, *args, width=700, height=600, **kwargs):
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
        # self.initgl()

    def initgl(self):
        """Inicializa o ambiente OpenGL"""
        self._after_id = None
        glClearColor(0.7, 0.7, 0.7, 0.0) #Cor de fundo do openGL
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-self.winfo_reqwidth()/2, self.winfo_reqwidth()/2, -self.winfo_reqheight()/2, self.winfo_reqheight()/2)
        self.points = []  # Lista de pontos para armazenar o desenho
        self.square_points_list = [] # Lista de pontos para armazenar os vértices do quadrado

    def redraw(self):
        self.draw_scene()

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
        self.draw_axes(self.winfo_reqwidth(), self.winfo_reqheight()) #Desenhar eixos X e Y

        # Desenha os pontos armazenados na lista
        glBegin(GL_POINTS)
        glColor3f(1.0, 0, 0)
        for point in self.points:
            glVertex2f(point[0], point[1])
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

    def draw_axes3d(self, width, height,depth): #Desenhar eixos X e Y 
        glBegin(GL_LINES)
        glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo x
        glVertex3f(-width/2, 0.0, 0.0)
        glVertex3f(width/2, 0.0, 0.0)
        glColor3f(0.30, 0.30, 0.30)  # Cor para o eixo y
        glVertex3f(0.0, -height/2, 0.0)
        glVertex3f(0.0, height/2, 0.0)
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
            #self.draw_pixel(round(x), round(y))
    
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
            
            while y > yEnd:
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

    def linePoliElip(self, rx, ry,centro):
        x = 0
        y = ry
        # Inicializa o parâmetro de decisão para a Região 1
        d1 = (ry**2) - (rx**2 * ry) + (0.25 * rx**2)
        dx = 2 * (ry**2) * x
        dy = 2 * (rx**2) * y

        # Desenha os pontos na Região 1
        self.pontosElipse(x, y,centro)
        while dx < dy:
            if d1 < 0:
                x += 1
                dx += 2 * (ry**2)
                d1 += dx + (ry**2)
            else:
                x += 1
                y -= 1
                dx += 2 * (ry**2)
                dy -= 2 * (rx**2)
                d1 += dx - dy + (ry**2)
            self.pontosElipse(x, y,centro)

    def pontosElipse(self, x, y,centro):
        cx= centro
        cy = centro  # O centro da elipse
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

    def translacao(self, tx, ty):
        
        self.square_points_list = Translacao.realizar_translacao(self.square_points_list, tx, ty)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado transladado
        self.draw_square(*self.square_points_list)
    
    def rotacao(self, angle):
        
        self.square_points_list = Rotacao.realizar_rotacao(self.square_points_list, angle)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
    def cisalhamento(self, a, b):

        self.square_points_list = Cisalhamento.realizar_cisalhamento(self.square_points_list, a, b)

        #Remove o quadrado anterior
        self.points = []

        #Desenha o novo quadrado rotacionado
        self.draw_square(*self.square_points_list)
    
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
    def draw_cube(self, point1, point2, point3, point4,point5, point6, point7, point8):
        self.DDA(point1[0], point1[1], point2[0], point2[1])
        self.DDA(point2[0], point2[1], point3[0], point3[1])
        self.DDA(point3[0], point3[1], point4[0], point4[1])
        self.DDA(point4[0], point4[1], point1[0], point1[1])

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
        self.animate = 0
        if hasattr(self, '_after_id') and self._after_id:
            try:
                self.after_cancel(self._after_id)
            except ValueError:
                pass  # Ignore if the after_id is invalid
        self.update_idletasks()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        super().destroy()            
        
    


