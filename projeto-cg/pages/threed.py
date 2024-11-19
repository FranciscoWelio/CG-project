from .utils import FloatEntry, IntEntry
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class ThreeDimensionsScreen:
    def __init__(self, window: tk.Tk) -> None:
        self.active = False
        self.window = window
        
        # Frame principal para conter o canvas e scrollbar
        self.main_frame = ttk.Frame(self.window)
        
        # Canvas e Scrollbar para permitir rolagem
        self.canvas = tk.Canvas(self.main_frame, background='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        
        # Frame para conter os controles
        self.frame = ttk.Frame(self.canvas, width=300)
        self.frame_right = ttk.Frame(self.window, width=700)
        
        # Configurar o canvas
        self.frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Control.TLabelframe', background='#f0f0f0', padding=5)
        self.style.configure('TButton', padding=3)
        self.style.configure('TLabel', background='#f0f0f0', padding=2)

    def create_labeled_entry(self, parent, label, width=10):
        """Criar uma entrada com label"""
        container = ttk.Frame(parent)
        container.pack(fill='x', padx=2, pady=2)
        ttk.Label(container, text=label).pack(side='left', padx=2)
        entry = ctk.CTkEntry(container, height=25, width=width)
        entry.pack(side='right', padx=2)
        return entry

    def create_widgets(self):
        # OpenGL Frame
        self.ogl_frame = AppOgl(self.frame_right, width=700, height=600, threed=True)
        self.ogl_frame.pack(fill=tk.BOTH, expand=True)
        self.ogl_frame.animate = 1

        # === Seção Cubo ===
        cubo_frame = ttk.LabelFrame(self.frame, text="Cubo", padding=5)
        cubo_frame.pack(fill='x', padx=5, pady=2)
        
        entry_tamanho_3d = self.create_labeled_entry(cubo_frame, "Tamanho:", 60)
        ttk.Button(cubo_frame, text="Desenhar Cubo", 
                  command=lambda: self.ogl_frame.cube_points(int(entry_tamanho_3d.get()))).pack(pady=2)

        # === Seção Escala ===
        escala_frame = ttk.LabelFrame(self.frame, text="Escala", padding=5)
        escala_frame.pack(fill='x', padx=5, pady=2)
        
        entry_sx = self.create_labeled_entry(escala_frame, "X:", 60)
        entry_sy = self.create_labeled_entry(escala_frame, "Y:", 60)
        entry_sz = self.create_labeled_entry(escala_frame, "Z:", 60)
        ttk.Button(escala_frame, text="Aplicar Escala", 
                  command=lambda: self.ogl_frame.escala3D(float(entry_sx.get()), 
                                                        float(entry_sy.get()), 
                                                        float(entry_sz.get()))).pack(pady=2)

        # === Seção Translação ===
        translacao_frame = ttk.LabelFrame(self.frame, text="Translação", padding=5)
        translacao_frame.pack(fill='x', padx=5, pady=2)
        
        entry_tx = self.create_labeled_entry(translacao_frame, "X:", 60)
        entry_ty = self.create_labeled_entry(translacao_frame, "Y:", 60)
        entry_tz = self.create_labeled_entry(translacao_frame, "Z:", 60)
        ttk.Button(translacao_frame, text="Aplicar Translação",
                  command=lambda: self.ogl_frame.translacao3D(int(entry_tx.get()), 
                                                           int(entry_ty.get()), 
                                                           int(entry_tz.get()))).pack(pady=2)

        # === Seção Rotação ===
        rotacao_frame = ttk.LabelFrame(self.frame, text="Rotação", padding=5)
        rotacao_frame.pack(fill='x', padx=5, pady=2)
        
        controls_frame = ttk.Frame(rotacao_frame)
        controls_frame.pack(fill='x', pady=2)
        
        selected_option = tk.StringVar(value="em x")
        ttk.Label(controls_frame, text="Eixo:").pack(side='left', padx=2)
        ttk.Radiobutton(controls_frame, text="X", value="em x", 
                       variable=selected_option).pack(side='left', padx=2)
        ttk.Radiobutton(controls_frame, text="Y", value="em y", 
                       variable=selected_option).pack(side='left', padx=2)
        ttk.Radiobutton(controls_frame, text="Z", value="em z", 
                       variable=selected_option).pack(side='left', padx=2)
        
        angle_frame = ttk.Frame(rotacao_frame)
        angle_frame.pack(fill='x', pady=2)
        ttk.Label(angle_frame, text="Ângulo:").pack(side='left', padx=2)
        angle_entry = ttk.Entry(angle_frame, width=10)
        angle_entry.pack(side='left', padx=2)
        angle_entry.insert(0, "0")
        
        ttk.Button(rotacao_frame, text="Aplicar Rotação",
                  command=lambda: self.ogl_frame.rotacao3D(selected_option.get(), 
                                                        int(angle_entry.get()))).pack(pady=2)

        # === Seção Cisalhamento ===
        cisalhamento_frame = ttk.LabelFrame(self.frame, text="Cisalhamento", padding=5)
        cisalhamento_frame.pack(fill='x', padx=5, pady=2)
        
        entry_a = self.create_labeled_entry(cisalhamento_frame, "Em Z:", 60)
        entry_b = self.create_labeled_entry(cisalhamento_frame, "Em Y:", 60)
        entry_c = self.create_labeled_entry(cisalhamento_frame, "Em X:", 60)
        ttk.Button(cisalhamento_frame, text="Aplicar Cisalhamento",
                  command=lambda: self.ogl_frame.cisalhamento3D(int(entry_a.get()), 
                                                             -int(entry_b.get()),
                                                             int(entry_c.get()))).pack(pady=2)

        # === Seção Reflexão ===
        reflexao_frame = ttk.LabelFrame(self.frame, text="Reflexão", padding=5)
        reflexao_frame.pack(fill='x', padx=5, pady=2)
        
        controls_refl = ttk.Frame(reflexao_frame)
        controls_refl.pack(fill='x', pady=2)
        
        selected_option_refl = tk.StringVar(value="em xy")
        ttk.Label(controls_refl, text="Plano:").pack(side='left', padx=2)
        ttk.Radiobutton(controls_refl, text="XY", value="em xy", 
                       variable=selected_option_refl).pack(side='left', padx=2)
        ttk.Radiobutton(controls_refl, text="YZ", value="em yz", 
                       variable=selected_option_refl).pack(side='left', padx=2)
        ttk.Radiobutton(controls_refl, text="XZ", value="em xz", 
                       variable=selected_option_refl).pack(side='left', padx=2)
        
        buttons_frame = ttk.Frame(reflexao_frame)
        buttons_frame.pack(fill='x', pady=2)
        
        ttk.Button(buttons_frame, text="Aplicar Reflexão",
                  command=lambda: self.ogl_frame.reflexao3D(selected_option_refl.get())).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Reflexão na Origem",
                  command=self.ogl_frame.reflexaoOrigem).pack(side='left', padx=2)
        ttk.Button(buttons_frame, text="Reflexão 45°",
                  command=self.ogl_frame.reflexao45).pack(side='left', padx=2)
        
        # === Seção Aplicaro Todos ===
        Composicao_frame = ttk.LabelFrame(self.frame, text="Aplicar Transformações", padding=5)
        Composicao_frame.pack(fill='x', padx=5, pady=2)
        
        controls_compo = ttk.Frame(Composicao_frame)
        controls_compo.pack(fill='x', pady=2)
        
        buttonsCompo_frame = ttk.Frame(Composicao_frame)
        buttonsCompo_frame.pack(fill='x', pady=2)
        
        ttk.Button(buttonsCompo_frame, text="Aplicar Composição",
                  command=lambda: [self.ogl_frame.translacao3D(-int(entry_tx.get()), -int(entry_ty.get()), -int(entry_tz.get())),
                                    self.ogl_frame.escala3D(float(entry_sx.get()), float(entry_sy.get()), float(entry_sz.get())),
                                    self.ogl_frame.rotacao3D(selected_option.get(),int(angle_entry.get())),
                                    self.ogl_frame.cisalhamento3D(int(entry_a.get()), -int(entry_b.get()),int(entry_c.get())),
                                    self.ogl_frame.reflexao3D(selected_option_refl.get()),
                                    self.ogl_frame.translacao3D(int(entry_tx.get()), int(entry_ty.get()), int(entry_tz.get()))]).pack(side='left', padx=2)


    def hide(self):
        if self.active:
            self.active = False
            if hasattr(self, 'ogl_frame'):
                self.ogl_frame.destroy()
            
            self.main_frame.pack_forget()
            self.frame_right.pack_forget()
            
            if hasattr(self, 'ogl_frame'):
                delattr(self, 'ogl_frame')
    
    def show(self):
        if not self.active:
            self.active = True
            self.create_widgets()
            
            # Configurar layout dos frames principais
            self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)