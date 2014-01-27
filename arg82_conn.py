#!/usr/bin/env python
from pymol import cmd
from collections import deque

import os, copy

SUB_RUNS_FOLDER = "mSub"
PATH_INFO_FILE = "pathinfo.txt"
DUMMY_PROTONATION = 211

CONVERT_RES_SYMBOL = {"ASP":'D', "GLU":'E', "ARG":'R', "HOH":'O', "TYR":'Y', "RSB":'U'}
CONVERT_PROTONATION_SYMBOL = {-1:'-', 0:'0', +1:'+'}
CONVERT_SYMBOL_PROTONATION = {'-':-1, '0':0, '+':1}

class ProtonationState(object):
    # the key residues in the pathway
    keyResidues = []
    
    def __init__(self):
        self.protonations = []
        self.energy = 0.0
        self.stateId = 0
        self.layer = 0       # which layer this state appears
        
        
    def __repr__(self):
        stateName = ""
        if len(ProtonationState.keyResidues) != len(self.protonations):
            raise Exception("Numbers of keyResidues and protonations don't match")
        
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
    
    def print_hop_seqence(self):
        for eachRes in self.intermediates[0].keyResidues:
            print "%10s" % eachRes,
        print "%10.3f" % self.energyBarrier
            
        for eachInter in self.intermediates:
            for eachProtonation in eachInter.protonations:
                print "%10s" % CONVERT_PROTONATION_SYMBOL[eachProtonation],
            print "%10.3f" % eachInter.energy
             
                         
        
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
            raise RuntimeError("Can't open %s" % fName)

        
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
        
    def load_intermediates(self, intermediatesFile="intermediates.txt"):
        '''Load energies of protonation states from intermediates.txt'''
        
        try:
            fp = open(intermediatesFile, 'r')
        except:
            raise RuntimeError("Can't open %s" % intermediatesFile)
        
        headline = fp.readline()
        keyRes = headline.split()[1:-1]
        
        # should always have the same key residues 
        if len(ProtonationState.keyResidues) == 0:
            ProtonationState.keyResidues = keyRes
        elif ProtonationState.keyResidues != keyRes:
            raise RuntimeError("Number of key residues in intermeidates doesn't match with that already loaded")
        
        for eachLine in fp:
            fields = eachLine.split()
            newProtonation = ProtonationState()
            newProtonation.stateId = int(fields[0])
            newProtonation.protonations = [int(CONVERT_SYMBOL_PROTONATION[p]) for p in fields[1:-1]]
            newProtonation.energy = float(fields[-1])
            
            self.protonationStates.add(newProtonation)
        
    def load_hopSequences(self, hopSequencesFile="hopSequences.txt"):
        '''Load all the possible hop sequences from hopSequences.txt file.
        
            Energies of intermediates should have been loaded from intermediates.txt first.
            It will not load the intermediates again in this file.
        '''
        index_states = {}
        if len(self.protonationStates) == 0:
            raise RuntimeError("energies of the intermediates have to be loaded first")
        
        for eachState in self.protonationStates:
            index_states[eachState.stateId] = eachState
          
        try:
            fp = open(hopSequencesFile, 'r')
        except:
            raise RuntimeError("Can't open %s" % hopSequencesFile)
        
        # number of rows for each hop sequence, including the head and the trailing blank line
        nRow = len(ProtonationState.keyResidues) + 2
        
        lineCount = 0
        for eachLine in fp:
            lineCount += 1
            
            # only read the first line of each hop sequence
            if lineCount % nRow != 1:
                continue
            fields = eachLine.split()
            nRes = len(fields) - 1
            if nRes != (nRow - 2):
                raise RuntimeError("Number of residues in hopSequences dones't match with that of loaded key residues")
            
            newHop = HopSequence()
            for i in range(nRes):
                newHop.intermediates.append(index_states[int(fields[i])])
                
            newHop.energyBarrier = float(fields[-1])
            self.hopSequences.append(newHop)
            
            
    
    def load_calculated_path(self, pathinfoFile="pathinfo.txt", intermediatesFile="intermediates.txt", hopSequencesFile="hopSequences.txt"):         
        self.loadPathInfo(pathinfoFile)
        self.load_intermediates(intermediatesFile)
        self.load_hopSequences(hopSequencesFile)

class Conf(object):
    def __init__(self):
        self.confName = ""
        self.occ = 0.0
        
