import tkinter as tk

class LunarCanvas(tk.Canvas):
    def __init__(self, parent, size=200):
        # El bg debe ser EL MISMO que el de la ventana para que la sombra sea invisible
        color_fondo_app = '#001F3F' 
        super().__init__(parent, width=size, height=size + 30, bg=color_fondo_app, highlightthickness=0)

        self.size = size
        self.center = size // 2
        self.radius = int(size * 0.4)
        self.bg_color = color_fondo_app 

    def dibujar_luna(self, porcentaje, fase_texto=""):
        print(f"Dibujando: {porcentaje}% - Texto: '{fase_texto}'")
        self.delete("all")
        
        color_luz = "#F0E68C"   # Amarillo
        color_sombra = self.bg_color # Azul fondo
        
        r = self.radius
        cx, cy = self.center, self.center

        # 1. Base Iluminada (Amarilla)
        self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color_luz, outline="")

        # 2. Cálculos
        p = porcentaje / 100.0
        texto = fase_texto.lower()
        
        # Detectar tendencia basado en el texto preciso del backend
        # Si dice "menguante", es decreciente. Si no, asumimos creciente.
        es_menguante = "menguante" in texto

        # Casos Extremos
        if p < 0.03: # Nueva (Tapar todo)
            self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color_sombra, outline="")
            self.create_text(cx, cy + r + 25, text=f"Iluminación: {int(porcentaje)}%", fill="white", font=("Arial", 10))
            return
        elif p > 0.97: # Llena (No tapar nada)
            self.create_text(cx, cy + r + 25, text=f"Iluminación: {int(porcentaje)}%", fill="white", font=("Arial", 10))
            return

        # Fases Intermedias
        w = 2 * r * (0.5 - p) # Ancho de la sombra

        # --- LÓGICA HEMISFERIO SUR ---
        
        if es_menguante:
            # MENGUANTE = Forma de "D" (Luz a la Derecha)
            # La sombra viene desde la IZQUIERDA.
            
            # 1. Medio círculo de sombra a la IZQUIERDA
            self.create_arc(cx-r, cy-r, cx+r, cy+r, start=90, extent=180, fill=color_sombra, outline="")
            
            # 2. Elipse correctora
            # Si luz > 50%, la elipse es AMARILLA (Luz) en la izquierda
            # Si luz < 50%, la elipse es AZUL (Sombra) comiendo la derecha
            relleno = color_luz if p > 0.5 else color_sombra
            self.create_oval(cx-w, cy-r, cx+w, cy+r, fill=relleno, outline="")

        else:
            # CRECIENTE = Forma de "C" (Luz a la Izquierda)
            # La sombra viene desde la DERECHA.
            
            # 1. Medio círculo de sombra a la DERECHA
            self.create_arc(cx-r, cy-r, cx+r, cy+r, start=270, extent=180, fill=color_sombra, outline="")
            
            # 2. Elipse correctora
            relleno = color_luz if p > 0.5 else color_sombra
            self.create_oval(cx-w, cy-r, cx+w, cy+r, fill=relleno, outline="")

        # Texto abajo
        y_texto = cy + r + 25 
        self.create_text(cx, y_texto, text=f"Iluminación: {int(porcentaje)}%", 
                         fill="white", font=("Arial", 10))