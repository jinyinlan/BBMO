#!/bin/bash

date=$1
echo "$1"

array_x=()
array_y=()

#FILENAME_x="all_file_name.txt"
FILENAME_1="/home/omiya/data/Flickr_Interestingness_test/"
FILENAME_2="/all_chosen_degraded_file_name.txt"
FILENAME=$FILENAME_1$1$FILENAME_2


while read line; do
	#echo $line
	array_x+=("$line")
done < $FILENAME

for i in {0..100}
do	
	echo "${array_x[i]}" 
	#echo "$x2" 
	python2 evaluate4.py ${array_x[i]}
done