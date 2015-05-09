import sys
import pprint
sys.path.append('/Users/jlenaghan/git/Python/lib/')
import usng

max_acc = 500
min_acc = 0.0 

# get list of mobile ip addresses
mobile_ips = [ line.strip() for line in open('/Users/jlenaghan/DataScratch/SkyhookIP/tt','r') ]

# get dict of ip address to network name
ips_to_network = {}
for line in open('/Users/jlenaghan/DataScratch/SkyhookIP/IPToRange.psv','r'):
    ip, network, beg, end = line.strip().split('|')
    ips_to_network[ip] = network

# get Skyhook geocoded data
ips = {}
for line in open('/Users/jlenaghan/DataScratch/SkyhookIP/ips_network.csv','r'):
    ip, lat, lng, accuracy = line.strip().split()
    if ip in ips_to_network:
        if ips_to_network[ip] not in mobile_ips:
            if float(accuracy) > min_acc and float(accuracy)  < max_acc:
                ips.setdefault(ip,{})
                ips[ip]['lat'] = float(lat)
                ips[ip]['lng'] = float(lng)
                ips[ip]['acc'] = float(accuracy)

# loop over all humand demand data, compute dist bn skyhook geocode and human demand lat lng
hd_geocodes = {}
for line in sys.stdin:
    ip, lat, lng = line.strip().split(',')
    hd_geocodes.setdefault(ip,{})
    hd_geocodes[ip]['lat'] = float(lat)
    hd_geocodes[ip]['lng'] = float(lng)
    if ip in ips:
        dist = usng.latlon_dist(ips[ip]['lat'],ips[ip]['lng'],hd_geocodes[ip]['lat'],hd_geocodes[ip]['lng'])
        print str(dist)

