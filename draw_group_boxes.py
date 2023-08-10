import json
def make_box(coords,layer,pr,fldr):
    

    # Define the four coordinates of the polygon
    coordinates = coords

    # Create the polygon geometry
    polygon = QgsGeometry.fromPolygonXY([[QgsPointXY(*coord) for coord in coordinates]])

    # Create a new feature and assign the geometry
    feature = QgsFeature()
    feature.setGeometry(polygon)
    feature.setAttributes([fldr])

    # Add the feature to the layer
    pr.addFeatures([feature])

    # Update extent of the layer
    layer.updateExtents()
    props = layer.renderer().symbol().symbolLayers()[0].properties()
    props["style"] ="no"
    props["outline_color"] = props["color"]
    layer.renderer().setSymbol(QgsFillSymbol.createSimple(props))
    # Add the layer to the map
    QgsProject.instance().addMapLayer(layer)
    
# Create a new memory layer for the polygon
layer = QgsVectorLayer('Polygon?crs=EPSG:4326', 'polygon', 'memory')
pr = layer.dataProvider()    
pr.addAttributes([QgsField("Folder",QVariant.String)])
layer.updateFields()
groups = json.loads(open("split_groups_missing.json").read())    
#groups = grps
lim = 5000
for key in groups:
    data = groups[key]
    s=data["bbox_start"]
    e = data["bbox_end"]
    #print(data)
    if len(data["images"]) >0:
        box = [(s[1],s[0]),(s[1],e[0]),(e[1],e[0]),(e[1],s[0])]
        #print(box)
        make_box(box,layer,pr,key)
        lim -=1
        if lim <0:
            break
    