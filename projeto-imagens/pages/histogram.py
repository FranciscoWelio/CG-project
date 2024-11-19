from typing import Callable, Dict
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from .utils import (
    PixelGridDisplay,
)


class HistogramEqualizer:
    def __init__(self, window: tk.Tk, restore: Callable[[], None]):
        self.restore = restore
        self.original_image = None
        self.equalized_image = None
        self.scale_factor = 1.0
        window.title("Projeto Unidade 2 > Equalização de Histograma")
        window.geometry("580x730")

        ttk.Button(window, text="Voltar", command=restore).pack(pady=5)
        
        # Controls
        controls = ttk.Frame(window)
        controls.pack(pady=10)
        
        ttk.Button(controls, text="Carregar Imagem", command=self.load_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Equalizar", command=self.equalize_histogram).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Salvar", command=self.save_image).pack(side=tk.LEFT, padx=5)

        # Scroll frame setup
        self.scroll_frame = ttk.Frame(window)
        self.scroll_frame.pack(expand=True, fill=tk.BOTH)

        # Canvas and scrollbar
        self.canvas = tk.Canvas(self.scroll_frame)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind("<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)
        # Main container
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Original image and histogram
        left_container = ttk.Frame(main_container)
        left_container.pack(side=tk.LEFT, padx=10)
        
        self.original_label = ttk.Label(left_container)
        self.original_label.pack()
        
        ttk.Label(left_container, text="Malha Original:").pack(pady=(10,5))
        self.original_grid = PixelGridDisplay(left_container, rows=7, cols=7)
        self.original_grid.pack()
        
        self.orig_hist_canvas = tk.Canvas(left_container, width=256, height=200, bg='white')
        self.orig_hist_canvas.pack(pady=10)
        
        # Equalized image and histogram
        right_container = ttk.Frame(main_container)
        right_container.pack(side=tk.LEFT, padx=10)
        
        self.equalized_label = ttk.Label(right_container)
        self.equalized_label.pack()
        
        ttk.Label(right_container, text="Malha Equalizada:").pack(pady=(10,5))
        self.equalized_grid = PixelGridDisplay(right_container, rows=7, cols=7)
        self.equalized_grid.pack()
        
        self.eq_hist_canvas = tk.Canvas(right_container, width=256, height=200, bg='white')
        self.eq_hist_canvas.pack(pady=10)
        
        # Mouse events
        self.original_label.bind('<Motion>', lambda e: self.update_grid_values(e, True))
        self.equalized_label.bind('<Motion>', lambda e: self.update_grid_values(e, False))

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def draw_histogram(self, canvas, image):
        canvas.delete("all")
        
        if image is None:
            return
            
        hist = cv2.calcHist([image], [0], None, [256], [0,256])
        max_val = np.max(hist)
        
        # Normalize histogram to fit canvas height
        hist = hist * (180 / max_val)
        
        # Draw histogram bars
        for i in range(256):
            height = int(hist[i])
            canvas.create_line(i, 200, i, 200-height, fill='black')

    def equalize_histogram(self):
        if self.original_image is None:
            return
            
        # Calculate histogram
        nk: Dict[int, int] = {i:0 for i in range(256) }
        rk: Dict[int, int] = {i:0 for i in range(256) }
        sk: Dict[int, int] = {i:0 for i in range(256) }
        height, width = self.original_image.shape
        output = np.zeros_like(self.original_image)
        mask_size = 3
        offset = mask_size // 2
        total = height*width
        
        for y in range(height):
            for x in range(width):
                pixel_value = int(self.original_image[y][x])
                nk[pixel_value] += 1
                

        prob_acumulada = 0
        for key, value in nk.items():
            rk[key] = key/255 # intensidade dividido por intensidade máxima
            prob_acumulada += value/total
            sk[key] = prob_acumulada # probabilidade acumulada
        
        # equalização da imagem
        for y in range(height):
            for x in range(width):
                pixel_value = int(self.original_image[y][x])
                # round(rk) -> round(sk)
                left = round(rk[pixel_value]*255) # obtém domínio da função
                output[y][x] = round(sk[left]*255) # obtém imagem da função
        
        
        # Apply equalization
        self.equalized_image = output
        
        self.update_display()
        
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp *.pgm")])
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.equalized_image = None
            self.update_display()
    
    def update_grid_values(self, event, is_original):
        if self.original_image is None:
            return
            
        x = event.x
        y = event.y
        
        if is_original:
            values, mask = self.get_pixel_neighborhood(self.original_image, x, y, 10)
            self.original_grid.update_values(values, mask)
            
            if self.equalized_image is not None:
                eq_values, eq_mask = self.get_pixel_neighborhood(self.equalized_image, x, y, 10)
                self.equalized_grid.update_values(eq_values, eq_mask)
        else:
            if self.equalized_image is not None:
                eq_values, eq_mask = self.get_pixel_neighborhood(self.equalized_image, x, y, 10)
                self.equalized_grid.update_values(eq_values, eq_mask)
                
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
            self.draw_histogram(self.orig_hist_canvas, self.original_image)

        if self.equalized_image is not None:
            display_image = prepare_image(self.equalized_image)
            photo = ImageTk.PhotoImage(Image.fromarray(display_image))
            self.equalized_label.configure(image=photo)
            self.equalized_label.image = photo
            self.draw_histogram(self.eq_hist_canvas, self.equalized_image)

    def save_image(self):
        if self.equalized_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"),
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            if file_path:
                cv2.imwrite(file_path, self.equalized_image)