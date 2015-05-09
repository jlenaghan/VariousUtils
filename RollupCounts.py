import os
import sys

data_dir = sys.argv[1]
listing = os.listdir(data_dir)
counts = {}

for fn in listing:
    f = open(data_dir+'/'+fn,'r')
    for line in f:
        slug, count = line.strip().split()
        counts.setdefault(slug,0)
        counts[slug] += int(count)
        
for slug in counts:
    print(slug+'\t'+str(counts[slug]))