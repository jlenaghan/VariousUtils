#!/bin/bash

msas=(atlanta	chicago		denver		losangeles	newyork		sacramento	sanfrancisco	washingtondc
baltimore	dallas		houston		miami		phoenix		sandiego	seattle )

data_dir=/Users/jlenaghan/Data/TraceAgg/
for msa in ${msas[@]}
do
cd ${data_dir}/${msa}

echo Catting ${msa}
gunzip -c part*gz > total_${msa}.dat

echo Sorting ${msa}
sort -k1,1 total_${msa}.dat > sorted_${msa}.dat

echo Compressing ${msa}
gzip -9 sorted_${msa}.dat

echo Removing Uncompressed file
rm total_${msa}.dat
rm part*.gz

done