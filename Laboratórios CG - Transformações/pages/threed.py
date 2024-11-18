from .utils import FloatEntry, IntEntry
import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class ThreeDimensionsScreen:
    def __init__(self, window: tk.Tk) -> None:
        self.active = False
        self.window = window
        self.frame = tk.Frame(self.window, width=300, height=600)
        self.frame.configure(background="#000C66")
        
        self.frame_right = tk.Frame(self.window, width=300, height=600)

    def create_widgets(self):
        self.ogl_frame = AppOgl(self.frame_right, width=700, height=600, threed=True)
        self.ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
        self.ogl_frame.animate = 1
        # COMEÇO 3d
        # Caixa de entrada para o tamanho do quadrado
        entry_tamanho_3d = ctk.CTkEntry(self.frame, placeholder_text="size", height=10, width=40)
        entry_tamanho_3d.grid(row=2, column=1, sticky="nsew")

        lbl_tamanho_3d = tk.Label(self.frame, background="#000C66")
        lbl_tamanho_3d.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")
        
        # Botão para desenhar um quadrado
        btn_desenhar_quadrado_3d = tk.Button(self.frame, text="Desenhar Cubo", command=lambda: self.ogl_frame.cube_points(int(entry_tamanho_3d.get())))
        btn_desenhar_quadrado_3d.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        # Caixa de entrada para Fator de escala Sx
        entry_sx = ctk.CTkEntry(self.frame, placeholder_text="sx_3d", height=10, width=40)
        entry_sx.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

        # Caixa de entrada para Fator de escala Sy
        entry_sy = ctk.CTkEntry(self.frame, placeholder_text="sy_3d", height=10, width=40)
        entry_sy.grid(row=4, column=0, padx=2, pady=2, sticky="nsew")
        # Caixa de entrada para Fator de escala Sz
        entry_sz = ctk.CTkEntry(self.frame, placeholder_text="sz_3d", height=10, width=40)
        entry_sz.grid(row=4, column=1, padx=6, pady=6, sticky="nsew")

        # Botão para Escala
        btn_scale_3d = tk.Button(self.frame, text="Aplicar Escala_3d", command=lambda: self.ogl_frame.escala3D(float(entry_sx.get()), float(entry_sy.get()), float(entry_sz.get())))
        btn_scale_3d.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Translação Tx
        entry_tx = IntEntry(self.frame, 0, placeholder_text="Tx_3d", height=10, width=40)
        entry_tx.grid(row=5, column=1, padx=5, pady=15, sticky="nsew")

        # Caixa de entrada para Translação Ty
        entry_ty = IntEntry(self.frame, 0, placeholder_text="Ty_3d", height=10, width=40)
        entry_ty.grid(row=6, column=0, padx=5, pady=15, sticky="nsew")
        # Caixa de entrada para Translação Tz
        entry_tz = IntEntry(self.frame, 0, placeholder_text="Tz_3d", height=10, width=40)
        entry_tz.grid(row=6, column=1, padx=5, pady=15, sticky="nsew")

        # Botão para Translação
        btn_translate_3d = tk.Button(self.frame, text="Aplicar Translação_3d", command=lambda: self.ogl_frame.translacao3D(entry_tx.get_value(), entry_ty.get_value(), entry_tz.get()))
        btn_translate_3d.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Rotacao
        entry_rot_x = ctk.CTkEntry(self.frame, placeholder_text="ang_3dX", height=10, width=40)
        entry_rot_x.grid(row=7, column=1, padx=5, pady=2, sticky="nsew")
        entry_rot_y = ctk.CTkEntry(self.frame, placeholder_text="ang_3dY", height=10, width=40)
        entry_rot_y.grid(row=8, column=0, padx=5, pady=2, sticky="nsew")
        entry_rot_z = ctk.CTkEntry(self.frame, placeholder_text="ang_3dZ", height=10, width=40)
        entry_rot_z.grid(row=8, column=1, padx=5, pady=2, sticky="nsew")

        lbl_rot_3d = tk.Label(self.frame, background="#000C66")
        lbl_rot_3d.grid(row=8, column=4, padx=5, pady=5, sticky="nsew")

        #entry_rot = ctk.CTkEntry(self.frame, placeholder_text="ang", height=10, width=40)
        #entry_rot.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        # Botão para Rotação
        btn_rotate_3d = tk.Button(self.frame, text="Aplicar Rotação_3d", command=lambda: self.ogl_frame.rotacao(int(entry_rot_x.get())))
        btn_rotate_3d.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator A de cisalhamento
        entry_a = ctk.CTkEntry(self.frame, placeholder_text="a_3d", height=10, width=40)
        entry_a.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator B de cisalhamento
        entry_b = ctk.CTkEntry(self.frame, placeholder_text="b_3d", height=10, width=40)
        entry_b.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")
        # Caixa de entrada para Fator B de cisalhamento
        entry_b = ctk.CTkEntry(self.frame, placeholder_text="c_3d", height=10, width=40)
        entry_b.grid(row=10, column=1, padx=5, pady=5, sticky="nsew")

        # Botão para Cisalhamento
        btn_shear_3d = tk.Button(self.frame, text="Aplicar Cisalhamento_3d", command=lambda: self.ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
        btn_shear_3d.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")

        # Botões para Reflexão
        btn_refx_3d = tk.Button(self.frame, text="Ref X_3d", command=lambda: self.ogl_frame.reflexaoX())
        btn_refx_3d.grid(row=11, column=1, padx=5, pady=5, sticky="nsew")

        btn_refy_3d = tk.Button(self.frame, text="Ref Y_3d", command=lambda: self.ogl_frame.reflexaoY())
        btn_refy_3d.grid(row=12, column=0, padx=5, pady=5, sticky="nsew")

        btn_refy_3d = tk.Button(self.frame, text="Ref Z_3d", command=lambda: self.ogl_frame.reflexaoY())
        btn_refy_3d.grid(row=12, column=1, padx=5, pady=5, sticky="nsew")

        btn_reforigem_3d = tk.Button(self.frame, text="Ref Origem_3d", command=lambda: self.ogl_frame.reflexaoOrigem())
        btn_reforigem_3d.grid(row=13, column=0, padx=5, pady=6, sticky="nsew")

        btn_ref45_3d = tk.Button(self.frame, text="Ref Reta 45_3d", command=lambda: self.ogl_frame.reflexao45())
        btn_ref45_3d.grid(row=13, column=1, padx=5, pady=7, sticky="nsew")
    
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