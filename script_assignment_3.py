# Enlace al video: https://youtu.be/c2A9WdlGdDY


# Instanciar la capa de los condados
counties_layer_name = "countyp010_census"
counties_layer = QgsProject.instance().mapLayersByName(counties_layer_name)[0]

# Crear objeto para calcular areas
area = QgsDistanceArea()
area.setEllipsoid('WGS84')

# Crear un diccionario para almacenar el area total por condado
county_areas = {}

# Filtrar los condados de Michigan y calcular el area total por condado
for feature in counties_layer.getFeatures():
    if feature["STATE"] == "MI":
        county_name = feature["COUNTY"]
 
        county_area_partial = area.measureArea(feature.geometry())/1e6

        # Agregar el area de los poligonos que pertenecen al mismo condado
        if county_name in county_areas:
            county_areas[county_name] += county_area_partial
        else:
            county_areas[county_name] = county_area_partial

# Ordenar los condados por area en orden ascendente
sorted_counties = sorted(county_areas.items(), key=lambda x: x[1])

# Obtener los 10 condados más pequeños
smallest_counties = sorted_counties[:10]

# Imprimir en la consola de Python los 10 condados más pequeños
print("10 Smallest Counties in Michigan:")
for county, area in smallest_counties:
    print(f"{county} (MI): {area:.2f} km²")
    
# Seleccionar los 10 condados más pequeños en el mapa
county_ids_to_select = []
for feature in counties_layer.getFeatures():
    if feature["STATE"] == "MI" and feature["COUNTY"] in dict(smallest_counties):
        county_ids_to_select.append(feature.id())

# Seleccionar las entidades en el mapa
counties_layer.selectByIds(county_ids_to_select)
    
