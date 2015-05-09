import sys

polys = {}
tiles = {}
for line in open('Stores.csv','r'):
    poly_uid, tile_id = line.strip().split(',')
    polys[poly_uid] = tile_id
    tiles[tile_id] = 1

msas = {}
for line in sys.stdin:
    msa, tile_id = line.strip().split(',')
    if tile_id in tiles:
        msas[tile_id] = msa

for poly_id in polys:
    tile_id = polys[poly_id]
    if tile_id in msas:
        print poly_id+','+msas[tile_id]
    else:
        print poly_id+',rusa'
