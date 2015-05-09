#!/usr/bin/python
import sys

def comparator(x,y):
    x_values = x.split(',')
    y_values = y.split(',')
    if x_values[0] > y_values[0]:
        return 1
    elif x_values[0] < y_values[0]:
        return -1
    else:
        if x_values[3] > y_values[3]:
            return 1
        else:
            return -1

lines_by_key = {}
for line in sys.stdin:
    line = line.strip()
    key, values = line.split('\t')
    lines_by_key.setdefault(key,[])
    lines_by_key[key].append(values)

for key in lines_by_key:
    lines_by_tile = lines_by_key[key]
    lines_by_tile.sort(comparator)
    
for key in sorted(lines_by_key):
    for line in lines_by_key[key]:
        fields = line.split(',')
        print '%s\t%s'% (key, line )