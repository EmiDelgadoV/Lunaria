import ephem
import re
from datetime import datetime, timedelta

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
        """
        Calcula la fase, iluminación y determina si es Creciente o Menguante
        comparando con el día siguiente.
        """
        obs = ephem.Observer()
        # Latitud/Longitud de Argentina (aprox) para mayor precisión
        obs.lat = '-34.6'
        obs.lon = '-58.4'
        
        if fecha:
            obs.date = fecha
            fecha_dt = fecha
        else:
            fecha_dt = datetime.now()
            obs.date = fecha_dt

        moon = ephem.Moon()
        
        # 1. Calcular iluminación HOY
        moon.compute(obs)
        iluminacion_hoy = moon.phase
        
        # 2. Calcular iluminación MAÑANA (para saber la tendencia)
        obs.date = fecha_dt + timedelta(days=1)
        moon.compute(obs)
        iluminacion_manana = moon.phase
        
        # 3. Determinar si crece o decrece
        es_creciente = iluminacion_manana > iluminacion_hoy

        # 4. Asignar Nombre Preciso
        # Definimos márgenes para Nueva y Llena
        if iluminacion_hoy <= 2:
            fase_texto = "Luna Nueva"
        elif iluminacion_hoy >= 98:
            fase_texto = "Luna Llena"
        else:
            # Si no es ni llena ni nueva, es intermedia
            if es_creciente:
                fase_texto = "Luna Creciente" # O "Cuarto Creciente" si prefieres
            else:
                fase_texto = "Luna Menguante" # O "Cuarto Menguante"

        return {
            "fase_texto": fase_texto,
            "iluminacion": round(iluminacion_hoy, 2),
            "fecha_calculada": fecha_dt
        }

    def calcular_proxima_fase(self, fase_nombre):
        """
        Calcula la fecha de la próxima fase lunar solicitada.
        fase_nombre: "luna nueva", "luna llena", "cuarto creciente", "cuarto menguante"
        """
        obs = ephem.Observer()
        obs.date = datetime.now()
        
        # Mapa de nombres a funciones de ephem
        # Usamos claves en minúscula para evitar errores
        fase_limpia = fase_nombre.lower().strip()
        
        mapa_fases = {
            "luna nueva": ephem.next_new_moon,
            "luna llena": ephem.next_full_moon,
            "cuarto creciente": ephem.next_first_quarter_moon,
            "cuarto menguante": ephem.next_last_quarter_moon
        }
        
        if fase_limpia not in mapa_fases:
            return f"Error: Fase '{fase_nombre}' no reconocida."
            
        try:
            # Llamamos a la función correspondiente de ephem
            funcion_ephem = mapa_fases[fase_limpia]
            fecha_ephem = funcion_ephem(obs.date)
            return ephem.localtime(fecha_ephem)
        except Exception as e:
            return f"Error calculando fase: {e}"
    
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