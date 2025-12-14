import tkinter as tk
from tkinter import messagebox
from lunar_backend import CalculadoraLunar
from canvas import LunarCanvas
import random

# Colores de la app
COLOR_FONDO = "#001F3F"    # Azul noche
COLOR_TEXTO = "white"
COLOR_BOTON = "#F0E68C"    # Amarillo Luna
COLOR_TEXTO_BTN = "black"

class LunariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lunaria 1.0")
        self.root.geometry("400x400")
        self.root.configure(bg=COLOR_FONDO)
        
        self.backend = CalculadoraLunar()

        # --- FONDO ESTRELLADO ---
        self.canvas_bg = tk.Canvas(root, bg=COLOR_FONDO, highlightthickness=0)
        self.canvas_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.dibujar_estrellas_fondo()
        # Redibujar estrellas si cambian el tamaño de ventana
        self.root.bind("<Configure>", lambda e: self.dibujar_estrellas_fondo())

        # --- FRAME PRINCIPAL (Para centrar el menú) ---
        self.frame_menu = tk.Frame(root, bg=COLOR_FONDO)
        self.frame_menu.place(relx=0.5, rely=0.5, anchor="center")

        # Título y Subtítulo
        tk.Label(self.frame_menu, text="Lunaria", font=("Arial", 24, "bold"), 
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(0, 5))
        
        tk.Label(self.frame_menu, text="¡Bienvenido! ¿Qué deseas consultar?", font=("Arial", 10), 
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(0, 20))

        # --- BOTONES DEL MENÚ ---
        self.crear_boton_menu("Consultar la fase de esta noche", self.abrir_ventana_esta_noche)
        self.crear_boton_menu("Consultar sobre una fecha específica", self.abrir_ventana_fecha)
        self.crear_boton_menu("Consultar siguiente fase", self.abrir_ventana_proxima)

    def crear_boton_menu(self, texto, comando):
        btn = tk.Button(self.frame_menu, text=texto, command=comando,
                        bg=COLOR_BOTON, fg=COLOR_TEXTO_BTN, 
                        font=("Arial", 10, "bold"), relief="ridge", bd=3, width=30)
        btn.pack(pady=5)

    def dibujar_estrellas_fondo(self):
        self.canvas_bg.delete("star")
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        # Dibujamos 50 estrellas aleatorias
        for _ in range(50):
            x = random.randint(0, w)
            y = random.randint(0, h)
            size = random.randint(1, 3)
            self.canvas_bg.create_oval(x, y, x+size, y+size, fill="white", tags="star")

    # ==========================================
    # CASO 1: ESTA NOCHE
    # ==========================================
    def abrir_ventana_esta_noche(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Fase de esta noche")
        ventana.geometry("350x450")
        ventana.configure(bg=COLOR_FONDO)

        datos = self.backend.obtener_fase_actual()
        fecha_str = datos['fecha_calculada'].strftime("%d/%m/%Y")

        # Texto Informativo
        tk.Label(ventana, text=f"La fase de esta noche ({fecha_str}) es:", 
                 bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Arial", 11)).pack(pady=20)
        
        tk.Label(ventana, text=datos['fase_texto'], 
                 bg=COLOR_FONDO, fg=COLOR_BOTON, font=("Arial", 16, "bold")).pack(pady=5)

        # Gráfico (Canvas)
        canvas_luna = LunarCanvas(ventana, size=200)
        canvas_luna.pack(pady=20)

        canvas_luna.dibujar_luna(datos['iluminacion'], datos['fase_texto'])

        # Porcentaje
        

    # ==========================================
    # CASO 2: FECHA ESPECÍFICA
    # ==========================================
    def abrir_ventana_fecha(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar Fecha")
        ventana.geometry("300x200")
        ventana.configure(bg=COLOR_FONDO)

        tk.Label(ventana, text="¿Cuál es la fecha que deseas consultar?", 
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=15)
        tk.Label(ventana, text="(Formatos: dd/mm/aa, dd-mm-aaaa)", 
                 bg=COLOR_FONDO, fg="#AAAAAA", font=("Arial", 8)).pack()

        entrada_fecha = tk.Entry(ventana)
        entrada_fecha.pack(pady=10)

        def buscar():
            texto = entrada_fecha.get()
            fecha_dt = self.backend.normalizar_fecha(texto)
            
            if not fecha_dt:
                messagebox.showerror("Error", "Formato de fecha no válido", parent=ventana)
                return
            
            # Si la fecha es válida, abrimos el resultado
            self.mostrar_resultado_fecha(fecha_dt)
            ventana.destroy() # Cerramos la ventanita de input

        btn = tk.Button(ventana, text="Consultar", command=buscar, bg=COLOR_BOTON, fg=COLOR_TEXTO_BTN)
        btn.pack(pady=10)

    def mostrar_resultado_fecha(self, fecha_dt):
        ventana = tk.Toplevel(self.root)
        ventana.title("Resultado por fecha")
        ventana.geometry("350x450")
        ventana.configure(bg=COLOR_FONDO)

        datos = self.backend.obtener_fase_actual(fecha_dt)
        fecha_str = fecha_dt.strftime("%d/%m/%Y")

        tk.Label(ventana, text=f"El día {fecha_str} la luna estaba/estará:", 
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=20)
        
        tk.Label(ventana, text=datos['fase_texto'], 
                 bg=COLOR_FONDO, fg=COLOR_BOTON, font=("Arial", 16, "bold")).pack(pady=5)

        canvas_luna = LunarCanvas(ventana, size=200)
        canvas_luna.pack(pady=20)
        canvas_luna.dibujar_luna(datos['iluminacion'], datos['fase_texto'])

    def abrir_ventana_proxima(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Consultar Siguiente Fase")
        ventana.geometry("300x300")
        ventana.configure(bg=COLOR_FONDO)

        tk.Label(ventana, text="Selecciona la fase:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=("Arial", 12)).pack(pady=15)

        fases = ["Luna Nueva", "Luna Llena", "Cuarto Creciente", "Cuarto Menguante"]
        
        for fase in fases:
            btn = tk.Button(ventana, text=fase, 
                            command=lambda f=fase: self.mostrar_resultado_proxima(f),
                            bg=COLOR_BOTON, fg=COLOR_TEXTO_BTN, width=20)
            btn.pack(pady=5)

    def mostrar_resultado_proxima(self, fase_nombre):
        fecha_dt = self.backend.calcular_proxima_fase(fase_nombre)
        
        if isinstance(fecha_dt, str): # Si hubo error
            messagebox.showerror("Error", fecha_dt)
            return

        fecha_str = fecha_dt.strftime("%d/%m/%Y")
        
        # Mostramos resultado (puede ser un messagebox simple o ventana, usaré messagebox para variar)
        messagebox.showinfo(f"Próxima {fase_nombre}", 
                            f"La próxima {fase_nombre} será el:\n\n{fecha_str}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LunariaApp(root)
    root.mainloop()