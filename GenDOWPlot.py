import numpy as np
import matplotlib.pyplot as plt
from math import log10
import datetime
import sys

filename = sys.argv[1]
outfilename = sys.argv[2]

hits = {}
f = open(filename,'r')
for line in f:
    day, num = line.strip().split(',')
    hits[day] = int(num)
    
labels, counts = [], []
for day in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
    labels.append(day)
    counts.append(hits[day])
ax = plt.figure().add_subplot(111)
ind = np.arange(len(counts))
width = 0.35
ax.set_title('Day-of-Week Distribution of Walmart TWC Impressions')
ax.set_xticks(ind+width)
ax.set_xticklabels(labels)
#ax.set_ylabel(ylabel)
ax.bar(ind, counts, width, color='r')
plt.savefig(outfilename)


