#!/usr/bin/env python
import os
import subprocess

from xhbpathpy.hbPath import HbPath

PATHINFO_TXT = "pathinfo.txt"

def getPathResidues(fname=PATHINFO_TXT):
    '''Get all the residues in the pathway from the text file pathinfo.txt.
    
    '''
    allLines = open(fname, 'r').readlines()
    
    allResidues = []
    
    for eachLine in allLines[:-1]:
        allResidues.append(eachLine.split()[0])
        
    return allResidues

  
def getAllConfs(residues, fname="fort.38"):
    '''Get all the conformers belong to the residues in fort.38.  
    
    '''
    allLines = open(fname, 'r').readlines()
    
    allConfs = []
    for eachLine in allLines[1:]:
        pass
        
        
def mfe_path():
    '''Do mfe++ on all the most occupied atoms of residues in the pathway.
    
    '''
    # all the residues in the pathway.
    pathResidues = getPathResidues()
    
    
    
    
    
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("stateId", help="an integer id of the protonation state", type=int)
    args = parser.parse_args()
    
    hbpath = HbPath()
    hbpath.readIntermediates()
    hbpath.readHopSeqences()
    
    if args.stateId > len(hbpath.protonationStates):
        raise RuntimeError("the state id number is out of the range.")
    
    for eachState in hbpath.protonationStates:
        if eachState.stateId == args.stateId:
            initState = eachState
            break
        
    initDir = initState.convertToDirName()
    
    print initDir
    
    os.chdir(os.path.join(os.getcwd(), "mSub", initDir))
    
    
    # need to have energies folder in the current directory.
    if not os.path.exists("energies"):
        if os.path.exists("../../../../energies"):
            os.system("ln -s ../../../../energies .")
        else:
            raise RuntimeError("No energies folder found.")
        
    for eachRes in initState.keyResidues:
        print "%s occupied conformers:" % eachRes.resName
        for eachConf in eachRes.findAllOccConf():
            print eachConf
        
        mostOccConf = eachRes.findFirstMostOccConf()
        print "most occupied conformer:"
        print mostOccConf
        os.system("mfe++ " + mostOccConf.confName)
        print
        
    
 
if __name__ == "__main__":
    main()
