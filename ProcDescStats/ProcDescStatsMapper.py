#!/usr/bin/python
import sys
import re

reDate = re.compile('^DATE')
reHod = re.compile('^HOD')

for line in sys.stdin:
    line = line.strip()
    try:
        key, value = line.split(None,1)
        matchObj = re.match(r'^[0-9]', key)
        if matchObj:
            tile_id, dev_id, count = value.split(',')
            dev_id = ''.join(dev_id.split())
            print '%s\t%s' % (tile_id + ',' + dev_id, count)
            print '%s\t%s' % (tile_id, count)
            print '%s\t%s' % (dev_id, count)
        else:
            print '%s\t%s' % (key, value)
    except:
        continue
