import ephem
import re
from datetime import datetime

class CalculadoraLunar:
    #se encarga de la logica astronomica, solo devuelve datos.
    def normalizar_fecha(self, fecha_str):
        fecha_str = re.sub(r'[-.]', '/', fecha_str)
        try:
            partes = fecha_str.split('/')
            if len(partes) != 3:
                return None
            d, m, y = partes
            if len(y) == 2:
                y = '20' + y

            fecha_limpia = f"{d.zfill(2)}/{m.zfill(2)}/{y}"
            return datetime.strptime(fecha_limpia, '%d/%m/%Y')
        except ValueError:
            return None


    def obtener_fase_actual(self, fecha=None):
        if fecha is None:
            fecha = datetime.now()
        luna = ephem.Moon(fecha)
        iluminacion = luna.phase
        fase_texto = ""
        if iluminacion < 2:
            fase_texto = "Luna Nueva"
        elif iluminacion > 95:
            fase_texto = "Luna Llena"
        else:
            fase_texto = "Cuarto Creciente/ Menguante"
        return {
            "fase_texto": fase_texto,
            "iluminacion": round(iluminacion, 2),
            "fecha_calculada": fecha

        }

    def calcular_proxima_fase(self, tipo_fase):
        fecha_ephem = None
        hoy = datetime.now()
        tipo_fase = tipo_fase.lower()

        if tipo_fase == "luna nueva":
            fecha_ephem = ephem.next_new_moon(hoy)

        elif tipo_fase == "luna llena":
            fecha_ephem = ephem.next_full_moon(hoy)

        else:
            return "Fase no reconocida."
        return fecha_ephem.datetime()
    
# ... todo tu código de la clase arriba ...

if __name__ == "__main__":
    # Zona de Pruebas (Esto no se ejecuta cuando importas el archivo)
    calc = CalculadoraLunar()
    
    print("--- PRUEBA 1: Fase Actual ---")
    datos = calc.obtener_fase_actual() # Prueba sin fecha (hoy)
    print(f"Hoy: {datos['fase_texto']} ({datos['iluminacion']}%)")
    
    print("\n--- PRUEBA 2: Próxima Luna Llena ---")
    prox_llena = calc.calcular_proxima_fase("luna llena")
    print(f"Próxima Luna Llena: {prox_llena}")