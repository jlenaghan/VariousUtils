import sys
import json

for line in sys.stdin:
    json_data = json.loads(line.strip())
    poly_uid = json_data['poly_uid']
    tile_id = json_data['tiles'][0][0]
    print poly_uid + ',' + tile_id
