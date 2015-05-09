import sys
import re
for line in sys.stdin:
	line = line.strip()
	if re.search(r'CAMPAIGN',line):
		print(line)
	else:
		try:
			fields = line.split('|')
			code = fields[4].lower()
			fn = open('/Users/jlenaghan/Data/Diageo/Thresholds_v2/'+code+'_1350000000.dat','r')
			thresholds = None
			for l in fn:
				l_fields = l.strip().split()
				thresholds = l_fields[-1]
			fn.close()
			print(line+'|'+thresholds)
		except:
			print line +'|8.5'