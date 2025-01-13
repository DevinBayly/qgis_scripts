# this script will take a selection of photo points and kick off the odm job for italic
from pathlib import Path
import subprocess as sp
photos = iface.activeLayer()
name = photos.name()
# check that the images path exists
images_path = Path(f"region_labeled_image_cluster_groups/{name}/images")
if images_path.exists() and len(list(images_path.iterdir())) >0:
    # kick off running job 
    proc = sp.run(f'''ssh wentletrap "
        . /usr/local/bin/slurm-selector.sh elgato
        cd /xdisk/bryancarter/baylyd/hpc_batch_processing
        sbatch -A cdh -J {name}_coordinator -o slurm_{name}_%A.out -p standard -t 12:00:00 -n 12 -N 1 coordinator.sh {name}
        "
    ''',stdout  = sp.PIPE,stderr = sp.PIPE,shell=True)

    print(proc.stdout.decode())
    print(proc.stderr.decode())
else:
    print("no images in ",name)
