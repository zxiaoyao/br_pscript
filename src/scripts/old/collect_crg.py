#!/usr/bin/python
from mdRunPrm import mdRunPrm 
from mdRunPrm import fix_head3
from mccepy.alterprotonation import freeAllConformers
import os, sys, time
import networkx as nx

home_dir = "/home/xzhu/BR_orig3/"
  
class ResPro(object):
    allRunTypes = ("cqr", "cql", "cdr", "cdl", "hqr", "hql", "hdr", "hdl")
    def __init__(self, name=''):
        defaultState = "na"   # means not exists, e.g. for the ipece waters
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
    lines = open("sum_crg.out", 'r').readlines()
    lines.pop(0)
    
    for eachLine in lines:
        if eachLine.startswith("----"): continue
        if eachLine.startswith("Electrons"): continue
        if eachLine.startswith("Net_Charge"): continue
        fields = eachLine.split()
        resName = fields[0]
        
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
            
def getPka(runType, allRes):            
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
    #pdbs = ["1C8R", "1KG9", "1DZE", "1KG8", "1C8S", "1F4Z"]
    pdbs = ["1C3W", "1C8R", "1KG9", "1DZE", "1KG8", "1C8S", "1F4Z"]
    #pdbs = ["1C3W"]
    #pdbs = ["1DZE", "1KG8"]
    #pdb_types = ["crystal", "hydro"]
    pdb_types = ["crystal"]
    #run_types = ["quick"]
    run_types = ["quick", "def"]
    #scale_types = ["raw", "lj01"]
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
                    #if not os.path.exists(finalPath):
                    #    os.makedirs(finalPath, 0755)

                    if not os.path.exists(finalPath):
                        sys.stderr.write("%s doesn't exist\n" % finalPath)
                    os.chdir(finalPath)
                    
                    sys.stdout.write(finalPath + '\n')
                    getProtonation(getRunTypeAbbreviation(pdbT, runT, scaleT), allRes)
                    #getPka(getRunTypeAbbreviation(pdbT, runT, scaleT), allRes)

                    #findSecondShortestpaths()
                    #os.system("/home/xzhu/bin/pythonScript/setuphbrun.py -s")
                    #actionForAllPaths(aPdb, pdbT, runT, scaleT)
                    #print_sorted_path_stat()
                    #step4(aPdb, pdbT, runT, scaleT)   
                    #step123(aPdb, pdbT, runT, scaleT)
        printAllRes(allRes)
