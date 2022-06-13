1
@nico
get_from_FlickrInterestingness$ python2 flickrAPI.py 2017-08-01

2
@nico
degrade_photos$ bash degrade_photos.sh 2017-08-01

3
@nico
scp /home/omiya/data/Flickr_Interestingness_test/degraded_photos/temp/2017-08-01* ipanema:/home/omiya/data/Flickr_Interestingness_test/degraded_photos/temp/
scp -r /home/omiya/data/Flickr_Interestingness_test/2017-08-01/ ipanema:/home/omiya/data/Flickr_Interestingness_test/

@ipanema
choose_degraded_photos$ python main-test.py test --savedir /home/omiya/data/Flickr_Interestingness_test/ --datedir 2017-08-01
choose_degraded_photos$ python thresholding.py /home/omiya/data/Flickr_Interestingness_test/ 2017-08-01

@nico
scp ipanema:/home/omiya/data/Flickr_Interestingness_test/2017-08-01/chosen_photos_2017-08-01_2.5.txt /home/omiya/data/Flickr_Interestingness_test/2017-08-01/
scp ipanema:/home/omiya/data/Flickr_Interestingness_test/2017-08-01/chosen_photos_2017-08-01.txt /home/omiya/data/Flickr_Interestingness_test/2017-08-01/

choose_degraded_photos$ bash choose_degraded_photos.sh 2017-08-01

4
@nico
scp /home/omiya/data/Flickr_Interestingness_test/degraded_photos/chosen/2017-08-01* jumeirah:/home/omiya/data/Flickr_Interestingness_test/degraded_photos/chosen/
scp -r /home/omiya/data/Flickr_Interestingness_test/2017-08-01/ jumeirah:/home/omiya/data/Flickr_Interestingness_test/

@jumeirah
calculate_parameters$bash makeDatasetNM2.sh 2017-08-01

@nico
(scp -r jumeirah:/home/omiya/data/Flickr_Datasets/temp/ /home/omiya/data/Flickr_Datasets/)
calculate_parameters$python2 choose_targetImages.py 2017-08-01


=====reuse=====
2
@nico
degrade_photos$ bash degrade_photos2.sh 2017-08-01

3
@ipanema
~/data/Flickr_Interestingness_test/degraded_photos/temp$ rm  2017-08-01*
@nico
scp /home/omiya/data/Flickr_Interestingness_test/degraded_photos/temp/2017-08-01* ipanema:/home/omiya/data/Flickr_Interestingness_test/degraded_photos/temp/
scp /home/omiya/data/Flickr_Interestingness_test/2017-08-01/all_bad_file_name.txt ipanema:/home/omiya/data/Flickr_Interestingness_test/2017-08-01/

@ipanema
choose_degraded_photos$ python main-test.py test –savedir /home/omiya/data/Flickr_Interestingness_test/ –datedir 2017-08-01
choose_degraded_photos$ python thresholding.py /home/omiya/data/Flickr_Interestingness_test/ 2017-08-01

@nico
scp ipanema:/home/omiya/data/Flickr_Interestingness_test/2017-08-01/chosen_photos_2017-08-01_2.5.txt /home/omiya/data/Flickr_Interestingness_test/2017-08-01/
scp ipanema:/home/omiya/data/Flickr_Interestingness_test/2017-08-01/chosen_photos_2017-08-01.txt /home/omiya/data/Flickr_Interestingness_test/2017-08-01/

choose_degraded_photos$ bash choose_degraded_photos2.sh 2017-08-01

4
@nico
scp /home/omiya/data/Flickr_Interestingness_test/degraded_photos/chosen/2017-08-01* jumeirah:/home/omiya/data/Flickr_Interestingness_test/degraded_photos/chosen/
scp /home/omiya/data/Flickr_Interestingness_test/2017-08-01/temp_file_name.txt jumeirah:/home/omiya/data/Flickr_Interestingness_test/2017-08-01/

@jumeirah
calculate_parameters$bash makeDatasetNM2.sh 2017-08-01

@nico
(scp -r jumeirah:/home/omiya/data/Flickr_Datasets/temp/ /home/omiya/data/Flickr_Datasets/)
calculate_parameters$python2 choose_targetImages.py 2017-08-01
