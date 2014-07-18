#!/usr/bin/env python
'''
Created on Jul 15, 2014

@author: xzhu
'''

'''Load all the conformers of specified residues from step1_out.pdb or step2_out.pdb.'''


def loadResAllConfs(resName, pdbFile):
    '''Load all the conformers of this residue.
    
    The residue is specified by the chain Id and the residue sequence number, such as A0085.
    
    '''
    for eachLine in open(pdbFile):
        rName = eachLine[21:26]
        
    
    

