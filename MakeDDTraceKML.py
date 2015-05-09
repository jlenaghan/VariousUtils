import simplekml, os, sys, re, pprint, gzip, io

# Given device id, read dwells file to extract dwells
# Read trace data, get traces

default_colors = ['ffee82ee','ff82004b','ffff0000','ffffff00','ff008000',
                  'ff32cd9a','ff00ffff','ff00a5ff','ff0045ff','ff0000ff']
icon_url = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png' 

dev_id = sys.argv[1]
outfile = '/Users/jlenaghan/tmp/dwell_test/'+dev_id+'.kml'
kml_file = simplekml.Kml()

# get dwells 
dwells = []
dwell_file = open('/Users/jlenaghan/tmp/InferedDwells/part-r-00000','r')
for line in dwell_file:
    if re.match(dev_id,line):
        fields = line.strip().split('[[')
        ds, ts = fields[1].split('|')
        latlngs = ds.split('],')
        for latlng in latlngs:
            lng, lat = latlng.split(',')
            lng = lng.replace('[','')
            lng = lng.replace(']','')
            lat = lat.replace('[','')
            lat = lat.replace(']','')
            pnt = kml_file.newpoint(coords=[(float(lng),float(lat))])
            pnt.iconstyle.color = default_colors[9]
            pnt.iconstyle.scale = 1
            pnt.iconstyle.icon.href = icon_url

#path = '/Users/jlenaghan/tmp/DDTraces'
trace_path = '/data/traces/production/'
listing = os.listdir(trace_path)
count = 0
for infile in listing:
    if not re.match('part',infile): continue
    g = gzip.GzipFile(trace_path+infile,'r')
    r = io.BufferedReader(g)
    for line in r:
        if not re.match(dev_id,line): continue
        fields = line.strip().split(',')
        gis_object = fields[7]
        gis_object = gis_object.replace('POINT(','')
        gis_object = gis_object.replace(')','')
        lng, lat = gis_object.split()
        pnt = kml_file.newpoint(coords=[(float(lng),float(lat))])
        pnt.iconstyle.color = default_colors[0]
        pnt.iconstyle.scale = 1
        pnt.iconstyle.icon.href = icon_url
    count += 1
kml_file.save(outfile)
