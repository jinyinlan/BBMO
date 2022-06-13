import sys
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np

file_num = 500
date = sys.argv[1]

"""
result_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/estimated_images/evaluate/'
bad_image_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/bad_images/'
"""
data_dir = '/home/omiya/data/Flickr_Interestingness_test/'
result_dir = '/home/omiya/data/Flickr_Datasets/temp/estimated_images/evaluate/'
bad_image_dir = '/home/omiya/data/Flickr_Interestingness_test/degraded_photos/chosen/'
dataset_dir = '/home/omiya/data/Flickr_Datasets/'
input_dir = '/home/omiya/data/Flickr_Datasets/Flickr_input_images/'
target_dir = '/home/omiya/data/Flickr_Datasets/Flickr_target/'

threshold=17

if __name__ == '__main__':
	
	f = open( data_dir+date+"/all_chosen_degraded_file_name.txt", 'r')
	file_name = f.readlines()
	f.close()


	#resNM = [0]*file_num
	resNM = np.zeros(file_num)
	allFileName = ['']*file_num
	#dataset_res = [0]*file_num

	temp_num = 0
	for i in range (len(file_name)):
		temp = file_name[i] #a0001~a0016
		image_name = bad_image_dir + temp[:-1] + '.jpg'
		fileNM = result_dir + 'result_' + temp[:-1] + '_nm.txt'

		print( temp.split('\n')[0] )
		if os.path.exists( fileNM ):
		
			allFileName[temp_num] = image_name
			#print( fileNM )
			#dataset_res[i] = float( eval_value[1] )

			f = open( fileNM, 'r' )
			eval_value = f.readlines()
			f.close()
			resNM[temp_num] = float( eval_value[0] )
			print( resNM[temp_num] )

			temp_num += 1
		else:
			print( temp, ': result file is not exists.' )
		print('')
	
	output_file = 'teacherData_' + temp[:10] + '.txt'
	op = open( dataset_dir+output_file , 'w')
	#op = open( dataset_dir+output_file , 'a')
	
	thresholded = 0
	for i in range (temp_num):
		name = (allFileName[i].split('/')[-1]).split('.jpg')[0]

		if resNM[i]<threshold: #use for dataset
			print( allFileName[i].split('/')[-1], resNM[i] )
			op.write( allFileName[i].split('/')[-1] )
			op.write('\n')
			thresholded += 1
			
			#move target images,parameters, and others
			if os.path.exists(dataset_dir+'temp/estimated_images/reproducedImages/'+name+'_new_nm.jpg'):
				shutil.move( dataset_dir+'temp/estimated_images/reproducedImages/'+name+'_new_nm.jpg', target_dir+'images/'+name+'_new_nm.jpg' )
			if os.path.exists(dataset_dir+'temp/estimated_images/parameters/'+name+'_parameter_nm.txt'):
				shutil.move( dataset_dir+'temp/estimated_images/parameters/'+name+'_parameter_nm.txt', target_dir+'parameters/'+name+'_parameter_nm.txt' )
			if os.path.exists(dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_nm.xmp'):
				shutil.move( dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_nm.xmp', target_dir+'xmpFiles/'+name+'_nm.xmp' )
			if os.path.exists(dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_tempXMPdata_nm.txt'):
				shutil.move( dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_tempXMPdata_nm.txt', target_dir+'xmpFiles/'+name+'_tempXMPdata_nm.txt' )
			if os.path.exists(dataset_dir+'temp/estimated_images/evaluate/result_'+name+'_nm.txt'):
				shutil.move( dataset_dir+'temp/estimated_images/evaluate/result_'+name+'_nm.txt', target_dir+'evaluate/result_'+name+'_nm.txt' )

			#cp input images
			if os.path.exists(bad_image_dir+name+'_bad.jpg'):
				shutil.copy2( bad_image_dir+name+'_bad.jpg', input_dir+name+'_bad.jpg')
			
		else: #not use
			if os.path.exists(dataset_dir+'temp/estimated_images/reproducedImages/'+name+'_new_nm.jpg'):
				os.remove( dataset_dir+'temp/estimated_images/reproducedImages/'+name+'_new_nm.jpg' )
			if os.path.exists(dataset_dir+'temp/estimated_images/parameters/'+name+'_parameter_nm.txt'):	
				os.remove( dataset_dir+'temp/estimated_images/parameters/'+name+'_parameter_nm.txt' )
			if os.path.exists(dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_nm.xmp'):
				os.remove( dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_nm.xmp' )
			if os.path.exists(dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_tempXMPdata_nm.txt'):
				os.remove( dataset_dir+'temp/estimated_images/xmpFiles/'+name+'_tempXMPdata_nm.txt' )
			if os.path.exists(dataset_dir+'temp/estimated_images/evaluate/result_'+name+'_nm.txt' ):
				os.remove( dataset_dir+'temp/estimated_images/evaluate/result_'+name+'_nm.txt' )
	op.close()

	print(thresholded, temp_num)
	