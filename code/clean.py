import shutil
import os
import time

def cleanFolder(folderName,keep1 = "Input",keep2 = "Output"):
	'''
	first var is the dir, keep the second and third var and delete the rest
	'''
	maindir = os.path.join('.',folderName)
	assert os.path.exists(maindir), "%s does not exists!" %(maindir)
	for file in os.listdir(maindir):
		if file !=keep1 and file!=keep2:
				filePath = os.path.join(maindir,file)
				while os.path.exists(filePath):
					shutil.rmtree(filePath,ignore_errors=True)
					print "deleting %s"%(filePath)
					time.sleep(1)