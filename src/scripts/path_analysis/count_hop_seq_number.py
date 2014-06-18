#!/usr/bin/env python
'''
Created on Jun 18, 2014

@author: xzhu
'''
import os

from xhbpathpy.hbPath import HbPath
'''Count the number of different hopping sequence of a pathway.'''

def countHopSeqNumber():
    '''Count number of hopping sequences.
    
    Have to be in a folder where all the files need to get the pathway are there.
    
    '''
    hbp = HbPath() 
    hbp.readIntermediates()
    hbp.readHopSeqences()
    
    return len(hbp.hopSequences)
    
def parsePath(fname="allPaths.txt"):
    '''Go to each path folder.
    
    '''
    for eachLine in open(fname):
        pathName = eachLine.split()[0]
        os.chdir(pathName)
        print eachLine[:-1], countHopSeqNumber()
        os.chdir("..")
        
        
if __name__ == '__main__':
    parsePath()