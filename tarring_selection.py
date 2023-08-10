#tar'ing selected
import tarfile
import uuid
from pathlib import Path 
layer = iface.activeLayer()
features = layer.selectedFeatures()
print(features)
print(features[0].attributes())
# make a tar model and pointcloud folder
output = Path("./model_prototyping")
output.mkdir(parents=True,exist_ok=True)

file_pth = Path(f"{output}/selection_download_{uuid.uuid4()}.tar")

with tarfile.TarFile(str(file_pth),mode="w") as tar:
    for f in features:
        fldr = f.attributes()[1]
        # get everything from the model folder and the gps folder 
        tar.add(f"tmp_group_split/{fldr}/odm_texturing")
        tar.add(f"tmp_group_split/{fldr}/odm_georeferencing")
        
        