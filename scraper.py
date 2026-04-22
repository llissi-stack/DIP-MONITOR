import pandas as pd
import json
import cloudscraper  # Importamos la nueva herramienta antibloqueos
from datetime import datetime
import io

def extraer_datos_reales():
    print("Iniciando extracción desde votaciones.hcdn.gob.ar...")
    url_acta = "https://votaciones.hcdn.gob.ar/votacion/6342"
    
    try:
        # 1. Creamos un "navegador fantasma" indetectable
        print("Configurando evasión de firewall...")
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        print(f"Descargando acta: {url_acta}...")
        # Usamos el scraper avanzado en lugar del requests básico
        respuesta = scraper.get(url_acta)
        
        # Verificamos si la descarga fue exitosa
        respuesta.raise_for_status() 
        
        # 2. Leemos la tabla HTML
        print("Leyendo la tabla de votos...")
        tablas = pd.read_html(io.StringIO(respuesta.text))
        df_votos = tablas[0]
        
        perfiles_armados = {}

        # 3. Procesamos los votos
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
            
        print(f"¡Éxito total! Se guardaron los perfiles de {len(perfiles_armados)} diputados.")

    except Exception as e:
        print(f"Error CRÍTICO al intentar extraer los datos: {e}")
        raise e

if __name__ == "__main__":
    extraer_datos_reales()
