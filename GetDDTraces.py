import os, usng

# read lat-lngs from file
tiles = []
input_filename = '/data/trace_extractor/dunkin_donuts/input.csv'
dev_date_filename = '/data/trace_extractor/dunkin_donuts/dev_dates.csv'

# get tile_ids for each lat_lng
input_file = open(input_filename,'r')
for line in input_file:
    lat,lng = line.strip().split(',')
    tiles.append(usng.usng_from_x_y(float(lng),float(lat)))

# get devices and dates for each lat_lag
if os.path.exists(dev_date_filename):
    try:
        os.remove(dev_date_filename)
    except:
        print("Exception: Couldn't remove "+dev_date_filename)

for tile_id in tiles:
    query = ( 'psql --username postgres xtify -c \" '
              ' set enable_hashjoin = false; '
              '  set enable_mergejoin = false; '
              ' COPY( select b.device_id, b.timestamp, st_x(b.geometry), st_y(b.geometry), b.tile_id '
              ' from traces a join traces b on b.device_id = a.device_id and date(b.timestamp) = date(a.timestamp) '
              ' where a.tile_id  =  \''+tile_id+'\' and a.accuracy < 50 '
              ' and a.timestamp = (select max(c.timestamp) from traces c '
              ' where c.device_id = a.device_id and a.tile_id = c.tile_id) '
              ' order by b.device_id, b.timestamp '
              ' ) to STDOUT DELIMITER \',\' ' 
              '\" >> ' + dev_date_filename + ' '
              )
    os.system(query)



#    query = ( 'psql --username postgres xtify -c \" '
#              ' select device_id, date(timestamp) date into '
#              ' TEMPORARY dates_devs from traces where tile_id = '
#              ' \''  + tile_id +   '\' and accuracy < 50; '
#              ' COPY( select a.device_id, a.timestamp, st_x(a.geometry), st_y(a.geometry), '
#              ' a.tile_id from traces a INNER JOIN dates_devs b ON b.date = date(a.timestamp) '
#              ' and b.device_id = a.device_id order by a.device_id, a.timestamp  ) to STDOUT DELIMITER \',\' ' 
#              '\" >> ' + dev_date_filename + ' '
#              )
