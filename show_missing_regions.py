import datetime 
from pathlib import Path
regions = iface.activeLayer()
regions.updateFields()
for i in range(5):
    pass
    #regions.dataProvider().deleteAttributes([regions.fields().indexOf(f"ortho-time-{i}")])
    #regions.dataProvider().addAttributes([QgsField(f"merged-time-{i}",QVariant.Double)])

regions.startEditing()
for f in regions.getFeatures():
  # it would be nice to add information to the layer such as
  # ortho exists, merged image exists, that sort of thing
  name = f["region"]
  missing = False
  for i in range(5):
    ortho = Path(f"/xdisk/bryancarter/baylyd/region_labeled_image_cluster_groups/{name}_{i}/odm_orthophoto/odm_orthophoto.tif")
    if not ortho.exists():
      missing = True
      break
    f.setAttribute(f"ortho-time-{i}",(datetime.datetime.now().timestamp() - ortho.stat().st_mtime)/(60*60*24))
    
    print(f[f"ortho-time-{i}"],name)
  merged = Path(f"/xdisk/bryancarter/baylyd/merging_workflow/{name}_merged.tif")
  if not merged.exists():
      print("missing merged",name)
      continue
  f.setAttribute(f"merged-time-{i}",(datetime.datetime.now().timestamp() - merged.stat().st_mtime)/(60*60*24))

  #f.setAttribute("ortho",f"{missing}")
  
  regions.updateFeature(f)
  print(f["ortho"],"is the new attribute")

regions.updateFields()

regions.commitChanges()
  
