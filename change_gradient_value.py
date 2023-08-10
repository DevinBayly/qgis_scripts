group = QgsProject.instance().layerTreeRoot().findGroup("sub-group1")

children = group.children()
print(children)
 
min=1400
max = 1200

# for c in children:
#     ce = c.layer().renderer().contrastEnhancement()
#     cmin =ce.minimumValue()
#     cmax = ce.maximumValue()
#     if cmin < min  and cmin >0 :
#         min = ce.minimumValue()
#         print("setting min",min)

#     if cmax > max and cmax <2000:
#         max = ce.maximumValue()
#         print("setting max",max)


print(min,max)
for c in children:
    print(c.layer())
    ce = c.layer().renderer().contrastEnhancement()
    ce.setMinimumValue(min)
    ce.setMaximumValue(max)
print(min,max)
