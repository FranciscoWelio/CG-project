from pages import (
    TwoDimensionsScreen,
    ThreeDimensionsScreen,
    Q1Screen,
    Q2Screen,
)
import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class MainPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x600")
        self.root.configure(background="#000C66")

        def show_2d_buttons() -> None:
            self.current_screen = self.twod_screen
            self.twod_screen.show()
            # Exibe os botões 2D
            self.three_screen.hide()
            self.q1_screen.hide()
            self.q2_screen.hide()
        # Esconde os botões 3D

        def show_3d_buttons() -> None:
            self.current_screen = self.three_screen
            self.three_screen.show()

            self.twod_screen.hide()
            self.q1_screen.hide()
            self.q2_screen.hide()

        def show_1Q_buttons():
            self.current_screen = self.q1_screen
            self.q1_screen.show()

            self.twod_screen.hide()
            self.three_screen.hide()
            self.q2_screen.hide()

        def show_2Q_buttons():
            self.current_screen = self.q1_screen
            self.q2_screen.show()

            self.twod_screen.hide()
            self.three_screen.hide()
            self.q1_screen.hide()
        #frame superior
        frame_top = tk.Frame(self.root, width=1200, height=20)
        frame_top.configure(background="#a0a0a0")
        frame_top.pack(side=tk.TOP, fill=tk.BOTH,expand=False)
        btn_top2d = tk.Button(frame_top, text="2D", command=show_2d_buttons)
        btn_top2d.grid(row=0, column=0, padx=5, pady=5)
        btn_top3d = tk.Button(frame_top, text="3D", command=show_3d_buttons)
        btn_top3d.grid(row=0, column=1, padx=5, pady=5)

        btn_top1Q = tk.Button(frame_top, text="Questao 1", command=show_1Q_buttons)
        btn_top1Q.grid(row=0, column=2, padx=5, pady=5)

        btn_top2Q = tk.Button(frame_top, text="Questao 2", command=show_2Q_buttons)
        btn_top2Q.grid(row=0, column=3, padx=5, pady=5)
        btn_limapr = tk.Button(frame_top, text="Limpeza", command=lambda: self.current_screen.ogl_frame.square_points(0))
        btn_limapr.grid(row=0, column=4, padx=5, pady=5)


        # Frame para o lado esquerdo
        frame_right = tk.Frame(self.root)
        # ogl_frame = AppOgl(frame_right, width=700, height=600)
        self.twod_screen = TwoDimensionsScreen(self.root)
        #ogl_frame = AppOgl(frame_right, width=700, height=600)
        self.three_screen = ThreeDimensionsScreen(self.root)
        self.q1_screen = Q1Screen(self.root)
        self.q2_screen = Q2Screen(self.root)
        

        # Frame para Questão 2
        '''frame_left2Q = tk.Frame(self.root, width=300, height=600)
        frame_left2Q.configure(background="#000C66")
        frame_left2Q.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        # Frame para o lado direito
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Adicionar o frame OpenGL ao lado direito
        ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
        ogl_frame.animate = 1'''
        show_2d_buttons()

    def run(self):
        self.root.mainloop()



if __name__ == '__main__':
   MainPage().run()
