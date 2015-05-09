import sys
import json

num_tag_cnts = {}

for line in sys.stdin:
    line = line.strip()
    try:
        json_data = json.loads(line)
        num_tags = len(json_data['tags'])
        num_tag_cnts.setdefault(num_tags,0)
        num_tag_cnts[num_tags] += 1
    except:
        print 'Bad record = ' + line
        exit()

for num_tags in num_tag_cnts:
    print(str(num_tags) + '|' + str(num_tag_cnts))
