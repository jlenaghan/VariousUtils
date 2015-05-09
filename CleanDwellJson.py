import sys
import pprint
import json
import re
sys.path.append('/Users/jlenaghan/git/Python/lib/')
import usng
is_4info = False

for line in sys.stdin:
    line = line.strip()
    try:
        if re.search(r'Processing|Computing|cluster',line):
            continue
        json_data = json.loads(line)
        dev_id_part = json_data[0]
        dwell_part = json_data[1]
        new_json_data = {}
        new_json_data['dev_id'] = dev_id_part['dev_id']
        new_json_data['dwells'] = dwell_part['dwells']
        dev_id = new_json_data['dev_id']
        for did in new_json_data['dwells']:
            dwell = new_json_data['dwells'][did]
            lnglat = dwell['latlng']
            lat, lng = float(lnglat[0]), float(lnglat[1])
            counts = dwell['counts']
            tile_id = usng.usng_from_x_y(lat,lng)
            tile_id = tile_id.replace(' ','')
            print(dev_id+'|'+tile_id+'|'+str(counts))
    except:
        print >> sys.stderr, 'Bad record -> ' + line
