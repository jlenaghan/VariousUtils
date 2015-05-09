import sys
import json
import pprint

infilename = sys.argv[1]
fn = open(infilename,'r')

udids = {}

for line in fn:
    line = line.strip()
    try:
        json_data = json.loads(line)
        dev_id = json_data['dev_id']
        tags = json_data['tags']
        if dev_id in udids:
            for tag in tags:
                #pprint.pprint(tag)
                #pprint.pprint(udids[dev_id])
                feature = tag['feature']
                #print(feature)
                include = True
                for element in udids[dev_id]['tags']:
                    if feature == element['feature']:
                        include = False
                if include:
                    udids[dev_id]['tags'].append(tag)
            #pprint.pprint(udids[dev_id])
            #print('\n\n')
        else:
            udids[dev_id] = json_data
    except:
        print('Bad record = ' + line)
        exit()

fn.close()

for udid in udids:
    print json.dumps(udids[udid])
