import uuid
from pathlib import Path
import json
import subprocess as sp
layer = iface.activeLayer()
print(layer)
#todo consider doing this outside qgis because we can probably do it in parallel quite fast
def split_images(start_corner,end_corner,chunks,overlap_factor,groups):
    # notice from the start to the end we go down in the first and down in the second, this is a downward diagonal on th emap from right top to bottom left
    total_deltas = [end_corner[i] - start_corner[i] for i in range(2)]
    print(total_deltas)
    # test getting a certain chunk
    chunk_deltas = [e/chunks for e in total_deltas]
    for lat in range(chunks):
        for lng in range(chunks):
            if Path("stop").exists():
                return
            chunk_num =[lat,lng]
            print(chunk_num)
            start_chunk_coords = [coord + chunk_num[i]*chunk_deltas[i] - overlap_factor*chunk_deltas[i] for i,coord in enumerate(start_corner)]
            end_chunk_coords =  [coord + (chunk_num[i]+1)*chunk_deltas[i] + overlap_factor*chunk_deltas[i] for i,coord in enumerate(start_corner)]
            ## and then if we want overlap we need to move in fractions of the chunk delta like .75 for a .25 percent overlap and such
            ## then we do nesting for loops to work out the amount we have moved in each
            # print("original starting coords are", start_corner)
            # print(start_chunk_coords)
            # print(end_chunk_coords)
            expr = f"""
            latitude<{start_chunk_coords[0]}
            and
            latitude>{end_chunk_coords[0]}
            and
            longitude>{start_chunk_coords[1]}
            and
            longitude<{end_chunk_coords[1]}
            """
            layer.selectByExpression(expr)
            features = layer.selectedFeatures()
            num_features = len(features)
            print(num_features)
            if num_features >0:
                groups[str(uuid.uuid4())] = {
                    "bbox_start":start_chunk_coords,
                    "bbox_end":end_chunk_coords,
                    "images":[f.attributes()[1:4] for f in features]
                }
        
grps = {}
start_corner =[31.69149,-110.18761]
end_corner = [31.58197,-110.32794]
chunks = 20
overlap_factor =.1
split_images(start_corner,end_corner,chunks,overlap_factor,grps)
if Path("stop").exists():
    sp.run("rm stop",shell=True)
else:
    Path("split_groups_missing.json").write_text(json.dumps(grps))