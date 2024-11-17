from .utils import FloatEntry, IntEntry
import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class Q2Screen:
    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.frame = tk.Frame(self.window, width=300, height=600)
        self.frame.configure(background="#000C66")
        
        self.frame_right = tk.Frame(self.window, width=300, height=600)
    
    def create_widgets(self):
        self.ogl_frame = AppOgl(self.frame_right, width=700, height=600)
        self.ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
        self.ogl_frame.animate = 1

    def hide(self):
        # Destroy all widgets in the frame
        if hasattr(self, 'ogl_frame'):
            self.ogl_frame.destroy()
            self.ogl_frame.pack_forget()
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        for widget in self.frame_right.winfo_children():
            widget.destroy()

        if hasattr(self, 'ogl_frame'):
            delattr(self, 'ogl_frame')
    
    def show(self):
        self.create_widgets()
        #self.frame.pack()