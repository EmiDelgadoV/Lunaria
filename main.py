import tkinter as tk
from tkinter import messagebox
from lunar_backend import CalculadoraLunar

class LunariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lunaria - Calculadora Lunar")
        self.root.geometry("400x300")

        self.backend = CalculadoraLunar()
        # Interfaz básica
        self.label_titulo = tk.Label(root, text="Fases de la Luna", font=("Arial", 16))
        self.label_titulo.pack(pady=20)

        self.btn_actual = tk.Button(root, text="Consultar Fase Hoy", command=self.mostrar_fase_actual)
        self.btn_actual.pack(pady=10)

        # Botón Luna Llena
        self.btn_llena = tk.Button(root, text="Próxima Luna Llena", 
                                   command=lambda: self.mostrar_proxima_fase("luna llena"))
        self.btn_llena.pack(pady=5)
    
        self.btn_nueva = tk.Button(root, text="Próxima Luna Nueva", 
                                   command=lambda: self.mostrar_proxima_fase("luna nueva"))
        self.btn_nueva.pack(pady=5)
        
        self.label_resultado = tk.Label(root, text="...", fg="blue")
        self.label_resultado.pack(pady=20)

    def mostrar_proxima_fase(self, fase):
        fecha_resultado = self.backend.calcular_proxima_fase(fase)
        if isinstance(fecha_resultado, str):
            messagebox.showerror("Error", fecha_resultado)
        else:
            fecha_texto = fecha_resultado.strftime('%d-%m-%y')
            mensaje = f"La próxima {fase} será el {fecha_texto}"
            messagebox.showinfo(f"Próxima {fase}", mensaje)

    def mostrar_fase_actual(self):
        datos = self.backend.obtener_fase_actual()
        mensaje = f"Fase: {datos['fase_texto']}\nIluminación: {datos['iluminacion']}%\nFecha: {datos['fecha_calculada'].strftime('%d-%m-%y')}"
        messagebox.showinfo("Fase Actual de la Luna", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = LunariaApp(root)
    root.mainloop()