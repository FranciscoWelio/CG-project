import tkinter as tk
from tkinter import ttk
import numpy as np


class FloatEntry(ttk.Entry):
    def __init__(self, master=None, default=1.0, **kwargs):
        # Define a validação
        self.vcmd = (master.register(self.validate), '%P', '%d')
        super().__init__(master, validate='key', validatecommand=self.vcmd, **kwargs)
        
        # Valor padrão é 0.0
        self.insert(0, str(default))
    
    def validate(self, new_value, action_type):
        # Permite campo vazio ou apenas o ponto decimal
        if new_value == "" or new_value == ".":
            return True
            
        # Verifica se é um número flutuante válido
        try:
            # Verifica se não tem múltiplos pontos decimais
            if new_value.count('.') > 1:
                return False
                
            # Se não for operação de deleção, tenta converter para float
            if action_type != '0':  # '0' é o código para deleção
                float(new_value)
            return True
        except ValueError:
            return False
    
    def get_value(self):
        """Retorna o valor como float"""
        try:
            return float(self.get())
        except ValueError:
            return 0.0

class MaskEditor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Editor de Máscara 3x3")
        self.mask = np.zeros((3, 3), dtype=float)
        self.mask[1, 1] = 1  # Valor padrão no centro
        
        self.entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = ttk.Entry(self, width=8)
                entry.insert(0, str(self.mask[i, j]))
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        ttk.Button(self, text="Aplicar", command=self.apply_mask).grid(row=3, column=0, columnspan=2)
        ttk.Button(self, text="Normalizar", command=self.normalize_mask).grid(row=3, column=1, columnspan=2)
    
    def apply_mask(self):
        for i in range(3):
            for j in range(3):
                try:
                    self.mask[i, j] = float(self.entries[i][j].get())
                except ValueError:
                    self.mask[i, j] = 0
    
    def normalize_mask(self):
        total = np.sum(self.mask)
        if total != 0:
            self.mask = self.mask / total
            for i in range(3):
                for j in range(3):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, f"{self.mask[i, j]:.3f}")

    def get_mask(self):
        self.apply_mask()
        return self.mask

class PixelGridDisplay(ttk.Frame):
    def __init__(self, parent, rows=3, cols=3):
        super().__init__(parent)
        self.entries = []
        
        # Criar grid de entries
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = ttk.Entry(self, width=4, justify='center')
                entry.insert(0, "-")
                entry.grid(row=i, column=j, padx=1, pady=1)
                entry.configure(state='readonly')
                row_entries.append(entry)
            self.entries.append(row_entries)
    
    def update_values(self, values, mask=None):
        """
        Atualiza os valores da grade.
        values: matriz 3x3 com os valores dos pixels
        mask: matriz booleana 3x3 indicando quais posições estão dentro da imagem (True) ou fora (False)
        """
        for i in range(len(self.entries)):
            for j in range(len(self.entries[i])):
                entry = self.entries[i][j]
                entry.configure(state='normal')
                entry.delete(0, tk.END)
                
                value = values[i][j]
                if mask is not None and not mask[i][j]:
                    # Pixel fora da imagem
                    pass
                    #entry.configure(foreground="red")
                    #entry.insert(0, "-")
                else:
                    # Pixel dentro da imagem
                    entry.configure(foreground="black")
                    entry.insert(0, str(int(value)))
                
                entry.configure(state='readonly')