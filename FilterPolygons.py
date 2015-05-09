import sys
import re
import pprint
script_name, infilename, s_upper_lat, s_upper_lng, s_lower_lat, s_lower_lng = sys.argv

upper_lat = float(s_upper_lat)
upper_lng = float(s_upper_lng)
lower_lat = float(s_lower_lat)
lower_lng = float(s_lower_lng)


f = open(infilename,'r')
for line in f:
	line = line.strip()
	m = re.search(r'POINT\((\S+\s\S+)\)',line)
	slng, slat = m.group(1).split()
	lng, lat = float(slng), float(slat)
	if lng < upper_lng and lat < upper_lat:
		if lng > lower_lng and lat > lower_lat:
			print(line) 
f.close()
