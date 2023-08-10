
# Define the extent of the polyline layer

# Create a new polyline layer
crs = QgsCoordinateReferenceSystem('EPSG:4326')  # Replace with your desired CRS
polyline_layer = QgsVectorLayer('LineString?crs={0}'.format(crs.authid()), 'Polyline Layer', 'memory')
provider = polyline_layer.dataProvider()

# Define the fields for the polyline layer (optional)
fields = QgsFields()
fields.append(QgsField('ID', QVariant.Int))

# Start editing the polyline layer
polyline_layer.startEditing()
provider.addAttributes(fields)

rect = iface.mapCanvas().layers()[0].extent()
# Create a polyline feature
feature = QgsFeature()
feature.setGeometry(QgsGeometry.fromWkt(rect.asWktPolygon()))
feature.setAttributes([1])  # Set attribute values (optional)

# Add the feature to the layer
provider.addFeature(feature)

# Commit changes to the polyline layer
polyline_layer.commitChanges()

# Add the polyline layer to the pro
project = QgsProject.instance()
project.addMapLayer(polyline_layer)