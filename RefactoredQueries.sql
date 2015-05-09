psql --username postgres xtify -c "  

select device_id, date(timestamp) date  from traces where tile_id =  '18T WL 852 115' and accuracy < 50 order by device_id;  



select a.device_id, a.timestamp, st_x(a.geometry), st_y(a.geometry),  a.tile_id from traces a INNER JOIN dates_devs b ON b.date = date(a.timestamp)  and b.device_id = a.device_id


explain

    
ste 
    
set enable_hashjoin = false;
set enable_mergejoin = false;

    select b.device_id, b.timestamp, st_x(b.geometry), st_y(b.geometry), b.tile_id 
  from traces a join traces b on b.device_id = a.device_id and date(b.timestamp) = date(a.timestamp) 
 where a.tile_id  =  '18T WL 852 115' and a.accuracy < 50
   and a.timestamp = (select max(c.timestamp) from traces c where c.device_id = a.device_id and a.tile_id = c.tile_id)
    order by b.device_id, b.timestamp
;

