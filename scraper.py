import pandas as pd
import json
from datetime import datetime

def extraer_datos_reales():
    print("Iniciando extracción desde votaciones.hcdn.gob.ar...")
    
    # ID de un acta real de prueba (Podemos programarlo para que busque las últimas 10)
    # Por ejemplo, el ID 6342 corresponde a una votación en la HCDN
    url_acta = "https://votaciones.hcdn.gob.ar/votacion/6342"
    
    try:
        # 1. Pandas lee mágicamente la tabla HTML de la página de la cámara
        print(f"Leyendo acta: {url_acta}")
        tablas = pd.read_html(url_acta)
        
        # La tabla de votos suele ser la primera que aparece en la página
        df_votos = tablas[0]
        
        perfiles_armados = {}

        # 2. Iteramos sobre cada fila de la tabla (cada voto de un diputado)
        for index, fila in df_votos.iterrows():
            # Limpiamos los textos
            nombre = str(fila.get('Diputado', '')).strip().upper()
            bloque = str(fila.get('Bloque', '')).strip()
            provincia = str(fila.get('Provincia', '')).strip()
            sentido_voto = str(fila.get('Voto', '')).strip().capitalize()
            
            if not nombre or nombre == 'NAN':
                continue
                
            # Si el diputado no está en nuestro diccionario, lo creamos
            if nombre not in perfiles_armados:
                perfiles_armados[nombre] = {
                    "nombre_oficial": nombre,
                    "provincia": provincia,
                    "bloque": bloque,
                    "mandatos": ["Actual"], # Esto lo podemos pulir luego cruzando bases
                    "alineamiento_bloques": {"Bloque Propio": 100}, # Placeholder temporal
                    "lealtad_anual": {"2026": 100},
                    "votos_anuales": {
                        "2026": {"afirmativo": 0, "negativo": 0, "ausente": 0, "abstencion": 0}
                    },
                    "leyes_destacadas": []
                }
            
            # Contamos su voto anual
            if sentido_voto in ['Afirmativo', 'Negativo', 'Ausente', 'Abstencion']:
                perfiles_armados[nombre]["votos_anuales"]["2026"][sentido_voto.lower()] += 1
            
            # Agregamos esta ley a sus leyes destacadas
            perfiles_armados[nombre]["leyes_destacadas"].append({
                "proyecto": "Acta 6342 (Ejemplo)",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "sentido": sentido_voto
            })

        # 3. Convertimos el diccionario en el formato que espera nuestro index.html
        datos_finales = {
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "diputados": list(perfiles_armados.values())
        }

        # 4. Guardamos el archivo JSON
        with open('datos_legislativos.json', 'w', encoding='utf-8') as archivo:
            json.dump(datos_finales, archivo, ensure_ascii=False, indent=4)
            
        print("¡Extracción y procesamiento completados exitosamente!")

    except Exception as e:
        print(f"Error al intentar extraer los datos: {e}")

if __name__ == "__main__":
    extraer_datos_reales()
