import sys
import pprint

prev_line = None
total = []

for line in sys.stdin:
    if prev_line is None:
        prev_line = line.strip()
    
    if 'Expand' not in line:
        prev_line += ' ' + line.strip()
    else:
        total.append(prev_line)
        prev_line = line.strip()


for element in total:
    print element
