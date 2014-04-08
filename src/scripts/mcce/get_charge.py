#!/usr/bin/env python

from mdRunPrm import mdRunPrm 
from mdRunPrm import fix_head3
from mcceutility.alterprotonation import freeAllConformers
import os, sys, time, shutil
import networkx as nx
import numpy
import pylab

'''Get the charges of residues. It's similar to the script "collect_crg.py".
'''

class ResPro(object):
    allRunTypes = ("cqr", "cql", "cdr", "cdl", "hqr", "hql", "hdr", "hdl")
    DEFAULT_CRG = "na"   # means not exists, e.g. for the ipece waters
    def __init__(self, name=''):        
        self.charges = {}
        for eachType in self.__class__.allRunTypes:
            self.charges[eachType] = ResPro.DEFAULT_CRG
            
        self.rName = name
        
        self.avg = 0.0
        self.std = 0.0
        self.protonation = 0
        
    def __str__(self):
        returnStr = "%-10s" % self.rName
        for eachType in self.__class__.allRunTypes:
            returnStr += ("%7s" % self.charges[eachType])
            
        self.getStat()
        returnStr += ("%10.2f" % self.avg)    
        returnStr += ("%6.2f" % self.std)
        returnStr += ("%6d" % self.protonation )    
        
        return returnStr
    
    def getStat(self):
        effectiveCrg = []
        for eachCrg in self.charges.values():
            if eachCrg != ResPro.DEFAULT_CRG:
                effectiveCrg.append(eachCrg)
        if effectiveCrg:
            self.avg = numpy.mean(effectiveCrg)
            self.std = numpy.std(effectiveCrg)
            self.protonation = int(round(self.avg))
        
    __repr__ = __str__
    
    
def getRunTypeAbbreviation(pdbT, runT, scaleT):
    '''Get the abbreviation a particular type of run.
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
           

def getProtonation(runType, allRes):
    if not os.path.isfile("sum_crg.out"): return
    
    lines = open("sum_crg.out", 'r').readlines()
    lines.pop(0)
    
    for eachLine in lines:
        if eachLine.startswith("----"): continue
        if eachLine.startswith("Electrons"): continue
        if eachLine.startswith("Net_Charge"): continue
        fields = eachLine.split()
        resName = fields[0][:3] + fields[0][4:9]
        
        # Be careful, Have to change the tiration so that the charges are all at pH 7.
        titrationPoint = 1
        crg = float(fields[titrationPoint])
        
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
            

def printAllRes(allRes, onlyPrintKeyResidues = True, stdThres=-0.01):
    keyResidues = ["ASPA0096", "RSBA0216", "ASPA0085", "ASPA0212", "ARGA0082", "GLUA0194", "GLUA0204"]
    ccResidues = ["RSBA0216", "ASPA0085", "ASPA0212"]
    ecResidues = ["GLUA0194", "GLUA0204"]
        
    centCluster = ResPro("central")
    exitCluster = ResPro("exit")
    
    for eachRes in allRes:
        if onlyPrintKeyResidues:
            if eachRes.rName not in keyResidues:
                continue
            
        if eachRes.rName in ccResidues:
            for eachRunType in eachRes.charges.keys():
                if centCluster.charges[eachRunType] == ResPro.DEFAULT_CRG:
                    centCluster.charges[eachRunType] = eachRes.charges[eachRunType]
                else:
                    centCluster.charges[eachRunType] += eachRes.charges[eachRunType]
        
        elif eachRes.rName in ecResidues:
            for eachRunType in eachRes.charges.keys():
                if exitCluster.charges[eachRunType] == ResPro.DEFAULT_CRG:
                    exitCluster.charges[eachRunType] = eachRes.charges[eachRunType]
                else:
                    exitCluster.charges[eachRunType] += eachRes.charges[eachRunType]           
        
        eachRes.getStat()
        # waters will be printed if they are not totally dummy        
        if eachRes.rName[:3] == "HOH":
            continue
            waterExist = False
            for eachCharge in eachRes.charges.values():
                if eachCharge != ResPro.DEFAULT_CRG:
                    if abs(float(eachCharge)) >= 0.01:
                        waterExist = True
                        break
            if waterExist:
                if eachRes.std >= stdThres: 
                    print eachRes
        else:
            # ordinary residues
            if eachRes.std >= stdThres:
                print eachRes
            
    
#     print centCluster
#     print exitCluster
    print
    
    allRes.append(centCluster)      
    allRes.append(exitCluster)
          
def getResCharges():
    home_dir = "/home/xzhu/BR2/"
    pdbs = ["1C3W", "1C8R", "1KG9", "1DZE", "1KG8", "1C8S", "1F4Z"]
    pdb_types = ["crystal", "hydro"]
    run_types = ["quick", "def"]
    scale_types = ["raw", "lj01"]
    
    keyResidues = ["ASPA0096", "RSBA0216", "ASPA0085", "ASPA0212", "ARGA0082", "GLUA0194", "GLUA0204"]
    
    allCharges = []
   
    for aPdb in pdbs:
        allRes = []
        print aPdb
        
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
                    
                    
                    
                    os.chdir("FreeMcce")
                    
                    getProtonation(getRunTypeAbbreviation(pdbT, runT, scaleT), allRes)
                    
        allCharges.append(allRes)            
        printAllRes(allRes, onlyPrintKeyResidues = False, stdThres=-0.1)
            
if __name__ == '__main__':
    getResCharges()
