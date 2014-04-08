#!/usr/bin/python
from mdRunPrm import mdRunPrm 
from mdRunPrm import fix_head3
from mccepy.alterprotonation import freeAllConformers
import os, sys, time
import networkx as nx

home_dir = "/home/xzhu/BR_orig3/"
  
class ResPro(object):
    '''Residue class.
    
    It only contains the charges of the residues in different types of runs.
    '''
    
    allRunTypes = ("cqr", "cql", "cdr", "cdl", "hqr", "hql", "hdr", "hdl")
    def __init__(self, name=''):
        defaultState = "na"   # means not existing, e.g. for the ipece waters
        self.charges = {}
        for eachType in self.__class__.allRunTypes:
            self.charges[eachType] = defaultState
            
        self.rName = name
        
    def __str__(self):
        returnStr = "%10s" % self.rName
        for eachType in self.__class__.allRunTypes:
            returnStr += ("%7s" % self.charges[eachType])
        
        return returnStr
    
    __repr__ = __str__


def getRunTypeAbbreviation(pdbT, runT, scaleT):
    '''Get the abbreviation of a certain type of run.
    
    Args:
        pdbT: different types due to different pdb files used, option={"crystal", "hydro"}.
        runT: quick or default run of MCCE, option={"quick", "def"}.
        scaleT: scale lj by 0.1 or don't scale lj, option={"raw", "lj01"}.
        
    Returns:
        The abbreviation the run type determined by the 3 parameters above.
        
    >>> getRunTypeAbbreviation("crystal", "quick", "lj01")
    "cql"
    '''
    
    firstLetter = ''     # for pdbT, "crystal" = 'c', "hydro" = 'h'
    secondLetter = ''    # for runT, "quick" = 'q', "def' = 'd'
    thirdLetter = ''     # for scaleT, "raw" = 'r', "lj01" = 'l'
    if pdbT == "crystal":
        firstLetter = 'c'
    elif pdbT == "hydro":
        firstLetter = 'h'
        
    if runT == "quick":
        secondLetter = 'q'
    elif runT == "def":
        secondLetter = 'd'
        
    if scaleT == "raw":
        thirdLetter = 'r'
    elif scaleT == "lj01":
        thirdLetter = 'l'
        
    return firstLetter + secondLetter + thirdLetter  
        

def getProtonation(runType, allRes, chargeFile="sum_crg.out", titrationPointIndex=1):
    '''Get the charges of the residues from "sum_crg.out".
    
    Args:
        runType: the type of the run, e.g. "cql".
        allRes: all the residues whose charges have to be found.
        chargeFile: the name of the file which has the info of the charges of the residues.
        titrationPointIndex: the index of the field where the charge of the residue is of interest.
    '''
    
    lines = open(chargeFile, 'r').readlines()
    lines.pop(0)
    
    for eachLine in lines:
        if eachLine.startswith("----"): continue
        if eachLine.startswith("Electrons"): continue
        if eachLine.startswith("Net_Charge"): continue
        
        fields = eachLine.split()
        resName = fields[0]
        
        crg = float(fields[titrationPointIndex])
        
        resFound = False
        if allRes:
            for eachRes in allRes:
                if resName == eachRes.rName:
                    eachRes.charges[runType] = crg
                    resFound = True
                    break
                
        if not resFound:
            newRes = ResPro(resName)
            newRes.charges[runType] = crg
            allRes.append(newRes)
 
            
def getPka(runType, allRes):
    '''Get pKa of all the residues.
    
    pKas of waters are not included.
    
    Args:
        runType: abbreviation of a run type.
        allRes: a list of all the residues.
    '''
    
    lines = open("pK.out", 'r').readlines()
    lines.pop(0)
    
    for eachLine in lines:
        if eachLine.startswith("HOH"): continue   # do not include waters.
        fields = eachLine.split()
        resName = fields[0]
        pka = fields[1]
        
        resFound = False
        if allRes:
            for eachRes in allRes:
                if resName == eachRes.rName:
                    eachRes.charges[runType] = pka
                    resFound = True
                    break
        
        if not resFound:
            newRes = ResPro(resName)
            newRes.charges[runType] = pka
            allRes.append(newRes)        
    
         
def printAllRes(allRes):
    '''Output all the charges of the residues.
    
    Args:
        allRes: a list of all the residues.
    '''
    
    for eachRes in allRes:
        if eachRes.rName[:3] == "HOH":
            continue
            waterExist = False
            for eachCharge in eachRes.charges.values():
                if eachCharge != "na":
                    if abs(float(eachCharge)) >= 0.01:
                        waterExist = True
                        break
            if waterExist: print eachRes
        else:
            print eachRes  
            
                 
if __name__ == '__main__':
    pdbs = ["1C3W", "1C8R", "1KG9", "1DZE", "1KG8", "1C8S", "1F4Z"]
    pdb_types = ["crystal"]
    run_types = ["quick", "def"]
    scale_types = ["lj01"]
    
    
    for aPdb in pdbs:
        allRes = []
        os.chdir(os.path.join(home_dir, aPdb))
        for pdbT in pdb_types:
            os.chdir(os.path.join(home_dir, aPdb, pdbT))
            for runT in run_types:
                os.chdir(os.path.join(home_dir, aPdb, pdbT, runT))
                for scaleT in scale_types:
                    finalPath = os.path.join(home_dir, aPdb, pdbT, runT, scaleT)

                    if not os.path.exists(finalPath):
                        sys.stderr.write("%s doesn't exist\n" % finalPath)
                    os.chdir(finalPath)
                    
                    sys.stdout.write(finalPath + '\n')
                    getProtonation(getRunTypeAbbreviation(pdbT, runT, scaleT), allRes)
                    
        printAllRes(allRes)
