files=(part-00002.gz    part-00010.gz   part-00014.gz   part-00018.gz)

for file in ${files[@]}
do
    echo processing ${file}
    gunzip -c /Users/jlenaghan/DataScratch/8000_300/${file} | python /Users/jlenaghan/git/Python/scripts/Campaigns/FindStoreTransitions.py 8000_300 >> /tmp/8000_300.dat
done
