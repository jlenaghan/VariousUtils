import sys
import io
import gzip
import re

infilename = sys.argv[1]

num_p_dwells = {}
num_demos = {}

agged_udids = {}
agged_counts = {}

total_num_udids = 0
total_air_counts = 0
total_imps = 349337015

r = io.BufferedReader( gzip.GzipFile(infilename,'r') )
for line in r:
    line = line.strip()
    if re.search(r'NUM_UDIDS',line):
        slug, counts = line.split(',')
        total_num_udids += int(counts)
    elif re.search(r'_p_dwells',line):
        slug, counts = line.split(',')
        num_p_dwells.setdefault(slug,0)
        num_p_dwells[slug] += int(counts)
    elif re.search(r'airport_cnt',line):
        udid, slug, counts = line.split(',')
        total_air_counts += int(counts)
        fat = 'airport'
        agged_udids.setdefault(fat,{}).setdefault(udid,0)
        agged_udids[fat][udid] += 1
    elif re.search(r'inhomedemographics',line):
        udid, fat, counts = line.split(',')
        num_demos.setdefault(fat,0)
        num_demos[fat] += 1
        agged_udids.setdefault(fat,{}).setdefault(udid,0)
        agged_udids[fat][udid] += 1
    #elif re.search(r'event_cnts',line):
    #    x = 1
    #else:
    #    print('Bad record -> ' + line)
r.close()

r = io.BufferedReader( gzip.GzipFile(infilename,'r') )
for line in r:
    line = line.strip()
    if re.search(r'event_cnts',line):
        udid, slug, cnt = line.split(',')
        for fat in agged_udids:
            if udid in agged_udids[fat]:
                agged_counts.setdefault(fat,0)
                agged_counts[fat] += int(cnt) 
r.close()

print('TOTAL NUM UDIDS = ' + str(total_num_udids))

for fat in agged_counts:
    print('TOTAL IMPS FROM DEMO ' + fat + ' = ' + str(agged_counts[fat]))
print('TOTAL IMPS AIRPORTS = ' + str(total_air_counts))

airport_inc = 100 * float(total_air_counts) / float(agged_counts['airport'])
print('PERC SERVED IN AIRPORTS = ' + str(airport_inc) ) 

for demo in num_demos:
    count = num_demos[demo]
    events_count = agged_counts[demo]
    perc = 100 * float(count) / float(events_count)
    print('TOTAL ' + demo + ' = ' + str(count) + ' ' + str(perc))

for p_dwell in num_p_dwells:
    tag = p_dwell
    count = num_p_dwells[p_dwell]
    print('TOTAL ' + tag + ' = ' + str(count))
