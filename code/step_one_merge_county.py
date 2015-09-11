# merge files into one

import os
import shutil
from distutils.dir_util import copy_tree
import time
#config


def createSample(targetdir,maindir,sampledir):
	rt = None
	cur_dir = None
	
	#check if already exists
	if os.path.exists(sampledir):
		print "%s already exists, now delete it and make a new one" %(sampledir)
		shutil.rmtree(sampledir)
		 
	os.makedirs(sampledir)
	for folder in os.listdir(targetdir):
		cur_dir = os.path.join(targetdir,folder)
		tar_dir = os.path.join(sampledir,folder)
		os.makedirs(tar_dir)
		copy_tree(cur_dir,tar_dir)
		rt = os.path.join(sampledir,folder)
		break
	return rt	
			
def mergeSameName(sampledir,desdir,targetdir):
	sample_Name = os.path.basename(os.path.normpath(sampledir))
	print "sample_Name", sample_Name
	while os.path.exists(desdir):
		shutil.rmtree(desdir,ignore_errors = True)
		print "deleting previous %s files" %(desdir)
		time.sleep(1)
	os.mkdir(desdir)
	print "creating changeMetaDataHere folder..."
	for files in os.listdir(sampledir):
		#print files
		if "with_ann.csv" in files:
			samplef = os.path.join(sampledir,files)
			desf = os.path.join(desdir,files)
			
			df = open(desf,'wb')
			with open(samplef,'rb') as sf:
				for line in sf:
					df.write(line)
				
				for tarf in os.listdir(targetdir):
					if tarf == sample_Name:
						#print tarf, "find dup and jump"
						continue #same file already being written
					else:
						tf = os.path.join(targetdir,tarf)
						tf = os.path.join(tf,files)
						#print tf
						assert os.path.exists(tf)
						with open(tf,'rb') as ff:
							ff.next()
							ff.next()
							for row in ff:
								df.write(row)
						
			df.close()
		elif 'metadata.csv' in files:
			desf = os.path.join(desdir,files)
			samplef = os.path.join(sampledir,files)
			df = open(desf,'wb')
			sf = open(samplef,'rb')
			for line in sf:
				df.write(line)
			sf.close()
			df.close()
			#print files
	print "county merge complete..."
		
def merge_main(folder):
	maindir = os.path.join(".",folder)#r'C:\\Users\\gstrode\\censusData'
	assert os.path.exists(maindir),"Unable to find dir %s" %s(maindir)
	targetdir = os.path.join(maindir,"extracted")
	sampledir = os.path.join(maindir,"SampleToMerge")
	desdir = os.path.join(maindir,"changeMetaDataHere")
	pass
	samplefolder = createSample(targetdir,maindir,sampledir)
	mergeSameName(samplefolder,desdir,targetdir)
	#delete sample folder and extracted folder
	shutil.rmtree(sampledir,ignore_errors = True)
	shutil.rmtree(targetdir,ignore_errors = True)