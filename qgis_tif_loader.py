from pathlib import Path

tifs = sorted(Path("/xdisk/bryancarter/baylyd/tmp_group_split").glob("*/odm_dem/dtm.tif"))
print(tifs)
for tif in tifs:
    iface.addRasterLayer(str(tif), f"{tif.parent.parent.stem}")
print("done")