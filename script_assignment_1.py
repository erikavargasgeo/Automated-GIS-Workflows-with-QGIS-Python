# Enlace al video: https://youtu.be/_R9NrestajM


# Crear capa poligonal del edificio
building_layer = QgsVectorLayer("Polygon?crs=epsg:2903", "building", "memory")

# Agregar el campo de atributos usando la funcion data provider addAttributes()
from qgis.PyQt.QtCore import QVariant
building_layer_data = building_layer.dataProvider()
building_layer_data.addAttributes([QgsField("name", QVariant.String)])
building_layer.updateFields()

# Definir las coordenadas del poligono correspondiente al edificio
lower_left = QgsPointXY(1524068, 1481448)
upper_right = QgsPointXY(1524312, 1481897)
building_polygon = QgsGeometry.fromPolygonXY([[
    lower_left,
    QgsPointXY(lower_left.x(), upper_right.y()),
    upper_right,
    QgsPointXY(upper_right.x(), lower_left.y()),
    lower_left
]])

# Agregar la entidad poligonal y añadir la capa al proyecto
f = QgsFeature()
f.setGeometry(building_polygon)
f.setAttributes(["Building_01"])
building_layer_data.addFeature(f)
building_layer.updateExtents()
QgsProject.instance().addMapLayer(building_layer)

# Cambiar el color del poligono 
building_layer.renderer().symbol().setColor(QColor("red"))
building_layer.triggerRepaint()

# Actualizar la simbologia
iface.layerTreeView().refreshLayerSymbology(building_layer.id())


# Cambiar el código de zona de la parcela con id 9 a R-1 de la capa poligonal 'Parcels'
parcels_layer = QgsProject.instance().mapLayersByName("Parcels")[0]
with edit(parcels_layer):
    for parcel in parcels_layer.getFeatures():
        if parcel["id"] == 9:
            parcel["zonecode"] = "R-1"
            parcels_layer.updateFeature(parcel)




