#!/usr/bin/env python
'''
Created on Jun 25, 2014

@author: xzhu
'''
from pymol import cmd

from xhbpathpy.hbPath import HbPath

'''Show the lowest energy barrier hopping sequence of this pathway.

Use the most occupied the pdb to represent the state of a protonation state.

@note: need to run this program in a pathway folder, e.g. 1C3W/hydro/def/raw_O/dummyWater/path1.
'''
import sys

sys.path.append("/home")

def lowestHopSeq():
    '''Load all the states in the lowest ebarrier hopping sequences.
    
    '''
    import os
    
    hbpath = HbPath()
    hbpath.readIntermediates()
    hbpath.readHopSeqences()
    
    cwd = os.getcwd()
    
    for eachState in hbpath.hopSequences[0]:
        os.chdir(os.path.join(cwd, "mSub", str(eachState)))
        os.system("mocc.py -t 7")
        cmd.load("mocc_7.0", eachState.stateId)
        

cmd.extend("lowestHopSeq", lowestHopSeq)
        