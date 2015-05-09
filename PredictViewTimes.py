from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from StringIO import StringIO
import sys
import io
import gzip
import csv
import re
import json
import pprint 

def get_class_label(secs_on_page):
	if secs_on_page == None or secs_on_page == 0:
		return 'A'
	elif secs_on_page < 5:
		return 'B'
	elif secs_on_page < 30:
		return 'C'
	elif secs_on_page < 90:
		return 'D'
	elif secs_on_page < 300:
		return 'E'
	else:
		return 'F'

def get_section_score(section):
	if section == 'Scores':
		return 1.0
	elif section == 'ingame':
		return 2.0
	elif section == 'login':
		return 3.0
	elif section == 'news':
		return 4.0
	elif section == 'team' or section == 'teams':
		return 5.0
	else:
		return 6.0

max_depth = 2
min_samples_leaf = 10
n_samples, max_samples = 0, 10000000

classified = []
features = []

section_counts = {}

infilename = sys.argv[1]
outfilename = sys.argv[2]

r = io.BufferedReader( gzip.GzipFile( infilename, 'r') )
for line in r:
	line = line.decode('utf-8').strip()
	if not line: continue

	if n_samples >= max_samples: break
	n_samples += 1
       
	json_data = json.loads(line)

	is_avid_user = 1 if json_data['avid user'] else 0
	is_expat = 1 if json_data['expat'] else 0

	sessions = json_data['sessions']
	num_sessions = len(sessions)

	for session_dt in sessions:
		hour = sessions[session_dt]['hour']
		#pprint.pprint(sessions[session_dt])
		imps = sessions[session_dt]['imps']
		for imp in imps:
			time_on_page = imp['seconds']
			class_label = get_class_label(time_on_page)
			classified.append(class_label)
			section_score = get_section_score(imp['section'])
			features.append([section_score,num_sessions,hour])
	
r.close()

clf = tree.DecisionTreeClassifier(max_depth=max_depth)
#clf = RandomForestClassifier(n_estimators=10)

clf = clf.fit(features,classified)

out = StringIO()
out = tree.export_graphviz(clf, out_file=outfilename)
