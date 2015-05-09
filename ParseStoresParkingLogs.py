import sys

store_wkts = {}
parking_lots_wkts = {}

def print_hash(hm):
	for sid in hm:
		store_name, junk = sid.split(':')
		print sid+'|'+store_name+'|'+hm[sid]+'|unknown'

for line in sys.stdin:
	line = line.strip()
	fields = line.split('|')
	if len(fields) < 2 or len(fields) > 3:
		sys.stderr.write('Wrong num fields -> ' + line)
		exit()
	polygon_id = fields[0]
	name, ssid = fields[0].split(':')
	store_wkt = fields[1]
	store_wkts[polygon_id] = store_wkt
	if len(fields) == 3:
		key = name+'_parkinglot:'+ssid
		parking_lots_wkt = fields[2]
		parking_lots_wkts[key] = parking_lots_wkt

print_hash(store_wkts)
print_hash(parking_lots_wkts)