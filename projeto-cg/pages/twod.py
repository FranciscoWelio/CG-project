import math
from .utils import FloatEntry
from tkinter import ttk
import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl
from viewport import ViewportWindow


class TwoDimensionsScreen:
    def __init__(self, window: tk.Tk) -> None:
        self.active = False
        self.window = window
        
        # Frame principal que conterá todos os elementos
        self.main_container = ttk.Frame(self.window)
        

    def create_labeled_entry(self, parent, label, default_value=0, width=60):
        """Criar uma entrada com label"""
        container = ttk.Frame(parent)
        container.pack(fill='x', padx=2, pady=2)
        ttk.Label(container, text=label).pack(side='left', padx=2)
        entry = FloatEntry(container, default_value, height=25, width=width)
        entry.pack(side='right', padx=2)
        return entry

    def create_widgets(self):
        self.window.update()
        # Create viewport window
        self.viewport_window = ViewportWindow(self.window)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Frame esquerdo para controles (menu lateral)
        self.controls_frame = ttk.Frame(self.main_container, width=300)
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.controls_frame.pack_propagate(False)  # Mantém o tamanho fixo
        
        # Frame direito para a área de desenho OpenGL
        self.right_container = ttk.Frame(self.main_container)
        self.right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Criar canvas de rolagem
        self.canvas = tk.Canvas(self.controls_frame, width=280, background='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.controls_frame, orient="vertical", command=self.canvas.yview)
        
        # Frame interno do canvas
        self.inner_frame = ttk.Frame(self.canvas)
        
        # Configurar canvas
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw', width=280)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Posicionar canvas e scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para atualizar scroll
        self.inner_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Control.TLabelframe', background='#f0f0f0', padding=5)
        self.style.configure('TButton', padding=3)
        self.style.configure('TLabel', background='#f0f0f0', padding=2)
        # OpenGL Frame
        self.ogl_frame = AppOgl(self.right_container, width=700, height=600)
        self.ogl_frame.pack(fill=tk.BOTH, expand=True)
        self.ogl_frame.animate = 1

        # === Botão Viewport ===
        viewport_frame = ttk.LabelFrame(self.inner_frame, text="Viewport", padding=5)
        viewport_frame.pack(fill='x', padx=5, pady=2)
        ttk.Button(viewport_frame, text="Toggle Viewport", 
                  command=self.toggle_viewport).pack(fill='x', pady=2)

        # === Seção Quadrado ===
        quadrado_frame = ttk.LabelFrame(self.inner_frame, text="Quadrado", padding=5)
        quadrado_frame.pack(fill='x', padx=5, pady=2)
        
        entry_tamanho = self.create_labeled_entry(quadrado_frame, "Tamanho:", 100)
        entry_pos_x = self.create_labeled_entry(quadrado_frame, "Posição X:", 0)
        entry_pos_y = self.create_labeled_entry(quadrado_frame, "Posição Y:", 0)
        
        def draw_square():
            self.ogl_frame.square_points(entry_tamanho.get_value())
            self.ogl_frame.translacao(entry_pos_x.get_value(), entry_pos_y.get_value())
            self.viewport_window.update_viewport(self.ogl_frame.points)
        
        ttk.Button(quadrado_frame, text="Desenhar Quadrado", 
                  command=draw_square).pack(fill='x', pady=2)

        # === Seção Escala ===
        escala_frame = ttk.LabelFrame(self.inner_frame, text="Escala", padding=5)
        escala_frame.pack(fill='x', padx=5, pady=2)
        
        entry_sx = self.create_labeled_entry(escala_frame, "X:", 1)
        entry_sy = self.create_labeled_entry(escala_frame, "Y:", 1)
        
        ttk.Button(escala_frame, text="Aplicar Escala", 
                  command=lambda: [
                      self.ogl_frame.escala(entry_sx.get_value(), entry_sy.get_value()),
                      self.viewport_window.update_viewport(self.ogl_frame.points)
                  ]).pack(fill='x', pady=2)

        # === Seção Translação ===
        translacao_frame = ttk.LabelFrame(self.inner_frame, text="Translação", padding=5)
        translacao_frame.pack(fill='x', padx=5, pady=2)
        
        entry_tx = self.create_labeled_entry(translacao_frame, "X:", 0)
        entry_ty = self.create_labeled_entry(translacao_frame, "Y:", 0)
        
        ttk.Button(translacao_frame, text="Aplicar Translação",
                  command=lambda: [
                      self.ogl_frame.translacao(entry_tx.get_value(), entry_ty.get_value()),
                      self.viewport_window.update_viewport(self.ogl_frame.points)
                  ]).pack(fill='x', pady=2)

        # === Seção Rotação ===
        rotacao_frame = ttk.LabelFrame(self.inner_frame, text="Rotação", padding=5)
        rotacao_frame.pack(fill='x', padx=5, pady=2)
        
        entry_rot = self.create_labeled_entry(rotacao_frame, "Ângulo:", 0)
        
        ttk.Button(rotacao_frame, text="Aplicar Rotação",
                  command=lambda: [
                      self.ogl_frame.rotacao(entry_rot.get_value()),
                      self.viewport_window.update_viewport(self.ogl_frame.points)
                  ]).pack(fill='x', pady=2)

        # === Seção Cisalhamento ===
        cisalhamento_frame = ttk.LabelFrame(self.inner_frame, text="Cisalhamento", padding=5)
        cisalhamento_frame.pack(fill='x', padx=5, pady=2)
        
        entry_a = self.create_labeled_entry(cisalhamento_frame, "A:", 0)
        entry_b = self.create_labeled_entry(cisalhamento_frame, "B:", 0)
        
        ttk.Button(cisalhamento_frame, text="Aplicar Cisalhamento",
                  command=lambda: [
                      self.ogl_frame.cisalhamento(entry_a.get_value(), entry_b.get_value()),
                      self.viewport_window.update_viewport(self.ogl_frame.points)
                  ]).pack(fill='x', pady=2)

        # === Seção Reflexão ===
        reflexao_frame = ttk.LabelFrame(self.inner_frame, text="Reflexão", padding=5)
        reflexao_frame.pack(fill='x', padx=5, pady=2)
        
        buttons_frame = ttk.Frame(reflexao_frame)
        buttons_frame.pack(fill='x', pady=2)
        
        ttk.Button(buttons_frame, text="Reflexão X",
                  command=lambda: self.ogl_frame.reflexaoX()).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Reflexão Y",
                  command=lambda: self.ogl_frame.reflexaoY()).pack(side='left', padx=2)
        
        buttons_frame2 = ttk.Frame(reflexao_frame)
        buttons_frame2.pack(fill='x', pady=2)
        
        ttk.Button(buttons_frame2, text="Reflexão na Origem",
                  command=lambda: self.ogl_frame.reflexaoOrigem()).pack(side='left', padx=2)
        ttk.Button(buttons_frame2, text="Reflexão 45°",
                  command=lambda: self.ogl_frame.reflexao45()).pack(side='left', padx=2)

        # === Seção Reflexão em Reta ===
        reta_frame = ttk.LabelFrame(self.inner_frame, text="Reflexão em Reta", padding=5)
        reta_frame.pack(fill='x', padx=5, pady=2)
        
        retaA = self.create_labeled_entry(reta_frame, "A:", 0)
        retaB = self.create_labeled_entry(reta_frame, "B:", 0)
        
        def reflexao_reta():
            a = retaA.get_value()
            b = retaB.get_value()
            thetaCosA = (1/math.sqrt((a**2)+1))
            thetaSinA = (a/math.sqrt((a**2)+1))
            self.ogl_frame.translacao(0, -b)
            self.ogl_frame.rotacaoReta(thetaCosA,-thetaSinA)
            self.ogl_frame.reflexaoX()
            self.ogl_frame.rotacaoReta(thetaCosA,thetaSinA)
            self.ogl_frame.translacao(0, b)
            
        ttk.Button(reta_frame, text="Reflexão y = ax + b",
                  command=reflexao_reta).pack(fill='x', pady=2)

        # === Seção Aplicar Todas ===
        todas_frame = ttk.LabelFrame(self.inner_frame, text="Aplicar Todas", padding=5)
        todas_frame.pack(fill='x', padx=5, pady=2)
        
        def aplicar_todas():
            self.ogl_frame.translacao(-entry_pos_x.get_value(), -entry_pos_y.get_value())
            self.ogl_frame.translacao(entry_tx.get_value(), entry_ty.get_value())
            self.ogl_frame.escala(entry_sx.get_value(), entry_sy.get_value())
            self.ogl_frame.rotacao(entry_rot.get_value())
            self.ogl_frame.cisalhamento(entry_a.get_value(), entry_b.get_value())
            self.ogl_frame.translacao(entry_pos_x.get_value(), entry_pos_y.get_value())
            
        ttk.Button(todas_frame, text="Aplicar Todas Transformações",
                  command=aplicar_todas).pack(fill='x', pady=2)

    def toggle_viewport(self):
        if self.viewport_window.window.state() == 'withdrawn':
            self.viewport_window.show()
        else:
            self.viewport_window.hide()

    def hide(self):
        if self.active:
            self.active = False
            
            # Primeiro esconde a viewport se existir
            if hasattr(self, 'viewport_window') and self.viewport_window:
                self.viewport_window.hide()
                self.viewport_window = None
            
            # Remove o frame OpenGL primeiro
            if hasattr(self, 'ogl_frame'):
                self.ogl_frame.destroy()
                delattr(self, 'ogl_frame')
            
            # Depois remove os widgets internos
            if hasattr(self, 'inner_frame'):
                self.inner_frame.destroy()
            
            if hasattr(self, 'canvas'):
                self.canvas.destroy()
            
            if hasattr(self, 'scrollbar'):
                self.scrollbar.destroy()
            
            if hasattr(self, 'controls_frame'):
                self.controls_frame.destroy()
            
            if hasattr(self, 'right_container'):
                self.right_container.destroy()
            
            # Por último, remove o container principal
            if hasattr(self, 'main_container'):
                self.main_container.pack_forget()
                # self.main_container.destroy()
    
    def show(self):
        if not self.active:
            self.active = True
            self.create_widgets()
            self.main_container.pack(side=tk.LEFT, fill=tk.BOTH)
            self.right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
