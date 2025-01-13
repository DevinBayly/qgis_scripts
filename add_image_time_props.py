import datetime
images = iface.activeLayer()

# add in a few attributes
if images.fields().indexOf("combined") == -1:
    images.dataProvider().addAttributes([
        QgsField("month",QVariant.Int),
        QgsField("hour",QVariant.Int),
        QgsField("combined",QVariant.String)
        ])
images.updateFields()
images.startEditing()
for f in images.getFeatures():
    month =f["timestamp"].date().month()
    
    hour =f["timestamp"].time().hour()
    combined = f"{hour} {month}"
    f.setAttribute("month",month)
    f.setAttribute("hour",hour)
    f.setAttribute("combined",combined)
    images.updateFeature(f)
    
images.commitChanges()