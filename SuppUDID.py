import sys

poly_to_mas_filename = '/Users/jlenaghan/DataVault/BlackFriday/PolysToMSA.csv'


polys_to_msas = {}
f_polys_to_msas = open(poly_to_mas_filename,'r')
for line in f_polys_to_msas:
	sid, msa = line.strip().split(',')
	polys_to_msas[sid] = msa
f_polys_to_msas.close()

for line in sys.stdin:
	sid, udid, tp, tile_id, dstr, week, s_imps, s_att_imps, s_reqs, s_clicks, s_lat, s_lng = line.strip().split(',')
	msa = polys_to_msas[sid]
	udid = udid+'_'+msa
	print sid+','+udid+','+tp+','+tile_id+','+dstr+','+week+','+s_imps+','+s_att_imps+','+s_reqs+','+s_clicks+','+s_lat+','+s_lng