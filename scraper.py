import pandas as pd
import json
from datetime import datetime

def extraer_datos_reales():
    print("Iniciando extracción desde votaciones.hcdn.gob.ar...")
    url_acta = "https://votaciones.hcdn.gob.ar/votacion/6342"
    
    try:
        print(f"Leyendo acta: {url_acta}")
        tablas = pd.read_html(url_acta)
        df_votos = tablas[0]
        
        perfiles_armados = {}

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

        datos_finales = {
            "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "diputados": list(perfiles_armados.values())
        }

        with open('datos_legislativos.json', 'w', encoding='utf-8') as archivo:
            json.dump(datos_finales, archivo, ensure_ascii=False, indent=4)
            
        print("¡Extracción y procesamiento completados exitosamente!")

    except Exception as e:
        print(f"Error al intentar extraer los datos: {e}")

if __name__ == "__main__":
    extraer_datos_reales()
