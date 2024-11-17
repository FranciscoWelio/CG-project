from typing import Callable
import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from .utils import (
    PixelGridDisplay,
    MaskEditor,
    FloatEntry,
)


class ImageFilterProcessor:
    def __init__(self, window: tk.Tk, restore: Callable[[], None]):
        self.restore = restore
        self.original_image = None
        self.processed_image = None
        self.custom_mask = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float)
        self.scale_factor = 1.0
        self.mask_editor= None
        self.edit_mask_button = None
        window.title("Projeto Unidade 2 > Filtros")
        window.geometry("700x630")
        self.windows = window

        ttk.Button(window, text="Voltar", command=restore).pack(pady=5)
        
        # Controles superiores
        self.controls = ttk.Frame(window)
        self.controls.pack(pady=10)
        
        ttk.Button(self.controls, text="Carregar Imagem", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
        self.filter_var = tk.StringVar(value="Média")
        filters = ["Customizada", "Média", "Mediana", "Passa Alto Básico", "Alto Reforço(High Boost)", "Prewitt em x", "Prewitt em y", "Prewitt Magnitude", "Sobel em x", "Sobel em y", "Sobel Magnitude", "Robert em x", "Robert em y", "Robert Magnitude", "Robert Cruzado em x", "Robert Cruzado em y", "Robert Cruzado Magnitude"]
        self.filter_combo = ttk.Combobox(self.controls, textvariable=self.filter_var, values=filters)
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        # Vincula a função que atualiza o botão à mudança no dropdown
        self.filter_combo.bind('<<ComboboxSelected>>', self.update_edit_mask_button)
        
        # Frame para o botão de editar máscara (para manter o espaço consistente)
        self.edit_mask_frame = ttk.Frame(self.controls)
        self.edit_mask_frame.pack(side=tk.LEFT, padx=5)

        self.update_edit_mask_button(None)

        # ttk.Button(controls, text="Editar Máscara", command=self.show_mask_editor).pack(side=tk.LEFT, padx=5)
        self.process_save_frame = ttk.Frame(self.controls)
        self.process_save_frame.pack(side=tk.LEFT)
        self.processar_button = ttk.Button(self.process_save_frame, text="Processar", command=self.process_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.process_save_frame, text="Salvar", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Criar frame com scrollbar
        self.scroll_frame = ttk.Frame(window)
        self.scroll_frame.pack(expand=True, fill=tk.BOTH)

        # Criar canvas
        self.canvas = tk.Canvas(self.scroll_frame)
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Configurar scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Criar janela no canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Empacotar canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Configurar mousewheel
        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

        # Container principal para imagens e malhas
        main_container = ttk.Frame(self.scrollable_frame)
        main_container.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Container esquerdo (imagem original e malha)
        left_container = ttk.Frame(main_container)
        left_container.pack(side=tk.LEFT, padx=10)
        
        self.original_label = ttk.Label(left_container)
        self.original_label.pack()
        
        ttk.Label(left_container, text="Malha Original:").pack(pady=(10,5))
        self.original_grid = PixelGridDisplay(left_container, rows=10, cols=10)
        self.original_grid.pack()
        
        # Container direito (imagem processada e malha)
        right_container = ttk.Frame(main_container)
        right_container.pack(side=tk.LEFT, padx=10)
        
        self.processed_label = ttk.Label(right_container)
        self.processed_label.pack()
        
        ttk.Label(right_container, text="Malha Processada:").pack(pady=(10,5))
        self.processed_grid = PixelGridDisplay(right_container, rows=10, cols=10)
        self.processed_grid.pack()
        
        # Bind eventos do mouse
        self.original_label.bind('<Motion>', self.update_grid_values)
        self.processed_label.bind('<Motion>', self.update_grid_values)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_edit_mask_button(self, event):
        if self.edit_mask_frame:
            self.edit_mask_frame.destroy()
            self.edit_mask_button = None
        
        # Só cria o novo frame e botão se o filtro for "Customizada"
        if self.filter_var.get() == "Customizada":
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
        elif self.filter_var.get() == "Alto Reforço(High Boost)":
            # Cria um novo frame
            self.edit_mask_frame = ttk.Frame(self.controls)  # controls é o primeiro filho
            
            self.edit_mask_frame.pack(side=tk.LEFT, padx=5, before=self.process_save_frame)
        
            # Label
            ttk.Label(self.edit_mask_frame, text="A=").pack(side=tk.LEFT, padx=(0, 5))
            
            # Float Entry
            self.high_boost_a = FloatEntry(self.edit_mask_frame, width=10)
            self.high_boost_a.pack(side=tk.LEFT)


    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp *.pgm")])
        if file_path:
            self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.update_display()
    
    def show_mask_editor(self):
        if self.mask_editor is None or not self.mask_editor.winfo_exists():
            self.mask_editor = MaskEditor(self.windows)
        self.mask_editor.focus()
    
    def get_pixel_neighborhood(self, image, x, y, size=3):
        if image is None:
            return np.zeros((size, size)), np.zeros((size, size), dtype=bool)
            
        height, width = image.shape
        half = size // 2
        
        # Converter coordenadas da tela para coordenadas da imagem
        img_x = int(x / self.scale_factor)
        img_y = int(y / self.scale_factor)
        
        neighborhood = np.zeros((size, size))
        mask = np.zeros((size, size), dtype=bool)


        # Preencher a vizinhança e a máscara
        for i in range(size):
            for j in range(size):
                # Calcular coordenadas na imagem
                ny = img_y + (i - half)
                nx = img_x + (j - half)
                
                # Se a coordenada estiver dentro da imagem, usar o valor do pixel
                if (0 <= ny < height) and (0 <= nx < width):
                    neighborhood[i, j] = image[ny, nx]
                    mask[i, j] = True
                # Se estiver fora, manter o valor 0 e máscara False

        # Extrair vizinhança
        return neighborhood, mask

    def update_grid_values(self, event):
        if self.original_image is None:
            return
            
        # Determinar qual label gerou o evento
        is_original = event.widget == self.original_label
        
        # Obter coordenadas relativas à imagem
        x = event.x
        y = event.y
        
        # Atualizar ambas as malhas com os valores correspondentes
        if is_original and self.original_image is not None:
            orig_values, orig_mask = self.get_pixel_neighborhood(self.original_image, x, y, 10)
            self.original_grid.update_values(orig_values, orig_mask)
            
            if self.processed_image is not None:
                proc_values, proc_mask = self.get_pixel_neighborhood(self.processed_image, x, y, 10)
                self.processed_grid.update_values(proc_values, proc_mask)
        
        elif not is_original and self.processed_image is not None:
            proc_values, proc_mask = self.get_pixel_neighborhood(self.processed_image, x, y, 10)
            self.processed_grid.update_values(proc_values, proc_mask)
            
            if self.original_image is not None:
                orig_values, orig_mask = self.get_pixel_neighborhood(self.original_image, x, y, 10)
                self.original_grid.update_values(orig_values, orig_mask)

    def update_display(self):
        if self.original_image is not None:
            # Redimensionar imagem se for muito grande
            height, width = self.original_image.shape
            max_size = 500
            if height > max_size or width > max_size:
                self.scale_factor = max_size / max(height, width)
                new_size = (int(width * self.scale_factor), int(height * self.scale_factor))
                display_image = cv2.resize(self.original_image, new_size)
            else:
                display_image = self.original_image.copy()
                self.scale_factor = 1.0
            
            original_photo = self.convert_to_photo(display_image)
            self.original_label.configure(image=original_photo)
            self.original_label.image = original_photo
        
        if self.processed_image is not None:
            # Usar o mesmo fator de escala da imagem original
            height, width = self.processed_image.shape
            if self.scale_factor != 1.0:
                new_size = (int(width * self.scale_factor), int(height * self.scale_factor))
                display_image = cv2.resize(self.processed_image, new_size)
            else:
                display_image = self.processed_image.copy()
                
            processed_photo = self.convert_to_photo(display_image)
            self.processed_label.configure(image=processed_photo)
            self.processed_label.image = processed_photo
    
    def convert_to_photo(self, cv_image):
        pil_image = Image.fromarray(cv_image)
        return ImageTk.PhotoImage(pil_image)
    
    def apply_mask_manually(self, image, mask):
        """Aplica a máscara pixel a pixel na imagem."""
        height, width = image.shape
        output = np.zeros_like(image)
        mask_size = len(mask)
        offset = mask_size // 2
        
        for y in range(height):
            for x in range(width):
                sum_value = 0.0
                
                # Aplicar a máscara
                for i in range(mask_size):
                    for j in range(mask_size):
                        # Coordenadas na vizinhança
                        img_y = y + (i - offset)
                        img_x = x + (j - offset)
                        
                        # Se a coordenada estiver fora da imagem, usar 0
                        if img_y < 0 or img_y >= height or img_x < 0 or img_x >= width:
                            pixel_value = 0
                        else:
                            pixel_value = image[img_y, img_x]
                        
                        mask_value = mask[i][j]
                        sum_value += pixel_value * mask_value
                
                # Garantir que o valor esteja no intervalo [0, 255]
                output[y, x] = np.clip(sum_value, 0, 255)
        
        return output

    def process_median(self, image) -> cv2.Mat:
        height, width = image.shape
        output = np.zeros_like(image)
        mask_size = 3
        offset = mask_size // 2
        
        for y in range(height):
            for x in range(width):
                processed_pixel = 0.0
                pixels = []
                # Aplicar a máscara
                for i in range(mask_size):
                    for j in range(mask_size):
                        # Coordenadas na vizinhança
                        img_y = y + (i - offset)
                        img_x = x + (j - offset)
                        
                        # Se a coordenada estiver fora da imagem, usar 0
                        if img_y < 0 or img_y >= height or img_x < 0 or img_x >= width:
                            pixels.append(0)
                        else:
                            pixels.append(image[img_y, img_x])
                pixels.sort()
                if len(pixels) % 2 == 0:
                    processed_pixel = (pixels[len(pixels) - 1] + pixels[len(pixels)])/2
                else:
                    processed_pixel = pixels[len(pixels) // 2]
                # Garantir que o valor esteja no intervalo [0, 255]
                output[y, x] = np.clip(processed_pixel, 0, 255)
        return output

    def process_image(self):
        if self.original_image is None:
            return
            
        filter_type = self.filter_var.get()
        
        if filter_type == "Customizada" and self.mask_editor is not None:
            kernel = self.mask_editor.get_mask()
        elif filter_type == "Média":
            kernel = np.ones((3, 3), dtype=float) / 9
        elif filter_type == "Mediana":
            self.processed_image = self.process_median(self.original_image)# cv2.medianBlur(self.original_image, 3)
            self.update_display()
            return
        elif filter_type == "Passa Alto Básico":
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float)
        elif filter_type == "Alto Reforço(High Boost)":
            # Aplica filtro da média em imagem temporária
            temp = self.process_median(self.original_image)
            
            height, width = temp.shape
            self.processed_image = np.zeros_like(temp)
            # Obtém o valor de A 
            a = self.high_boost_a.get_value()
            for y in range(height):
                for x in range(width):
                    # Obtem o valor da média a partir da imagem temporária
                    mediana = temp[y, x]
                    pixel_original = float(self.original_image[y, x])
                    # Realiza o calculo do valor do pixel a ser processado
                    mascara_nitidez = pixel_original - float(mediana)
                    processed_pixel = pixel_original + a*mascara_nitidez
                    processed_pixel = max(processed_pixel, 0) if processed_pixel <0 else min(processed_pixel, 255)
                    self.processed_image[y, x] = np.clip(processed_pixel, 0, 255)
            self.update_display()
            return
        elif filter_type == "Gradiente em y":
            kernel = np.array([[0, 0, 0], [0, 1, -1], [0, -1, -1]], dtype=float)
        elif filter_type == "Prewitt em x":
            kernel = np.array([[-1, -1, -1], [ 0, 0,  0], [1, 1, 1]], dtype=float)
        elif filter_type == "Prewitt em y":
            kernel = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
        elif filter_type == "Prewitt Magnitude":
            kernel = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]], dtype=float)
        elif filter_type == "Sobel em x":
            kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
        elif filter_type == "Sobel em y":
            kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
        elif filter_type == "Sobel Magnitude":
            kernel = np.array([[-2, -2, 0], [-2, 0, 2], [0, 2, 2]], dtype=float)
        elif filter_type == "Robert em x":
            kernel = np.array([[0, 0, 0], [0, 1, 0], [0, -1, 0]], dtype=float)
        elif filter_type == "Robert em y":
            kernel = np.array([[0, 0, 0], [0, 1, -1], [0, 0, 0]], dtype=float)
        elif filter_type == "Robert Magnitude":
            kernel = np.array([[0, 0, 0], [0, 2, -1], [0, -1, 0]], dtype=float)
        elif filter_type == "Robert Cruzado em x":
            kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, -1]], dtype=float)
        elif filter_type == "Robert Cruzado em y":
            kernel = np.array([[0, 0, 0], [0, 0, 1], [0, -1, 0]], dtype=float)
        elif filter_type == "Robert Cruzado Magnitude":
            kernel = np.array([[0, 0, 0], [0, 1, 1], [0, -1, -1]], dtype=float)

        
        self.processed_image = self.apply_mask_manually(self.original_image, kernel)# cv2.filter2D(self.original_image, -1, kernel)
        self.update_display()
    
    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                   filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
            if file_path:
                cv2.imwrite(file_path, self.processed_image)