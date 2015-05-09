import sys
import re 

counts, hours, durations = {}, {}, {}
total_counts, total_hours, total_durations = 0.0,0.0,0.0

for line in sys.stdin:
    line = line.strip()
    m_obj = re.search(r"^Expand(.+)(j\-\w+)(.+)(\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2})(.+)$",line)
    
    if m_obj:
        name = m_obj.group(1)
        job_id = m_obj.group(2)
        status = m_obj.group(3)
        dt = m_obj.group(4)
        duration = m_obj.group(5)
      
        if '@' in name:
            fields = name.split('@')
            name = fields[0]
            user = name.lower().replace('hyqup--','').replace(' ','')
            user = user.replace('terminatedwitherrors','')
            user = user.replace('waiting','')
            user = user.replace('running','')
            if 'nataliya' in user: user = 'cron'
        elif 'AUTOMATED' in name or 'Aggregation' in name:
            user = 'cron'
        elif 'SegmentsFlow' in name:
            user = 'cron'
        elif 'Development Job Flow' in name:
            user = 'zombie'
        elif 'Dylan' in name:
            user = 'cron'
        elif 'alal' in name:
            user = 'alal'
        elif 'nataliya' in name:
            user = 'nataliya'
        elif 'roop' in name and 'pig' in name:
            user = 'bganguly'
        elif 'pig interactive' in name:
            user = 'zombie pig'
        elif 'stats' in name:
            user = 'zombie stats'
        elif 'tgif custom' in name:
            user = 'szhang'
        else:
            print 'problem b = ' + line


        runtime = 0
        fields = duration.split()
        instance_hours = int(fields[-1])

        if 'hour' in duration and 'minute' in duration:
            runtime = int(fields[0]) * 60 + int(fields[2])
        elif 'day' in duration and 'hour' in duration:
            runtime = int(fields[0])*24*60+int(fields[2])*60
        elif 'hour' in duration:
            runtime = int(fields[0]) * 60
        elif 'minutes' in duration and 'hour' not in duration:
            runtime = int(fields[0])
        elif 'seconds' in duration:
            runtime = 0
        elif '1 day' in duration:
            runtime = int(fields[0]) * 24 * 60
        else:
            runtime = 0 
        
        counts.setdefault(user,0)
        hours.setdefault(user,0)
        durations.setdefault(user,0)
        counts[user] += 1
        hours[user] += instance_hours
        durations[user] += runtime
        total_counts += 1
        total_hours += instance_hours
        total_durations += runtime

    else:
        print 'problem a = ' + line


for user in counts:
    perc_counts = str(float(counts[user])/total_counts)
    perc_hours = str(float(hours[user])/total_hours)
    perc_durations = str(float(durations[user]/total_durations))

    print user + ',' + str(counts[user]) + ',' + str(hours[user]) + ',' + str(durations[user]) + ',' + perc_counts + ',' + perc_hours + ',' + perc_durations + ',' + str(float(hours[user])/float(durations[user]+1))
