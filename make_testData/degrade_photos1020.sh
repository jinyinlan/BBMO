#!/bin/bash

date=$1
echo "$1"

python2 randomely_degrade_photos1020.py $date
python2 list_degradedPhotos1020.py $date

