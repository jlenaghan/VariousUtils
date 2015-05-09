#!/bin/sh
bf_bucket=s3://com.placeiq.analytics/emr/data/PolygonImpressionEstimates/BlackFriday/
trace_data_dir=/home/jlenaghan/Data/BlackFriday/
src_dir=/home/jlenaghan/Src/runHadoop/
data_dir=/data/walmart_black_friday/
mkdir ${data_dir}

trace_sets=(human_demand 4info_camp 4info_full)
competitor_geofences=(geo_100_m geo_200_m geo_300_m geo_500_m geo_750_m geo_1000_m)
walmart_poly_files=(walmart_polys walmart_geo_300_m)

for trace_file in ${trace_sets[@]}
do
	trace_data_file=${trace_data_dir}${trace_file}.dat

	local_dir=${data_dir}${trace_file}/
	mkdir ${local_dir}
	for walmart_poly_file in ${walmart_poly_files[@]}
		do

		walmart_poly_bucket=${bf_bucket}${walmart_poly_file}/
		local_dir=${data_dir}${trace_file}/${walmart_poly_file}/
		mkdir ${local_dir}
		for competitor_geofence in ${competitor_geofences[@]}
		do

			output_dir=${bf_bucket}output/${trace_file}/${walmart_poly_file}/${competitor_geofence}/
			local_dir=${data_dir}${trace_file}/${walmart_poly_file}/${competitor_geofence}/
			mkdir ${local_dir}
			s3cmd get ${output_dir}part* ${local_dir}
			sleep 1

		done

	done

done


