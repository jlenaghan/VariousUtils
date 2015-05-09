import sys
import os
import subprocess 
import pprint
import whois

f_ip = open('/Users/jlenaghan/DataScratch/SkyhookIP/IPToRange.psv','w')
f_network = open('/Users/jlenaghan/DataScratch/SkyhookIP/Network.psv','w')
networks = {}

for line in sys.stdin:
    ip, lat, lng, accuracy = line.strip().split()
    p = subprocess.check_output(['whois',ip])
    beg, end, name, orgid = 'nl','nl','nl'
    for line in p.split('\n'):
        if 'NetRange' in line:
            tok, beg, delim, end = line.split()
        if 'NetName' in line:
            tok, name = line.split()
        if 'OrgID' in line:
            tok, name = line.split()
    if beg != 'nl' and end != 'nl' and name != 'nl':
        f_ip.write(ip + '|' + name + '|' + beg + '|' + end+'\n')
        networks[name] = beg+'|'+end

for name,range in networks.iteritems():
    f_network.write(name+'|'+range+'\n')

f_ip.close()
f_network.close()
