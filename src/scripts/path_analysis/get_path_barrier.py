#!/usr/bin/env python

#===============================================================================
# The way I use this script:
# 1. In your working directory where you already have "head3.lst", "fort.38", "sum_crg.out",
#    generate a file called "fixedProtonations.txt", in which you need to specify the protonation
#    states of all the residues.
#    You can use -1, 0, 1, or 211. 211 denotes the residue in dummy.
#
# 2. Make a sub directory (e.g "pathdir") in working directory 
# 3. In the sub directory, generate a file called "pathinfo.txt".
#    Specify the residues in the pathway, all their possible protonation states, and the initial state.
#    Refer to the "loadPathInfo" method in class "HbPath" for the file format please.
#
# 3. Go to the working directory, use "get_path_barrier.py -s pathdir" to submit the jobs.
# 4. After all jobs are done, use "get_path_barrier.py -p pathdir" to retrieve the calculated path info.
#    There will be 3 output files in the "pathdir" directory, "hopSequences.txt",
#    "intermediates.txt", and "lowestHopSeq.txt".
#    You can find the lowest energy barrier of the path in the "lowestHopSeq.txt" file.
#===============================================================================
SUB_RUNS_FOLDER = "subProtonation"
PATH_INFO_FILE = "pathinfo.txt"
DUMMY_PROTONATION = 211

import os, sys, shutil
import copy
import argparse
from collections import deque

CONVERT_RES_SYMBOL = {"ASP":'D', "GLU":'E', "ARG":'R', "HOH":'O', "TYR":'Y', "RSB":'U'}
CONVERT_PROTONATION_SYMBOL = {-1:'-', 0:'0', +1:'+'}
CONVERT_SYMBOL_PROTONATION = {'-':-1, '0':0, '+':1}

class ProtonationState(object):
    
    keyResidues = []
    
    def __init__(self):
        self.protonations = []
        self.energy = 0.0
        self.stateId = 0
        self.layer = 0       # which layer this state appears
        
        
    def __repr__(self):
        stateName = ""
        for i in range(len(ProtonationState.keyResidues)):
            stateName += CONVERT_RES_SYMBOL[ProtonationState.keyResidues[i][:3]]
            stateName += ProtonationState.keyResidues[i][3]
            stateName += str(int(ProtonationState.keyResidues[i][4:]))
            stateName += CONVERT_PROTONATION_SYMBOL[self.protonations[i]]
        
        return stateName
    
    def __eq__(self, other):
        return repr(self) == repr(other)
    
    def __hash__(self):
        return hash(repr(self))
    
class HopSequence(object):
    possibleProtonations = []
    def __init__(self, initialState=None):
        self.hopHistory = []
        self.energyBarrier = 0.0
        
        self.intermediates = []
        if initialState:
            self.intermediates.append(initialState)
            for i in range(len(initialState.protonations)):
                self.hopHistory.append(0)
                
    def nextHop(self):
        allNewHopSequence = []
        lastState = self.intermediates[-1]
        for i in range(len(self.hopHistory) - 1):
            if self.hopHistory[i] == 0:
                if (lastState.protonations[i] - 1) in HopSequence.possibleProtonations[i]:
                    if (lastState.protonations[i+1] + 1) in HopSequence.possibleProtonations[i+1]:
                        newState = copy.deepcopy(lastState)
                        newState.protonations[i] -= 1
                        newState.protonations[i+1] += 1
                        newState.layer = len(self.intermediates) + 1
                        
                        newHopSequence = HopSequence()
                        newHopSequence.hopHistory = self.hopHistory[:]
                        newHopSequence.intermediates = self.intermediates[:]
                        newHopSequence.hopHistory[i] = 1
                        newHopSequence.intermediates.append(newState)
                        
                        allNewHopSequence.append(newHopSequence)
                        
        return allNewHopSequence
    
    def getEBarrier(self):
        highestE = self.intermediates[0].energy
        for eachState in self.intermediates:
            if eachState.energy > highestE:
                highestE = eachState.energy
        self.energyBarrier = highestE - self.intermediates[0].energy
        
        return self.energyBarrier 
                         
        
