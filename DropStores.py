import sys
sys.path.append('/Users/jlenaghan/git/Python/lib/')
import usng

walmarts = {}
for line in open('Walmarts.csv','r'):
    if 'park' in line: continue
    uid, tile_id = line.strip().split(',')
    walmarts[uid] = tile_id

comps = {}
MIN_DIST = 5000.0
for line in open('CompStores.csv','r'):
    uid, tile_id = line.strip().split(',')
    good_to_keep = False
    min_dist = 100000000000.0
    for walmart_id in walmarts:
        dist = usng.tile_distance(tile_id,walmarts[walmart_id])
        if min_dist > dist: min_dist = dist
        if dist < MIN_DIST:
            good_to_keep = True
            continue
    if not good_to_keep:
        print uid+','+str(min_dist)
