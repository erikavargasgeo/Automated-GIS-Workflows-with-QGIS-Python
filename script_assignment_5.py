# Enlace al video: https://youtu.be/QBj9TbyWBkQ


import requests
from qgis.core import *
from qgis.utils import *

@qgsfunction(args='auto', group='Custom')
def fetch_population(feature, parent):
  
    # Obtener el codigo ISO del pais a partir de la entidad
    iso_code = feature['iso_a2']
    if not iso_code:
        return None
    
    # Definir la URL de the Worldbank API 
    url = f"http://api.worldbank.org/v2/countries/{iso_code}/indicators/SP.POP.TOTL?format=json"
    
    try:
        # Hacer la solicitud GET a la API
        response = requests.get(url)
        
        # Obtener el JSON de la respuesta a la solicitud
        data = response.json()
        
        # Verificar di la respuesta contiene información valida
        if len(data) > 1 and "value" in data[1][0]:
            # Obtener el ultimo valor de población
            population = data[1][0]["value"]
            return int(population) if population is not None else None
            # Retornar None si el dato no se encuentra o es inavalido
        else:
            return None
    
    except requests.RequestException as e:
        # Reaccionar a errores a la solicitud GET
        QgsMessageLog.logMessage(f"Error fetching population data: {e}", "fetch_population", Qgis.Warning)
        return None