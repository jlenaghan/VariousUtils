import re, sys

regions = {}
p = re.compile('(^[0-9]+)([A-Z])')

filename = sys.argv[1]
f = open(filename,'r')
for line in f:
    tile_id, count = line.strip().split(',')
#    words = line.strip().split()
    codes = re.split('^([0-9]+)([A-Z])',tile_id)
    utmZoneCode = int(codes[1])
    latZone = codes[2]

    # Split world into US, CA, LatinAmerica and Africa, Europe, Asia
    if (utmZoneCode < 26):
        #Polynesia
        if (latZone <= "M" and utmZoneCode < 16):
            region = "Polynesia"
        #Latin America
        elif (latZone <= "Q"):
            region = "LatinAmerica"
        #Canada
        elif (latZone >= "U" and utmZoneCode >= 8):
            region = "Canada"
        else:
            region = "USA"
    else:
        #Africa
        if (latZone <= "R" and utmZoneCode <= 39):
            region = "Africa"
        #Europe
        elif (utmZoneCode <= 37):
            region = "Europe"
        #Former Soviet
        elif (latZone >= "U"):
            region = "FormerSoviet"
        elif (latZone <= "L"):
            region = "OZ/NZ"
        else:
            region = "Asia"
    regions.setdefault(region,0)
    regions[region] += int(count)
    
for region in regions:
    print(region,regions[region])