class HbPath(object):    
    def __init__(self):
        self.keyResidues = []
        self.possibleProtonations = []
        self.initialState = ProtonationState()
        self.nResidues = 0
        
        self.hopSequences = []
        self.protonationStates = set()
        
    def loadPathInfo(self, fName = PATH_INFO_FILE):
        '''
        Get the key residues in the pathway, and their possible protonation states, 
        and the initial state. Return an object of class PathConfig containing this information.
    
        The file format should be like this:
        ASPA0085  -1  0
        HOHA0402  -1  0  1
        HOHA0406  -1  0  1
        ARGA0082   0  1
        HOHA0403  -1  0  1
        GLUA0194  -1  0
         0 0 0 1 0 -1
     
         The last line is the initial state.
         The other lines give the name of the residues, following all their possible protonation states
         '''
        try:
            fp = open(fName, 'r')
        except:
            print "Can't open %s to load path info" % fName
            raise
        
        allLines = fp.readlines()
    
        # the last line should give the initial state.
        for eachLine in allLines[:-1]:
            if eachLine.startswith("#"): continue     # line is a comment
            fields = eachLine.split()
        
            self.keyResidues.append(fields[0])
            self.possibleProtonations.append([int(eachProtonation) for eachProtonation in fields[1:]])

        
        self.initialState.protonations = [int(eachProtonation) for eachProtonation in allLines[-1].split()]
        self.initialState.layer = 1
        
        if len(self.keyResidues) != len(self.initialState.protonations):
            print "Error: Number of residues doesn't match with the initial state"
        else:
            self.nResidues = len(self.keyResidues)
        
    def getAllHopSequences(self):
        ProtonationState.keyResidues = self.keyResidues
        HopSequence.possibleProtonations = self.possibleProtonations
        
        firstHopSequence = HopSequence(self.initialState) 
        sequenceQueue = deque()
        sequenceQueue.append(firstHopSequence)
        
        while sequenceQueue:
            newOutSeq = sequenceQueue.popleft()
            if len(newOutSeq.intermediates) != self.nResidues:
                for eachSeq in newOutSeq.nextHop():
                    sequenceQueue.append(eachSeq)
            else:
                self.hopSequences.append(newOutSeq)
                
        for eachSeq in self.hopSequences:
            for eachState in eachSeq.intermediates:
                self.protonationStates.add(eachState)
                
        self.protonationStates = sorted(self.protonationStates, key = lambda state: state.layer)
        #print self.protonationStates
        
        # number all the possible protonation states
        idCounter = 1
        for eachState in self.protonationStates:
            eachState.stateId = idCounter
            idCounter += 1
            
        labeledSeq = []
        for eachSeq in self.hopSequences:
            newSeq = HopSequence()
            for i in range(len(eachSeq.intermediates)):
                for eachState in self.protonationStates:
                    if str(eachSeq.intermediates[i]) == str(eachState):
                        newSeq.intermediates.append(eachState)
                        break
            labeledSeq.append(newSeq)
        self.hopSequences = labeledSeq
        
#         print len(self.hopSequences)
#         for eachSeq in self.hopSequences:
#             print len(eachSeq.intermediates)
#             for eachState in eachSeq.intermediates:
#                 print eachState, eachState.stateId                
                
