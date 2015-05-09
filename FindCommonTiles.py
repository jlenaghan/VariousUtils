import gzip
import io

def get_count(filename):
    total = 0
    fn = None
    if filename.endswith('.gz'):
        g = gzip.GzipFile(filename,'r')
        fn = io.BufferedReader(g)
    else:
        fn = open(filename,'r')
    for line in fn:
        key, count = line.strip().split()
        total += float(count)
    fn.close()
    if filename.endswith('.gz'):
        g.close()
    return total

def get_counts(filename):
    counts = {}
    fn = None
    if filename.endswith('.gz'):
        g = gzip.GzipFile(filename,'r')
        fn = io.BufferedReader(g)
    else:
        fn = open(filename,'r')
    for line in fn:
        key, count = line.strip().split()
        counts[key] = count
    fn.close()
    if filename.endswith('.gz'):
        g.close()
    return counts

def gen_perc_file(total,filename):
    outfilename = filename.replace('bad_tiles.csv','perc_bad_tiles.csv')
    fn = open(filename,'r')
    ofn = open(outfilename,'w')
    for line in fn:
        key, count = line.strip().split()
        perc = float(count) / total
        ofn.write(key+'\t'+str(perc)+'\n')
    fn.close()
    ofn.close()
    
mojiva_total_file = '/Users/jlenaghan/tmp/TileRollups/mojiva/mojiva_tile.csv.gz'
twc_total_file = '/Users/jlenaghan/tmp/TileRollups/twc/twc_tiles.csv.gz'
xtify_total_file = '/Users/jlenaghan/tmp/TileRollups/xtify/xtify_tiles.csv.gz'

mojiva_file = '/Users/jlenaghan/tmp/TileRollups/mojiva/mojiva_bad_tiles.csv'
twc_file = '/Users/jlenaghan/tmp/TileRollups/twc/twc_bad_tiles.csv'
xtify_file = '/Users/jlenaghan/tmp/TileRollups/xtify/xtify_bad_tiles.csv'

mojiva = get_counts(mojiva_file)
twc = get_counts(twc_file)
xtify = get_counts(xtify_file)

mojiva_total = get_count(mojiva_total_file)
twc_total = get_count(twc_total_file)
xtify_total = get_count(xtify_total_file)

gen_perc_file(mojiva_total, mojiva_file)
gen_perc_file(twc_total, twc_file)
gen_perc_file(xtify_total, xtify_file)


print('twc,mojiva')
for twc_key, twc_value in twc.iteritems():
    if twc_key in mojiva:
        print(twc_key,twc_value,mojiva[twc_key])
        
print('mojiva,xtify')
for mojiva_key, mojiva_value in mojiva.iteritems():
    if mojiva_key in xtify:
        print(mojiva_key,mojiva_value,xtify[mojiva_key])
        
print('xtify,twc')
for xtify_key, xtify_value in xtify.iteritems():
    if xtify_key in twc:
        print(xtify_key,xtify_value,twc[xtify_key])        
        



