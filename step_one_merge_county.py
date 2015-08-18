# merge files into one

import os
import shutil
from distutils.dir_util import copy_tree
#config


desdir = r'C:\\Users\\GIS_tech\\Desktop\\66county\\changeMetaDataHere'
targetdir = r'C:\\Users\\GIS_tech\\Desktop\\66county\\extracted'
maindir = r'C:\\Users\\GIS_tech\\Desktop\\66county'
sampledir = os.path.join(maindir,"SampleToMerge")

def createSample(targetdir,maindir,sampledir):
	rt = None
	cur_dir = None
	assert not os.path.exists(sampledir), "%s already exists!" %(sampledir)
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
	if not os.path.exists(desdir):
		os.makedirs(desdir)
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
					if tarf == 'aff_download (1).zip':
						print tarf, "find dup"
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
			
samplefolder = createSample(targetdir,maindir,sampledir)
mergeSameName(samplefolder,desdir,targetdir)
shutil.rmtree(sampledir)