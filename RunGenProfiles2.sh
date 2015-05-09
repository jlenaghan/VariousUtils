#!/bin/bash

msas=(chicago		denver		losangeles	newyork		sacramento	sanfrancisco	washingtondc
baltimore	dallas		houston		miami		phoenix		sandiego	seattle )

data_dir=/Users/jlenaghan/Data/
exec_dir=/Users/jlenaghan/git/Python/scripts/Trace/
for msa in ${msas[@]}
do
echo Running InferDwells for $msa
mkdir ${data_dir}/InferredDwells/${msa}/
/usr/local/bin/python ./InferDwells.py --in ${data_dir}/TraceAgg/${msa}/sorted_${msa}.dat.gz \
	--json --out ${data_dir}/InferredDwells/${msa}/dwells_${msa}.json
done