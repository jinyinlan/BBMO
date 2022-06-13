import numpy as np
import sys
import os.path
import subprocess
from scipy.optimize import minimize
from PIL import Image

import encodeModule_Float2Binary as encodeF2B
import makeXMLfileModule as makeXML

#change here
"""
source_directry_name = '/mnt/data/omiya/omiya_data/flickr_annotated0130/original_images/'
bad_image_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/bad_images/'
estimated_dir = '/mnt/data/omiya/omiya_data/flickr_annotated0130/estimated_images/'
"""
source_directry_name = '/home/omiya/data/Flickr_Interestingness_test/'
bad_image_dir = '/home/omiya/data/test-set0811/small/'
estimated_dir = '/home/omiya/data/test-set0811/temp/'

np.set_printoptions(formatter={'float': '{: 0.4f}'.format})
#initial_param = np.array( [0, 0, 50, 0, -50, 100, 50, 0, 0, 0.5, 1, 1, 1, 25, 0, 0, 0, 0, 1, 1, 1] ) 



def read_param(paramfile_name):
	
	f = open(paramfile_name, 'r')
	initial_param = np.zeros(21)
	default_param = np.array( [0, 0, 50, 0, -50, 100, 50, 0, 0, 0, 1, 1, 1, 25, 0, 0, 0, 0, 1, 1, 1] )

	for input_string in f:

		if input_string.split(' ')[0]=='exposure':
			exposure_black = input_string.split(' ')[2]
			exposure_exposure = input_string.split(' ')[3]

			initial_param[0] = exposure_black
			initial_param[1] = exposure_exposure
		
		if input_string.split(' ')[0]=='shadhi':
			shadhi_shadow = input_string.split(' ')[2]
			shadhi_whitepoint = input_string.split(' ')[3]
			shadhi_highlight = input_string.split(' ')[4]
			shadhi_shadowSat = input_string.split(' ')[5]
			shadhi_highlightSat = input_string.split(' ')[6]

			initial_param[2] = shadhi_shadow
			initial_param[3] = shadhi_whitepoint
			initial_param[4] = shadhi_highlight
			initial_param[5] = shadhi_shadowSat
			initial_param[6] = shadhi_highlightSat			

		if input_string.split(' ')[0]=='colisa':
			colisa_contrast = input_string.split(' ')[2]
			colisa_light = input_string.split(' ')[3]
			colisa_saturation = input_string.split(' ')[4]
			
			initial_param[7] = colisa_contrast
			initial_param[8] = colisa_light
			initial_param[9] = colisa_saturation

		if input_string.split(' ')[0]=='temperature':
			temperature_red = input_string.split(' ')[2]
			temperature_green = input_string.split(' ')[3]
			temperature_blue = input_string.split(' ')[4]
			
			initial_param[10] = temperature_red
			initial_param[11] = temperature_green
			initial_param[12] = temperature_blue

		if input_string.split(' ')[0]=='vibrance':
			vibrance_vibrance = input_string.split(' ')[2]
			
			initial_param[13] = vibrance_vibrance

		if input_string.split(' ')[0]=='colorcorrection':
			colorcorrection_highX = input_string.split(' ')[2]
			colorcorrection_highY = input_string.split(' ')[3]
			colorcorrection_shadX = input_string.split(' ')[4]
			colorcorrection_shadY = input_string.split(' ')[5]
			colorcorrection_saturation = input_string.split(' ')[6]
			
			initial_param[14] = colorcorrection_highX
			initial_param[15] = colorcorrection_highY
			initial_param[16] = colorcorrection_shadX
			initial_param[17] = colorcorrection_shadY
			initial_param[18] = colorcorrection_saturation		

		if input_string.split(' ')[0]=='colorcontrast':
			colorcontrast_GM = input_string.split(' ')[2]
			colorcontrast_BY = input_string.split(' ')[3]
			
			initial_param[19] = colorcontrast_GM
			initial_param[20] = colorcontrast_BY

	f.close()

	initial_param = 2*default_param - initial_param 

	initial_param[0] = np.clip(initial_param[0], -0.1, 0.1) #exposre black
	initial_param[1] = np.clip(initial_param[1], -3, 3) 	#exposre exposure
	initial_param[2] = np.clip(initial_param[2], -100, 100) #shadhi shadow
	initial_param[3] = np.clip(initial_param[3], -10, 10)	#shadhi whitepoint
	initial_param[4] = np.clip(initial_param[4], -100, 100) #shadhi highlight
	initial_param[5] = np.clip(initial_param[5], 0, 100)	#shadhi shadowsaturation
	initial_param[6] = np.clip(initial_param[6], 0, 100)	#shadhi highlightsaturation
	initial_param[7] = np.clip(initial_param[7], -1, 1)		#colisa contrast
	initial_param[8] = np.clip(initial_param[8], -1, 1)		#colisa lightness
	initial_param[9] = np.clip(initial_param[9], -1, 1)		#colisa saturation
	initial_param[10] = np.clip(initial_param[10], 0, 8)	#temperature R
	initial_param[11] = np.clip(initial_param[11], 0, 8)	#temperature G
	initial_param[12] = np.clip(initial_param[12], 0, 8)	#temperature B
	initial_param[13] = np.clip(initial_param[13], 0, 100)	#vibrance vibrance
	initial_param[14] = np.clip(initial_param[14], -40, 40)	#colorcorrection highlightX
	initial_param[15] = np.clip(initial_param[15], -40, 40)	#colorcorrection highlightY
	initial_param[16] = np.clip(initial_param[16], -40, 40)	#colorcorrection shadowX
	initial_param[17] = np.clip(initial_param[17], -40, 40)	#colorcorrection shadowY
	initial_param[18] = np.clip(initial_param[18], -3, 3)	#colorcorrection saturation
	initial_param[19] = np.clip(initial_param[19], 0, 5)	#colorcontrast GM
	initial_param[20] = np.clip(initial_param[20], 0, 5)	#colorcontrast BY

	return initial_param


