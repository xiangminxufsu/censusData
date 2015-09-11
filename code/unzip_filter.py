#created by Xiangmin Xu to process census data
import os
import re
import logging
import shutil
import time
#newdirectory = r'C:\\Users\\gstrode\\censusData\\FiltedAnnFile'
#directory = r'C:\\Users\\gstrode\\censusData\\changeMetaDatahere'

def handler(outf,annf,metaf):
    #print annf.readline()
    #get head from annf
	annf.readline() #first line is useless
	headlist = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', annf.readline())
	headlist=map(lambda x:x.strip(),headlist)
    #print headlist
    
    #match metadata with head ang put index into indexlist
	indexlist = []
	outheadlist = []
	modifiedhead = []
	for x in metaf:
		try:
			meta = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', x)[1] #use the second one to match
			outheadlist.append(meta)
			try:
				newmata = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', x)[2]
				#print re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', x),newmata
				modifiedhead.append(newmata)
				print "modified name %s found, using new name..." %(newmata)
			except Exception:
				modifiedhead.append(meta)
		except IndexError:
			print "I am here"
			raise("can not process s%: ",x)
        
		try:
            #print x, headlist.index(x)
			indexlist.append(headlist.index(meta))
		except ValueError:
			logging.error("this line processed uncorrect.\n line:{0}\n matched:{1}".format(meta,headlist))
			raise ValueError("could not find {0} in the".format(meta),headlist) 
    
    #write into newfiles:
	if len(modifiedhead)==0:
		outf.write((','.join(outheadlist)+'\r\n'))
	else:
		outf.write((','.join(modifiedhead)+'\r\n'))
	
	for line in annf:
		matched = re.findall(r'(?:[^\r\n,"]|"(?:\\.|[^"])*")+', line)
        #print matched
        #print indexlist
        #print headlist
		try:
			assert len(matched) == len(headlist)
		except AssertionError:
			logging.error("this line processed uncorrect.\n line:{0}\n matched:{1}".format(line,matched))
		writelist = []
		for i in indexlist:
            #print matched[int(i)]
			try:
				writelist.append(matched[int(i)])
			except IndexError:
				raise("find uncorrect mapping between mataf and annf")
		outf.write(','.join(writelist)+'\r\n')
        #break
    
def unziped_filter_main(maindir):
	print "filter_start"
	maindir = os.path.join('.',maindir)
	newdirectory = os.path.join(maindir,"FiltedAnnFile")#r'C:\\Users\\gstrode\\censusData\\FiltedAnnFile'
	directory = os.path.join(maindir,"Input")#r'C:\\Users\\gstrode\\censusData\\changeMetaDatahere'
	logging.basicConfig(filename = 'log.log',format = '%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
	logging.info('start running')
	while os.path.exists(newdirectory):
		shutil.rmtree(newdirectory,ignore_errors = True)
		print "deleting previous %s" % (newdirectory)
		time.sleep(1)
	os.makedirs(newdirectory)
    #logging.debug('looks good')   
	for filename in os.listdir(directory):
        #get the needed files _with_ann and find the matching metadata
		if filename.split('.')[-1] == 'csv' and not 'metadata' in filename:
			metafile = filename.replace("with_ann","metadata")
			assert metafile in os.listdir(directory), "Cab not find metadata!!!"
            
			output = newdirectory+"\\"+filename
			outf = open(output,"wb")
			annf = open(directory+"\\"+filename,"rb") 
			metaf = open(directory+"\\"+metafile,"rb")
			handler(outf,annf,metaf)
			outf.close()
			annf.close()
			metaf.close()
            #break
	print "filter ended"