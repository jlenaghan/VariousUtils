import sys
import pprint
import json

json_data = {}
tiles = {}
for line in sys.stdin:
	tile_id, tp, feature, attribute, score = line.strip().split(',')
	tiles[tile_id] = 1
	lowest_level = {'confidence':'5','coverage':'5','attribute':attribute,'score':str(score)}
	json_data.setdefault(tile_id,[])
	json_data[tile_id].append(lowest_level)

for tile_id in sorted(tiles):
	final_json = {'periods':{},'_id':tile_id}
	final_json['periods'].setdefault('6',[])
	entries = []
	for entry in json_data[tile_id]:
		entries.append(entry)
	final_json['periods']['6'].append({'feature':'Verizon','attributes':entries})
	json_doc = '{"periods":'+str(final_json['periods'])+',"_id":"'+str(final_json['_id'])+'"}'

	json_doc.replace("'",'"')
	print tile_id + '\t' + json_doc
#	need to pass thru sed s/\'/\"/g 