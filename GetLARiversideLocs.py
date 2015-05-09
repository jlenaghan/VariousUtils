
msas = {}
for line in open('/Users/jlenaghan/Data/WalmartBlackFriday/OutputV1/PolysToMSA.csv','r'):
	uid, msa = line.strip().split(',')
	msas[uid] = msa

for line in open('/Users/jlenaghan/Data/WalmartBlackFriday/OutputV1/all_store_locations.psv','r'):
	sid, wkt = line.strip().split('|')
	msa = msas[sid]
	if msa == 'losangeles' or msa == 'riverside':
		wkt = wkt.replace('POINT((','').replace(')','')
		lng, lat = wkt.split()
		sid = sid.lower()
		print sid+','+lng+','+lat