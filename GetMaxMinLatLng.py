import sys 
import io
import gzip

infilename = sys.argv[1]
tag = sys.argv[2]

min_lat, min_lng =  1000.0,  1000.0
max_lat, max_lng = -1000.0, -1000.0

count = 0
r = io.BufferedReader( gzip.GzipFile( infilename, 'r' ) )
for line in r:
    _dev_id, tile_id, server_ts, client_ts, type, acc, filler, geom, alt = line.strip().split(',')
    count += 1
    if count > 10000000: break
    geom = geom.replace("POINT(","")
    geom = geom.replace(")","")
    slng, slat = geom.split()
    lng, lat = float(slng), float(slat)
    if lng < min_lng: min_lng = lng
    if lat < min_lat: min_lat = lat
    if lng > max_lng: max_lng = lng
    if lat > max_lat: max_lat = lat
r.close()

print(tag+'|'+str(min_lng)+'|'+str(max_lng)+'|'+str(min_lat)+'|'+str(max_lat))

