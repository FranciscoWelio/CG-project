from typing import Callable
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from .utils import (
    PixelGridDisplay,
    FloatEntry,
)


class ImageIntensityProcessor:
    def __init__(self, window: tk.Tk, restore: Callable[[], None]):
        self.restore = restore
        self.original_image = None
        self.processed_image = None
        self.scale_factor = 1.0
        window.title("Projeto Unidade 2 > Transformações")
        window.geometry("700x630")

        ttk.Button(window, text="Voltar", command=restore).pack(pady=5)
        
        # Controls
        controls = ttk.Frame(window)
        controls.pack(pady=10)
        
        ttk.Button(controls, text="Carregar Imagem", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
        # Transformation selection
        self.transform_var = tk.StringVar(value="Negativo")
        transforms = ["Negativo", "Gamma", "Logaritmo", "Sigmoide", "Faixa Dinâmica", "Linear"]
        self.transform_combo = ttk.Combobox(controls, textvariable=self.transform_var, values=transforms)
        self.transform_combo.pack(side=tk.LEFT, padx=5)
        self.transform_combo.bind('<<ComboboxSelected>>', self.update_parameters)
        
        # Parameters frame
        self.params_frame = ttk.Frame(controls)
        self.params_frame.pack(side=tk.LEFT, padx=5)
        
        # Process and save buttons
        ttk.Button(controls, text="Processar", command=self.process_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Salvar", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Image display setup
        self.setup_image_display(window)
        
    def setup_image_display(self, window):
        # Scroll frame setup
        self.scroll_frame = ttk.Frame(window)
        self.scroll_frame.pack(expand=True, fill=tk.BOTH)
        
        self.canvas = tk.Canvas(self.scroll_frame)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind("<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Main container
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Original image container
        left_container = ttk.Frame(main_container)
        left_container.pack(side=tk.LEFT, padx=10)
        self.original_label = ttk.Label(left_container)
        self.original_label.pack()
        ttk.Label(left_container, text="Malha Original:").pack(pady=(10,5))
        self.original_grid = PixelGridDisplay(left_container, rows=10, cols=10)
        self.original_grid.pack()
        
        # Processed image container
        right_container = ttk.Frame(main_container)
        right_container.pack(side=tk.LEFT, padx=10)
        self.processed_label = ttk.Label(right_container)
        self.processed_label.pack()
        ttk.Label(right_container, text="Malha Processada:").pack(pady=(10,5))
        self.processed_grid = PixelGridDisplay(right_container, rows=10, cols=10)
        self.processed_grid.pack()
        
        # Mouse events
        self.original_label.bind('<Motion>', lambda e: self.update_grid_values(e, True))
        self.processed_label.bind('<Motion>', lambda e: self.update_grid_values(e, False))

    def update_parameters(self, event=None):
        # Clear existing parameters
        for widget in self.params_frame.winfo_children():
            widget.destroy()
            
        transform = self.transform_var.get()
        
        if transform == "Gamma":
            ttk.Label(self.params_frame, text="c=").pack(side=tk.LEFT)
            self.c_entry = FloatEntry(self.params_frame, width=5)
            self.c_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.params_frame, text="γ=").pack(side=tk.LEFT)
            self.gamma_entry = FloatEntry(self.params_frame, width=5)
            self.gamma_entry.pack(side=tk.LEFT)
            
        elif transform == "Logaritmo":
            ttk.Label(self.params_frame, text="a=").pack(side=tk.LEFT)
            self.a_entry = FloatEntry(self.params_frame, 35, width=5)
            self.a_entry.pack(side=tk.LEFT)

        elif transform == "Sigmoide":
            ttk.Label(self.params_frame, text="w=").pack(side=tk.LEFT)
            self.w_entry = FloatEntry(self.params_frame, 100, width=5)
            self.w_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.params_frame, text="σ=").pack(side=tk.LEFT)
            self.sigma_entry = FloatEntry(self.params_frame, 100, width=5)
            self.sigma_entry.pack(side=tk.LEFT)

        elif transform == "Faixa Dinâmica":
            ttk.Label(self.params_frame, text="w=").pack(side=tk.LEFT)
            self.w_target = FloatEntry(self.params_frame, 255, width=5)
            self.w_target.pack(side=tk.LEFT, padx=5)
            
        elif transform == "Linear":
            ttk.Label(self.params_frame, text="a=").pack(side=tk.LEFT)
            self.a_entry = FloatEntry(self.params_frame, width=5)
            self.a_entry.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(self.params_frame, text="b=").pack(side=tk.LEFT)
            self.b_entry = FloatEntry(self.params_frame, width=5)
            self.b_entry.pack(side=tk.LEFT)
    
    def process_image(self):
        if self.original_image is None:
            return
            
        transform = self.transform_var.get()
        img = self.original_image.astype(float)
        
        if transform == "Negativo":
            self.processed_image = 255 - img
            
        elif transform == "Gamma":
            c = self.c_entry.get_value()
            gamma = self.gamma_entry.get_value()
            self.processed_image = c * np.power(img, gamma)
            
        elif transform == "Logaritmo":
            a = self.a_entry.get_value()
            self.processed_image = a * np.log(1 + img)
            
        elif transform == "Sigmoide":
            w = self.w_entry.get_value()
            sigma = self.sigma_entry.get_value()
            self.processed_image = 255 / (1 + np.exp(-(img - w)/sigma))
            
        elif transform == "Faixa Dinâmica":
            w_target = self.w_target.get_value()
            min_val = img.min()
            max_val = img.max()
            self.processed_image = ((img - min_val) / (max_val - min_val)) * w_target
            
        elif transform == "Linear":
            a = self.a_entry.get_value()
            b = self.b_entry.get_value()
            self.processed_image = a * img + b
        
        self.processed_image = np.clip(self.processed_image, 0, 255).astype(np.uint8)
        self.update_display()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp *.pgm")])
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.update_display()
    
    def update_grid_values(self, event, is_original):
        if self.original_image is None:
            return
            
        x = event.x
        y = event.y
        
        if is_original:
            values, mask = self.get_pixel_neighborhood(self.original_image, x, y, 10)
            self.original_grid.update_values(values, mask)
            
            if self.processed_image is not None:
                proc_values, proc_mask = self.get_pixel_neighborhood(self.processed_image, x, y, 10)
                self.processed_grid.update_values(proc_values, proc_mask)
        else:
            if self.processed_image is not None:
                proc_values, proc_mask = self.get_pixel_neighborhood(self.processed_image, x, y, 10)
                self.processed_grid.update_values(proc_values, proc_mask)
                
                orig_values, orig_mask = self.get_pixel_neighborhood(self.original_image, x, y, 10)
                self.original_grid.update_values(orig_values, orig_mask)

    def get_pixel_neighborhood(self, image, x, y, size=3):
        height, width = image.shape
        half = size // 2
        
        img_x = int(x / self.scale_factor)
        img_y = int(y / self.scale_factor)
        
        neighborhood = np.zeros((size, size))
        mask = np.zeros((size, size), dtype=bool)

        for i in range(size):
            for j in range(size):
                ny = img_y + (i - half)
                nx = img_x + (j - half)
                
                if (0 <= ny < height) and (0 <= nx < width):
                    neighborhood[i, j] = image[ny, nx]
                    mask[i, j] = True

        return neighborhood, mask

    def update_display(self):
        def prepare_image(image):
            if image is None:
                return None
                
            height, width = image.shape
            max_size = 500
            if height > max_size or width > max_size:
                self.scale_factor = max_size / max(height, width)
                new_size = (int(width * self.scale_factor), int(height * self.scale_factor))
                return cv2.resize(image, new_size)
            self.scale_factor = 1.0
            return image.copy()

        if self.original_image is not None:
            display_image = prepare_image(self.original_image)
            photo = ImageTk.PhotoImage(Image.fromarray(display_image))
            self.original_label.configure(image=photo)
            self.original_label.image = photo

        if self.processed_image is not None:
            display_image = prepare_image(self.processed_image)
            photo = ImageTk.PhotoImage(Image.fromarray(display_image))
            self.processed_label.configure(image=photo)
            self.processed_label.image = photo

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"),
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            if file_path:
                cv2.imwrite(file_path, self.processed_image)