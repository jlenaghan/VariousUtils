import json
import sys

tps = range(7,33)

infilename = sys.argv[1]
f_in = open(infilename,'r')
for line in f_in:
	json_data = json.loads(line.strip())
	polyid = json_data['poly_uid']
	tiles = json_data['tiles']
	name = None
	if polyid == 'grove:1':
		name = 'GROVE_GEOFENCE'
	else:
		name = 'CENTURY_GEOFENCE'
	for tile in tiles:
		tile_id, perc = tile
		for tp in tps:
			print tile_id + '\t' + str(tp)+',"'+name+'","'+name+'","'+name+'",10.0'
