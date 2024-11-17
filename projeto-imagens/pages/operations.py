from typing import Callable
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from .utils import (
    PixelGridDisplay
)


class ImageOperationsProcessor:
    def __init__(self, window: tk.Tk, restore: Callable[[], None]):
        self.restore = restore
        self.image1 = None
        self.image2 = None
        self.result_image = None
        self.scale_factor = 1.0
        window.title("Projeto Unidade 2 > Operações")
        window.geometry("1050x600")

        ttk.Button(window, text="Voltar", command=restore).pack(pady=5)
        
        # Controls frame
        controls = ttk.Frame(window)
        controls.pack(pady=10)
        
        # Image loading buttons
        img_buttons = ttk.Frame(controls)
        img_buttons.pack(side=tk.LEFT, padx=5)
        ttk.Button(img_buttons, text="Carregar Imagem 1", command=lambda: self.load_image(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(img_buttons, text="Carregar Imagem 2", command=lambda: self.load_image(2)).pack(side=tk.LEFT, padx=5)
        
        # Operation selection
        self.operation_var = tk.StringVar(value="soma")
        operations = ["soma", "subtração", "multiplicação", "divisão", "and", "or", "xor"]
        self.operation_combo = ttk.Combobox(controls, textvariable=self.operation_var, values=operations)
        self.operation_combo.pack(side=tk.LEFT, padx=5)
        
        # Process and save buttons
        ttk.Button(controls, text="Processar", command=self.process_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls, text="Salvar", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Images display frame
        self.scroll_frame = ttk.Frame(window)
        self.scroll_frame.pack(expand=True, fill=tk.BOTH)
        
        # Canvas setup
        self.canvas = tk.Canvas(self.scroll_frame)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

        # Main containers
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Image 1 container
        self.img1_container = ttk.Frame(main_container)
        self.img1_container.pack(side=tk.LEFT, padx=10)
        self.img1_label = ttk.Label(self.img1_container)
        self.img1_label.pack()
        ttk.Label(self.img1_container, text="Malha Imagem 1:").pack(pady=(10,5))
        self.img1_grid = PixelGridDisplay(self.img1_container, rows=10, cols=10)
        self.img1_grid.pack()
        
        # Image 2 container
        self.img2_container = ttk.Frame(main_container)
        self.img2_container.pack(side=tk.LEFT, padx=10)
        self.img2_label = ttk.Label(self.img2_container)
        self.img2_label.pack()
        ttk.Label(self.img2_container, text="Malha Imagem 2:").pack(pady=(10,5))
        self.img2_grid = PixelGridDisplay(self.img2_container, rows=10, cols=10)
        self.img2_grid.pack()
        
        # Result container
        self.result_container = ttk.Frame(main_container)
        self.result_container.pack(side=tk.LEFT, padx=10)
        self.result_label = ttk.Label(self.result_container)
        self.result_label.pack()
        ttk.Label(self.result_container, text="Malha Resultado:").pack(pady=(10,5))
        self.result_grid = PixelGridDisplay(self.result_container, rows=10, cols=10)
        self.result_grid.pack()
        
        # Mouse event bindings
        self.img1_label.bind('<Motion>', lambda e: self.update_grid_values(e, 1))
        self.img2_label.bind('<Motion>', lambda e: self.update_grid_values(e, 2))
        self.result_label.bind('<Motion>', lambda e: self.update_grid_values(e, 3))

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_image(self, img_num):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp *.pgm")])
        if file_path:
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if img_num == 1:
                self.image1 = img
            else:
                self.image2 = img
            self.update_display()

    def process_images(self):
        if self.image1 is None or self.image2 is None:
            return

        # Ensure images have the same size
        if self.image1.shape != self.image2.shape:
            h1, w1 = self.image1.shape
            h2, w2 = self.image2.shape
            min_h = min(h1, h2)
            min_w = min(w1, w2)
            self.image1 = cv2.resize(self.image1, (min_w, min_h))
            self.image2 = cv2.resize(self.image2, (min_w, min_h))

        operation = self.operation_var.get()
        img1 = self.image1.astype(float)
        img2 = self.image2.astype(float)

        if operation == "soma":
            result = img1 + img2
        elif operation == "subtração":
            result = img1 - img2
        elif operation == "multiplicação":
            result = img1 * img2
        elif operation == "divisão":
            img2[img2 == 0] = 1
            result = img1 / img2
        elif operation == "and":
            img1 = img1 / 255.0
            img2 = img2 / 255.0
            result = np.minimum(img1, img2)
            result = (result * 255).astype(np.uint8)
        elif operation == "or":
            img1 = img1 / 255.0
            img2 = img2 / 255.0
            result = np.maximum(img1, img2)
            result = (result * 255).astype(np.uint8)
        elif operation == "xor":
            img_height, img_width = img1.shape
            result = np.zeros_like(img1)
            img1 = img1 / 255.0
            img2 = img2 / 255.0
            for y in range(img_height):
                for x in range(img_width):
                    result[y, x] = round(abs(img1[y,x] - img2[y,x]) * 255)

        self.result_image = np.clip(result, 0, 255).astype(np.uint8)
        self.update_display()

    def update_grid_values(self, event, img_num):
        x = event.x
        y = event.y
        
        # Atualiza malha 1
        values, mask = self.get_pixel_neighborhood(self.image1, x, y, 10)
        self.img1_grid.update_values(values, mask)
        # Atualiza malha 2
        values, mask = self.get_pixel_neighborhood(self.image2, x, y, 10)
        self.img2_grid.update_values(values, mask)
        # Atualiza malha 3
        values, mask = self.get_pixel_neighborhood(self.result_image, x, y, 10)
        self.result_grid.update_values(values, mask)

    def get_pixel_neighborhood(self, image, x, y, size=3):
        if image is None:
            return np.zeros((size, size)), np.zeros((size, size), dtype=bool)
            
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

        if self.image1 is not None:
            display_image = prepare_image(self.image1)
            photo = ImageTk.PhotoImage(Image.fromarray(display_image))
            self.img1_label.configure(image=photo)
            self.img1_label.image = photo

        if self.image2 is not None:
            display_image = prepare_image(self.image2)
            photo = ImageTk.PhotoImage(Image.fromarray(display_image))
            self.img2_label.configure(image=photo)
            self.img2_label.image = photo

        if self.result_image is not None:
            display_image = prepare_image(self.result_image)
            photo = ImageTk.PhotoImage(Image.fromarray(display_image))
            self.result_label.configure(image=photo)
            self.result_label.image = photo

    def save_image(self):
        if self.result_image is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"),
                          ("JPEG files", "*.jpg"),
                          ("All files", "*.*")]
            )
            if file_path:
                cv2.imwrite(file_path, self.result_image)