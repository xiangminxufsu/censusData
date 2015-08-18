#preprocess file including unzip
import os
import zipfile
import logging
from distutils.dir_util import copy_tree
import shutilimport time

directory = r'C:\\Users\\GIS_tech\\Desktop\\66county' #main dir
unzipdir = os.path.join(directory,'source1') #zip file source
unzipdes = os.path.join(directory,'extracted')#r'C:\\Users\\GIS_tech\\Desktop\\66county\\extracted' #unzip dir
sampledir = os.path.join(directory,"sample")


def unzip(directory,subdir,desdir):
  
    logging.basicConfig(filename = 'log.log',format = '%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    #print directory
    assert os.path.exists(directory), "%s not exists!"%(directory)
    assert os.path.exists(subdir), "%s not exists!"%(directory)
    
    if not os.path.exists(desdir):
        logging.warning("folder %s not exists, we are making one now" %desdir)
        os.mkdir(desdir)
        
    logging.info("paths checked, now start unzip")   
    for x in os.listdir(subdir):
        xdir = os.path.join(subdir,x)

        if "._" in x: #shadow file from osx no need to process
            print  "find useless file",x
            continue
            
        fh = open(xdir,'rb')
        z = zipfile.ZipFile(fh)
        newdir = os.path.join(desdir,"biu_"+x)
        #print newdir
        os.mkdir(newdir)
        for name in z.namelist():
            z.extract(name,newdir)
        fh.close()
    logging.info("unzip completed, have a great day!")
	
	
def checkdata(Directory,SampleDir,CmpDir):
    #check have same attributes
	assert os.path.exists(SampleDir), "%s not exists!"%(SampleDir)
	
	for x in os.listdir(SampleDir):
		if "metadata" in x:
            #print x
			for folder in os.listdir(CmpDir):
                #print folder
				cur_dir = os.path.join(CmpDir,folder)
				#print cur_dir
				file = os.path.join(cur_dir,x)
				assert os.path.exists(file), file
                #f=open(file,'rb')
                #print f
	print "GOOD"

    #check no duplicated counties
	first_list = []
	for county in os.listdir(CmpDir):

		cur_dir = os.path.join(CmpDir,county+'\\DEC_10_SF1_H1_with_ann.csv')
		assert os.path.exists(cur_dir),cur_dir
		cur_f = open(cur_dir,'rb')
		cur_f.readline()
		cur_f.readline()
		line = cur_f.readline()
		if line in first_list:
			raise Exception(line,CmpDir)
		else:
			first_list.append(line)
		cur_f.close()
		
def createSample(sampledir,unzipdes):
	"""
	create tempararly and will be deleted later
	"""
	assert not os.path.exists(sampledir), "%s already exists!" %(sampledir)
	assert os.path.exists(unzipdes), "could not find %s"%(unzipdes)
	os.makedirs(sampledir)
	for x in os.listdir(unzipdes):
		ori_path = os.path.join(unzipdes,x)
		copy_tree(ori_path,sampledir)
		break


def main():
	unzip(directory,unzipdir,unzipdes)
	createSample(sampledir,unzipdes)
	checkdata(directory,sampledir,unzipdes)	time.sleep(5)
	shutil.rmtree(sampledir)
	
	
main()