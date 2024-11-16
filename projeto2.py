import tkinter as tk
from tkinter import ttk
from pages import (
    ImageFilterProcessor,
    ImageIntensityProcessor,
    ImageOperationsProcessor,
    HistogramEqualizer,
    MorphologicalProcessor,
)


class MainPage:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Projeto Unidade 2")
        self.window.geometry("400x300")
        self.restore()

    def clear_window(self):
        # Destroy all widgets in the window
        for widget in self.window.winfo_children():
            widget.destroy()

    def restore(self):
        self.clear_window()
        self.window.title("Projeto Unidade 2")
        self.window.geometry("400x300")
        center_frame = ttk.Frame(self.window)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Button(center_frame, text="Filtros", command=self.open_filters, width=20).pack(pady=10)
        ttk.Button(center_frame, text="Operações Básicas", command=self.open_operations, width=20).pack(pady=10)
        ttk.Button(center_frame, text="Transformações de Intensidade", command=self.open_transform, width=30).pack(pady=10)
        ttk.Button(center_frame, text="Histograma", command=self.open_histogram, width=20).pack(pady=10)
        ttk.Button(center_frame, text="Operações Morfológicas", command=self.open_morphology, width=25).pack(pady=10)

    def open_filters(self):
        self.clear_window()
        ImageFilterProcessor(self.window, self.restore)
    
    def open_operations(self):
        self.clear_window()
        ImageOperationsProcessor(self.window, self.restore)

    def open_transform(self):
        self.clear_window()
        ImageIntensityProcessor(self.window, self.restore)

    def open_histogram(self):
        self.clear_window()
        HistogramEqualizer(self.window, self.restore)

    def open_morphology(self):
        self.clear_window()
        MorphologicalProcessor(self.window, self.restore)

        

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = MainPage()
    try:
        app.run()
    except KeyboardInterrupt:
        pass