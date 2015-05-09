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
    results = parser.parse_args()
    return results.network


def doubleLogHistogram(counts,outfilename,xlabel):
    log_counts = []
    for count in counts:
        log_counts.append(log_ten(count))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(log_counts, 1000, log=True)
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

def copy_from_s3(source, target):
    cmd = 's3cmd -c /etc/s3cmd.cfg get ' + source + ' ' + target
    log.debug('Executing ['+ cmd +']')
    os.system('s3cmd -c /etc/s3cmd.cfg get ' + source + ' ' + target)

def copy_to_s3(source,target):
    os.system('s3cmd -c /etc/s3cmd.cfg put ' + source + ' ' + target)

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
    network = parse_args()
    data_dir = '/Users/jlenaghan/tmp/analyzeLogsRollupTmp/'+network+'/All/'
    if network == 'All':
        data_dir = '/Users/jlenaghan/tmp/analyzeLogsRollupTmp/All/'
    #data_dir = '/Users/jlenaghan/tmp/analyzeLogsTmp/'
    log = setupLogging('analyzeLogs', logging.DEBUG)

    date_counts, hod_counts = {}, {}
    tiles, devs = [], []
    total_impressions, total_tiles, total_devs = 0, 0, 0
    
    p_suc = re.compile('SUCCESS')
    reDate = re.compile('^DATE')
    reHod = re.compile('^HOD')
    reTileRecord = re.compile(r'^[0-9]+[A-Z]{3}[0-9]{6}$')
    reTileDeviceRecord = re.compile(r'^[0-9]+[A-Z]{3}[0-9]{6}\,[A-Z0-9]')
    
    tiles_file_name = data_dir + 'tiles_file.csv.gz'
    g = gzip.GzipFile(tiles_file_name,'r')
    tiles_file = io.BufferedReader(g)
    for line in tiles_file:
        tile_id, count = line.strip().split()
        total_impressions += int(count)
        total_tiles += 1
        tiles.append(int(count))
    tiles_file.close()

    hod_file_name = data_dir + 'hod_file.csv'
    hod_file = open(hod_file_name,'r')
    for line in hod_file:
        hod, count = line.strip().split(',')
        hod_counts[hod] = int(count)
    hod_file.close()

    dates_file_name = data_dir + 'dates_file.csv'
    dates_file = open(dates_file_name,'r')
    for line in dates_file:
        date, count = line.strip().split(',')
        date_counts[date] = int(count)
    dates_file.close()
    
    log.info('Computing means and medians.')
    t_counts = np.array(tiles)
    tile_mean = t_counts.mean()
    tile_median = np.median(t_counts)

#    d_counts = np.array(devs)
#    dev_mean = d_counts.mean()
#    dev_median = np.median(d_counts)
    
    log.info('Writing Descriptive Statistics file.')
    desc_stats_file_name = data_dir + 'desc_stats.csv'
    desc_stats_file = open(desc_stats_file_name,'w')
    desc_stats_file.write("TOTAL_IMPRESSIONS|" + str(total_impressions) + '\n')
    desc_stats_file.write("TOTAL_TILES|" + str(total_tiles) + '\n')
    desc_stats_file.write("TOTAL_DEVS|" + str(total_devs) + '\n')
    desc_stats_file.write("MEAN_TILE_COUNTS|" + str(tile_mean) + '\n')
    desc_stats_file.write("MEAN_DEV_COUNTS|0" + '\n')
    desc_stats_file.write("MEDIAN_TILE_COUNTS|" + str(tile_median) + '\n')
    desc_stats_file.write("MEDIAN_DEV_COUNTS|0" + '\n')
    desc_stats_file.close()
    
    log.info('Generating plots.')
    barPlotLabelCount(hod_counts,data_dir+'hod_hist.png')
    barPlotDateCount(date_counts,data_dir+'dates.png')
    doubleLogHistogram(tiles,data_dir+'tiles_hist.png','Log Tile Counts')
    doubleLogHistogram(devs,data_dir+'devices_hist.png','Log Device Counts')
    
#    target_s3_bucket = 's3://com.placeiq.analytics/LogQualityAnalytics/'
#    target_s3_bucket += network + '/' + sub_dir + '/' + serial_num + '/'
#    
#    log.info('Gziping large files.')
#    os.system('gzip -f9 '+devs_file_name)
#    os.system('gzip -f9 '+tiles_file_name)
#    
#    log.info('Moving files to s3 bucket.')
#    move_to_s3(desc_stats_file_name,target_s3_bucket)
#    move_to_s3(devs_file_name+'.gz',target_s3_bucket)
#    move_to_s3(hod_file_name,target_s3_bucket)
#    move_to_s3(tiles_file_name+'.gz',target_s3_bucket)
#    move_to_s3(dates_file_name,target_s3_bucket)
#    move_to_s3(data_dir+'hod_hist.png',target_s3_bucket)
#    move_to_s3(data_dir+'dates.png',target_s3_bucket)
#    move_to_s3(data_dir+'tiles_hist.png',target_s3_bucket)
#    move_to_s3(data_dir+'devices_hist.png',target_s3_bucket)
#
#    clean_dir(data_dir,log)