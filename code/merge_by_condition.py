'''
Try to merge several colums into one, such as (0-5)(5-10)->(0,10)
Read from JoinTable, which contains the rule defined by user, then process the target file and create new file
'''

import os
import logging
import sys

def SearchFile(filename,mode="rb"):
    if mode == "wb":
        target = raw_input("Please input the {0} file: ".format(filename))
        f = open(target,"wb")
        print "created file {0}".format(target)
    else:
        while True:
            #try:
            target = raw_input("Please input the {0} file: ".format(filename))
            if not os.path.exists(target):
                print "File not found, please try again"
            else:
                f = open(target,mode)
                print "Good, file found"
                break
    return f
    
def tablehandler(tablef):
    """
    process table and return list containing list
    total:
    total
    would return [[total:,total]]
    """
    table = []
    element = []
    for x in tablef:
        x = x.rstrip()
        if x =='':
            table.append(element)
            element=[]
        else:
            element.append(x)
    tablef.close()
    return table

def write_des(table,desf,targetf):
    logging.info("write into desfile, starting from head")
    s = ','.join([x[0] for x in table])
    desf.write("%s\r\n"%s)
    
    #print targetf.readline()
    tarlist = targetf.readline().split(',')
    tarlist = [x.rstrip() for x in tarlist] #remove enter for the last element
    reflist = []
    logging.info("start matching table with target file")
    for ele in table:
        temlist = []
        for i in range(1,len(ele)):
            try:
                temlist.append(tarlist.index(ele[i].split(',')[1]))
            except ValueError:
                print "Whoops!!! could not match {0}".format(ele[i])
                logging.error("could not match {0}".format(ele[i]))
            except IndexError:
                temlist.append(tarlist.index(ele[i].split(',')[0]))
        reflist.append(temlist)
    #print reflist
    logging.info("matching completed,now we have the map between des file index and target file index, now\
                    write into desfile")
    '''
    This is the critical section
    targetf contains each line in the target file and reflist is like [[0],[1,2][3,4,5]]
    reflist provide position and we need to find the val in target file then sum them up in a 
    small list, then write into new des file.
    '''
    for line in targetf:
        newlist = []
        xlist = [e.rstrip() for e in line.split(',')]
        for x in reflist:
            if len(x)<=1:
                newlist.append(xlist[x[0]])
            else:
                newlist.append(sum([int(z) for z in [xlist[y] for y in x]]))
        newlist = [str(x) for x in newlist]
        desf.write("%s\n"%(','.join(newlist)))
    logging.info("desfile written compelete!")
    desf.close()
    targetf.close()
    
def Process():
    
    logging.basicConfig(filename = 'log.log',format = '%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
    logging.info("start running merge_by_condition.py")
    rmf = raw_input("please input the original file to be removed later: ")
    targetf = SearchFile("target")
    logging.info("target file found, now read the join table")
    tablef = SearchFile("join table")
    logging.info("join table found, now create destination file")
    desf = SearchFile("Desfile","wb")
    logging.info("created desfile and start processing table")
    
    table = tablehandler(tablef)
    logging.info("Table read completed")
    write_des(table,desf,targetf)
    os.remove(rmf)
    logging.info("%s removed, and replaced by new file" %rmf)
Process()