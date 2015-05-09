import os
import re
import numpy as np
import datetime
import matplotlib.pyplot as plt
import logging
import argparse 
import io
import gzip
from math import log as log_ten

def parse_args():
    parser = argparse.ArgumentParser(description="""
        Grabs ProcDescStats files from s3. Computes statistics
        and generates plots.  Stat files and plots are pushed 
        back to s3.  All files in temp working directory are 
        deleted.
                    --network [NETWORK]
                    --subDir [SUB DIR]
                    --serialNum [SERIAL NUM]
            """)
    parser.add_argument('--network', action="store", dest='network',
                        default = None, type=str, required=True)
    parser.add_argument('--subDir', action="store", dest='sub_dir',
                        default = None, type=str, required=True)
    parser.add_argument('--serialNum', action="store", dest='serial_num',
                        default = None, type=str, required=True)
    results = parser.parse_args()
    return results.network, results.sub_dir, results.serial_num

# EXTRACT THESE TO MODULE

def doubleLogHistogram(counts,outfilename,xlabel):
    log_counts = []
    for count in counts:
        log_counts.append(log_ten(float(count)))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(log_counts, bins=1000, log=True)
    plt.xlabel(xlabel)
    plt.ylabel('Log Counts')
    plt.savefig(outfilename)

def barPlotDateCount(date_hash,outfilename):
    dates = []
    counts = []
    for date in date_hash:
        counts.append(int(date_hash[date]))
        YYYY, MM, DD = int(date[0:4]), int(date[4:6]), int(date[6:8])
        dates.append(datetime.date(YYYY,MM,DD))    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Impressions')
    ax.set_title('Impressions by Date')
    plt.bar(dates, counts)
    plt.savefig(outfilename)


def barPlotLabelCount(hod_hash,outfilename):
    labels = []
    counts = []
    for hod in hod_hash:
        labels.append(hod)
        counts.append(int(hod_hash[hod]))
    N = len(counts)
    ind = np.arange(N)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    width = 0.35
    ax.set_xticks(ind+width)
    ax.set_xticklabels( labels )
    ax.set_ylabel('Impressions')
    ax.set_title('Impressions by PIQ Time Period')
    ax.bar(ind, counts, width, color='r')
    plt.savefig(outfilename)

def barPlotCount(counts,outfilename):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Log(Impressions)')
    ax.set_title('Log(Impressions) by Tile')
    plt.plot(sorted(counts))
    plt.savefig(outfilename)

# EXTRACT TO MOVING AROUND 

def copy_from_s3(source, target):
    cmd = 's3cmd get ' + source + ' ' + target
    log.debug('Executing ['+ cmd +']')
    try:
        os.system('s3cmd  get ' + source + ' ' + target)
    except:
        log.error('Could not copy '+source+' to '+target+'.')
        
def copy_to_s3(source,target):
    os.system('s3cmd put ' + source + ' ' + target)

def move_to_s3(source,target):
    copy_to_s3(source,target)
    try:
        os.remove(source)
    except:
        print("Couldn't remove " + source)

