from typing import Callable
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from .utils import (
    PixelGridDisplay,
    MaskEditor
)


def apply_dilation(image: np.ndarray, kernel: np.ndarray, binary=False) -> np.ndarray:
    if len(image.shape) != 2:
        raise ValueError("Image must be 2D")
        
    img_height, img_width = image.shape
    k_height, k_width = kernel.shape
    pad_h = k_height // 2
    pad_w = k_width // 2
    
    # Padding the image
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    output = np.zeros_like(image)
    
    if binary:
        for i in range(img_height):
            for j in range(img_width):
                if image[i, j]:
                    for y in range(k_height):
                        for x in range(k_width):
                            if kernel[y,x] == 1:
                                cur_y = y - pad_h
                                cur_x = x - pad_w
                                if (0 <= i+cur_y < img_height) and (0 <= j+cur_x < img_width):
                                    output[i+cur_y, j+cur_x] = 255
    else:
        for i in range(img_height):
            for j in range(img_width):
                # Get region of interest
                region = padded[i:i+k_height, j:j+k_width]
                # For grayscale images
                values = region + kernel
                output[i, j] = min(np.max(values), 254) + 1
                
    return np.clip(output, 0, 255).astype(np.uint8)

def apply_erosion(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    if len(image.shape) != 2:
        raise ValueError("Image must be 2D")
        
    img_height, img_width = image.shape
    k_height, k_width = kernel.shape
    pad_h = k_height // 2
    pad_w = k_width // 2
    
    # Padding the image
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=255)
    output = np.zeros_like(image)
    
    if binary:
        for i in range(img_height):
            for j in range(img_width):
                if image[i, j]:
                    vizinhos = []
                    for y in range(k_height):
                        for x in range(k_width):
                            if kernel[y,x] == 1:
                                cur_y = y - pad_h
                                cur_x = x - pad_w
                                if (0 <= i+cur_y < img_height) and (0 <= j+cur_x < img_width):
                                    vizinhos.append(image[i+cur_y, j+cur_x] == 255)
                                else:
                                    vizinhos.append(False)
                    if not all(vizinhos):
                        output[i, j] = 0
                    else:
                        output[i, j] = image[i,j]
                else:
                    output[i, j] = image[i,j]
    else:
        for i in range(img_height):
            for j in range(img_width):
                region = padded[i:i+k_height, j:j+k_width]
                values = region - kernel
                output[i, j] = max(np.min(values), 1) - 1
                
    return np.clip(output, 0, 255).astype(np.uint8)

