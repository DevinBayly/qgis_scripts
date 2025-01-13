# this script will take a selection of photo points and kick off the odm job for italic
from pathlib import Path
import subprocess as sp
photos = iface.activeLayer()
name = "jeff_spring_recap_1"
out =Path(f"./region_labeled_image_cluster_groups/{name}/images")
out.mkdir(exist_ok=True,parents=True)

for f in photos.getSelectedFeatures():
    # get the photo name rom the f
    fpath = Path(f["photo"])
    sympath = Path(f"{out}/{fpath.name}")
    if not sympath.is_symlink():
        sympath.symlink_to(fpath.absolute())
    
# kick off running job 
proc = sp.run(f'''ssh wentletrap "
    . /usr/local/bin/slurm-selector.sh elgato
    cd /xdisk/bryancarter/baylyd/hpc_batch_processing
    sbatch -A cdh -o slurm_{name}_%A.out -p standard -t 4:00:00 -n 12 -N 1 coordinator.sh {name}
    "
''',stdout  = sp.PIPE,stderr = sp.PIPE,shell=True)

print(proc.stdout.decode())
print(proc.stderr.decode())
