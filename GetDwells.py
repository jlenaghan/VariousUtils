import simplekml
kml_file = simplekml.Kml()

filename = '/Users/jlenaghan/tmp/clust_dwells.txt'
file = open(filename,'r')
icon_url = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png' 

for line in file:
    line = line.replace("[","")
    line = line.replace("]","")
    line = line.replace(",","")
    fields = line.strip().split()
    for i in range(1,len(fields),2):
        pnt = kml_file.newpoint(coords=[(float(fields[i]),float(fields[i+1]))])
        pnt.iconstyle.color = 'ffee82ee'
        pnt.iconstyle.scale = 1
        pnt.iconstyle.icon.href = icon_url
kml_file.save('/Users/jlenaghan/tmp/some_dwells.kml')

    
    