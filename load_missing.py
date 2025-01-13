# load the missing images
from pathlib import Path
missing = [f for f in Path("region_labeled_image_cluster_groups").iterdir() if not Path(f"{f}/odm_orthophoto/odm_orthophoto.tif").exists()]
for m in missing:
processing.runAndLoadResults("native:importphotos", {'FOLDER':str(Path(f"{m}/images")),'RECURSIVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})