
# Iterate over the layers
for layer in layers:
    # Check if the layer is a vector layer
    if layer.type() == QgsMapLayerType.VectorLayer:
        # Check if the layer has polygon geometry
        if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            # Get the layer's style
            layer_style = layer.renderer().symbol().symbolLayer(0)

            # Check if the layer has a fill symbol
            if isinstance(layer_style, QgsFillSymbol):
                # Remove the fill color
                layer_style.setColor(QColor(Qt.transparent))

                # Update the layer's style
                renderer = QgsSingleSymbolRenderer(layer_style)
                layer.setRenderer(renderer)

                # Refresh the layer
                layer.triggerRepaint()

# Refresh the map canvas
iface.mapCanvas().refreshAllLayers()