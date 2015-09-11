#09/02/2015

import os
import time
import zipfile
from code.pre_process import pre_Process_main
from code.step_one_merge_county import merge_main
from code.step_two_filter_ann import filter_main
from code.step_three_merge_table import merge_table_main
from code.unzip_filter import unziped_filter_main
from code.clean import cleanFolder

def ProcessZip(folder):
	pre_Process_main(folder)
	merge_main(folder)
	
	condition = raw_input("Do you want to change metadata in order to filter tables? (Y/N)  ")
	if condition.lower() == 'y' or condition.lower() == 'yes':
		print "Now please change the metadat..."
		stopsign = None
		while stopsign == None:
			stopsign = raw_input("Press any key when you are ready...")
			time.sleep(1)
		print "Key is caught and start processing modified file..."
	else:
		time.sleep(1)
		print "You don't want to change so nothing will be changed..."
		
	filter_main(folder)
	merge_table_main(folder)
	pass
def ProcessUnzip(folder):
	unziped_filter_main(folder)
	merge_table_main(folder)
	pass

#finding folders
#folders contains input folder, input folder contains files to be processed
while True:
	folder = raw_input("Please input the folders you want to process:\r\n")
	if os.path.exists('.\\'+folder):
		print folder,"found, good!"
		break
	else:
		print "Folder not found!"

#write folder name into a temfile	
'''	
temfile = open('folderInfo','wb')
temfile.write(folder)
temfile.close()
'''

folderPath = os.path.join('.',folder)
inputPath = os.path.join(folder,'Input')
outPath = os.path.join(folder,'Output')

assert os.path.exists(inputPath),\
"Please make sure you have a folder named Input and put the original files into it!"
if not os.path.exists(outPath):
	os.mkdir(outPath)

#make sure the Input folder has files
assert os.listdir(inputPath)!=[], "the Input folder is empty, please put zipped files into it"	

for x in os.listdir(inputPath):
	filePath = os.path.join(inputPath,x)
	
	if zipfile.is_zipfile(filePath):
		ProcessZip(folder)
		#print "We are prosessing",filePath
	else:
		ProcessUnzip(folder)
		print filePath,'no'
	cleanFolder(folder,"Input","Output")
	break
