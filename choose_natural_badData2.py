import os
import sys
#import csv
import random
import numpy as np
import cv2
import re
import commands

import encodeModule_Float2Binary_5 as encodeF2B
import makeXMLfileModule_5 as makeXML

#python2

# y or 1 : natural
# n or 2 : not natural
# 0	  : default

#change here
argvs = sys.argv
data = argvs[1]
#data = '2017-12-07'



previmage = None
original_image_dir = '/home/omiya/data/Flickr_Interestingness_test/'+data+'/'
bad_image_dir = '/home/omiya/data/Flickr_Interestingness_test/degraded_photos/temp/'
#parameter_name = bad_image_dir + name +'_parameter_bad.txt'



f = open(original_image_dir+'all_file_name.txt', 'r')
file_name = f.readlines()
f.close()

annotations = [0]*len(file_name)

def make_random_parameters():
	#param_scale = [ 0.2, 6, 200, 20, 200, 100, 100, 2, 2, 2, 8, 8, 8, 100, 80, 80, 80, 80, 6, 5, 5 ]
	param_initial = [ 0, 0, 50, 0, -50, 100, 50, 0, 0, 0, 1, 1, 1, 25, 0, 0, 0, 0, 1, 1, 1 ]

	"""
	param_max = [ 0.1, 2.5, 100, 10, 100, 100, 100, 1.0, 1.0, 1.0, 1.2, 1.2, 1.2, 100, 20, 20, 20, 20, 3.0, 1.2, 1.2 ]
	param_min = [ -0.1, -3.0, -100, -10, -100, 0, 0, -1.0, -1.0, -1.0, 0.8, 0.8, 0.8, 0, -20, -20, -20, -20, -3.0, 0.8, 0.8 ]
	"""
	param_max = [ 0.1, 2.5, 100, 10, 100, 100, 100, 1.0, 1.0, 0.75, 1.2, 1.2, 1.2, 100, 20, 20, 20, 20, 1.5, 1.2, 1.2 ]
	param_min = [ -0.1, -2.5, -100, -10, -100, 0, 0, -1.0, -1.0, -1.0, 0.8, 0.8, 0.8, 0, -20, -20, -20, -20, 0.25, 0.8, 0.8 ]

	param_num = len(param_initial)
	random_param= [0]*param_num

	for i in range(param_num):
		random_param[i] = random.uniform(param_min[i], param_max[i])
	return random_param

def make_parameter_file(parameter, paramfile_name ):

	parameter[0] = np.clip(parameter[0], -0.1, 0.1) #exposre black
	parameter[1] = np.clip(parameter[1], -3, 3) 	#exposre exposure
	parameter[2] = np.clip(parameter[2], -100, 100) #shadhi shadow
	parameter[3] = np.clip(parameter[3], -10, 10)	#shadhi whitepoint
	parameter[4] = np.clip(parameter[4], -100, 100) #shadhi highlight
	parameter[5] = np.clip(parameter[5], 0, 100)	#shadhi shadowsaturation
	parameter[6] = np.clip(parameter[6], 0, 100)	#shadhi highlightsaturation
	parameter[7] = np.clip(parameter[7], -1, 1)		#colisa contrast
	parameter[8] = np.clip(parameter[8], -1, 1)		#colisa lightness
	parameter[9] = np.clip(parameter[9], -1, 1)		#colisa saturation
	parameter[10] = np.clip(parameter[10], 0, 8)	#temperature R
	parameter[11] = np.clip(parameter[11], 0, 8)	#temperature G
	parameter[12] = np.clip(parameter[12], 0, 8)	#temperature B
	parameter[13] = np.clip(parameter[13], 0, 100)	#vibrance vibrance
	parameter[14] = np.clip(parameter[14], -40, 40)	#colorcorrection highlightX
	parameter[15] = np.clip(parameter[15], -40, 40)	#colorcorrection highlightY
	parameter[16] = np.clip(parameter[16], -40, 40)	#colorcorrection shadowX
	parameter[17] = np.clip(parameter[17], -40, 40)	#colorcorrection shadowY
	parameter[18] = np.clip(parameter[18], -3, 3)	#colorcorrection saturation
	parameter[19] = np.clip(parameter[19], 0, 5)	#colorcontrast GM
	parameter[20] = np.clip(parameter[20], 0, 5)	#colorcontrast BY


	exposure = str(parameter[0])+' '+str(parameter[1])
	shadhi = str(parameter[2])+' '+str(parameter[3])+' '+str(parameter[4])+' '+str(parameter[5])+' '+str(parameter[6])
	colisa = str(parameter[7])+' '+str(parameter[8])+' '+str(parameter[9])
	temperature = str(parameter[10])+' '+str(parameter[11])+' '+str(parameter[12])
	vibrance = str(parameter[13])
	colorcorrection = str(parameter[14])+' '+str(parameter[15])+' '+str(parameter[16])+' '+str(parameter[17])+' '+str(parameter[18])
	colorcontrast = str(parameter[19])+' '+str(parameter[20])
	#f = open('tempParameter.txt', 'w')
	f = open(paramfile_name, 'w')
	#f.write('flip : ffffffff\n')
	f.write('exposure : '+exposure+'\n')
	f.write('shadhi : '+shadhi+'\n')
	f.write('colisa : '+colisa+'\n')
	f.write('temperature : '+temperature+'\n')
	f.write('vibrance : '+vibrance+'\n')
	f.write('colorcorrection : '+colorcorrection+'\n')
	f.write('colorcontrast : '+colorcontrast+'\n')
	f.close()

