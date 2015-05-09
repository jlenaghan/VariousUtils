import sys
import io
import gzip
import re
import pprint 
sys.path.append('../../git/Python/lib')
import usng
from shapely.wkt import dumps, loads
from shapely.geometry import Point
import json

retail_apparel = (
"Retail->Apparel_and_Accessories->Clothing",
"Retail->Apparel_and_Accessories->Mens_Apparel",
"Retail->Apparel_and_Accessories->Shoes",
"Retail->Apparel_and_Accessories->Sports_and_Fitness_Apparel",
"Retail->Apparel_and_Accessories->Womens_Apparel->General"
)

dining = (
"Dining->Bars_and_Pubs->General",
"Dining->Daylife->Bakery",
"Dining->Daylife->Deli",
"Dining->Food_and_Drink->Restaurant"
)

hotels = (
"Lodging->Hotel_Motel->General"
)

retail_electronics = (
"Retail->Electronics->Cell_Phone_Providers",
"Retail->Electronics->Computing",
"Retail->Electronics->General",
"Retail->Electronics->Home_Entertainment",
"Retail->Electronics->Video_Games"
)

retail_food = (
"Retail->Food->Grocery->General",
"Retail->Food->Grocery->Health_Food"
)

theaters_museums = (
"Art_and_Museums->Museums",
"Entertainment->Theaters_and_Music->General",
"Entertainment->Theaters_and_Music->Movies"
)

shopping = (
"Retail->Department_Stores",
"Retail->Malls_and_Shopping_Centers->Shopping_Centers",
"Retail->Pawnshop",
"Retail->Rental->Consumer_Rental->General"
)

auto_repair = (
"Auto->Repair_and_Servicing->General"
)

health = (
"Service->Health->Specialists",
"Sports_Facilities->Health_Clubs"
)

atms = (
"Service->ATM"
)

retail_general = (
"Retail->Books->General",
"Retail->Convenience_Stores",
"Retail->Crafts_and_Hobbies",
"Retail->Drugs_and_Health->Drugstore_and_Pharmacy",
"Retail->Gifts_and_Curios",
"Retail->Liquor_Stores->General",
"Retail->Video_Rental_and_Sales"
)

rolled_fat_names = { 
	'atms':atms,
	'retail_general':retail_general,
	'healthy_living':health,
	'auto_repair':auto_repair,
	'retail_apparel':retail_apparel,
	'dining_drinking':dining,
	'hotels_motels':hotels,
	'retail_electronics':retail_electronics,
	'retail_food':retail_food,	
	'theaters_museums':theaters_museums,
	'shopping':shopping
	}

counts = {}
total = 0
total_in_college = 0
tiles = {}
polys = {}
rolled_fats = {}
MIN_SCORE = 0.25

r = io.BufferedReader( gzip.GzipFile( sys.argv[1],'r') )
for line in r:
	line = line.strip()
	try:
		tile_id, tp, ft, att, score = line.split(',')
	except:
		continue
	for rolled_fat_name in rolled_fat_names:
		if att in rolled_fat_names[rolled_fat_name]:
			rolled_fats.setdefault(rolled_fat_name,{}).setdefault(tile_id,[])
			rolled_fats[rolled_fat_name][tile_id].append(score)
r.close()

json_data = {}

for rolled_fat_name in rolled_fats:
	for tile_id in rolled_fats[rolled_fat_name]:
		scores = []
		for score in rolled_fats[rolled_fat_name][tile_id]:
			scores.append(float(score))
		mean = sum(scores)/len(scores)
		if mean > MIN_SCORE:
			print(tile_id+',6,Verizon,'+rolled_fat_name+','+str(mean))
			# json_data.setdefault(tile_id,{})
			# json_data[tile_id].setdefault('6',[])
			# json_fat = {'feature':'Verizon','attributes':[]}
			# lowest_hm = {'confidence':'5', 'coverage':'5', 'attribute':rolled_fat_name, 'score':str(mean)}
			# json_fat['attributes'].append(lowest_hm)
			# json_data[tile_id]['6'].append(json_fat)

exit()


poly_filename = '/Users/jlenaghan/Data/Verizon/losangeles/universities-ca.psv'
poly_in = open(poly_filename,'r')
for line in poly_in:
	tag, polygon = line.strip().split('|')
	polys[tag] = loads(polygon)
poly_in.close()

outfilename = '/Users/jlenaghan/tmp/la_verizon.csv'
f_out = open(outfilename,'w')
for tile_id in tiles:
	lng, lat = usng.USNGtoLL(tile_id)
	point = Point(lng,lat)
	for poly in polys:
		polygon = polys[poly]
		if point.within(polygon):
			total_in_college += 1
	f_out.write(str(lat)+','+str(lng)+'\n')
f_out.close()

print(total_in_college)