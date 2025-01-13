layer = iface.activeLayer()
print(layer)
start_corner =[31.69380,-110.18412]
end_corner = [31.58302,-110.32952]
chunks = 2
overlap_factor =.1

# notice from the start to the end we go down in the first and down in the second, this is a downward diagonal on th emap from right top to bottom left
total_deltas = [end_corner[i] - start_corner[i] for i in range(2)]
print(total_deltas)
# test getting a certain chunk
chunk_deltas = [e/chunks for e in total_deltas]
lat = 1
lng = 1
chunk_num =[lat,lng]
start_chunk_coords = [coord + chunk_num[i]*chunk_deltas[i]*(1-overlap_factor) for i,coord in enumerate(start_corner)]
end_chunk_coords =  [coord + (chunk_num[i]+1)*chunk_deltas[i]*(1+overlap_factor) for i,coord in enumerate(start_corner)]
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
print(expr)
layer.selectByExpression(expr)