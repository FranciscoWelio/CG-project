from pages import TwoDimensionsScreen
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
            self.twod_screen.show()
            # Exibe os botões 2D
            frame_left3d.pack_forget()
            frame_left1Q.pack_forget()
        # Esconde os botões 3D

        def show_3d_buttons() -> None:
            frame_left3d.pack()

            self.twod_screen.hide()
            frame_left1Q.pack_forget()  # Esconde os botões 2D

        def show_1Q_buttons():
            frame_left1Q.pack()

            self.twod_screen.hide()
            frame_left3d.pack_forget()

        def show_2Q_buttons():
            frame_left2Q.pack()

            self.twod_screen.hide()
            frame_left3d.pack_forget()
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

        btn_top2Q = tk.Button(frame_top, text="Questao 2", command=show_1Q_buttons)
        btn_top2Q.grid(row=0, column=3, padx=5, pady=5)
        btn_limapr = tk.Button(frame_top, text="Limpeza", command=lambda: ogl_frame.square_points(0))
        btn_limapr.grid(row=0, column=4, padx=5, pady=5)


        # Frame para o lado esquerdo
        frame_right = tk.Frame(self.root)
        ogl_frame = AppOgl(frame_right, width=700, height=600)
        self.twod_screen = TwoDimensionsScreen(self.root, ogl_frame)

        # Frame para o lado esquerdo
        frame_left3d = tk.Frame(self.root, width=300, height=600)
        frame_left3d.configure(background="#000C66")
        frame_left3d.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Frame para Questão 1
        frame_left1Q = tk.Frame(self.root, width=300, height=600)
        frame_left1Q.configure(background="#000C66")
        frame_left1Q.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Frame para Questão 2
        frame_left2Q = tk.Frame(self.root, width=300, height=600)
        frame_left2Q.configure(background="#000C66")
        frame_left2Q.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        # Frame para o lado direito
        frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        # Adicionar o frame OpenGL ao lado direito
        ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
        ogl_frame.animate = 1


        # Configuração de grid para alinhar os widgets
        #
        # Caixa de entrada para o tamanho do quadrado

        lbl_tamanho2 = tk.Label(frame_left1Q, background="#000C66")
        lbl_tamanho2.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")
        # Botão para desenhar um quadrado

        # COMEÇO 3d
        # Caixa de entrada para o tamanho do quadrado
        entry_tamanho_3d = ctk.CTkEntry(frame_left3d, placeholder_text="size", height=10, width=40)
        entry_tamanho_3d.grid(row=2, column=1, sticky="nsew")

        lbl_tamanho_3d = tk.Label(frame_left3d, background="#000C66")
        lbl_tamanho_3d.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")
        
        # Botão para desenhar um quadrado
        btn_desenhar_quadrado_3d = tk.Button(frame_left3d, text="Desenhar Cubo", command=lambda: ogl_frame.square_points(int(entry_tamanho_3d.get())))
        btn_desenhar_quadrado_3d.grid(row=2, column=0, padx=2, pady=2, sticky="nsew")

        # Caixa de entrada para Fator de escala Sx
        entry_sx_3d = ctk.CTkEntry(frame_left3d, placeholder_text="sx_3d", height=10, width=40)
        entry_sx_3d.grid(row=3, column=1, padx=2, pady=2, sticky="nsew")

        # Caixa de entrada para Fator de escala Sy
        entry_sy_3d = ctk.CTkEntry(frame_left3d, placeholder_text="sy_3d", height=10, width=40)
        entry_sy_3d.grid(row=4, column=0, padx=2, pady=2, sticky="nsew")
        # Caixa de entrada para Fator de escala Sz
        entry_sy_3d = ctk.CTkEntry(frame_left3d, placeholder_text="sz_3d", height=10, width=40)
        entry_sy_3d.grid(row=4, column=1, padx=6, pady=6, sticky="nsew")

        # Botão para Escala
        btn_scale_3d = tk.Button(frame_left3d, text="Aplicar Escala_3d", command=lambda: ogl_frame.escala(float(entry_sx.get()), float(entry_sy.get())))
        btn_scale_3d.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Translação Tx
        entry_tx_3d = ctk.CTkEntry(frame_left3d, placeholder_text="Tx_3d", height=10, width=40)
        entry_tx_3d.grid(row=5, column=1, padx=5, pady=15, sticky="nsew")

        # Caixa de entrada para Translação Ty
        entry_ty_3d = ctk.CTkEntry(frame_left3d, placeholder_text="Ty_3d", height=10, width=40)
        entry_ty_3d.grid(row=6, column=0, padx=5, pady=15, sticky="nsew")
        # Caixa de entrada para Translação Tz
        entry_ty_3d = ctk.CTkEntry(frame_left3d, placeholder_text="Tz_3d", height=10, width=40)
        entry_ty_3d.grid(row=6, column=1, padx=5, pady=15, sticky="nsew")

        # Botão para Translação
        btn_translate_3d = tk.Button(frame_left3d, text="Aplicar Translação_3d", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())))
        btn_translate_3d.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Rotacao
        entry_rot_3d = ctk.CTkEntry(frame_left3d, placeholder_text="ang_3dX", height=10, width=40)
        entry_rot_3d.grid(row=7, column=1, padx=5, pady=2, sticky="nsew")
        entry_rot_3d = ctk.CTkEntry(frame_left3d, placeholder_text="ang_3dY", height=10, width=40)
        entry_rot_3d.grid(row=8, column=0, padx=5, pady=2, sticky="nsew")
        entry_rot_3d = ctk.CTkEntry(frame_left3d, placeholder_text="ang_3dZ", height=10, width=40)
        entry_rot_3d.grid(row=8, column=1, padx=5, pady=2, sticky="nsew")

        lbl_rot_3d = tk.Label(frame_left3d, background="#000C66")
        lbl_rot_3d.grid(row=8, column=4, padx=5, pady=5, sticky="nsew")

        entry_rot = ctk.CTkEntry(frame_left3d, placeholder_text="ang", height=10, width=40)
        entry_rot.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        # Botão para Rotação
        btn_rotate_3d = tk.Button(frame_left3d, text="Aplicar Rotação_3d", command=lambda: ogl_frame.rotacao(int(entry_rot.get())))
        btn_rotate_3d.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator A de cisalhamento
        entry_a_3d = ctk.CTkEntry(frame_left3d, placeholder_text="a_3d", height=10, width=40)
        entry_a_3d.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")

        # Caixa de entrada para Fator B de cisalhamento
        entry_b_3d = ctk.CTkEntry(frame_left3d, placeholder_text="b_3d", height=10, width=40)
        entry_b_3d.grid(row=10, column=0, padx=5, pady=5, sticky="nsew")
        # Caixa de entrada para Fator B de cisalhamento
        entry_b_3d = ctk.CTkEntry(frame_left3d, placeholder_text="c_3d", height=10, width=40)
        entry_b_3d.grid(row=10, column=1, padx=5, pady=5, sticky="nsew")

        # Botão para Cisalhamento
        btn_shear_3d = tk.Button(frame_left3d, text="Aplicar Cisalhamento_3d", command=lambda: ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
        btn_shear_3d.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")

        # Botões para Reflexão
        btn_refx_3d = tk.Button(frame_left3d, text="Ref X_3d", command=lambda: ogl_frame.reflexaoX())
        btn_refx_3d.grid(row=11, column=1, padx=5, pady=5, sticky="nsew")

        btn_refy_3d = tk.Button(frame_left3d, text="Ref Y_3d", command=lambda: ogl_frame.reflexaoY())
        btn_refy_3d.grid(row=12, column=0, padx=5, pady=5, sticky="nsew")

        btn_refy_3d = tk.Button(frame_left3d, text="Ref Z_3d", command=lambda: ogl_frame.reflexaoY())
        btn_refy_3d.grid(row=12, column=1, padx=5, pady=5, sticky="nsew")

        btn_reforigem_3d = tk.Button(frame_left3d, text="Ref Origem_3d", command=lambda: ogl_frame.reflexaoOrigem())
        btn_reforigem_3d.grid(row=13, column=0, padx=5, pady=6, sticky="nsew")

        btn_ref45_3d = tk.Button(frame_left3d, text="Ref Reta 45_3d", command=lambda: ogl_frame.reflexao45())
        btn_ref45_3d.grid(row=13, column=1, padx=5, pady=7, sticky="nsew")


        ## Questão 1
        ##

        entry_X1Q = ctk.CTkEntry(frame_left1Q, placeholder_text="X Inicio", height=10, width=40)
        entry_X1Q.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        entry_Y1Q = ctk.CTkEntry(frame_left1Q, placeholder_text="Y Inicio", height=10, width=40)
        entry_Y1Q.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        entry_XEND_1Q = ctk.CTkEntry(frame_left1Q, placeholder_text="X Fim", height=10, width=40)
        entry_XEND_1Q.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
        entry_YEND_1Q = ctk.CTkEntry(frame_left1Q, placeholder_text="Y Fim", height=10, width=40)
        entry_YEND_1Q.grid(row=2, column=4, padx=5, pady=5, sticky="nsew")

        btn_DDA = tk.Button(frame_left1Q, text="Reta DDA", command=lambda: ogl_frame.DDA(int(entry_X1Q.get()), int(entry_Y1Q.get()), int(entry_XEND_1Q.get()), int(entry_YEND_1Q.get())))
        btn_DDA.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")



        btn_PM = tk.Button(frame_left1Q, text="Reta PM", command=lambda: ogl_frame.PontoMedio(float(entry_X1Q.get()), float(entry_Y1Q.get()), float(entry_XEND_1Q.get()), float(entry_YEND_1Q.get())))
        btn_PM.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")


        entry_Circ = ctk.CTkEntry(frame_left1Q, placeholder_text="Raio", height=10, width=40)
        entry_Circ.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        btn_CIRC_EXP = tk.Button(frame_left1Q, text="Circun Exp.", command=lambda: ogl_frame.linePoliExpli(int(entry_Circ.get())))
        btn_CIRC_EXP.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        btn_CIRC_TRI = tk.Button(frame_left1Q, text="Circun TRI.", command=lambda: ogl_frame.linePoliTrig(int(entry_Circ.get())))
        btn_CIRC_TRI.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        btn_CIRC_PM = tk.Button(frame_left1Q, text="Circun PM.", command=lambda: ogl_frame.linePoliPM(int(entry_Circ.get())))
        btn_CIRC_PM.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")


        entry_R1_ELI = ctk.CTkEntry(frame_left1Q, placeholder_text="Eixo X", height=10, width=40)
        entry_R1_ELI.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")
        entry_R2_ELI = ctk.CTkEntry(frame_left1Q, placeholder_text="Eixo Y", height=10, width=40)
        entry_R2_ELI.grid(row=6, column=2, padx=5, pady=5, sticky="nsew")
        entry_R3_ELI = ctk.CTkEntry(frame_left1Q, placeholder_text="Raio", height=10, width=40)
        entry_R3_ELI.grid(row=6, column=3, padx=5, pady=5, sticky="nsew")
        btn_CIRC_ELIP = tk.Button(frame_left1Q, text="Circun ELIP.", command=lambda: ogl_frame.linePoliElip(int(entry_R1_ELI.get()), int( entry_R2_ELI.get()),int( entry_R3_ELI.get()) ))
        btn_CIRC_ELIP.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

        show_2d_buttons()

    def run(self):
        self.root.mainloop()



if __name__ == '__main__':
   MainPage().run()
