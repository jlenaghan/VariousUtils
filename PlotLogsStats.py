import datetime, math
import matplotlib.pyplot as plt

data_dir = '/data/mojivaLogs/'

def doubleLogHistogram(filename,outfilename,xlabel):
    file = open(filename,'r')
    counts = []
    for line in file:
        toks = line.strip().split(',')
        counts.append(math.log(float(toks[-1])))
    file.close()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(counts, 1000, log=True)
    plt.xlabel(xlabel)
    plt.ylabel('Log Counts')
    plt.savefig(data_dir+outfilename)

def barPlotDateCount(filename):
    file = open(filename,'r')
    dates = []
    counts = []
    for line in file:
        _date, _counts = line.strip().split(',')
        YYYY, MM, DD = int(_date[0:4]), int(_date[4:6]), int(_date[6:8])
        dates.append(datetime.date(YYYY,MM,DD))
        counts.append(int(_counts))
    file.close()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Impressions')
    ax.set_title('Impressions by Date')
    plt.bar(dates, counts)
    
    plt.savefig(data_dir+'dates.png')


def barPlotLabelCount(filename):
    import numpy as np
    f = open(filename,'r')
    labels = []
    counts = []
    for line in f:
        _label, _counts = line.strip().split(',')
        labels.append(_label)
        counts.append(int(_counts))
    N = len(counts)
    ind = np.arange(N)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    width = 0.35
    ax.set_xticks(ind+width)
    ax.set_xticklabels( labels )
    ax.set_ylabel('Impressions')
    ax.set_title('Impressions by PIQ Time Period')
    rects1 = ax.bar(ind, counts, width, color='r')

    plt.savefig(data_dir+'hod.png')
    f.close()

def barPlotCount(filename):
    file = open(filename,'r')
    counts = []
    for line in file:
        _date, _counts = line.strip().split(',')
        counts.append(math.log(float(_counts)))
    file.close()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Log(Impressions)')
    ax.set_title('Log(Impressions) by Tile')
    plt.plot(counts)
    plt.savefig(data_dir+'tiles.png')

hod_filename = data_dir+'hod_file.csv'
barPlotLabelCount(hod_filename)

dates_filename = data_dir+'dates_file.csv'
barPlotDateCount(dates_filename)

tiles_filename = data_dir+'tiles_file.csv'
barPlotCount(tiles_filename)
doubleLogHistogram(tiles_filename,'tiles_hist','Log Tile Counts')

devices_filename = data_dir+'devices_file.csv'
barPlotCount(devices_filename)
doubleLogHistogram(devices_filename,'devices_hist','Log Device Counts')