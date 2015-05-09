#!/bin/bash

msas=(chicago		denver		losangeles	newyork		sacramento	sanfrancisco) 
#msas=(washingtondc baltimore	dallas		houston		miami		phoenix		sandiego	seattle )

for msa in ${msas[@]}
do
/usr/local/bin/python ~/git/Python/scripts/Trace/GetProfileTags.py \
    --traceFile ~/Data/TraceAgg/${msa}/sorted_${msa}.dat.gz \
    --polygonFile ~/Data/UDIDPolygons/polygons.psv \
    --outFile ~/Data/UDIDSeeding/${msa}_profiles.json 
done
