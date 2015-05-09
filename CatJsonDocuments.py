# Reads various json documents for UDID project
# and combines them into single document 
import json
import sys
import pprint

infilename = sys.argv[1]
tags_type = sys.argv[2]

full_data = {}
num_records = 0
num_dups = 0

fn = open(infilename,'r')
for line in fn:
    line = line.strip()
    try:
        json_data = json.loads(line)
        
        data = {}

        dev_id = json_data[0]['dev_id']
        data['dev_id'] = dev_id
        data['tags'] = []

        if tags_type == 'array':
            tags = json_data[1]['tags']
            for i in range(0,len(tags)):
                single_hm = tags[i]
                for key in single_hm:
                    tag_hash = {}
                    tag_hash['feature'] = key
                    tag_hash['confidence'] = single_hm[key]
                    data['tags'].append(tag_hash)
        else:
            tags = json_data[1]['tags']
            for tag in tags:
                tag_hash = {}
                tag_hash['feature'] = tag
                tag_hash['confidence'] = tags[tag]
                data['tags'].append(tag_hash)
        # now add to full_data
        #if dev_id in full_data:
        #    num_dups += 1
            #print('\n')
            #print(line)
            #pprint.pprint(full_data[dev_id])

       #:if dev_id in full_data:

        full_data[dev_id] = data
        
        num_records += 1
    except:
        print("Unable to process record: " + line)
        pprint.pprint(tags)
        exit()

# first write everything out. then dedup with another script.
for record in full_data:
    print json.dumps(full_data[record])

