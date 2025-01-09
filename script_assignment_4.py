# Enlace al video: https://youtu.be/u9lpt56iJSQ


import processing
from qgis.core import QgsProject

project = QgsProject.instance()
project.read('D:\MasterGIS\Modulo_12_GIS_workflows\assignment_4\Baltimore_Atlas_neighborhoods.qgz')

# Definir el ID del modelo
model_id = "model:Model_Neighborhoods_begin_letters"

# Definir la carpeta para almacenar la salida
output_folder = "D:/MasterGIS/Modulo_12_GIS_workflows/assignment_4/"

# Definir las letras de interes
letters = ['U','S','A']

# Correr en ciclo cada letra y usar el modelo creado anteriormente
for letter in letters:
    # Definir la ruta para el PDF de salida
    output_pdf = f"{output_folder}Neighborhoods_begin_with_{letter}.pdf"
    
    # Definir los parametros usados en el modelo
    params = {
        'initial_letter': letter,
        'neighborhoods_layout_pdf': output_pdf
    }
    
    # Correr el modelo
    try:
        result = processing.run(model_id, params)
        print(f"Successfully created PDF for neighborhoods starting with '{letter}': {output_pdf}")
    except Exception as e:
        print(f"Failed to process neighborhoods for letter '{letter}': {e}")