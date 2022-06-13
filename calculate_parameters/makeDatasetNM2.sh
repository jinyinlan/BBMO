#!/bin/bash

SECONDS=0
date=$1
echo "$1"

array_x=()
array_y=()

FILENAME_1="/home/omiya/data/Flickr_Interestingness_test/"
FILENAME_2="/temp_file_name.txt"
FILENAME=$FILENAME_1$date$FILENAME_2
extensionName=".txt"
while read line; do
	array_x+=("$line")
done < $FILENAME

for i in {0..100}
do
	echo "${array_x[i]}" 
	#time python nm-estimate-flickr.py ${array_x[i]}
	time python2 nm-estimate-flickr.py ${array_x[i]} > /dev/null
	python2 evaluate4.py ${array_x[i]} "nm"
done

time=$SECONDS
echo $time