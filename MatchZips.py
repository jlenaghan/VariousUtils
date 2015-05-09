import sys
import pprint
# read kevin's zip file
kevin_zips = {}
kevin_in = open(sys.argv[2],'r')
for line in kevin_in:
	zipcode = line.strip()
	kevin_zips[zipcode] = 1
kevin_in.close()

# read mary's zip file
mary_zips = {}
mary_in = open(sys.argv[1],'r')
for line in mary_in:
	fields = line.strip().split('|')
	zipcode = fields[1]
	if len(zipcode) == 4: zipcode = '0'+zipcode
	if len(zipcode) > 5: zipcode = zipcode[0:5]
	if not zipcode in kevin_zips:
		print 'missing zip -> '  + zipcode
	mary_zips[zipcode] = 1
mary_in.close()
