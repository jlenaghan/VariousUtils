import sys
import os 
import re
base_dir = sys.argv[1]
dirList = os.listdir(base_dir)
for d in dirList:
	if not re.search(r'_imp',d):
		msa = d
		new_listing = base_dir+'/'+msa
		for file in os.listdir(new_listing):
			if re.search(r'_aud',file):
				fn = open(base_dir+'/'+msa+'/'+file,'r')
				for line in fn:
					line = line.strip()
					print(msa+','+line)	
