import sys
sys.path.append('../../git/Python/lib/')
import usng

f_in = open(sys.argv[1],'r')
for line in f_in:
	msa, tile_id = line.strip().split(',')
	lng, lat = usng.USNGtoLL(tile_id)
	print(msa+'|'+tile_id+'|POINT(' + str(lng) + ' ' + str(lat) +')')