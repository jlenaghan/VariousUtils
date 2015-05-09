import sys
sys.path.append('/Users/jlenaghan/git/analysis/lib/')
import usng
import os
import json
import pprint
import re
base_dir = '/Users/jlenaghan/Data/InferredDwells/'

f_out = open('/Users/jlenaghan/tmp/UDIDPDwells.psv','w')

listing = os.listdir(base_dir)
for d in listing:
    filename = base_dir + d + '/dwells_'+d+'.json'
    f = open(filename, 'r')
    for line in f:
        json_data = json.loads(line)
        dev_id = json_data[0]['dev_id']
        dwells = json_data[1]['dwells']
        for dwell in dwells:
            lat_lng = dwells[dwell]['latlng']
            lat, lng = float(lat_lng[0]), float(lat_lng[1])
            tile_id = usng.usng_from_x_y(lng,lat)
            tile_id = tile_id.replace(' ','')
            
            tiles = dwells[dwell]['tiles']
            num_points = 0
            for tile_id in tiles:
                num_points += tiles[tile_id]

            f_out.write(dev_id+'|'+tile_id+'|'+str(num_points)+'\n')
    f.close()
    
f_out.close()