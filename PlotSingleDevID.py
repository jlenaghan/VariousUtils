import simplekml, os, sys, re, pprint, gzip, io

# Given device id, read dwells file to extract dwells
# Read trace data, get traces

default_colors = ['ffee82ee','ff82004b','ffff0000','ffffff00','ff008000',
                  'ff32cd9a','ff00ffff','ff00a5ff','ff0045ff','ff0000ff']
icon_url = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png' 
venue_url = 'http://maps.google.com/mapfiles/kml/shapes/ranger_station.png'

infilename = sys.argv[1]
outfilename = sys.argv[2]
#infilename = '/Users/jlenaghan/tmp/back_prop/'+campaign+'.csv'
#outfilename = '/Users/jlenaghan/tmp/back_prop/'+campaign+'.kml'
kml_file = simplekml.Kml()

count = 0
prev_dev = 'prev_dev'
infile = open(infilename,'r')
for row in infile:
    dev_id, tile_id, sts, cts, dev, bl1, bl2, geom, bl3 = row.strip().split(',')
    if prev_dev != dev_id: count += 1
    prev_dev = dev_id
    geom = geom.replace("POINT(","")
    geom = geom.replace(")","")
    lng, lat = geom.split()
    pnt = kml_file.newpoint(coords=[(float(lng),float(lat))])
    pnt.iconstyle.color = default_colors[count%10]
    pnt.iconstyle.scale = 1
    pnt.iconstyle.icon.href = icon_url
kml_file.save(outfilename)