def apply_opening(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    eroded = apply_erosion(image, kernel, binary)
    return apply_dilation(eroded, kernel, binary)

def apply_closing(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    dilated = apply_dilation(image, kernel, binary)
    return apply_erosion(dilated, kernel, binary)

def apply_inner_contour(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    return image - apply_erosion(image, kernel, binary)

def apply_outer_contour(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    return apply_dilation(image, kernel, binary) - image

def apply_gradient(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    dilated = apply_dilation(image, kernel, binary)
    eroded = apply_erosion(image, kernel, binary)
    return dilated - eroded

def apply_tophat(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    return image - apply_opening(image, kernel, binary)

def apply_bottomhat(image: np.ndarray, kernel: np.ndarray, binary = False) -> np.ndarray:
    return apply_closing(image, kernel, binary) - image


class MorphologicalProcessor:
    def __init__(self, window, restore: Callable[[], None]):
        self.restore = restore
        self.original_image = None
        self.processed_image = None
        self.mask_editor= None
        self.binary_threshold = 127
        self.scale_factor = 1.0
        window.title("Projeto Unidade 2 > Operações Morfológicas")
        window.geometry("750x630")
        self.windows = window

        ttk.Button(window, text="Voltar", command=restore).pack(pady=5)
        
        # Controls
        self.controls = ttk.Frame(window)
        self.controls.pack(pady=10)

        # Frame para o botão de editar máscara (para manter o espaço consistente)
        self.edit_mask_frame = ttk.Frame(self.controls)
        self.edit_mask_frame.pack(side=tk.LEFT, padx=5)

        # Image loading and type selection
        load_frame = ttk.Frame(self.controls)
        load_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(load_frame, text="Carregar Imagem", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
        self.image_type = "binária"
        self.label = tk.Label(load_frame, text=f"Tipo: {self.image_type}")
        self.label.pack(side=tk.LEFT)
        # Operation selection
        self.operation_var = tk.StringVar(value="Dilatação")
        operations = ["Dilatação", "Erosão", "Abertura", "Fechamento", "Contorno Interno", "Contorno Externo", "Gradiente", "Top-Hat", "Bottom-Hat"]
        self.operation_combo = ttk.Combobox(self.controls, textvariable=self.operation_var, values=operations)
        self.operation_combo.pack(side=tk.LEFT, padx=5)
        
        # Element structure selection
        self.element_var = tk.StringVar(value="3x3")
        elements = ["3x3", "Cruz", "Linha H", "Linha V", "Customizada"]
        ttk.Label(self.controls, text="Elemento Estruturante:").pack(side=tk.LEFT)
        self.element_combo = ttk.Combobox(self.controls, textvariable=self.element_var, values=elements, width=10)
        self.element_combo.pack(side=tk.LEFT, padx=5)
        self.element_combo.bind('<<ComboboxSelected>>', self.update_edit_mask_button)

        self.update_edit_mask_button(None)
        
        self.process_save_frame = ttk.Frame(self.controls)
        self.process_save_frame.pack(side=tk.LEFT)
        self.processar_button = ttk.Button(self.process_save_frame, text="Processar", command=self.process_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.process_save_frame, text="Salvar", command=self.save_image).pack(side=tk.LEFT, padx=5)

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
        
        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)
        
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

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def show_mask_editor(self):
        if self.mask_editor is None or not self.mask_editor.winfo_exists():
            self.mask_editor = MaskEditor(self.windows)
        self.mask_editor.focus()


    def update_edit_mask_button(self, event):
        if self.edit_mask_frame:
            self.edit_mask_frame.destroy()
            self.edit_mask_button = None
        
        # Só cria o novo frame e botão se o filtro for "Customizada"
        if self.element_var.get() == "Customizada":
            self.windows.geometry("820x630")
            # Cria um novo frame
            self.edit_mask_frame = ttk.Frame(self.controls)  # controls é o primeiro filho
            
            self.edit_mask_frame.pack(side=tk.LEFT, padx=5, before=self.process_save_frame)
            # Cria o botão dentro do novo frame
            self.edit_mask_button = ttk.Button(
                self.edit_mask_frame, 
                text="Editar Máscara",
                command=self.show_mask_editor
            )
            self.edit_mask_button.pack(fill=tk.BOTH, expand=True)
        else:
            self.windows.geometry("750x630")

    def get_structuring_element(self):
        element_type = self.element_var.get()
        if element_type == "Customizada":
            return self.mask_editor.get_mask()
        elif element_type == "3x3":
            return np.ones((3, 3), np.uint8)
        elif element_type == "Cruz":
            return np.array([[0,1,0], [1,1,1], [0,1,0]], np.uint8)
        elif element_type == "Linha H":
            return np.array([[0,0,0], [1,1,1], [0,0,0]], np.uint8)
        else:  # Linha V
            return np.array([[0,1,0], [0,1,0], [0,1,0]], np.uint8)

    def process_image(self):
        if self.original_image is None:
            return
            
        kernel = self.get_structuring_element()
        operation = self.operation_var.get()
        # Convert to binary if needed
        if self.image_type == "binária":
            img = cv2.threshold(self.original_image, self.binary_threshold, 255, cv2.THRESH_BINARY)[1]
        else:
            img = self.original_image.copy()
        
        if operation == "Dilatação":
            self.processed_image = apply_dilation(img, kernel, self.image_type == "binária")
        elif operation == "Erosão":
            self.processed_image = apply_erosion(img, kernel, self.image_type == "binária")
        elif operation == "Abertura":
            self.processed_image = apply_opening(img, kernel, self.image_type == "binária")
        elif operation == "Fechamento":
            self.processed_image = apply_closing(img, kernel, self.image_type == "binária")
        elif operation == "Contorno Interno":
            self.processed_image = apply_inner_contour(img, kernel, self.image_type == "binária")
        elif operation == "Contorno Externo":
            self.processed_image = apply_outer_contour(img, kernel, self.image_type == "binária")
        elif operation == "Gradiente":
            self.processed_image = apply_gradient(img, kernel, self.image_type == "binária")
        elif operation == "Top-Hat":
            self.processed_image = apply_tophat(img, kernel, self.image_type == "binária")
        else:  # Bottom-Hat
            self.processed_image = apply_bottomhat(img, kernel, self.image_type == "binária")
        
        self.update_display()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.bmp *.pgm *.pbm")])
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.image_type = "binária" if file_path.find("pbm")!=-1 else "cinza"
            self.label.config(text=f"Tipo: {self.image_type}")
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
                    neighborhood[i, j] = image[ny, nx]//255 if self.image_type == "binária" else image[ny, nx]
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