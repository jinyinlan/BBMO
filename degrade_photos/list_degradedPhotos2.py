import glob
import sys
import os
import shutil

argvs = sys.argv
date = argvs[1]
#date = '2017-12-07'

dir_name = '/home/omiya/data/Flickr_Interestingness_test/'

if os.path.exists( dir_name+date+'/all_bad_file_name.txt' ):
	shutil.copyfile( dir_name+date+'/all_bad_file_name.txt', dir_name+date+'/all_bad_file_name_0.txt')

if os.path.exists( dir_name+date+'/chosen_photos_'+date+'.txt' ):
	shutil.copyfile( dir_name+date+'/chosen_photos_'+date+'.txt', dir_name+date+'/chosen_photos_'+date+'_0.txt')

if os.path.exists( dir_name+date+'/chosen_photos_'+date+'_2.5.txt' ):
	shutil.copyfile( dir_name+date+'/chosen_photos_'+date+'_2.5.txt', dir_name+date+'/chosen_photos_'+date+'_2.5_0.txt')

if os.path.exists( dir_name+date+'/all_chosen_degraded_file_name.txt' ):
	shutil.copyfile( dir_name+date+'/all_chosen_degraded_file_name.txt', dir_name+date+'/all_chosen_degraded_file_name_.txt')


all_bad_images = glob.glob( dir_name+'degraded_photos/temp/*' )
number = 0
with open( '/home/omiya/data/Flickr_Interestingness_test/'+date+'/all_bad_file_name.txt', 'w' ) as file:
	for f in all_bad_images:
		strings = (f.split('/')[-1])
		if ( strings.startswith(date) ):
			if ( not f.endswith('parameter_bad.txt') ):
				file.write( strings+'\n')
				number += 1

print ('chosen:', number)