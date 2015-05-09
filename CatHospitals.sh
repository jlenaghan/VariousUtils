#!/bin/bash

data_dir='/Users/jlenaghan/Data/UDIDSeeding/hospitals/'
msas=(baltimore	chicago		dallas		houston		losangeles	miami		phoenix		sandiego	sanfrancisco	seattle		washingtondc)

for msa in ${msas[@]}
do
    cd ${data_dir}/${msa}/
    gunzip -c part*.gz >> ${msa}_hospitals.json
done
