#!/bin/bash

msas=(atlanta		chicago		denver		losangeles	newyork		sacramento	sanfrancisco	washingtondc
baltimore	dallas		houston		miami		phoenix		sandiego	seattle)

for msa in ${msas[@]}
do
    cd /Users/jlenaghan/Data/TraceAgg/${msa}/
    gunzip -c sorted_${msa}.dat.gz | wc -l
done
