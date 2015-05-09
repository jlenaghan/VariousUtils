import sys
import os
import re
from datetime import date

data_dir = sys.argv[1]
dow_hits = {}

listing = os.listdir(data_dir)
for fn in listing: 
    if not re.match(r'2012',fn): continue
    print("Processing " + fn)
    f = open(data_dir+'/'+fn,'r')
    for line in f:
        if re.match(r'Date',line): continue
        try:
            fields = line.strip().split(',')
            YYYY, MM, DD = fields[0].split('-')
            d = date(int(YYYY),int(MM),int(DD))
            day_of_week = d.weekday() # Monday is zero 
            dow_hits.setdefault(day_of_week,0)
            num_imps = fields[8]
            dow_hits[day_of_week] += float(num_imps)
        except:
            print("BAD LINE -> " + line)
    f.close()

for day in dow_hits:
    print(str(day)+","+str(dow_hits[day]))


        
