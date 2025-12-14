import tkinter as tk

class LunarCanvas(tk.Canvas):
    def __init__(self, parent, size=200):
        super().__init__(parent, width=size, height=size, bg='#001F3F', highlightthickness=0)

        self.size = size
        self.center = size // 2
        self.radius = int(size * 0.4)

    def dibujar_luna(self, porcentaje, fase_nombre=""):
        """
        Dibuja la fase lunar usando superposición de elipses.
        porcentaje: 0 a 100
        fase_nombre: Texto para saber si es Creciente o Menguante
        """
        self.delete("all")
        
        # 1. Definimos colores
        color_luz = "#F0E68C"   # Amarillo Luna (Khaki)
        color_sombra = "#001F3F" # El mismo azul del fondo (¡Truco!)
        
        r = self.radius
        cx, cy = self.center, self.center

        # 2. Dibujamos la base (Luna Llena)
        # Esto crea el círculo iluminado de fondo
        self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color_luz, outline="")

        # 3. Lógica de sombras
        # Convertimos 0-100 a decimal 0.0-1.0
        p = porcentaje / 100.0

        # Determinamos si es Creciente o Menguante basándonos en el nombre
        # (Esto es una heurística simple: si dice "Menguante" o "Nueva", la sombra va a un lado)
        es_menguante = "menguante" in fase_nombre.lower() or "nueva" in fase_nombre.lower()

        # CASO A: LUNA NUEVA (O casi nueva) -> Todo sombra
        if p < 0.02:
            self.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color_sombra, outline="")
            return # Terminamos

        # CASO B: LUNA LLENA (O casi llena) -> Nada de sombra
        if p > 0.98:
            return # Terminamos (ya dibujamos la base amarilla al principio)

        # CASO C: FASES INTERMEDIAS
        # Aquí viene la magia de la elipse que se encoge
        
        # Ancho de la sombra (va de r a -r)
        # Si p es 0.5 (cuarto), el ancho es 0.
        w = 2 * r * (0.5 - p) # Matemáticas de proyección esférica simplificada

        if es_menguante:
            # Lado izquierdo iluminado, sombra avanza desde la derecha (Hemisferio Norte)
            # Dibuja semicírculo de sombra
            self.create_arc(cx-r, cy-r, cx+r, cy+r, start=270, extent=180, fill=color_sombra, outline="")
            # Dibuja elipse correctora
            self.create_oval(cx-w, cy-r, cx+w, cy+r, fill=color_luz if p > 0.5 else color_sombra, outline="")
        
        else: # Creciente
            # Lado derecho iluminado, sombra avanza desde la izquierda
            # Dibuja semicírculo de sombra
            self.create_arc(cx-r, cy-r, cx+r, cy+r, start=90, extent=180, fill=color_sombra, outline="")
            # Dibuja elipse correctora
            self.create_oval(cx-w, cy-r, cx+w, cy+r, fill=color_luz if p > 0.5 else color_sombra, outline="")

        # 4. Texto informativo encima (Opcional, para debug)
        # self.create_text(cx, cy + r + 20, text=f"{int(porcentaje)}%", fill="white", font=("Arial", 10))

        # Dibujar el círculo base
        self.create_oval(x1, y1, x2, y2, fill='black', outline='white')
        
        # Logica temporal (texto)
        self.create_text(self.center, self.center, text=f"{iluminacion}%", fill="white", font=("Arial", 14, "bold"))