def make_parameter_file(parameter):

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

def objectFunc(parameter): # x=original image, z=target image

	make_parameter_file(parameter)
	#print 'made parameter file'
	encodeF2B.encode_f2b(paramfile_name, XMPdataFile_name)
	#print 'encoded'
	makeXML.makeXMP_file(input_imX, XMPdataFile_name, xmpfile_name)
	#print 'made xmpFile'

	#commands.getoutput('mv '+output_imY+' '+output_prev)
	if os.path.exists( output_imY ):
		subprocess.call( ['mv', output_imY, output_prev] )
	#tempImage = commands.getoutput('darktable-cli '+input_imX+' '+xmpfile_name+' '+output_imY+' --hq false')
	subprocess.call( ['darktable-cli', input_imX, xmpfile_name, output_imY, '--hq false'] )

	return np.array( Image.open( output_imY ) ).astype(np.float64)/255.0
	


def lossNM(parameter):
	#print( np.mean( np.power( z-objectFunc(parameter), 2 ) ), parameter )
	
	return  np.mean( np.power( z-objectFunc(parameter), 2 ) )
	

if __name__ == '__main__':
	
	argvs = sys.argv
	input_name = argvs[1] #2017-10-20-***
	#input file
	input_imZ = source_directry_name + input_name[:10] + '/' + input_name + '.jpg'
	input_imX = bad_image_dir + input_name +'_bad.jpg'
	original_param = bad_image_dir + input_name +'_parameter_bad.txt'

	#output file
	paramfile_name = estimated_dir + 'parameters/' + input_name +'_parameter_nm.txt'
	XMPdataFile_name = estimated_dir + 'xmpFiles/' + input_name +'_tempXMPdata_nm.txt'
	xmpfile_name = estimated_dir + 'xmpFiles/' + input_name +'_nm.xmp'
	output_imY = estimated_dir + 'reproducedImages/' + input_name + '_new_nm.jpg'
	output_prev = estimated_dir + 'reproducedImages/' + input_name +'_prev_nm.jpg'
	

	if os.path.isfile(input_imX) and os.path.isfile(input_imZ):

		print( input_imX )
		print( input_imZ )
		"""
		print( paramfile_name )
		print(XMPdataFile_name)
		print(xmpfile_name)
		print(output_imY)
		print(original_param)
		"""

		#initial_param = read_param( original_param )  #use degraded params
		initial_param = np.array( [0, 0, 50, 0, -50, 100, 50, 0, 0, 0.5, 1, 1, 1, 25, 0, 0, 0, 0, 1, 1, 1] ) 
		print( initial_param )

		#get image
		x = np.array( Image.open( input_imX ) ).astype(np.float64)/255.0
		z = np.array( Image.open( input_imZ ) ).astype(np.float64)/255.0
		
		#optimized_param = minimize( lossNM, initial_param, method='Nelder-Mead', tol=1.0e-4,  options={'disp': True, 'maxiter': 700, 'maxfev':650}) # 'fatol': 0.0001
		optimized_param = minimize( lossNM, initial_param, method='Nelder-Mead', tol=1.0e-6,  options={'disp': True, 'maxiter': 700, 'maxfev':650}) # 'fatol': 0.0001
		

		#make new image
		objectFunc(optimized_param.x)
		#commands.getoutput('rm '+output_prev)
		subprocess.call( ['rm', output_prev] )
	elif os.path.isfile(input_imZ):
		print( input_imX, 'is not exist.' )
	else:
		print( input_imZ, 'is not exist.' )

	