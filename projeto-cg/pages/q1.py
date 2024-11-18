from .utils import FloatEntry, IntEntry
import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class Q1Screen:
    def __init__(self, window: tk.Tk) -> None:
        self.active = False
        self.window = window
        self.frame = tk.Frame(self.window, width=300, height=600)
        self.frame.configure(background="#000C66")
        
        self.frame_right = tk.Frame(self.window, width=300, height=600)
    
    def create_widgets(self):
        self.ogl_frame = AppOgl(self.frame_right, width=700, height=600)
        self.ogl_frame.pack(fill=tk.BOTH, expand=False)
        self.ogl_frame.animate = 1

        lbl_tamanho2 = tk.Label(self.frame, background="#000C66")
        lbl_tamanho2.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")
        # Botão para desenhar um quadrado

        

        ## Questão 1
        ##

        entry_X1Q = ctk.CTkEntry(self.frame, placeholder_text="X Inicio", height=10, width=40)
        entry_X1Q.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        entry_Y1Q = ctk.CTkEntry(self.frame, placeholder_text="Y Inicio", height=10, width=40)
        entry_Y1Q.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        entry_XEND_1Q = ctk.CTkEntry(self.frame, placeholder_text="X Fim", height=10, width=40)
        entry_XEND_1Q.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
        entry_YEND_1Q = ctk.CTkEntry(self.frame, placeholder_text="Y Fim", height=10, width=40)
        entry_YEND_1Q.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")

        btn_DDA = tk.Button(self.frame, text="Reta DDA", command=lambda: self.ogl_frame.DDA(int(entry_X1Q.get()), int(entry_Y1Q.get()), int(entry_XEND_1Q.get()), int(entry_YEND_1Q.get())))
        btn_DDA.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")



        btn_PM = tk.Button(self.frame, text="Reta PM", command=lambda: self.ogl_frame.PontoMedio(float(entry_X1Q.get()), float(entry_Y1Q.get()), float(entry_XEND_1Q.get()), float(entry_YEND_1Q.get())))
        btn_PM.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")


        entry_Circ = ctk.CTkEntry(self.frame, placeholder_text="Raio", height=10, width=40)
        entry_Circ.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        btn_CIRC_EXP = tk.Button(self.frame, text="Circun Exp.", command=lambda: self.ogl_frame.linePoliExpli(int(entry_Circ.get())))
        btn_CIRC_EXP.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        btn_CIRC_TRI = tk.Button(self.frame, text="Circun TRI.", command=lambda: self.ogl_frame.linePoliTrig(int(entry_Circ.get())))
        btn_CIRC_TRI.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        btn_CIRC_PM = tk.Button(self.frame, text="Circun PM.", command=lambda: self.ogl_frame.linePoliPM(int(entry_Circ.get())))
        btn_CIRC_PM.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")


        entry_R1_ELI = ctk.CTkEntry(self.frame, placeholder_text="Tamanho X", height=10, width=40)
        entry_R1_ELI.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        entry_R2_ELI = ctk.CTkEntry(self.frame, placeholder_text="Tamanho Y", height=10, width=40)
        entry_R2_ELI.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")
        entry_R3_ELI = ctk.CTkEntry(self.frame, placeholder_text="Eixo X", height=10, width=40)
        entry_R3_ELI.grid(row=7, column=2, padx=5, pady=5, sticky="nsew")
        entry_R4_ELI = ctk.CTkEntry(self.frame, placeholder_text="Eixo Y", height=10, width=40)
        entry_R4_ELI.grid(row=7, column=3, padx=5, pady=5, sticky="nsew")
        btn_CIRC_ELIP = tk.Button(self.frame, text="Circun ELIP.", command=lambda: self.ogl_frame.linePoliElip(int(entry_R1_ELI.get()), int( entry_R2_ELI.get()),int( entry_R3_ELI.get()) ,int( entry_R4_ELI.get())))
        btn_CIRC_ELIP.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

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