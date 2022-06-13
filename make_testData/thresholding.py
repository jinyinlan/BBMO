import sys
"""
directry = sys.argv[1]
iteration = sys.argv[2]
threshold = float(sys.argv[3])
"""
directry = sys.argv[1]
date = sys.argv[2]
iteration = '47500'
threshold = 2.5

datedir = directry+date

original_file_name = datedir+'/chosen_photos_'+date+'.txt'
output_file_name = datedir+'/chosen_photos_'+date+'_'+str(threshold)+'.txt'

print (original_file_name, output_file_name)

original_file = open( original_file_name, 'r')
lines = original_file.readlines()
original_file.close()


file_names = []
output_result = []

for i in range(len(lines)):
	

	file_name, output_float = lines[i].split(' ')
	output_float = float(output_float)

	if (output_float>threshold):
		output_int = 1
	else:
		output_int = 0
		
	print( file_name+' '+str(output_int))
	file_names.append(file_name)
	output_result.append(output_int)

resultFile = open( output_file_name, 'w')
"""
resultFile.write('threshold:'+str(threshold)+'\n')

resultFile.write('--------------------------------\n')
resultFile.write("file_name output\n")
"""
for i in range(len(output_result)):
	resultFile.write(file_names[i]+' '+str(output_result[i])+'\n')
resultFile.close()