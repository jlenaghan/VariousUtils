import sys
import pprint
import re

dows, hods, hows = {},{},{}
metro_scores, rel_scores = {}, {}
total = 0

def output_hash(hm,filename):
	f_out = open(filename,'w')
	for key in hm:
		f_out.write(str(key)+','+str(hm[key])+'\n')
	f_out.close()

for line in sys.stdin:
	tile_id, dow, hod, how, s_rel_score, metro_id, s_metro_score, lat, lng = line.strip().split()
	total =+ 1

	dows.setdefault(dow,0)
	hods.setdefault(hod,0)
	hows.setdefault(how,0)
	dows[dow] += 1
	hods[hod] += 1
	hows[how] += 1

	# Now process scores
	rel_score, metro_score = 0,0
	if not re.search(r'N',s_rel_score):
		rel_score = int(s_rel_score)
		rel_scores.setdefault(rel_score,0)
		rel_scores[rel_score] += 1
	if not re.search(r'N',s_metro_score):
		metro_score = int(s_metro_score)
		metro_scores.setdefault(metro_score,0)
		metro_scores[metro_score] += 1


output_hash(dows,'/Users/jlenaghan/tmp/Skyhook/dow.dat')
output_hash(hods,'/Users/jlenaghan/tmp/Skyhook/hod.dat')
output_hash(hows,'/Users/jlenaghan/tmp/Skyhook/how.dat')
output_hash(metro_scores,'/Users/jlenaghan/tmp/Skyhook/metro_score.dat')
output_hash(rel_scores,'/Users/jlenaghan/tmp/Skyhook/rel_score.dat')




