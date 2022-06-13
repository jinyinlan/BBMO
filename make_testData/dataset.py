import torch
import numpy as np
import pandas as pd
import os
#from skimage import io

from PIL import Image
from torch.utils.data import Dataset
#from scaling import scaling, descaling
#from normalize import normalize

def load_image(file):
	return Image.open(file)


"""
class FiveK(Dataset): #MIT-FiveK dataset (c)

	def __init__(self, csv_file, root, input_transform=None, mode='train'):

		self.root_dir = root
		self.csv_file = os.path.join(root, csv_file)
		self.enhance_param_frame = pd.read_csv(self.csv_file)
		self.mode = mode
		
		self.input_transform = input_transform

	def __getitem__(self, index):
		
		img_name = str(self.root_dir)+'/'+str(self.enhance_param_frame.ix[index, 0])+'-s.png'
		#print img_name
		
		with open(img_name, 'rb') as f:
			image = load_image(f).convert('RGB')

		if self.mode == 'train' or self.mode == 'val':
			enhance_param = self.enhance_param_frame.ix[index, 1:].as_matrix().astype('float')
			#enhance_param = scaling(enhance_param)
			
			#enhance_param = normalize(enhance_param)
			#print('normalized param:'+str(enhance_param))
			
			enhance_param = torch.from_numpy(enhance_param).float() #ndarray -> tensor
			#print enhance_param

		#width, height = image.size

		
		if self.input_transform is not None:
			#print 'self.transform is not None'
			image = self.input_transform(image)

		if self.mode == 'test':
			enhance_param = []

		#print(image.size())
		if self.mode == 'train':
			return image, enhance_param
		else: #val or test
			fileName0 = img_name.split('/')[-1]
			fileName = fileName0[:5]
			return image, enhance_param, fileName


		

	def __len__(self): #the size of the dataset
		return len(self.enhance_param_frame)

class FlickrInteresting(Dataset): #flickr dataset

	def __init__(self, csv_file, root, input_transform, mode='train'):

		self.root_dir = root
		self.csv_file = os.path.join(root, csv_file)
		#self.enhance_param_frame = pd.read_csv(self.csv_file)
		self.annotated_class_frame = pd.read_csv(self.csv_file)
		self.mode = mode
		
		self.input_transform = input_transform

	def __getitem__(self, index):
		
		#img_name = str(self.root_dir)+'/'+str(self.enhance_param_frame.ix[index, 0])+'-s.png'
		#img_name = str(self.root_dir)+'/'+str(self.enhance_param_frame.ix[index, 0])
		bad_img_name = str(self.root_dir)+'/'+str(self.annotated_class_frame.ix[index, 0]) #bad img
		print( bad_img_name )
		
		with open(bad_img_name, 'rb') as f:
			bad_image = load_image(f).convert('RGB')
		with open(orig_img_name, 'rb') as f:
			orig_image = load_image(f).convert('RGB')

		if self.mode == 'train' or self.mode == 'val':

			annotated_class = self.annotated_class_frame.ix[index, 1].astype('int') #numpy.int64
			#print (annotated_class, type(annotated_class))
			annotated_class = int(annotated_class) #numpy.int64 -> int
			#print (annotated_class, type(annotated_class))
			annotated_class = torch.IntTensor( [annotated_class ]) # int -> torch.IntTensor
			#print (annotated_class, type(annotated_class))

			

		bad_image = self.input_transform(image)

		if self.mode == 'test':
			#enhance_param = []
			annotated_class = []

		#print(image.size())
		if self.mode == 'train':
			return bad_image, annotated_class
		else: #val or test
			fileName0 = bad_img_name.split('/')[-1]
			#fileName = fileName0[:5]
			fileName = fileName0
			return bad_image, annotated_class, fileName


		

	def __len__(self): #the size of the dataset
		return len(self.annotated_class_frame)
"""

class FlickrInterestingDouble(Dataset): #flickr dataset original image & bad image

	def __init__(self, txt_file, root, datedir, input_bad_transform, input_orig_transform, mode='train'):
		print('FlickrInterestingDouble')

		self.root_dir = root
		self.datedir = datedir
		self.txt_file = os.path.join(root, datedir, txt_file)
		#self.enhance_param_frame = pd.read_csv(self.csv_file)
		with open(self.txt_file, 'r') as file:
			self.image_files = file.readlines()

		self.mode = mode
		
		self.input_bad_transform = input_bad_transform
		self.input_orig_transform = input_orig_transform

	def __getitem__(self, index):
		
		#img_name = str(self.root_dir)+'/'+str(self.enhance_param_frame.ix[index, 0])+'-s.png'
		#img_name = str(self.root_dir)+'/'+str(self.enhance_param_frame.ix[index, 0])

		temp_img = str(self.image_files[index]).split('\n')[0]
		bad_img_name = str(self.root_dir)+'degraded_photos/temp/'+temp_img #bad img
		orig_img_name = str(self.root_dir)+str(self.datedir)+'/'+temp_img.split("_bad.jpg")[0]+'.jpg'  #original img
		print(temp_img, bad_img_name, orig_img_name)
		with open(bad_img_name, 'rb') as f:
			bad_image = load_image(f).convert('RGB')
		with open(orig_img_name, 'rb') as f:
			orig_image = load_image(f).convert('RGB')

		bad_image = self.input_bad_transform(bad_image)
		orig_image = self.input_orig_transform(orig_image)
		
		if self.mode == 'test':
			annotated_class = []

		images = [ bad_image, orig_image ]

		fileName = bad_img_name.split('/')[-1]
		return images, annotated_class, fileName


	def __len__(self): #the size of the dataset
		return len(self.image_files)

