#t = datetime.strptime('Jul 9, 2009 @ 20:02:58 UTC',"%b %d, %Y @ %H:%M:%S %Z")
#Timestamp (EST),Hash,Device ID,Campaign id,Campaign,Carrier,IP,Device Brand,Device Model,Country Code,App Name,Site Name,Audience,Latitude,Longitude
#00170004536990,16TDN264701,1301071832000,1301071832000,wifi,55.0,,POINT(-87.90374115 43.0805114),

import datetime
import sys
sys.path.append('/home/jlenaghan/git/Python/lib/')
import usng
import time

for line in sys.stdin:
	try:
		fields = line.strip().split(',')
	 	dt = fields[0]
		t = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
		epoch = int(t.strftime('%s')) * 1000
		udid = fields[2]
		lat, lng = fields[-2], fields[-1]
		tile_id = usng.usng_from_x_y(float(lng), float(lat)).replace(' ','')
		print udid+','+tile_id+','+str(epoch)+','+str(epoch)+',gps,14.0,,POINT('+lng +' ' + lat+'),'
	except:
		continue