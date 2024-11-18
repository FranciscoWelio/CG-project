from .utils import FloatEntry, IntEntry
import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class TwoDimensionsScreen:
    def __init__(self, window: tk.Tk) -> None:
        self.active = False
        self.window = window
        self.frame = tk.Frame(self.window, width=300, height=600)
        self.frame.configure(background="#000C66")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        self.frame_right = tk.Frame(self.window, width=300, height=600)

    def create_widgets(self):
        self.ogl_frame = AppOgl(self.frame_right, width=700, height=600)
        self.ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
        self.ogl_frame.animate = 1
        entry_tamanho = FloatEntry(self.frame, 100, placeholder_text="size", height=10, width=40)
        entry_tamanho.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        entry_pos_x = FloatEntry(self.frame, 0, placeholder_text="x", height=10, width=40)
        entry_pos_x.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        entry_pos_y = FloatEntry(self.frame, 0, placeholder_text="y", height=10, width=40)
        entry_pos_y.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        lbl_tamanho = tk.Label(self.frame, background="#000C66")
        lbl_tamanho.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")
        btn_desenhar_quadrado = tk.Button(self.frame, text="Desenhar Quadrado", command=lambda: [self.ogl_frame.square_points(entry_tamanho.get_value()),self.ogl_frame.translacao(entry_pos_x.get_value(), entry_pos_y.get_value())])
        btn_desenhar_quadrado.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator de escala Sx
        entry_sx = FloatEntry(self.frame, 1, placeholder_text="sx", height=10, width=40)
        entry_sx.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator de escala Sy
        entry_sy = FloatEntry(self.frame, 1, placeholder_text="sy", height=10, width=40)
        entry_sy.grid(row=3, column=2, padx=6, pady=6, sticky="nsew")

        # Botão para Escala
        btn_scale = tk.Button(self.frame, text="Aplicar Escala", command=lambda: self.ogl_frame.escala(entry_sx.get_value(), entry_sy.get_value()))
        btn_scale.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Translação Tx
        entry_tx = FloatEntry(self.frame, 0, placeholder_text="Tx", height=10, width=40)
        entry_tx.grid(row=4, column=1, padx=5, pady=15, sticky="nsew")

        # Caixa de entrada para Translação Ty
        entry_ty = FloatEntry(self.frame, 0, placeholder_text="Ty", height=10, width=40)
        entry_ty.grid(row=4, column=2, padx=5, pady=15, sticky="nsew")

        # Botão para Translação
        btn_translate = tk.Button(self.frame, text="Aplicar Translação", command=lambda: self.ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())) if entry_tx.get() and entry_ty.get() else 0 )
        btn_translate.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Rotacao
        entry_rot = FloatEntry(self.frame, 0, placeholder_text="ang", height=10, width=40)
        entry_rot.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        lbl_rot = tk.Label(self.frame, background="#000C66")
        lbl_rot.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Botão para Rotação
        btn_rotate = tk.Button(self.frame, text="Aplicar Rotação", command=lambda: self.ogl_frame.rotacao(entry_rot.get_value()) )
        btn_rotate.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator A de cisalhamento
        entry_a = FloatEntry(self.frame, 0, placeholder_text="a", height=10, width=40)
        entry_a.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator B de cisalhamento
        entry_b = FloatEntry(self.frame, 0, placeholder_text="b", height=10, width=40)
        entry_b.grid(row=6, column=2, padx=5, pady=5, sticky="nsew")

        # Botão para Cisalhamento
        btn_shear = tk.Button(self.frame, text="Aplicar Cisalhamento", command=lambda: self.ogl_frame.cisalhamento(entry_a.get_value(), entry_b.get_value()))
        btn_shear.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

        # Botões para Reflexão
        btn_refx = tk.Button(self.frame, text="Ref X", command=lambda: self.ogl_frame.reflexaoX())
        btn_refx.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        btn_refy = tk.Button(self.frame, text="Ref Y", command=lambda: self.ogl_frame.reflexaoY())
        btn_refy.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

        btn_reforigem = tk.Button(self.frame, text="Ref Origem", command=lambda: self.ogl_frame.reflexaoOrigem())
        btn_reforigem.grid(row=8, column=1, padx=5, pady=6, sticky="nsew")

        btn_ref45 = tk.Button(self.frame, text="Ref Reta 45", command=lambda: self.ogl_frame.reflexao45())
        btn_ref45.grid(row=8, column=2, padx=5, pady=7, sticky="nsew")


        # Botões para Aplicar Todos
        btn_AplicarAll = tk.Button(self.frame, text="Aplicar Transformações", command=lambda: [self.ogl_frame.translacao(-entry_pos_x.get_value(), -entry_pos_y.get_value()), self.ogl_frame.escala(entry_sx.get_value(), entry_sy.get_value()), self.ogl_frame.rotacao(entry_rot.get_value()),self.ogl_frame.cisalhamento(entry_a.get_value(), entry_b.get_value()),self.ogl_frame.translacao(entry_pos_x.get_value(), entry_pos_y.get_value())])
        btn_AplicarAll.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")

    def hide(self):
        if self.active:
            self.active = False
            if hasattr(self, 'ogl_frame'):
                self.ogl_frame.destroy()
                self.ogl_frame.pack_forget()
            
            for widget in self.frame.winfo_children():
                widget.destroy()
            
            for widget in self.frame_right.winfo_children():
                widget.destroy()
            
            if hasattr(self, 'ogl_frame'):
                delattr(self, 'ogl_frame')
            
            self.frame.pack_forget()
            self.frame_right.pack_forget()
    
    def show(self):
        if not self.active:
            self.active = True
            self.create_widgets()
            self.frame.pack(side=tk.LEFT, fill=tk.BOTH)
            self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
