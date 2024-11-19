import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
from opengl_frame import AppOgl


class FloatEntry(ctk.CTkEntry):
    def __init__(self, master=None, default=1.0, **kwargs):
        # Define a validação
        self.vcmd = (master.register(self.validate), '%P', '%d')
        super().__init__(master, validate='key', validatecommand=self.vcmd, **kwargs)
        
        # Valor padrão é 0.0
        self.insert(0, str(default))
    
    def validate(self, new_value, action_type):
        # Permite campo vazio ou apenas o ponto decimal
        if new_value == "" or new_value == ".":
            return True
            
        # Verifica se é um número flutuante válido
        try:
            # Verifica se não tem múltiplos pontos decimais
            if new_value.count('.') > 1:
                return False
                
            # Se não for operação de deleção, tenta converter para float
            if action_type != '0':  # '0' é o código para deleção
                float(new_value)
            return True
        except ValueError:
            return False
    
    def get_value(self):
        """Retorna o valor como float"""
        try:
            return float(self.get())
        except ValueError:
            return 0.0

class ViewportWindow:
    def __init__(self, parent_window):
        self.window = tk.Toplevel(parent_window)
        self.window.title("Viewport")
        self.window.geometry("800x600")
        
        # Container principal
        self.container = tk.Frame(self.window)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Frame para controles (esquerda)
        self.control_frame = tk.Frame(self.container, bg="#000C66")
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Frame para viewport (direita)
        self.viewport_frame = tk.Frame(self.container)
        self.viewport_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_controls()
        self.create_viewport()
        
        # Inicialmente esconder a janela
        self.window.withdraw()
        
    def create_controls(self):
        # Viewport Settings
        tk.Label(self.control_frame, text="Viewport Settings", 
                bg="#000C66", fg="white").pack(pady=5)
        
        # Width
        tk.Label(self.control_frame, text="Width:", 
                bg="#000C66", fg="white").pack()
        self.width_entry = FloatEntry(self.control_frame, 200, 
                                    placeholder_text="width", height=10, width=100)
        self.width_entry.pack(pady=2)
        
        # Height
        tk.Label(self.control_frame, text="Height:", 
                bg="#000C66", fg="white").pack()
        self.height_entry = FloatEntry(self.control_frame, 200, 
                                     placeholder_text="height", height=10, width=100)
        self.height_entry.pack(pady=2)
        
        # World Coordinates
        tk.Label(self.control_frame, text="\nWorld Coordinates", 
                bg="#000C66", fg="white").pack(pady=5)
        
        # X range
        tk.Label(self.control_frame, text="X min:", 
                bg="#000C66", fg="white").pack()
        self.xmin_entry = FloatEntry(self.control_frame, -100, 
                                   placeholder_text="xmin", height=10, width=100)
        self.xmin_entry.pack(pady=2)
        
        tk.Label(self.control_frame, text="X max:", 
                bg="#000C66", fg="white").pack()
        self.xmax_entry = FloatEntry(self.control_frame, 100, 
                                   placeholder_text="xmax", height=10, width=100)
        self.xmax_entry.pack(pady=2)
        
        # Y range
        tk.Label(self.control_frame, text="Y min:", 
                bg="#000C66", fg="white").pack()
        self.ymin_entry = FloatEntry(self.control_frame, -100, 
                                   placeholder_text="ymin", height=10, width=100)
        self.ymin_entry.pack(pady=2)
        
        tk.Label(self.control_frame, text="Y max:", 
                bg="#000C66", fg="white").pack()
        self.ymax_entry = FloatEntry(self.control_frame, 100, 
                                   placeholder_text="ymax", height=10, width=100)
        self.ymax_entry.pack(pady=2)
        
        # Apply button
        tk.Button(self.control_frame, text="Apply Settings", 
                 command=self.apply_settings).pack(pady=10)
        
    def create_viewport(self):
        self.viewport = ViewportDisplay(self.viewport_frame)
        self.viewport.pack(fill=tk.BOTH, expand=True)
        
    def apply_settings(self):
        try:
            width = self.width_entry.get_value()
            height = self.height_entry.get_value()
            xmin = self.xmin_entry.get_value()
            xmax = self.xmax_entry.get_value()
            ymin = self.ymin_entry.get_value()
            ymax = self.ymax_entry.get_value()
            
            self.viewport.update_settings(width, height, xmin, xmax, ymin, ymax)
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers")
    
    def show(self):
        self.window.deiconify()
        self.viewport.draw_world_object(self.viewport.points)
        
    def hide(self):
        self.window.withdraw()
        
    def update_viewport(self, points):
        """Update viewport with new points"""
        if hasattr(self, 'viewport'):
            self.viewport.draw_world_object(points)