def getAllResProtonation(fnHead3="head3.lst", fnCrg="sum_crg.out", fnFort="fort.38"):
    '''Assuming residues are ordinary ones, which only can change their charges by lose or gain protons.
    
    First, get all residues to be considered from "head3.lst". 
    And all the residues are assigned a default protonation state 0.
    
    Then, look through "sum_crg.out".
        if charge >= 0.5, residue protonation state is 1.
        if 0.5 > charge > -0.5, residue protonation state is 0.
        if charge <= -0.5, residue protonation state is -1.
        
    At last look through "fort.38" for the dummy conformers.
    If the occupancy of the dummy conformer is greater than 0.5, the residue state is DUMMY_PROTONATION.
    '''
    
    allResidues = set()
    
    allHLines = open(fnHead3, 'r').readlines()
    allHLines.pop(0)
    for eachLine in allHLines:
        allResidues.add(eachLine[6:9] + eachLine[11:16])
        
    resProtonations = {}
    for eachRes in allResidues:
        resProtonations[eachRes] = 0
        
    allCLines = open(fnCrg, 'r').readlines()
    allCLines.pop(0)
    for eachLine in allCLines[:-4]:
        fields = eachLine.split()
        resName = fields[0][:3] + fields[0][4:9]
        crg = float(fields[1])
        if crg >= 0.5:
            resProtonations[resName] = 1
        elif crg > -0.5:
            resProtonations[resName] = 0
        else:
            resProtonations[resName] = -1
            
    allFLines = open(fnFort, 'r').readlines()
    allFLines.pop(0)
    for eachLine in allFLines:
        if eachLine[:5] == "HOHDM":   # deal with dummy conformers, only consider waters
            occ = float(eachLine.split()[1])
            if occ > 0.5:
                resProtonations[eachLine[:3] + eachLine[5:10]] = DUMMY_PROTONATION
            
    return resProtonations
 
        
def getConfProtonation(confName):
    '''
    Get the protonation state of a conformer ONLY by its name.
    '''
    
    if confName[3] == '0':
        return 0
    elif confName[3] == '-':
        return -1
    elif confName[3] == '+':
        return 1
    elif confName[3:5] == "DM":
        return DUMMY_PROTONATION
    else:
        return 0


def alterHead3ByProtonation(resProtonations, hbPath, fName="head3.lst", keepDummy=False):
    newLines = []
    allLines = open(fName, 'r').readlines()
    newLines.append(allLines.pop(0))
        
    for eachLine in allLines:
        confName = eachLine[6:20]
        resName = eachLine[6:9] + eachLine[11:16]
        
        # only fix the protonations of residues in path
        # the other residues are free to change protonations, except those whose protonations are already fixed.
        
        # by default the protonation states of residues are fixed.
        # This can be changed by adding one option "fixed=False" at the end of the program arguments

#         if not resName in hbPath.keyResidues:
#             newLines.append(eachLine) 
#             continue
        
        fixedProtonation = resProtonations[resName]
        
        # special treat for the dummy water conformers.
        # if it's not fixed to be dummy then always keep the dummy conformers of waters not in the pathway.
        if (resName not in hbPath.keyResidues) and resName[:3] == "HOH":
            if keepDummy and fixedProtonation != DUMMY_PROTONATION:
                if getConfProtonation(confName) == DUMMY_PROTONATION:
                    newLines.append(eachLine[:21] + 'f 0.00' + eachLine[27:])
                    continue
                
        if getConfProtonation(confName) == fixedProtonation:
            newLines.append(eachLine[:21] + 'f 0.00' + eachLine[27:])
        else:
            newLines.append(eachLine[:21] + 't 0.00' + eachLine[27:])
            
    open("head3.lst", 'w').writelines(newLines)        


def write_ms_gold(keyResidues):
    ''' write the key residues into "ms_gold" file.
    '''
    
    fp = open("ms_gold", 'w')
    for eachRes in keyResidues:
        fp.write(eachRes + '\n')
    fp.close()
   
   
def loadResProtonation(fname="fixedProtonations.txt"):
    '''Return the protonation states of all residues in a dictionary.
    ''' 
    resProtonatios = {}
    for eachLine in open(fname, 'r'):
        fields = eachLine.split()
        resProtonatios[fields[0]] = int(fields[1])
    return resProtonatios
     
    
def submit_subruns(hbPath, parentPath, runPath):
    from xmccepy.mdRunPrm import mdRunPrm
#     resProtonations = getAllResProtonation(os.path.join(parentPath, "head3.lst"),\
#                                            os.path.join(parentPath, "sum_crg.out"),\
#                                            os.path.join(parentPath, "fort.38"))

    # load the fixed protonation states of all the residues.
    resProtonations = loadResProtonation(os.path.join(parentPath, "fixedProtonations.txt"))
    
    if not os.path.isdir(runPath):
        os.makedirs(runPath, 0755)
    os.chdir(runPath)
    
    for eachState in hbPath.protonationStates:
        # remove the existing sub directories
