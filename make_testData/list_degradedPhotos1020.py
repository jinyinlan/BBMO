import glob
import sys

argvs = sys.argv
date = argvs[1]
#date = '2017-12-07'

all_bad_images = glob.glob( '/home/omiya/data/test-set1020/degraded_photos/temp/*' )

with open( '/home/omiya/data/test-set1020/2018-10-20/all_bad_file_name.txt', 'w' ) as file:
	for f in all_bad_images:
		strings = (f.split('/')[-1])
		#if ( strings.startswith(date) ):
		if ( not f.endswith('parameter_bad.txt') ):
			file.write( strings+'\n')