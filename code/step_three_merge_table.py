"""
simple script
merge all files under dir into one, all files have the same row length and append them by row.
Created by Xiangmin Xu

"""

import os
from os.path import join,isfile
import logging
import time
import shutil

def merge_table_main(folder):
	print "merging table started"
	logging.basicConfig(filename = 'log.log',format = '%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
	logging.info('merge started')
	main_dir = os.path.join('.',folder)
	path = os.path.join(main_dir,'FiltedAnnFile')#r'C:\\Users\\gstrode\\censusData\\FiltedAnnFile'
	destination = os.path.join(main_dir,"Output")#r'C:\\Users\\gstrode\\censusData'
    
	assert os.path.exists(destination)
	assert os.path.exists(path), "Could not find %s !!!" % path
    
	files = os.listdir(path)
	
	#print file orders 
	ordered_file_path = os.path.join(folder,"file_orders")
	ordered_file = open(ordered_file_path,"wb")
	for x in files:
		ordered_file.write(x+"\r\n")
	ordered_file.close()
	
	files = [join(path,x) for x in files if 'ann.csv' in x]
	#print files
    
	length = 0
	for x in open(files[0]):
		length+=1
        
    #print length
	results = [open(f) for  f in files]
    #print results

	with open(join(destination,"final.csv"),"wb") as des:

		for x in range(0,length):
			iterator = (f.readline().strip('\r\n') for f in results)
			newline = ','.join(iterator)
			des.write(newline+'\r\n')
	print "merging table complete"    
#mergefile()

    