def occonf(cutoff=0.001, **kwarg):
    fp = open("fort.38", 'r')
    fp.readline()
    
    occupiedConfs = []
    for eachLine in fp:
        confName = eachLine.split()[0]
        occ = float(eachLine.split()[1])
        
        if occ < cutoff: continue
        
        if "keyResidues" in kwarg:
            keyResidues = kwarg["keyResidues"]
            resName = confName[:3] + confName[5:10]
            if resName not in keyResidues: continue
        newConf = Conf()
        newConf.confName = confName
        newConf.occ = occ
        occupiedConfs.append(newConf)
    
    return occupiedConfs


         
def most_occ_conf(keyResidues):
    fp = open("fort.38", 'r')
    fp.readline()
    
    maxOcc = {}
    for eachRes in keyResidues:
        maxOcc[eachRes] = 0.0
    
    mostConf = {}
        
    for eachLine in fp:
        confName = eachLine.split()[0]
        resName = confName[:3] + confName[5:10]
        if resName in keyResidues:
            occ = float(eachLine.split()[1])
            if occ > maxOcc[resName]:
                mostConf[resName] = confName
                maxOcc[resName] = occ
    
    occConfs = []
    for eachRes in keyResidues:
        newConf = Conf()
        newConf.confName = mostConf[eachRes]
        newConf.occ = maxOcc[eachRes]
        occConfs.append(newConf)
              
    return occConfs


def occupied_arg():
    hbpath = HbPath()
    hbpath.load_calculated_path()
    
    pathDir = os.getcwd()
    head3_lst = "/home/xzhu/BR2/1C3W/hydro/def/raw_O/head3.lst"
    
    possible_N = ("NE", "NH1", "NH2")
    arg_atom_N = {"01":"NE", "02":"NH1", "03":"NH2"}
    arg_conf_N = {}
    fp = open(head3_lst)
    fp.readline()    
    for eachLine in fp:
        confName = eachLine.split()[1]
        resName = confName[:3] + confName[5:10]
        if resName != "ARGA0082": continue
        if confName[3] == "+": continue
        
        conf_short = eachLine.split()[-1][:2]
        arg_conf_N[confName] = arg_atom_N[conf_short] 
    
    for eachHop in hbpath.hopSequences:
        argN = []
        for eachState in eachHop.intermediates:
            if "RA82+" in str(eachState): continue
            os.chdir(os.path.join(pathDir, SUB_RUNS_FOLDER, str(eachState)))
            confs = occonf(keyResidues=["ARGA0082"])
            Nitrogens = []
            for eachConf in confs:
                Nitrogens.append(eachConf.confName)
            argN.append(Nitrogens)
            
            os.chdir(pathDir)
        
        if len(argN) <= 1: continue
        
        commonN = []
        for eachN in possible_N:
            foundN = True
            for eachOconf in argN:
                foundConf = False
                if eachN not in [arg_conf_N[conf] for conf in eachOconf]:
                    foundN = False
                    break
            if foundN:
                commonN.append(eachN)
        
        
                
        if commonN:
            allSameConf = True
            for eachN in commonN:
                Nconf = set()
                for eachOconf in argN:
                    for eachConf in eachOconf:
                        if arg_conf_N[eachConf] == eachN:
                            Nconf.add(eachConf)
                if len(Nconf) > 1:
                    allSameConf = False
                    break
                else:
                    commonN.remove(eachN)
            if allSameConf: continue
            
            print "Found common moving nitrogen", 
            for eachN in commonN: print eachN,
            print
            
            for eachState in eachHop.intermediates:
                print str(eachState)
                if "RA82+" in str(eachState): 
                    os.chdir(os.path.join(pathDir, SUB_RUNS_FOLDER, str(eachState)))
                    confs = occonf(keyResidues=["ARGA0082"])
                    for eachConf in confs:
                        print "%s %.3f" % (eachConf.confName, eachConf.occ)
            
                    os.chdir(pathDir)
                else:
                    os.chdir(os.path.join(pathDir, SUB_RUNS_FOLDER, str(eachState)))
                    confs = occonf(keyResidues=["ARGA0082"])
                    for eachConf in confs:
                        print "%s %.3f %s" % (eachConf.confName, eachConf.occ, arg_conf_N[eachConf.confName])
                                
                    os.chdir(pathDir) 
            eachHop.print_hop_seqence()
        
    
def main():
    occupied_arg()
    
if __name__ == "__main__":
    main()