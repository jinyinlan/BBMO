import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sys
import os

from PIL import Image

#constant number
NUM_R = 0.299
NUM_G = 0.587
NUM_B = 0.114


#get image
argvs = sys.argv
input_name = argvs[1]

date = input_name[0:10]
"""
bad_image_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/bad_images/'+date+'/'
source_image_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/original_images/'+date+'/'
estimated_image_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/estimated_images/reproductionImages/'
evaluate_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/estimated_images/evaluate/'
"""
bad_image_dir = '/home/omiya/data/Flickr_Interestingness_test/degraded_photos/chosen/'
source_image_dir = '/home/omiya/data/Flickr_Interestingness_test/'+date+'/'
estimated_image_dir = '/home/omiya/data/Flickr_Datasets/temp/estimated_images/reproducedImages/'
evaluate_dir = '/home/omiya/data/Flickr_Datasets/temp/estimated_images/evaluate/'


im_01 = bad_image_dir + input_name + '_bad.jpg'
im_02 = source_image_dir + input_name + '.jpg'


optimizationMethod = 'nm'
im_rs = estimated_image_dir + input_name +  '_new_' + optimizationMethod + '.jpg'

if (os.path.exists(im_01) and os.path.exists(im_rs)):

	print(im_01)
	print(im_02)
	print(im_rs)
	output_name = evaluate_dir + 'result_' + input_name +  '_' + optimizationMethod + '.txt'

	nameR = evaluate_dir + 'graphR_' + input_name +  '_' + optimizationMethod + '.png'
	nameG = evaluate_dir + 'graphG_' + input_name +  '_' + optimizationMethod + '.png'
	nameB = evaluate_dir + 'graphB_' + input_name +  '_' + optimizationMethod + '.png'
	#tone-cuve
	imgArrayX = np.array( Image.open(im_01) )
	imgArrayY = np.array( Image.open(im_02) )
	imgArrayZ = np.array( Image.open(im_rs) )

	#get size
	img_in = Image.open(im_01)
	maxcol , maxrow = img_in.size 


	imgArrayX_R = np.zeros([maxrow,maxcol])
	imgArrayY_R = np.zeros([maxrow,maxcol])
	imgArrayZ_R = np.zeros([maxrow,maxcol])

	imgArrayX_G = np.zeros([maxrow,maxcol])
	imgArrayY_G = np.zeros([maxrow,maxcol])
	imgArrayZ_G = np.zeros([maxrow,maxcol])

	imgArrayX_B = np.zeros([maxrow,maxcol])
	imgArrayY_B = np.zeros([maxrow,maxcol])
	imgArrayZ_B = np.zeros([maxrow,maxcol])

	imgArrayAveX = np.zeros([maxrow,maxcol])
	imgArrayAveY = np.zeros([maxrow,maxcol])
	imgArrayAveZ = np.zeros([maxrow,maxcol])

	difference1 = np.zeros([maxrow,maxcol])
	difference2 = np.zeros([maxrow,maxcol])
	sum_diff1 = 0
	sum_diff2 = 0

	for i in range(maxrow):
		for j in range(maxcol):
			#R
			imgArrayX_R[i, j] = imgArrayX[i, j][0]
			imgArrayY_R[i, j] = imgArrayY[i, j][0]
			imgArrayZ_R[i, j] = imgArrayZ[i, j][0]

			#G
			imgArrayX_G[i, j] = imgArrayX[i, j][1]
			imgArrayY_G[i, j] = imgArrayY[i, j][1]
			imgArrayZ_G[i, j] = imgArrayZ[i, j][1]

			#B
			imgArrayX_B[i, j] = imgArrayX[i, j][2]
			imgArrayY_B[i, j] = imgArrayY[i, j][2]
			imgArrayZ_B[i, j] = imgArrayZ[i, j][2]

			imgArrayAveX[i, j] = imgArrayX_R[i, j]*NUM_R + imgArrayX_G[i, j]*NUM_G + imgArrayX_B[i, j]*NUM_B
			imgArrayAveY[i, j] = imgArrayY_R[i, j]*NUM_R + imgArrayY_G[i, j]*NUM_G + imgArrayY_B[i, j]*NUM_B
			imgArrayAveZ[i, j] = imgArrayZ_R[i, j]*NUM_R + imgArrayZ_G[i, j]*NUM_G + imgArrayZ_B[i, j]*NUM_B

			difference1[i, j] = abs(imgArrayAveY[i, j]-imgArrayAveZ[i, j])
			difference2[i, j] = abs(imgArrayAveY[i, j]-imgArrayAveX[i, j])
			sum_diff1 += difference1[i, j]
			sum_diff2 += difference2[i, j]

	xR = np.reshape(imgArrayX_R, (maxrow*maxcol))
	yR = np.reshape(imgArrayY_R, (maxrow*maxcol))
	zR = np.reshape(imgArrayZ_R, (maxrow*maxcol))

	xG = np.reshape(imgArrayX_G, (maxrow*maxcol))
	yG = np.reshape(imgArrayY_G, (maxrow*maxcol))
	zG = np.reshape(imgArrayZ_G, (maxrow*maxcol))

	xB = np.reshape(imgArrayX_B, (maxrow*maxcol))
	yB = np.reshape(imgArrayY_B, (maxrow*maxcol))
	zB = np.reshape(imgArrayZ_B, (maxrow*maxcol))

	X = np.reshape(imgArrayAveX, (maxrow*maxcol))
	Y = np.reshape(imgArrayAveY, (maxrow*maxcol))
	Z = np.reshape(imgArrayAveZ, (maxrow*maxcol))


	#R
	plt.figure()
	plt.title("x-y tone curve(R)")
	plt.xlabel("input")
	plt.ylabel("output")
	plt.xlim([0,255])
	plt.ylim([0,255])

	#plt.plot(xR, xR, 'k.', label ='original R')
	plt.plot(xR, yR, 'r.',  label ='actual R')
	plt.plot(xR, zR, 'm.', label ='estimated R')

	plt.legend(loc='upper left')
	
	#plt.savefig( nameR )

	#G
	plt.figure()
	plt.title("x-y tone curve(G)")
	plt.xlabel("input")
	plt.ylabel("output")
	plt.xlim([0,255])
	plt.ylim([0,255])

	#plt.plot(xG, xG, 'k.', label ='original G')
	plt.plot(xG, yG, 'g.', label ='actual G')
	plt.plot(xG, zG, 'y.', label ='estimated G')

	plt.legend(loc='upper left')
	
	#plt.savefig( nameG )

	#B
	plt.figure()
	plt.title("x-y tone curve(B)")
	plt.xlabel("input")
	plt.ylabel("output")
	plt.xlim([0,255])
	plt.ylim([0,255])

	#plt.plot(xB, xB, 'k.', label ='original B')
	plt.plot(xB, yB, 'b.', label ='actual B')
	plt.plot(xB, zB, 'c.', label ='estimated B')

	plt.legend(loc='upper left')
	
	#plt.savefig( nameB )


	#result
	ave_diff1 = sum_diff1/(maxrow*maxcol)
	ave_diff2 = sum_diff2/(maxrow*maxcol)
	print( 'Loss (After image - result) : ', ave_diff1 )
	print( 'Loss (After image - Before)  : ', ave_diff2 )

	
	op = open( output_name , 'w')
	op.write(str (ave_diff1))
	op.write('\n')
	op.write(str (ave_diff2))
	

