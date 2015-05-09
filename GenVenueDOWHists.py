import sys
import os
import re
from datetime import datetime

filename = sys.argv[1]
dow_hits = {}

f = open(filename,'r')
for line in f:
    try:
        fields = line.strip().split(',')
        timestamp = int(fields[3])
        d = datetime.fromtimestamp(timestamp)
        day_of_week = d.weekday() # Monday is zero
        strDay = d.strftime("%a")
        dow_hits.setdefault(strDay,0)
        dow_hits[strDay] += 1
    except:
        print("BAD LINE -> " + line)
f.close()

for day in dow_hits:
    print(str(day)+","+str(dow_hits[day]))


        
