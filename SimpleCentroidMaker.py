import sys
import json
import pprint
import urllib2
# input: poly_id|name|wkt polygon|msa
# output: PIQ polygon json doc

def get_centroid(wkt):
	coords = wkt.replace('MULTI','').replace('POLYGON','').replace(')','').replace('(','').split(',')
	centroid_lng, centroid_lat = 0.0, 0.0
	for pair in coords:
		slng,slat = pair.split()
		centroid_lat += float(slat)
		centroid_lng += float(slng)
	centroid_lat /= float(len(coords))
	centroid_lng /= float(len(coords))
	return centroid_lng, centroid_lat

for line in sys.stdin:
	try:
		uid, name, wkt, msa = line.strip().split('|')
		wkt = wkt.replace('"','')
		centroid_lng, centroid_lat = get_centroid(wkt)
		print uid+'|'+'POINT('+str(centroid_lng) +' '+str(centroid_lat)+')'
	except:
		print 'Bad record = ' + line
		exit()