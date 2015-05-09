import sys
import datetime
import pprint

clicks_by_hour = {}
imps_by_hour = {}

for line in sys.stdin:
        fields = line.strip().split(',')
        dt = fields[4]
        imps = fields[6]
        clicks = fields[9]
        if dt == '' or imps == '' or clicks == '':
                continue
        dt = datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S')
        day = dt.day
        hour = dt.hour
        clicks_by_hour.setdefault(day,{}).setdefault(hour,0)
        clicks_by_hour[day][hour] += int(clicks)
        imps_by_hour.setdefault(day,{}).setdefault(hour,0)
        imps_by_hour[day][hour] += int(imps)

for day in imps_by_hour:
        for hour in imps_by_hour[day]:
                imps = imps_by_hour[day][hour]
                clicks = clicks_by_hour[day][hour]
                ctr = float(clicks)/float(imps)
                print day, hour, imps, clicks, ctr