from collections import deque
import pylab as plt
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
    
    def fine_output(self):
        for i in range(len(ProtonationState.keyResidues)):
            print "%10s" % ProtonationState.keyResidues[i],
        print
        
        for i in range(len(ProtonationState.keyResidues)):
            print "%10s" % self.protonations[i],
        print
    
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
