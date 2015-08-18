#unzip files in different folder into one folder
#need to change config when the path/destination is different
import os
import zipfile
import logging

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
            print x
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

        
if __name__ == "__main__":
    directory = r'C:\\Users\\GIS_tech\\Desktop\\66county' #main dir
    subdir = os.path.join(directory,'source2') #zip file source
    desdir = r'C:\\Users\\GIS_tech\\Desktop\\66county\\extracted' #unzip dir
    unzip(directory,subdir,desdir)