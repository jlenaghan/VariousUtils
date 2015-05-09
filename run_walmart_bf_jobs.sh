#!/bin/sh

# first argument is location of logs files
# second argument is comma-sep s3 polygon file name
# third is output
# jobflow

# /runPolygonReachEstimates.sh ~/Data/BlackFriday/four_info.dat 
# s3://com.placeiq.analytics/emr/data/PolygonImpressionEstimates/BlackFriday/geo_1000_m/ 
# s3://com.placeiq.analytics/emr/data/PolygonImpressionEstimates/BlackFriday/4info_1000/
# jobflow
# network / walmart_poly_type / competito_poly_type

# humand_demand/walmart_poly/comp_100/

jobflow=$1

if [ -z "$jobflow" ]
then
        export jobflow=$( /data/emr/bin/elastic-mapreduce \
                --create --alive --plain-output \
                --master-instance-type m1.xlarge \
                --slave-instance-type m1.xlarge \
                --num-instances 20 \
                --enable-debugging \
                --log-uri s3://com.placeiq.analytics/emr/logs/ \
                --args "--mapred-config-file,s3://com.placeiq.analytics/emr/bin/mapred-site-config-big-heap.xml" \
                --args -s,mapred.output.compress=true  \
                --name "Impression Estimates"  
       )
fi

bf_bucket=s3://com.placeiq.analytics/emr/data/PolygonImpressionEstimates/BlackFriday/
trace_data_dir=/home/jlenaghan/Data/BlackFriday/
src_dir=/home/jlenaghan/Src/runHadoop/

trace_sets=(human_demand 4info_camp 4info_full  twc)
competitor_geofences=(geo_100_m geo_200_m geo_300_m geo_500_m geo_750_m geo_1000_m)
walmart_poly_files=(walmart_polys walmart_geo_300_m)

for trace_file in ${trace_sets[@]}
do
	trace_data_file=${trace_data_dir}${trace_file}.dat

	for walmart_poly_file in ${walmart_poly_files[@]}
		do

		walmart_poly_bucket=${bf_bucket}${walmart_poly_file}/
		for competitor_geofence in ${competitor_geofences[@]}
		do

			poly_files=${walmart_poly_bucket},${bf_bucket}${competitor_geofence}/
			output_dir=${bf_bucket}output/${trace_file}/${walmart_poly_file}/${competitor_geofence}/
			${src_dir}runPolygonReachEstimates.sh ${trace_data_file} ${poly_files} ${output_dir} ${jobflow}
			sleep 5

		done

	done

done


