#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from retry import retry
import requests
import xml.dom.minidom as md
import time
import os
import sys

# set these here or using flickr.API_KEY in your application
API_KEY = 'c125873b4163face79644e6ceea77af5'
API_SECRET = '264c6e310beb398e'
#IMG_FOLDER = '/home/omiya/data/1214/'
#moakane14@yahoo.co.jp

class Flickr(object):
	u"""
	基本的な使い方

	# 適宜修正してください
	api_key = 'ENTER_YOUR_API_KEY'

	f = Flickr(api_key)

	# pyconjpのuser_id
	print(f.get_photoset_ids_from_user_id('102063383@N02'))
	# PyCon JP 2014 day4 Sprintフォトセットのphotoset_id
	print(f.get_photos_from_photoset_id('72157647739640505'))
	# 上記フォトセットの中の写真のひとつ
	print(f.get_url_from_photo_id('15274792845'))
	"""

	def __init__(self, api_key):
		self.api_url = 'https://api.flickr.com/services/rest/'
		self.api_key = api_key
	"""
	def get_photoset_ids_from_user_id(self, user_id):
		u
		# requestの送信
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.photosets.getList',
										 'user_id': user_id
										 })		

		# xmlをパースしてdomオブジェクトにする
		dom = md.parseString(r.text.encode('utf-8'))

		# domオブジェクトからphotoset_idを探し出す
		result = []		
		for elem in dom.getElementsByTagName('photoset'):
			result.append(elem.getAttribute('id'))			
		return result
	
	def get_photos_from_photoset_id(self, photoset_id):
		u
		
		# requestの送信
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.photosets.getPhotos',
										 'photoset_id': photoset_id
										 })  

		# xmlをパースしてdomオブジェクトにする
		dom = md.parseString(r.text.encode('utf-8'))

		# domオブジェクトからphoto_idを探し出す
		result = []
		for elem in dom.getElementsByTagName('photo'):
			result.append(elem.getAttribute('id'))			
		return result
	"""
	def get_interestingness_photos_id(self, date):
		u"""
		dateの写真一覧(interestingness_photosのリスト)を返す
		"""
		# requestの送信
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.interestingness.getList',
										 'date': date ,
										 'per_page': '500'
										 })  

		# xmlをパースしてdomオブジェクトにする
		dom = md.parseString(r.text.encode('utf-8'))

		# domオブジェクトからphoto_idを探し出す
		result = []
		for elem in dom.getElementsByTagName('photo'):
			result.append(elem.getAttribute('id'))			
		return result

	@retry(tries=4, delay=5, backoff=2)
	def get_url_from_photo_id(self, photo_id):
		
		u"""
		写真(photo_id)が実際に格納されているURLを返す
		"""
		# requestの送信
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.photos.getSizes',
										 'photo_id': photo_id
										 })		

		# xmlをパースしてdomオブジェクトにする
		dom = md.parseString(r.text.encode('utf-8'))
		
		# domオブジェクトからURLを探し出す
		result = None
		for elem in dom.getElementsByTagName('size'):
			# largeのサイズのもののみにする
			if elem.getAttribute('label') == 'Large':
				result = elem.getAttribute('source')
				# small他はスキップ
				break
			else:
				# 何もない場合はNone
				pass
		print('id :', photo_id, 'url:', result)
		return result

	@retry(tries=4, delay=5, backoff=2)
	def check_tags(self, photo_id):
		r = requests.post(self.api_url, {'api_key': self.api_key,
										 'method': 'flickr.tags.getListPhoto',
										 'photo_id': photo_id
										 })	

		dom = md.parseString(r.text.encode('utf-8'))
		result = False
		for elem in dom.getElementsByTagName('tag'):
			# smallのサイズのもののみにする
			if elem.getAttribute('raw') == 'blackandwhite':
				result = True
			elif elem.getAttribute('raw') == 'black and white':
				result = True
			elif elem.getAttribute('raw') == 'b&w':
				result = True
			elif elem.getAttribute('raw') == 'BW':
				result = True
			elif elem.getAttribute('raw') == 'bw':
				result = True
			elif elem.getAttribute('raw') == 'Black & White':
				result = True
			elif elem.getAttribute('raw') == 'B&W':
				result = True
			elif elem.getAttribute('raw') == 'Mono':
				result = True
			elif elem.getAttribute('raw') == 'monochrome':
				result = True
			else:
				# 何もない場合はNone
				pass
		return result		

"""
def download_images(url_list, id_list, photo_date):
	savedir = '/home/omiya/data/flickr_interestingness/'+photo_date+'/'
	if not os.path.exists(savedir):
		os.mkdir(savedir)

	file_name = ['']*len(url_list)
	for i in range(len(url_list)):
		time.sleep(0.5)
		file_name[i] = savedir+photo_date+'-'+id_list[i]+'.jpg'
		r = requests.get(url_list[i])
		#print(file_name[i])
		#save file
		if r.status_code == 200:
			f = open(file_name[i], 'w')
			f.write(r.content)
			f.close()
"""
@retry(tries=4, delay=5, backoff=2)
def download_image(photo_url, photo_id, photo_date):
	savedir = '/home/omiya/data/test-set0811/'+photo_date+'/'
	if not os.path.exists(savedir):
		os.mkdir(savedir)

	file_name = savedir+photo_date+'-'+photo_id+'.jpg'
	r = requests.get(photo_url)
	#save file
	if r.status_code == 200:
		f = open(file_name, 'w')
		f.write(r.content)
		f.close()


if __name__ == '__main__':
	# 動作確認

	# 適宜修正してください
	api_key = API_KEY

	argvs = sys.argv
	photo_date = argvs[1]
	#photo_date = '2017-12-13'

	all_photos_name = ['']

	f = Flickr(api_key)
	
	id_list = f.get_interestingness_photos_id(photo_date)
	#print(id_list)

	size = len(id_list)
	print(size)
	url_list = ['']*size
	for i in range(size):
		#print(i, id_list[i], end=" ")
		url_list[i] = f.get_url_from_photo_id(id_list[i])
		#print(url_list[i])
	print('url list finished')
	
	#url_list = [ 'https://farm5.staticflickr.com/4569/38337389574_1ee1064129_m.jpg', 'https://farm5.staticflickr.com/4730/38344106814_fe2b4be110_m.jpg']
	#id_list = [ '38337389574', '38344106814']
	
	#download_images(url_list, id_list, photo_date)

	for i in range(size):
		if not(f.check_tags(id_list[i])):
			#print(id_list[i], url_list[i])
			if (url_list[i]):
				download_image(url_list[i], id_list[i], photo_date)
				all_photos_name.append(photo_date+'-'+id_list[i])
			else:#url_list=None
				print(id_list[i], ': url is None.')
						
			time.sleep(0.5)
		else:
			print(id_list[i], 'blackwhite: not saved')
		

	with open( '/home/omiya/data/test-set0811/'+photo_date+'/all_file_name.txt', 'w' ) as file:
		for f in all_photos_name:
			file.write( f+'\n')