#         if os.path.isdir(str(eachState)): 
#             shutil.rmtree(str(eachState))
            
        if not os.path.isdir(str(eachState)):
            os.mkdir(str(eachState))
            
        os.chdir(str(eachState))
        
        # calculation has already been done.
        if os.path.isfile("pK.out") and len(open("pK.out").readlines()) != 0:
            print "Already has pK.out in", os.getcwd()
            os.chdir("..")
            continue
        
        # copy head3.lst from parent directory and modify it accordingly.
        shutil.copy(os.path.join(parentPath, "head3.lst"), ".")
        
        for i in range(len(hbPath.keyResidues)):
            resProtonations[hbPath.keyResidues[i]] = eachState.protonations[i]
        alterHead3ByProtonation(resProtonations, hbPath, keepDummy=True)
        
        write_ms_gold(hbPath.keyResidues)
        
        shutil.copy(os.path.join(parentPath, "run.prm"), ".")
        changePrm = {"MFE_CUTOFF":"10.0", "MONTE_NITER":"2000"}
        mdRunPrm(changePrm)
        
        shutil.copy("/home/xzhu/pfile/submit_temp.sh", ".")
        
        files_to_link = ["energies.opp", "extra.tpl"]
        if not os.path.islink("energies.opp"):
            os.system("ln -s " + os.path.join(parentPath, "energies.opp") + " .")
        if not os.path.islink("extra.tpl"):
            os.system("ln -s " + os.path.join(parentPath, "extra.tpl") + " .")
        
        os.system("qsub submit_temp.sh")
    
        os.chdir("..")


def run_te():
    shutil.copy("/home/xzhu/pfile/submit_te.sh", ".")
    os.system("qsub submit_te.sh")

    
def retrieve_info_from_microstate(hbPath, subFolder):
    '''Get energy of the protonation state from the microstates.
    '''
    
    os.chdir(subFolder)
    te_program_path = "/home/xzhu/gmcce/serialte/te"
    
    for eachState in hbPath.protonationStates:
        os.chdir(str(eachState))
        if os.path.isfile("respair.lst"):
            os.remove("respair.lst")

        if not os.path.isfile("ms_crg") :
            run_te()
        elif len(open("ms_crg").readlines()) != 2:
            run_te()
        
        os.chdir("..")
        
        
