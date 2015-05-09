import sys
import datetime
import pprint

clicks_by_hour = {}
imps_by_hour = {}

for line in sys.stdin:
dd, imps, clicks = line.strip().split(',')
        if dd == '' or imps == '' or clicks == '':
                continue
        dt = datetime.datetime.strptime(dd,'%Y-%m-%d %H:%M:%S')

        day = dt.day
        hour = dt.hour
        clicks_by_hour.setdefault(day,{}).setdefault(hour,0)
        clicks_by_hour[day][hour] += int(clicks)
        imps_by_hour.setdefault(day,{}).setdefault(hour,0)
        imps_by_hour[day][hour] += int(imps)

pprint.pprint(imps_by_hour)