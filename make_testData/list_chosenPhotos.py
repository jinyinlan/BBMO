import glob
import sys
import shutil

argvs = sys.argv
date = argvs[1]
#date = '2017-12-07'
print(date)

all_chosen_images = glob.glob( '/home/omiya/data/test-set0811/supplemental/degraded_photos/chosen/*' )

with open( '/home/omiya/data/test-set0811/'+date+'/all_chosen_degraded_file_name.txt', 'w' ) as file:
	for f in all_chosen_images:
		strings = (f.split('/')[-1]).split('_bad')[0]
		if ( strings.startswith(date) ):
			if ( not f.endswith('parameter_bad.txt') ):
				file.write( strings+'\n' )

shutil.copy2( '/home/omiya/data/test-set0811/'+date+'/all_chosen_degraded_file_name.txt', '/home/omiya/data/test-set0811/'+date+'/temp_file_name.txt')