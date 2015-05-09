#!/bin/bash

msas=(atlanta boston chicago dallas houston 
	losangeles miami newyork philadelphia sanfrancisco washingtondc)

s3_bucket=s3://com.placeiq.data.emr/processing/core/1345573917

for msa in ${msas[@]}; do
	s3cmd get $s3_bucket/$msa/output/csv/part-r-00* - \
	| gunzip -c | grep Aff | awk -F\, '{if($5>3.0){print}}'
done
