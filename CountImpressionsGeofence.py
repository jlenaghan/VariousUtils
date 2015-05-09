import sys 
import os
import pprint
import io
import gzip
import re
import usng

start_date = 20120725
end_date = 20120824

sfo_lat = 37.6180555556
sfo_lng = -122.3786111111

dirs = []
dirs.append('/data/twc/csv/daily/2012/07')
dirs.append('/data/twc/csv/daily/2012/08')

impression_count = 0

for dir in dirs:
	listing = os.listdir(dir)
	for filename in listing:
		toks = filename.split('.')
		filename_date = toks[0].replace('-','')
		if int(filename_date) < int(start_date) or int(filename_date) > int(end_date):
			continue
		print('Processing ' + filename + '\n')
		r = io.BufferedReader( gzip.GzipFile( dir+'/'+filename, 'r' ) )
		for line in r:
			line = line.decode('utf-8')
			line = line.strip()
			fields = line.split(',')
			tile_id = fields[0]
			if not re.search(r'^10S EG', tile_id):
				continue
			lng, lat = usng.USNGtoLL(tile_id)
			dist = usng.latlon_dist(lat, lng, sfo_lat, sfo_lng)
			if dist < 3200.0:
				impression_count += 1
		r.close()
		print('Impressions =  '+ str(impression_count) + '\n')

print('Total impressions = ' + int(impression_count));
		