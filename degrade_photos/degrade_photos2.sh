#!/bin/bash

date=$1
echo "$1"

python2 randomely_degrade_photos2.py $date
python2 list_degradedPhotos2.py $date