def setupLogging(name,level):        
    log = logging.getLogger(name)
    log.setLevel(level)
    formatter = logging.Formatter('%(asctime)s:[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

def clean_dir(dir_to_clean,log):
    for f in sorted(os.listdir(dir_to_clean)):
        full_filename = dir_to_clean+'/'+f
        if os.path.isfile(full_filename):
            log.debug('Removing ' + full_filename )
            os.remove(full_filename)

#----------------------------------------------#

if __name__ == "__main__":
    network, sub_dir, serial_num = parse_args()
#    data_dir = '/data/analyzeLogsTmp/'
    data_dir = '/Users/jlenaghan/tmp/analyzeLogsRollupTmp/'+ \
        network+'/'+sub_dir+'/'+serial_num+'/'
    log = setupLogging('analyzeLogs', logging.DEBUG)

    date_counts, hod_counts = {}, {}
    tiles, devs = [], []
    total_impressions, total_tiles, total_devs = 0, 0, 0
    
    p_suc = re.compile('SUCCESS')
    reDate = re.compile('^DATE')
    reHod = re.compile('^HOD')
    reTileRecord = re.compile(r'^[0-9]+[A-Z]{3}[0-9]{6}$')
    reTileDeviceRecord = re.compile(r'^[0-9]+[A-Z]{3}[0-9]{6}\,[A-Z0-9]')
    
#    clean_dir(data_dir,log)
    stats_files = 's3://com.placeiq.data.emr/processing/traces/'
    stats_files += network +'/'+ sub_dir +'/'+ serial_num +'/ProcDescStats/part*'
    log.info('Getting files from s3 [' + stats_files + '].')
    copy_from_s3(stats_files,data_dir)

    tiles_file_name = data_dir + 'tiles_file.csv'
    tiles_file = open(tiles_file_name,'w')
    devs_file_name = data_dir + 'devices_file.csv'
    devs_file = open(devs_file_name,'w')
    
    log.info('Reading input files.')
    start = 'part'
    for f in sorted(os.listdir(data_dir)):
        log.debug('File: '+f)
        if f.startswith(start):
            is_gzip = f.endswith('.gz')
            data_file = None
            if is_gzip:
                data_file = io.BufferedReader(gzip.open(data_dir+f))
            else:
                data_file = open(data_dir+f, 'r')
            log.info('Processing ' + data_dir + f)
            
            for line in data_file:
                line = line.decode('utf-8')
                try:
                    fields = line.strip().split()
                    count = int(fields[1])
                    if reTileRecord.match(fields[0]):
                        tiles.append(count)
                        total_impressions += count
                        tiles_file.write(fields[0] + ',' + str(count) + '\n')
                        total_tiles += 1
                    elif reTileDeviceRecord.match(fields[0]):
                        continue
                    elif reDate.match(fields[0]) :
                        toks = fields[0].split('_')
                        date_counts[toks[-1]] = count
                    elif reHod.match(fields[0]):
                        toks = fields[0].split('_')
                        hod_counts[toks[-1]] = count
                    else:
                        devs.append(count)
                        devs_file.write(fields[0] + ',' + str(count) + '\n')
                        total_devs += 1
                except:
                    log.error('Bad row ' + line)
                    continue
            data_file.close()
    tiles_file.close()
    devs_file.close()
    
    log.info('Writing Hour-Of-Day file.')
    hod_file_name = data_dir + 'hod_file.csv'
    hod_file = open(hod_file_name,'w')
    for hod in hod_counts:
        result = str(hod)+','+str(hod_counts[hod])+'\n'
        hod_file.write(result)
    hod_file.close()
    
    log.info('Writing Dates file.')
    dates_file_name = data_dir + 'dates_file.csv'
    dates_file = open(dates_file_name,'w')
    for date in sorted(date_counts.keys()):
        dates_file.write(str(date)+','+str(date_counts[date])+'\n')
    dates_file.close()
    
    log.info('Computing means and medians.')
    d_counts = np.array(devs)
    t_counts = np.array(tiles)
    tile_mean = t_counts.mean()
    dev_mean = d_counts.mean()
    tile_median = np.median(d_counts)
    dev_median = np.median(d_counts)
    
    log.info('Writing Descriptive Statistics file.')
    desc_stats_file_name = data_dir + 'desc_stats.csv'
    desc_stats_file = open(desc_stats_file_name,'w')
    desc_stats_file.write("TOTAL_IMPRESSIONS|" + str(total_impressions) + '\n')
    desc_stats_file.write("TOTAL_TILES|" + str(total_tiles) + '\n')
    desc_stats_file.write("TOTAL_DEVS|" + str(total_devs) + '\n')
    desc_stats_file.write("MEAN_TILE_COUNTS|" + str(tile_mean) + '\n')
    desc_stats_file.write("MEAN_DEV_COUNTS|" + str(dev_mean) + '\n')
    desc_stats_file.write("MEDIAN_TILE_COUNTS|" + str(tile_median) + '\n')
    desc_stats_file.write("MEDIAN_DEV_COUNTS|" + str(dev_median) + '\n')
    desc_stats_file.close()
    
    log.info('Generating plots.')
    barPlotLabelCount(hod_counts,data_dir+'hod_hist.png')
    barPlotDateCount(date_counts,data_dir+'dates.png')
    doubleLogHistogram(tiles,data_dir+'tiles_hist.png','Log Tile Counts')
    doubleLogHistogram(devs,data_dir+'devices_hist.png','Log Device Counts')
    
    target_s3_bucket = 's3://com.placeiq.analytics/LogQualityAnalytics/'
    target_s3_bucket += network + '/' + sub_dir + '/' + serial_num + '/'
    
    log.info('Gziping large files.')
    os.system('gzip -f9 '+devs_file_name)
    os.system('gzip -f9 '+tiles_file_name)
    
    log.info('Moving files to s3 bucket.')
    copy_to_s3(desc_stats_file_name,target_s3_bucket)
    copy_to_s3(devs_file_name+'.gz',target_s3_bucket)
    copy_to_s3(hod_file_name,target_s3_bucket)
    copy_to_s3(tiles_file_name+'.gz',target_s3_bucket)
    copy_to_s3(dates_file_name,target_s3_bucket)
    copy_to_s3(data_dir+'hod_hist.png',target_s3_bucket)
    copy_to_s3(data_dir+'dates.png',target_s3_bucket)
    copy_to_s3(data_dir+'tiles_hist.png',target_s3_bucket)
    copy_to_s3(data_dir+'devices_hist.png',target_s3_bucket)

#    clean_dir(data_dir,log)