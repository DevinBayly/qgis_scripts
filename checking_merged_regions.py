from pathlib import Path
l = iface.activeLayer()
regions=[]
for f in l.getFeatures():
    res = Path(f"merging_workflow/{f['region']}_merged.tif")
    exists = res.exists()
    if exists:
        size = res.stat().st_size
    if not exists or size == 0:
        print(f["region"],"not found")
        regions.append(f["region"])
        
print(regions)