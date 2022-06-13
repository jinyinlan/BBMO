import os
import commands

import encodeModule_Float2Binary_5 as encodeF2B
import makeXMLfileModule_5 as makeXML
#python2

DataDir = '/home/omiya/data/test-set0811/'
smallDataDir = '/home/omiya/data/test-set0811/small-val/'

with open( smallDataDir+'all_bad_file_name.txt', 'r') as f:
	file_name = f.readlines()

#print( file_name )
#print( len(file_name) )

for f in file_name:
	temp = f.split('\n')[0]
	original_big_file = DataDir + f[:10] + '/' + temp + '.jpg'
	degraded_big_file = DataDir + 'degraded-val/' + temp + '_bad.jpg'
	bad_param_file = smallDataDir + temp + '_parameter_bad.txt'
	XMPdataFile_name = smallDataDir + temp + '_tempXMPdata_bad.txt'
	bad_param_xmp = smallDataDir + temp + '_bad.xmp'

	#txt -> xmp
	if os.path.exists(bad_param_file):
		encodeF2B.encode_f2b( bad_param_file, XMPdataFile_name )
		makeXML.makeXMP_file( original_big_file, XMPdataFile_name, bad_param_xmp)
		commands.getoutput('darktable-cli '+original_big_file+' '+bad_param_xmp+' '+degraded_big_file)
	else:
		print(bad_param_file, 'is not exists.')
