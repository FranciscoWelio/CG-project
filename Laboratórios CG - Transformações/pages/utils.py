from tkinter import ttk
import customtkinter as ctk


class FloatEntry(ctk.CTkEntry):
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


class IntEntry(ctk.CTkEntry):
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
                int(new_value)
            return True
        except ValueError:
            return False
    
    def get_value(self):
        """Retorna o valor como float"""
        try:
            return int(self.get())
        except ValueError:
            return 0.0