def make_retouched_photo(parameter, imgname ): # x=original image, z=target image

	input_name = re.split('[/.]', imgname)[-2] #2017-12-14-00...0
	paramfile_name = bad_image_dir + input_name + '_parameter_bad.txt'
	XMPdataFile_name = bad_image_dir + input_name + '_tempXMPdata_bad.txt'
	xmpfile_name = bad_image_dir + input_name + '_bad.xmp'
	output_im = bad_image_dir + input_name +'_bad.jpg'

	make_parameter_file( parameter, paramfile_name )
	#print 'made parameter file'
	encodeF2B.encode_f2b(paramfile_name, XMPdataFile_name)
	#print 'encoded'
	makeXML.makeXMP_file(imgname, XMPdataFile_name, xmpfile_name)
	#print 'made xmpFile'
	tempImage = commands.getoutput('darktable-cli '+imgname+' '+xmpfile_name+' '+output_im+' --hq false')
	#commands.getoutput('rm '+XMPdataFile_name)
	#commands.getoutput('rm '+xmpfile_name)


def make_bad_photo( imgname ):
	parameter = np.array( make_random_parameters() )
	make_retouched_photo( parameter, imgname )

def process_image( imgname, imgnum, redo=False ):
	#if not redo and imgname in annotations.keys():
	#	return True

	make_bad_photo( imgname )
	input_name = re.split('[/.]', imgname)[-2] #2017-12-14-00...0
	paramfile_name = bad_image_dir + input_name + '_parameter_bad.txt'
	bad_imgname = bad_image_dir + input_name +'_bad.jpg'
	org_imgname = imgname

	# Load and view the image
	img = cv2.imread( bad_imgname )
	org_img = cv2.imread( org_imgname )

	if img is None:
		print(bad_imgname.split('/')[-1]+" can't be loaded")
		return True
	cv2.imshow('image',img)
	cv2.imshow('original_image',org_img)

	# Handle input
	imgclass = None
	while True:
		k = (cv2.waitKey(0) & ~0x100000)
		if k in [49,65457]: #input =1
			imgclass = 1
			new_dir = bad_image_dir+'yes/'
			commands.getoutput('mv '+bad_imgname+' '+new_dir)
			commands.getoutput('mv '+paramfile_name+' '+new_dir)
		elif k in [50,65458]: #input =2
			imgclass = 2
			new_dir = bad_image_dir+'no/'
			commands.getoutput('mv '+bad_imgname+' '+new_dir)
			commands.getoutput('mv '+paramfile_name+' '+new_dir)			
		#elif k in [51,65459]:
		#	imgclass = 3
		#elif k in [52,65460]:
		#   imgclass = 4
		#elif k in [53,65461]:
		#   imgclass = 5
		elif k is ord('u'):
			return False
		elif k is ord('x') or k is ord('q') or k is 27 or k < 0:
			print('Exiting~')
			sys.exit()
		else:
			continue
		break

		

	if imgclass is None:
		print(bad_imgname.split('/')[-1]+" is not annotated!")
		return True

	print( '[%d] %s is class %d' % (imgnum+1, bad_imgname.split('/')[-1], imgclass) )
	annotations[ imgnum ] = imgclass

	#annotef = open( annotations_file, 'ab' )
	#csvwriter = csv.writer( annotef, lineterminator='\n' )
	#csvwriter.writerow( [imgname, imgclass] )
	#annotef.close()
	return True


cv2.namedWindow( 'image', cv2.WINDOW_NORMAL )
cv2.resizeWindow( 'image', 250, 250 )

cv2.namedWindow( 'original_image', cv2.WINDOW_NORMAL )
cv2.resizeWindow('original_image', 250, 250 )

imgnum = 0

for imgname in file_name:

	temp = imgname.split('\n')[0] #2017-12-14-0000...0

	original_image_name = original_image_dir + temp + '.jpg'
	#bad_image_name = bad_image_dir + temp + '_bad.jpg'
	#print image_name

	#skip image
	#if image_name in annotations.keys():
	#	continue
	while not process_image( original_image_name, imgnum ):
		while not process_image( previmage, imgnum-1, True ):
			continue
	#make bad photo
	previmage = original_image_name
	imgnum+=1



for i in range(len(file_name)-1):
	temp = file_name[i]
	image_name = bad_image_dir + temp.split('\n')[0] + '.jpg'

	print i, image_name, annotations[i]
"""
if os.path.exists(image_name):
	im = Image.open(image_name)
	im.show
"""
