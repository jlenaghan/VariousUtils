from shapely.wkt import loads
from geojson import dumps
import pprint

msas = {}
for line in open('/Users/jlenaghan/Data/WalmartBlackFriday/OutputV1/PolysToMSA.csv','r'):
	uid, msa = line.strip().split(',')
	msas[uid] = msa

for line in open('/Users/jlenaghan/Data/WalmartBlackFriday/AnalysisDataSets/prod_walmarts_wkts.psv','r'):
	sid,name,wkt,msa = line.strip().split('|')
	msa = msas[sid]
	if msa == 'losangeles' or msa == 'riverside':
		wkt = wkt.replace('"','')
		x = loads(wkt)
		gdata = dumps(x)
		print gdata