import sys
sys.path.append('/Users/jlenaghan/git/analysis/lib/')
import usng
import json
import pprint

import simplekml

eps = 0.0000000001 

default_colors = ['ffee82ee','ff82004b','ffff0000','ffffff00','ff008000',
                  'ff32cd9a','ff00ffff','ff00a5ff','ff0045ff','ff0000ff']


walmart_filename = '/Users/jlenaghan/tmp/WalmartKPI/atlanta_unique.csv'
uuid_filename = '/Users/jlenaghan/tmp/WalmartKPI/atlantaUDIDs.csv'

wal_f = open(walmart_filename,'r')
uuid_f = open(uuid_filename,'r')

wals = {}
wal_id = 1
for line in wal_f:
    lat,lng = line.strip().split(',')
    wals.setdefault(wal_id,[])
    wals[wal_id].append([lat,lng])
    wal_id += 1
wal_f.close()

uuids = {}
for line in uuid_f:
    _dev_id, tile_id, server_ts, client_ts, type, acc, filler, geom, alt = line.strip().split(',')
    geom = geom.replace("POINT(","")
    geom = geom.replace(")","")
    lng, lat = geom.split()
    for wal_id in wals:
        wal_lat, wal_lng = wals[wal_id][0][0], wals[wal_id][0][1]
        dist = usng.latlon_dist(float(lat),float(lng),float(wal_lat),float(wal_lng))
        if dist < 60.0:
            uuids[_dev_id] = wal_id
uuid_f.close()

tiles = {}
dwells_file = '/Users/jlenaghan/tmp/Dwells/atlanta.dwells.json'
dwells_f = open(dwells_file,'r')
for line in dwells_f:
    obj = json.loads(line)
    dev_id = obj[0]['dev_id']
    if dev_id in uuids:
        tiles.setdefault(uuids[dev_id],[])
        dwell = obj[1]['dwells']
        for dwell_num in dwell:
            if 'DWELL0' in dwell[dwell_num]:
                for tileid in dwell[dwell_num]['DWELL0']:
                    tiles[uuids[dev_id]].append(tileid)
                    break
            else:
                for tileid in dwell[dwell_num]:
                    tiles[uuids[dev_id]].append(tileid)
                    break
dwells_f.close()

kml_file = simplekml.Kml()
icon_url = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png' 

for wal_id in tiles:
    tts = tiles[wal_id]
    wal_lat, wal_lng = wals[wal_id][0][0], wals[wal_id][0][1]
    pnt = kml_file.newpoint(coords=[(wal_lng,wal_lat)])
    pnt.iconstyle.icon.href = icon_url
    pnt.iconstyle.scale = 3
    pnt.iconstyle.color = default_colors[wal_id % 10]
    pnt.iconstyle.icon.href = icon_url
    for tile in tts:
        lng, lat = usng.USNGtoLL(tile)
        pnt1 = kml_file.newpoint(coords=[(lng,lat)])
        pnt1.iconstyle.icon.href = icon_url
        pnt1.iconstyle.color = default_colors[wal_id % 10]
        pnt1.iconstyle.scale = 1
        pnt1.iconstyle.icon.href = icon_url
kml_file.save('/Users/jlenaghan/tmp/ForDrew.png')