def obtain_path_info(hbPath, pathFolder, subRunFolder):
    os.chdir(subRunFolder)
    for eachState in hbPath.protonationStates:
        os.chdir(str(eachState))
        eachState.energy = float(open("ms_crg").readlines()[-1].split()[-4])
        if os.path.isfile("ms.dat"):
            os.remove("ms.dat")
        os.chdir("..")
        
        
    # sort all the intermediate states, first by layer, then by energy. 
    hbPath.protonationStates = sorted(hbPath.protonationStates, key=lambda state: (state.layer, state.energy)) 
    for i in range(len(hbPath.protonationStates)):
        hbPath.protonationStates[i].stateId = i + 1
     
    os.chdir(pathFolder)
    # output of all the intermediate states.      
    fpIntermediates = open("intermediates.txt", 'w')
    fpIntermediates.write("%-6s" % "id")
    for res in hbPath.keyResidues:
        fpIntermediates.write("%9s" % res)
    fpIntermediates.write("%10s\n" % "E")
    
    for eachState in hbPath.protonationStates:
        fpIntermediates.write("%-6s" % eachState.stateId)
        for eachProtonation in eachState.protonations:
            fpIntermediates.write("%9s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
        fpIntermediates.write("%10.3f\n" % eachState.energy)
    fpIntermediates.close()
    
    # sort all the possible hopping sequences, by the energy barrier
    for eachSeq in hbPath.hopSequences:
        eachSeq.getEBarrier()
#         highestE = eachSeq.intermediates[0].energy
#         for eachState in eachSeq.intermediates:
#             if eachState.energy > highestE:
#                 highestE = eachState.energy
#         eachSeq.energyBarrier = highestE - eachSeq.intermediates[0].energy        
    hbPath.hopSequences = sorted(hbPath.hopSequences, key=lambda seq: seq.energyBarrier)
    
    # output all the possible hopping sequences.
    lowestEnergyBarrier = hbPath.hopSequences[0].energyBarrier
    for eachSeq in hbPath.hopSequences:
        if eachSeq.energyBarrier < lowestEnergyBarrier:
            lowestEnergyBarrier = eachSeq.energyBarrier
            
    fpHop = open("hopSequences.txt", 'w')
    fpLowE = open("lowestHopSeq.txt", 'w')
    for eachSeq in hbPath.hopSequences:
        for eachState in eachSeq.intermediates:
            fpHop.write("%-6s" % eachState.stateId)
        fpHop.write("%10.3f\n" % eachSeq.energyBarrier)
        
        for eachState in eachSeq.intermediates:
            for eachProtonation in eachState.protonations:
                fpHop.write("%-6s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
            fpHop.write("%10.3f\n" % eachState.energy)
        fpHop.write("\n")
        
        if eachSeq.energyBarrier == lowestEnergyBarrier:
            for eachState in eachSeq.intermediates:
                fpLowE.write("%-6s" % eachState.stateId)
            fpLowE.write("%10.3f\n" % eachSeq.energyBarrier)
        
            for eachState in eachSeq.intermediates:
                for eachProtonation in eachState.protonations:
                    fpLowE.write("%-6s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
                fpLowE.write("%10.3f\n" % eachState.energy)
            fpLowE.write("\n")
            
    fpHop.close()
    fpLowE.close()
    
    
def load_path_energy_info(hbPath):
    '''
    Get the energies of intermediate states and energy barriers of different hopping sequences,
    by reading the files "intermediates.txt", "hopSequences.txt".
    '''
    allLines = open("intermediates.txt", 'r').readlines()
    allLines.pop(0)
    
    for eachLine in allLines:
        fields = eachLine.split()
        newState = ProtonationState()
        newState.stateId = fields[0]
        newState.protonations = [CONVERT_SYMBOL_PROTONATION[eachCrg] for eachCrg in fields[1:-1]]
        newState.energy = float(fields[-1])
        
        for eachState in hbPath.protonationStates:
            if eachState.protonations == newState.protonations:
                eachState.stateId = newState.stateId
                eachState.energy = newState.energy
                break
            
    for eachSeq in hbPath.hopSequences:
        eachSeq.getEBarrier()
   
       
def print_path_info(pathName):
    pass
      
                   
def main():
    # need "head3.lst", "sum_crg.out", "fort.38" in parentPath
    # "pathInfo.txt" has to be in pathFolder.
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", action="store_true", 
                        help="submit the jobs of the sub runs")
    parser.add_argument("-r", action="store_true",
                        help="retrieve the results of the sub runs")
    parser.add_argument("-p", action="store_true", 
                        help="obtain the path information")
    parser.add_argument("-l", action="store_true", 
                        help="print the highest energy state in the lowest energy barrier hopping sequence")
    parser.add_argument("pathName", default="path1", nargs='?',
                        help="name of the path")
    parser.add_argument("subFolder", default="mSub", nargs='?',
                        help="sub directory name where sub runs are in")
    args = parser.parse_args()   
    pathName = args.pathName
    subRunName = args.subFolder
    
    parentPath = os.getcwd()

    pathFolder = os.path.join(parentPath, pathName)

    subRunFolder = os.path.join(pathFolder, subRunName) 
    pathInfoFile = "pathinfo.txt"
    
    hbPath = HbPath()
    hbPath.loadPathInfo(os.path.join(pathFolder, pathInfoFile))
    hbPath.getAllHopSequences()
    
    if args.s:
        submit_subruns(hbPath, parentPath, subRunFolder)
    elif args.r:
        retrieve_info_from_microstate(hbPath, subRunFolder)
    elif args.p:
        obtain_path_info(hbPath, pathFolder, subRunFolder)
    elif args.l:
        pass
  
if __name__ == "__main__":
    main()