class ViewportDisplay(AppOgl):
    def __init__(self, parent):
        super().__init__(parent, width=200, height=200)
        # Viewport properties
        self.viewport_width = 200
        self.viewport_height = 200
        self.world_left = -100
        self.world_right = 100
        self.world_bottom = -100
        self.world_top = 100
        
        # Override animation
        self.initialised = False
        self.animate = 0
        
        # Current object points
        self.current_points = []
        
    def initgl(self):
        """Inicializa o ambiente OpenGL específico para a viewport"""
        self._after_id = None
        glClearColor(0.7, 0.7, 0.7, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # Configurar para coordenadas da viewport
        glOrtho(self.world_left, self.world_right, 
                self.world_bottom, self.world_top, -1.0, 1.0)
        
        self.points = []
        self.square_points_list = []
        self.initialised = True
        self.redraw()

    def make_current(self):
        """Torna este contexto OpenGL o atual"""
        if not hasattr(self, 'context'):
            self.context = self.tk.call('winfo', 'id', self._w)
        self.tk.call('winfo', 'id', self._w)

    def setup_viewport(self):
        """Configura a viewport e a projeção"""
        self.make_current()
        
        try:
            # Define a viewport para usar toda a área disponível
            glViewport(0, 0, self.viewport_width, self.viewport_height)
            
            # Configura a projeção para mapear diretamente as coordenadas do mundo
            # para a viewport, permitindo distorção
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(self.world_left, self.world_right,
                    self.world_bottom, self.world_top, -1, 1)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
        finally:
            self.release_current()

    def bit(self, codigo, pos):
        """Obtém o bit na posição especificada"""
        bit = (codigo << (31 - pos)) & 0xFFFFFFFF
        bit = bit >> 31
        return bit & 1

    def obter_codigo(self, x, y, xmin, ymin, xmax, ymax):
        """Calcula o código de região do ponto"""
        codigo = 0
        
        if x < xmin:  # Esquerda
            codigo |= 1
        if x > xmax:  # Direita
            codigo |= 2
        if y < ymin:  # Baixo
            codigo |= 4
        if y > ymax:  # Topo
            codigo |= 8
            
        return codigo

    def cohen_sutherland(self, x1, y1, x2, y2, xmin, ymin, xmax, ymax):
        """Implementação corrigida do algoritmo de Cohen-Sutherland"""
        aceito = False
        pronto = False
        
        # Obter códigos iniciais
        codigo1 = self.obter_codigo(x1, y1, xmin, ymin, xmax, ymax)
        codigo2 = self.obter_codigo(x2, y2, xmin, ymin, xmax, ymax)
        
        while not pronto:
            # Se ambos os pontos estão dentro, aceita a linha
            if (codigo1 | codigo2) == 0:
                aceito = True
                pronto = True
            # Se ambos os pontos compartilham um código fora, rejeita a linha
            elif (codigo1 & codigo2) != 0:
                pronto = True
            else:
                # Linha precisa ser recortada
                # Pega o ponto que está fora
                codigo_fora = codigo1 if codigo1 != 0 else codigo2
                
                # Encontra o ponto de interseção
                if codigo_fora & 1:  # Ponto está à esquerda
                    x = xmin
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                elif codigo_fora & 2:  # Ponto está à direita
                    x = xmax
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                elif codigo_fora & 4:  # Ponto está abaixo
                    y = ymin
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                else:  # Ponto está acima
                    y = ymax
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                
                # Substitui o ponto e recalcula o código
                if codigo_fora == codigo1:
                    x1, y1 = x, y
                    codigo1 = self.obter_codigo(x1, y1, xmin, ymin, xmax, ymax)
                else:
                    x2, y2 = x, y
                    codigo2 = self.obter_codigo(x2, y2, xmin, ymin, xmax, ymax)
        
        if aceito:
            return (x1, y1, x2, y2)
        return None


    def clip_line(self, p1, p2):
        """Aplica recorte em uma linha"""
        result = self.cohen_sutherland(
            p1[0], p1[1], p2[0], p2[1],
            self.world_left, self.world_bottom,
            self.world_right, self.world_top
        )
        return result

    def redraw(self):
        """Redesenha a cena OpenGL"""
        if not hasattr(self, 'initialised') or not self.initialised:
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Desenha os eixos
        self.draw_axes(self.viewport_width, self.viewport_height)
        
        # Desenha a área de recorte (janela do mundo)
        glColor3f(1.0, 1.0, 1.0)  # Branco
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.world_left, self.world_bottom)
        glVertex2f(self.world_right, self.world_bottom)
        glVertex2f(self.world_right, self.world_top)
        glVertex2f(self.world_left, self.world_top)
        glEnd()
        
        # Desenha o objeto recortado
        if self.points:
            glBegin(GL_LINES)
            glColor3f(1.0, 1.0, 0.0)  # Amarelo
            for i in range(0, len(self.points), 2):
                if i + 1 < len(self.points):
                    glVertex2f(self.points[i][0], self.points[i][1])
                    glVertex2f(self.points[i+1][0], self.points[i+1][1])
            glEnd()
        
        self.update()
    
    def update_settings(self, width, height, left, right, bottom, top):
        """Atualiza as configurações da viewport"""
        self.viewport_width = int(width)
        self.viewport_height = int(height)
        self.world_left = left
        self.world_right = right
        self.world_bottom = bottom
        self.world_top = top
        
        # Atualiza o tamanho da janela
        # self.configure(width=self.viewport_width, height=self.viewport_height)
        
        #if hasattr(self, 'initialised') and self.initialised:
            # Reconfigura a viewport com as novas dimensões
            #self.setup_viewport()
            
            # Redesenha o objeto se existir
        if self.current_points:
            self.draw_world_object(self.current_points)

    def transform_points(self, world_points):
        """Transforma pontos do mundo para coordenadas da viewport"""
        if not world_points:
            return []
            
        viewport_points = []
        for point in world_points:
            # Primeiro aplica o recorte
            clipped_points = []
            n = len(world_points)
            for i in range(n):
                p1 = world_points[i]
                p2 = world_points[(i + 1) % n]
                
                clipped = self.clip_line(p1, p2)
                if clipped:
                    x1, y1, x2, y2 = clipped
                    clipped_points.extend([(x1, y1), (x2, y2)])
            
            # Depois transforma para coordenadas da viewport
            for point in clipped_points:
                # Normaliza as coordenadas
                nx = (point[0] - self.world_left) / (self.world_right - self.world_left)
                ny = (point[1] - self.world_bottom) / (self.world_top - self.world_bottom)
                
                # Mapeia para coordenadas da viewport
                vx = nx * self.viewport_width
                vy = ny * self.viewport_height
                
                viewport_points.append((vx, vy))
                
        return viewport_points


    def draw_world_object(self, points):
        """Desenha objeto usando coordenadas do mundo com recorte"""
        if not points:
            return
            
        self.current_points = points.copy()
        self.points = []
        
        # Aplica recorte em cada linha do objeto
        for i in range(0, len(points), 2):
            if i + 1 < len(points):
                p1 = points[i]
                p2 = points[i + 1]
                
                # Aplica o algoritmo de recorte
                clipped = self.cohen_sutherland(
                    p1[0], p1[1], p2[0], p2[1],
                    self.world_left, self.world_bottom,
                    self.world_right, self.world_top
                )
                
                if clipped:
                    x1, y1, x2, y2 = clipped
                    self.points.extend([(x1, y1), (x2, y2)])
        
        self.redraw()