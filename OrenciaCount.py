import sys
import gzip
import io

tiles = {}

fn = open(sys.argv[1],'r')
for tile_id in fn:
	tile_id = tile_id.strip()
	tiles[tile_id] = 1

counts = 0

imp_file = '/Users/jlenaghan/Data/thresholding/ImpressionEstimates/twchl.csv.gz'
r = io.BufferedReader( gzip.GzipFile(imp_file,'r') )
for line in r:
	tile_id, tp, imps, clicks = line.strip().split(',')
	if tile_id in tiles:
		counts += int(imps)
r.close()
print(counts)
