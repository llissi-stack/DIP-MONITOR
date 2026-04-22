import pandas as pd
import json
import requests
from datetime import datetime
import io

def extraer_datos_reales():
    print("Iniciando extracción desde votaciones.hcdn.gob.ar...")
    url_acta = "https://votaciones.hcdn.gob.ar/votacion/6342"
    
    try:
        # 1. Le ponemos un "disfraz" (User-Agent) para que la página no bloquee al robot
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        print(f"Descargando acta: {url_acta}")
        respuesta = requests.get(url_acta, headers=headers)
        
        # Si la página nos bloquea, esto fuerza a que el programa tire un error y nos avise
        respuesta.raise_for_status() 
        
        # 2. Leemos las tablas desde el texto HTML descargado
        print("Leyendo la tabla de votos...")
        # io.StringIO evita una advertencia técnica de la librería pandas
        tablas = pd.read_html(io.StringIO(respuesta.text))
        df_votos = tablas[0]
        
        perfiles_armados = {}

        # 3. Procesamos fila por fila
        for index, fila in df_votos.iterrows():
            nombre = str(fila.get('Diputado', '')).strip().upper()
            bloque = str(fila.get('Bloque', '')).strip()
            provincia = str(fila.get('Provincia', '')).strip()
            sentido_voto = str(fila.get('Voto', '')).strip().capitalize()
            
            if not nombre or nombre == 'NAN':
                continue
                
            if nombre not in perfiles_armados:
                perfiles_armados[nombre] = {
                    "nombre_oficial": nombre,
                    "provincia": provincia,
                    "bloque": bloque,
                    "mandatos": ["Actual"],
                    "alineamiento_bloques": {"Bloque Propio": 100}, 
                    "lealtad_anual": {"2026": 100},
                    "votos_anuales": {
                        "2026": {"afirmativo": 0, "negativo": 0, "ausente": 0, "abstencion": 0}
                    },
                    "leyes_destacadas": []
                }
            
            if sentido_voto in ['Afirmativo', 'Negativo', 'Ausente', 'Abstencion']:
                perfiles_armados[nombre]["votos_anuales"]["2026"][sentido_voto.lower()] += 1
            
            perfiles_armados[nombre]["leyes_destacadas"].append({
                "proyecto": "Acta 6342",
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "sentido": sentido_voto
            })

        # 4. Guardamos los datos
        datos_finales = {
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "diputados": list(perfiles_armados.values())
        }

        with open('datos_legislativos.json', 'w', encoding='utf-8') as archivo:
            json.dump(datos_finales, archivo, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se guardaron los perfiles de {len(perfiles_armados)} diputados.")

    except Exception as e:
        print(f"Error CRÍTICO al intentar extraer los datos: {e}")
        # Hacemos que el script falle "ruidosamente" para que GitHub nos avise si algo sale mal
        raise e

if __name__ == "__main__":
    extraer_datos_reales()
