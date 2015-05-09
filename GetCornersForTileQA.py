import sys
sys.path.append('/Users/jlenaghan/git/analysis/lib')
import usng 

side_length = 100.0*1000.0

bases = []
bases.append([29.36302703778376, -95.82275390625])
# bases.append([41.049291503191824, -73.55844497680664])
# bases.append([42.35042512243457, -71.06918334960938])
# bases.append([33.750998548784956, -84.39783096313477])
# bases.append([25.41403190206025, -80.51287651062012])
# bases.append([33.82165621547623, -117.9177188873291])
# bases.append([44.329220627804176, -120.85527420043945])
# bases.append([36.02244668175846, -79.01461601257324])
# bases.append([37.769018558337955, -122.42769241333008])

for base in bases:
	base_lat, base_lng = base
	next_lat, next_lng = usng.lat_lon_plus_dist_dir( base_lat, base_lng, side_length, 'E' ) 
	final_lat, final_lng = usng.lat_lon_plus_dist_dir( next_lat, next_lng, side_length, 'N' ) 
	print(base_lat, base_lng)
	print(final_lat, final_lng)
	print('---------------------')