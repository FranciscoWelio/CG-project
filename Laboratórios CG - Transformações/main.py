import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from opengl_frame import AppOgl


def main():
    root = tk.Tk()
    root.geometry("1000x600")
    root.configure(background="#000C66")

    # Frame para o lado esquerdo
    frame_left = tk.Frame(root, width=150, height=600)
    frame_left.configure(background="#000C66")
    frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame intermediário1
    frame_mid1 = tk.Frame(root, width=75, height=600)
    frame_mid1.configure(background="#000C66")
    frame_mid1.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame intermediário2
    frame_mid2 = tk.Frame(root, width=75, height=600)
    frame_mid2.configure(background="#000C66")
    frame_mid2.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Frame para o lado direito
    frame_right = tk.Frame(root, width=700, height=600)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
    
    # Adicionar o frame OpenGL ao lado direito
    ogl_frame = AppOgl(frame_right, width=700, height=600)
    ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo

    ogl_frame.animate = 1

    # Configuração de grid para alinhar os widgets

    # Caixa de entrada para o tamanho do quadrado
    entry_tamanho = ctk.CTkEntry(frame_mid1, placeholder_text="size", height=10, width=40)
    entry_tamanho.grid(row=0, column=0, padx=5, pady=5)

    lbl_tamanho = tk.Label(frame_mid2, background="#000C66")
    lbl_tamanho.grid(row=0, column=0, padx=5, pady=5)

    # Botão para desenhar um quadrado
    btn_desenhar_quadrado = tk.Button(frame_left, text="Desenhar Quadrado", command=lambda: ogl_frame.square_points(int(entry_tamanho.get())))
    btn_desenhar_quadrado.grid(row=1, column=0, padx=5, pady=5)

    # Caixa de entrada para Fator de escala Sx
    entry_sx = ctk.CTkEntry(frame_mid1, placeholder_text="sx", height=10, width=40)
    entry_sx.grid(row=2, column=0, padx=5, pady=5)

    # Caixa de entrada para Fator de escala Sy
    entry_sy = ctk.CTkEntry(frame_mid2, placeholder_text="sy", height=10, width=40)
    entry_sy.grid(row=2, column=0, padx=6, pady=6)

    # Botão para Escala
    btn_scale = tk.Button(frame_left, text="Aplicar Escala", command=lambda: ogl_frame.escala(float(entry_sx.get()), float(entry_sy.get())))
    btn_scale.grid(row=2, column=0, padx=5, pady=5)

    # Caixa de entrada para Translação Tx
    entry_tx = ctk.CTkEntry(frame_mid1, placeholder_text="Tx", height=10, width=40)
    entry_tx.grid(row=3, column=0, padx=5, pady=15)

    # Caixa de entrada para Translação Ty
    entry_ty = ctk.CTkEntry(frame_mid2, placeholder_text="Ty", height=10, width=40)
    entry_ty.grid(row=3, column=0, padx=5, pady=15)

    # Botão para Translação
    btn_translate = tk.Button(frame_left, text="Aplicar Translação", command=lambda: ogl_frame.translacao(int(entry_tx.get()), int(entry_ty.get())))
    btn_translate.grid(row=3, column=0, padx=5, pady=5)

    # Caixa de entrada para Rotacao
    entry_rot = ctk.CTkEntry(frame_mid1, placeholder_text="ang", height=10, width=40)
    entry_rot.grid(row=4, column=0, padx=5, pady=5)

    lbl_rot = tk.Label(frame_mid2, background="#000C66")
    lbl_rot.grid(row=4, column=0, padx=5, pady=5)

    # Botão para Rotação
    btn_rotate = tk.Button(frame_left, text="Aplicar Rotação", command=lambda: ogl_frame.rotacao(int(entry_rot.get())))
    btn_rotate.grid(row=4, column=0, padx=5, pady=5)

    # Caixa de entrada para Fator A de cisalhamento
    entry_a = ctk.CTkEntry(frame_mid1, placeholder_text="a", height=10, width=40)
    entry_a.grid(row=5, column=0, padx=5, pady=5)

    # Caixa de entrada para Fator B de cisalhamento
    entry_b = ctk.CTkEntry(frame_mid2, placeholder_text="b", height=10, width=40)
    entry_b.grid(row=5, column=0, padx=5, pady=5)

    # Botão para Cisalhamento
    btn_shear = tk.Button(frame_left, text="Aplicar Cisalhamento", command=lambda: ogl_frame.cisalhamento(int(entry_a.get()), int(entry_b.get())))
    btn_shear.grid(row=5, column=0, padx=5, pady=5)

    # Botões para Reflexão
    btn_refx = tk.Button(frame_mid1, text="Ref X", command=lambda: ogl_frame.reflexaoX())
    btn_refx.grid(row=6, column=0, padx=5, pady=5)

    btn_refy = tk.Button(frame_mid2, text="Ref Y", command=lambda: ogl_frame.reflexaoY())
    btn_refy.grid(row=6, column=0, padx=5, pady=5)

    btn_reforigem = tk.Button(frame_mid1, text="Ref Origem", command=lambda: ogl_frame.reflexaoOrigem())
    btn_reforigem.grid(row=7, column=0, padx=5, pady=6)

    btn_ref45 = tk.Button(frame_mid2, text="Ref Reta 45", command=lambda: ogl_frame.reflexao45())
    btn_ref45.grid(row=7, column=0, padx=5, pady=7)

    root.mainloop()

if __name__ == '__main__':
    main()
