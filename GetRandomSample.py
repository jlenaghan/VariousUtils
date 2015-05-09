import sys
import io
import gzip

in_filename = sys.argv[1]
count = 0

r = io.BufferedReader( gzip.GzipFile( in_filename, 'r') )
for line in r:
    count += 1
    if count % 1000 == 0:
        _dev_id, tile_id, server_ts, client_ts, type, acc, filler, geom, alt = line.strip().split(',')
        geom = geom.replace("POINT(","")
        geom = geom.replace(")","")
        lng, lat = geom.split()
        print lng+','+lat