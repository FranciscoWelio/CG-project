from .utils import FloatEntry, IntEntry
import tkinter as tk
import customtkinter as ctk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from opengl_frame import AppOgl


class Q2Screen:
    def __init__(self, window: tk.Tk) -> None:
        self.active = False
        self.window = window
        
        # Create frames
        self.frame = tk.Frame(self.window, width=300, height=600)
        self.frame.configure(background="#000C66")
        
        self.frame_right = tk.Frame(self.window, width=700, height=600)
    
    def create_widgets(self):
        # Initialize animation state
        self.animation_active = False
    
        self.ogl_frame = AppOgl(self.frame_right, width=700, height=600)
        self.ogl_frame.pack(fill=tk.BOTH, expand=False)  # Definindo expand=False para manter o tamanho fixo
        self.ogl_frame.animate = 1
        # self.ogl_frame.initgl()
        # Pack frames
        
        # Create control buttons
        self.start_button = tk.Button(self.frame, text="Start Animation", 
                                    command=self.start_animation)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(self.frame, text="Stop Animation", 
                                   command=self.stop_animation)
        self.stop_button.pack(pady=10)
        
        # Create OpenGL frame
        # self.start_animation()
    
    def start_animation(self):
        if not self.animation_active:
            self.animation_active = True
            self.ogl_frame.animate = 1
            self.ogl_frame.update_animation()
    
    def stop_animation(self):
        self.animation_active = False
        self.ogl_frame.animate = 0
    
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