#!/usr/bin/env python
'''
Created on Jun 20, 2014

@author: xzhu
'''
from xmccepy.runPrm import RunPrm

if __name__ == '__main__':
    rp = RunPrm()
    rp.readFromFile()
    
    d = {"DO_PREMCCE":'t'}
    rp.mdRunPrm(d)
    
    rp.writeToFile() 