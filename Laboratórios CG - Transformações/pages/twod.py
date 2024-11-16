import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class TwoDimensionsScreen:
    def __init__(self, window: tk.Tk, ogl_frame) -> None:
        self.frame = tk.Frame(window, width=300, height=600)
        self.frame.configure(background="#000C66")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        entry_tamanho = ctk.CTkEntry(self.frame, placeholder_text="size", height=10, width=40)
        entry_tamanho.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        lbl_tamanho = tk.Label(self.frame, background="#000C66")
        lbl_tamanho.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")
        btn_desenhar_quadrado = tk.Button(self.frame, text="Desenhar Quadrado", command=lambda: ogl_frame.square_points(int(entry_tamanho.get())) if entry_tamanho.get() else 0 )
        btn_desenhar_quadrado.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator de escala Sx
        entry_sx = ctk.CTkEntry(self.frame, placeholder_text="sx", height=10, width=40)
        entry_sx.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator de escala Sy
        entry_sy = ctk.CTkEntry(self.frame, placeholder_text="sy", height=10, width=40)
        entry_sy.grid(row=3, column=2, padx=6, pady=6, sticky="nsew")

        # Botão para Escala
        btn_scale = tk.Button(self.frame, text="Aplicar Escala", command=lambda: ogl_frame.escala(float(entry_sx.get()), float(entry_sy.get())) if entry_sx.get() and entry_sy.get() else 0 )
        btn_scale.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Translação Tx
        entry_tx = ctk.CTkEntry(self.frame, placeholder_text="Tx", height=10, width=40)
        entry_tx.grid(row=4, column=1, padx=5, pady=15, sticky="nsew")

        # Caixa de entrada para Translação Ty
        entry_ty = ctk.CTkEntry(self.frame, placeholder_text="Ty", height=10, width=40)
        entry_ty.grid(row=4, column=2, padx=5, pady=15, sticky="nsew")

        # Botão para Translação
        btn_translate = tk.Button(self.frame, text="Aplicar Translação", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())) if entry_tx.get() and entry_ty.get() else 0 )
        btn_translate.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Rotacao
        entry_rot = ctk.CTkEntry(self.frame, placeholder_text="ang", height=10, width=40)
        entry_rot.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        lbl_rot = tk.Label(self.frame, background="#000C66")
        lbl_rot.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Botão para Rotação
        btn_rotate = tk.Button(self.frame, text="Aplicar Rotação", command=lambda: ogl_frame.rotacao(int(entry_rot.get())) if entry_rot.get() else 0 )
        btn_rotate.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator A de cisalhamento
        entry_a = ctk.CTkEntry(self.frame, placeholder_text="a", height=10, width=40)
        entry_a.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator B de cisalhamento
        entry_b = ctk.CTkEntry(self.frame, placeholder_text="b", height=10, width=40)
        entry_b.grid(row=6, column=2, padx=5, pady=5, sticky="nsew")

        # Botão para Cisalhamento
        btn_shear = tk.Button(self.frame, text="Aplicar Cisalhamento", command=lambda: ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
        btn_shear.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

        # Botões para Reflexão
        btn_refx = tk.Button(self.frame, text="Ref X", command=lambda: ogl_frame.reflexaoX())
        btn_refx.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        btn_refy = tk.Button(self.frame, text="Ref Y", command=lambda: ogl_frame.reflexaoY())
        btn_refy.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")

        btn_reforigem = tk.Button(self.frame, text="Ref Origem", command=lambda: ogl_frame.reflexaoOrigem())
        btn_reforigem.grid(row=8, column=1, padx=5, pady=6, sticky="nsew")

        btn_ref45 = tk.Button(self.frame, text="Ref Reta 45", command=lambda: ogl_frame.reflexao45())
        btn_ref45.grid(row=8, column=2, padx=5, pady=7, sticky="nsew")

    def hide(self):
        self.frame.pack_forget()
    
    def show(self):
        self.frame.pack()
