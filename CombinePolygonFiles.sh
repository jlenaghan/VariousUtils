#!/bin/bash

venues=(airport	arena college	shopping stadium
		amusement_theme_waterparks	golfcourse	speedway)
		
data_dir=/Users/jlenaghan/Data/UDIDPolygons/

for venue in ${venues[@]}
do

if [ "$venue" = airport ]; then
	tag=air_traveller
fi

if [ "$venue" = arena ]; then
	tag=concert_goer
fi

if [ "$venue" = college ]; then
	tag=college_affliation
fi

if [ "$venue" = shopping ]; then
	tag=retail_shopper
fi

if [ "$venue" = stadium ]; then
	tag=sports_fan
fi

if [ "$venue" = amusement_theme_waterparks ]; then
	tag=rider_lover
fi

if [ "$venue" = golfcourse ]; then
	tag=golfer
fi

if [ "$venue" = speedway ]; then
	tag=nascar_fan
fi

less ${data_dir}/${venue}/${venue}.csv | awk -v ref="${tag}" -F\| '{print ref "|" $1 "|" $2 "|" $3}' >> ${data_dir}/polygons.psv

done