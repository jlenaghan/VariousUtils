import sys

lines1 = [ line for line in open(sys.argv[1],'r')]
lines2 = [ line for line in open(sys.argv[2],'r')]

for i in range(0,len(lines1)):
	fields1 = lines1[i].strip().split('|')
	wkt = lines2[i].strip()
	print fields1[0]+'|geofence|'+wkt+'|unknown'