from pathlib import Path
l = iface.activeLayer()
regions=[]
for f in l.getFeatures():
    clusters = sorted(Path(f"region_labeled_image_cluster_groups/").glob(f"{f['region']}_*/odm_orthophoto/odm_orthophoto.tif"))
    
    for res in cluster:
        exists = res.exists()
        if exists:
            size = res.stat().st_size
        if not exists or size == 0:
            print(f["region"],"not found")
            regions.append(f["region"])
        
print(regions)