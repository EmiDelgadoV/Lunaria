import tkinter as tk

class LunarCanvas(tk.Canvas):
    def __init__(self, parent, size=200):
        super().__init__(parent, width=size, height=size, bg='#001F3F', highlightthickness=0)

        self.size = size
        self.center = size // 2
        self.radius = int(size * 0.4)

    def dibujar_luna(self, iluminacion, fase_texto=""):
        # Recibe la iluminacion y dibuja la luna correspondiente.
        self.delete("all")  # Limpiar el canvas antes de dibujar
        x1 = self.center - self.radius
        y1 = self.center - self.radius
        x2 = self.center + self.radius
        y2 = self.center + self.radius

        # Dibujar el círculo base
        self.create_oval(x1, y1, x2, y2, fill='black', outline='white')
        
        # Logica temporal (texto)
        self.create_text(self.center, self.center, text=f"{iluminacion}%", fill="white", font=("Arial", 14, "bold"))