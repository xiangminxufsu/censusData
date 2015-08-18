"""
simple script
merge all files under dir into one, all files have the same row length and append them by row.
Created by Xiangmin Xu

"""

import os
from os.path import join,isfile
import logging

def mergefile():
    logging.basicConfig(filename = 'log.log',format = '%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info('merge started')
    path = r'C:\\Users\\GIS_tech\\Desktop\\66county\\FiltedAnnFile'
    destination = r'C:\\Users\\GIS_tech\\Desktop\\66county'
    
    assert os.path.exists(destination)
    assert os.path.exists(path), "Could not find %s !!!" % path
    
    files = os.listdir(path)
    #print files
    files = [join(path,x) for x in files if 'ann.csv' in x]
    print files
    
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
        
mergefile()
    

