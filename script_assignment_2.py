# Enlace al video: https://youtu.be/Up1B6h675Dw


from qgis.utils import iface
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeatureRequest
)
from PyQt5.QtCore import QVariant

# Obtener el id del county seleccionado y el identificador de la capa a la cual pertenece la acción
feature_id = [%$id%]
layer_id = '[%@layer_id%]'
layer = QgsProject.instance().mapLayer(layer_id)

# Verificar que la geometria este reproyectada en EPSG:5070 si el CRS es diferente - EPSG:5070 es el CRS en el que se visualiza el mapa
target_crs = QgsCoordinateReferenceSystem('EPSG:5070')
transform_context = QgsProject.instance().transformContext()
transform_to_target = QgsCoordinateTransform(layer.crs(), target_crs, transform_context)

# Crear una capa temporal para el buffer con el CRS EPSG:5070
buffer_layer = QgsVectorLayer(f"Polygon?crs={target_crs.authid()}", "[%COUNTY%]_200km_buffer", "memory")
buffer_layer_data = buffer_layer.dataProvider()

# Agregar un campo a la capa temporal para agregar cualquier atributo necesario 
buffer_layer_data.addAttributes([QgsField("id", QVariant.Int)])
buffer_layer.updateFields()

# Definir la distancia del buffer en metros (200 km)
buffer_distance = 200000

# Obtener la geometria del county seleccionado y reprojectarla a EPSG:5070
county_feature = layer.getFeature(feature_id)
county_geometry = county_feature.geometry()
county_geometry.transform(transform_to_target)

# Crear la geometria del buffer
county_buffer = county_geometry.buffer(buffer_distance, 5)

# Crear un feature en la capa temporal y se le asigna la geometria del buffer
f = QgsFeature()
f.setGeometry(county_buffer)

# Establecer el ID de la entidad en la capa original como un atributo
f.setAttributes([feature_id]) 

# Agregar la entidad del buffer a la capa del buffer
buffer_layer_data.addFeatures([f])
buffer_layer.updateExtents()

# Agregar la capa del buffer al projecto
QgsProject.instance().addMapLayer(buffer_layer)

# Obtener el estado del condado seleccionado 
state_name = county_feature["STATE"]  

# Usar la expresion para filtrar los condados que estan en el mismo estado que el condado seleccionado
expression = f'"STATE" = \'{state_name}\''
state_request = QgsFeatureRequest().setFilterExpression(expression)
state_features = layer.getFeatures(state_request)

# Crear una lista para guardar el id de los condados que estan en el mismo estado y se intersectan con el buffer
intersecting_ids = []

# Extraer la geometria del condado seleccionado y se transforma a EPSG:5070
for feature in state_features:
    feature_geometry = feature.geometry()
    feature_geometry.transform(transform_to_target)  
    if feature_geometry.intersects(county_buffer):
        intersecting_ids.append(feature.id())

print(intersecting_ids)

# Seleccionar los condados cuyo id esta en la lista
layer.selectByIds(intersecting_ids)

# Refrescar la visualización para ver los condados de la lista
iface.setActiveLayer(layer)
iface.mapCanvas().refresh()

