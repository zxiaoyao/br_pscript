#!/usr/bin/env python
import subprocess, argparse, os, shutil, sys

PH2KCAL  =    1.364

class Conf(object):
    PH_NOW = 7.0
    
    def __init__(self):
        self.confName = ""
        self.occ = 0.0
        
        # head3.lst energy terms
        self.Em0 = 0.0
        self.pKa0 = 0.0
        self.ne = 0
        self.nH = 0
        self.vdw0 = 0.0
        self.vdw1 = 0.0
        self.tors = 0.0
        self.epol = 0.0
        self.dsolv = 0.0
        self.extra = 0.0
        # total self energy of the conformer from head3.lst
        self.totalSelf = 0.0
        
        self.mfeSum = 0.0
        
    def __str__(self):
        return "%s%10.3f" % (self.confName, self.occ)
    
    def isDummy(self):
        return self.confName[3:5] == "DM"
    
    def read_fort38_line(self, line):
        fields = line.split()
        self.confName = fields[0]
        self.occ = float(fields[1])
        
    def read_head3_line(self, line):
        
        
        self.Em0 = float(line[34:40])
        self.pKa0 = float(line[40:46])
        self.ne = int(line[46:49])
        self.nH = int(line[49:52])
        self.vdw0 = float(line[52:61])
        self.vdw1 = float(line[61:68])
        self.tors = float(line[68:76])
        self.epol = float(line[76:84])
        self.dsolv = float(line[84:92])
        self.extra = float(line[92:100])
        
        self.totalSelf = self.nH * (Conf.PH_NOW - self.pKa0) * PH2KCAL\
                        + self.vdw0 + self.vdw1 + self.tors + self.epol\
                        + self.dsolv + self.extra   
        
def read_fort38(fName="fort.38"):
    fp = open(fName, 'r')
    fp.readline()
    
    allConfs = []
    for eachLine in fp:
        newConf = Conf()
        newConf.read_fort38_line(eachLine)
        allConfs.append(newConf)
        
    return allConfs

def occupied_confs(threshold=0.0, fName="fort.38"):
    allConfs = read_fort38(fName)
    occConfs = []
    for eachConf in allConfs:
        if eachConf.occ > threshold:
            occConfs.append(eachConf)
            
    return occConfs

def print_occ_confs(occConfs):
    
    for eachConf in occConfs:
        print eachConf, 
        print "%10.3f%10.3f%10.3f%10.3f" % (eachConf.totalSelf, eachConf.mfeSum, \
                                            eachConf.totalSelf * eachConf.occ,\
                                            eachConf.mfeSum * eachConf.occ )

def load_head3_info(allConfs, fName="head3.lst"):
    allLines = open(fName, 'r').readlines()
    allLines.pop(0)
    
    for eachConf in allConfs:
        for eachLine in allLines:
            confName = eachLine.split()[1]
            if eachConf.confName == confName:
                eachConf.read_head3_line(eachLine)
                break
            
def calculate_mfe(allConfs):
    MFE_PATH = "/home/xzhu/bin/mfe++"
    for eachConf in allConfs:
        if eachConf.isDummy(): continue
        p = subprocess.Popen([MFE_PATH, eachConf.confName], stdout=subprocess.PIPE)
        mfeOut = p.communicate()[0]
        
        eachConf.mfeSum = float(mfeOut.split()[-1]) * PH2KCAL
        
def statistics_oconf(allConfs):
    totalSelf = 0.0
    totalPair = 0.0
    
    for eachConf in allConfs:
        totalSelf += eachConf.totalSelf * eachConf.occ
        totalPair += eachConf.mfeSum * eachConf.occ
        
    return (totalSelf, totalPair/2)

def main():
    if not os.path.isdir("energies"):
        subprocess.check_call(["/home/xzhu/bin/zopp", "-x", "energies"])
    occConfs = occupied_confs(threshold=0.0)
    load_head3_info(occConfs)
    calculate_mfe(occConfs)
    print_occ_confs(occConfs)
    
    totalSelf, totalPair = statistics_oconf(occConfs)
    print "Self: %10.3f, Pair: %10.3f" % (totalSelf, totalPair)
    
    shutil.rmtree("energies")
    

def mfeResAllConf(resName):
    ''' Do mfe for all the conformers of a residues, including the self energy.
    '''
#     if not os.path.isdir("energies"):
#         subprocess.check_call(["/home/xzhu/bin/zopp", "-x", "energies"])
#   
    if not os.path.exists("energies"):      
        os.symlink("/home/xzhu/BR2/1C3W/hydro/def/raw_O/path1/mSub/DA850OX2920RA820OX358+EA194-/energies", "energies")
    allConfs = read_fort38()
    resConfs = []
    for eachConf in allConfs:
        confResName = eachConf.confName[:3] + eachConf.confName[5:10]
        if confResName == resName:
            resConfs.append(eachConf)
    
    load_head3_info(resConfs)
    calculate_mfe(resConfs)
    
    print "%14s%10s%10s%10s" % ("confName", "totalSelf", "mfeSum", "total")
    for eachConf in resConfs:
        print "%14s%10.3f%10.3f%10.3f" % (eachConf.confName, eachConf.totalSelf, eachConf.mfeSum, eachConf.totalSelf+eachConf.mfeSum)
    
    
if __name__ == "__main__":
    mfeResAllConf(sys.argv[1])