#!/bin/bash

data_dir='/Users/jlenaghan/Data/UDIDSeeding'
hospital_data_dir=${data_dir}'/hospitals'
src_dir='/Users/jlenaghan/workspace/VariousUtils'
outfilename='catted_records.json'

arrayed_msas=(baltimore chicago dallas houston losangeles miami phoenix sandiego seattle washingtondc)
hashed_msas=(newyork sanfrancisco)

for msa in ${arrayed_msas[@]}
do
    python ${src_dir}/CatJsonDocuments.py ${data_dir}/${msa}_profiles.json    array >>  ${data_dir}/${outfilename}
    python ${src_dir}/CatJsonDocuments.py ${hospital_data_dir}/${msa}/${msa}_hospitals.json hash >> ${data_dir}/${outfilename}
done

for msa in ${hashed_msas[@]}
do
    python ${src_dir}/CatJsonDocuments.py ${data_dir}/${msa}_profiles.json      hash  >> ${data_dir}/${outfilename}
done

msa=sanfrancisco
python ${src_dir}/CatJsonDocuments.py ${hospital_data_dir}/${msa}/${msa}_hospitals.json      hash  >> ${data_dir}/${outfilename}

