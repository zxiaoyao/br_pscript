'''
Created on May 17, 2014

@author: xzhu
'''
from collections import deque

from protonationState import ProtonationState
from hopSequence import HopSequence

from xmccepy.residue import Residue
from xutility.constant import CONVERT_PROTONATION_SYMBOL, CONVERT_SYMBOL_PROTONATION

'''

@note: 
To load a pathway from a folder in which the calculation has been done,
first read in all the intermediates from the text file "intermediates.txt",
then read all the possible hopping sequences from file "hopSequences.txt".

'''

class HbPath(object):
    '''Pathway from the hydrogen bond network.
    
    '''
    PATH_INFO_FILE = "pathinfo.txt"
    
    ## file name to write all the intermediate protonation states.
    INTERMEDIATES_FNAME = "intermediates.txt"
    
    ## file name to write all the hopping sequences.
    HOPSEQUENCES_FNAME = "hopSequences.txt"
    
    ## file name to write the lowest energy barrier hopping sequences.
    LOWESTHOPSEQ_FNAME = "lowestHopSeq.txt"
    
    def __init__(self):
        '''Constructor.
        
        '''
        ## all the key residues in the pathway.
        self.keyResidues = []
        
        ## initial protonation state.
        self.initialState = ProtonationState()
        
        ## all the possible hopping sequences.
        self.hopSequences = []
        
        ## all the possible protonation states.
        self.protonationStates = set()
        
        ## the lowest energy barrier of this pathway.
        self.lowestEnergyBarrier = 0.0
        
        
    def loadPathInfo(self, fName=PATH_INFO_FILE):
        '''Load the info of the pathway for a file.
        
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
        The other lines give the name of the residues, followed by all their possible protonation states.
         
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
            
            newRes = Residue()
            newRes.resName = fields[0]
            newRes.possibleProtonations = [int(eachProtonation) for eachProtonation in fields[1:]]
            
            self.keyResidues.append(newRes)

        self.initialState.keyResidues = self.keyResidues
        self.initialState.protonations = [int(eachProtonation) for eachProtonation in allLines[-1].split()]
        self.initialState.layer = 1
        
        # the number of residues and the number of protonations in the initial state should match.
        if len(self.keyResidues) != len(self.initialState.protonations):
            raise RuntimeError("Fatal error: Number of residues doesn't match with the initial state")
        
        
    def getAllHopSequences(self):
        '''Get all the possible hopping sequences given an initial state.
        
        The path has to have already loaded an initial state, and will start from the initial state.
        
        '''
#         ProtonationState.keyResidues = self.keyResidues
#         HopSequence.possibleProtonations = self.possibleProtonations
        
        firstHopSequence = HopSequence(self.initialState) 
        sequenceQueue = deque()
        sequenceQueue.append(firstHopSequence)
        
        while sequenceQueue:
            newOutSeq = sequenceQueue.popleft()
            if len(newOutSeq.intermediates) != len(self.keyResidues):
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
        
        
        # Use the same protonation states in the set to constitute hop sequences again.
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
        
        
    def writeIntermediates(self, fname=INTERMEDIATES_FNAME):
        '''Write all the intermediate states in file fname in current directory.
        
        '''
        # sort all the intermediate states, first by layer, then by energy. 
        hbPath.protonationStates = sorted(hbPath.protonationStates, key=lambda state: (state.layer, state.energy)) 
        for i in range(len(hbPath.protonationStates)):
            hbPath.protonationStates[i].stateId = i + 1
            
        fpIntermediates = open(fname, 'w')
        
        
        fpIntermediates.write("%-6s" % "id")
        for res in hbPath.keyResidues:
            fpIntermediates.write("%9s" % res.resName)
            fpIntermediates.write("%10s\n" % "E")
    
        for eachState in hbPath.protonationStates:
            fpIntermediates.write("%-6s" % eachState.stateId)
            for eachProtonation in eachState.protonations:
                fpIntermediates.write("%9s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
            fpIntermediates.write("%10.3f\n" % eachState.energy)
            
        fpIntermediates.close()
        
        
    def writeHopSequences(self, fname=HOPSEQUENCES_FNAME):
        '''Write all the hop sequences in file fname in current directory.
        
        '''
        # sort all the possible hopping sequences, by the energy barrier
         
        fpHop = open(fname, 'w')
        
        for eachSeq in self.hopSequences:
            for eachState in eachSeq.intermediates:
                fpHop.write("%-6s" % eachState.stateId)
            fpHop.write("%10.3f\n" % eachSeq.energyBarrier)
        
            for eachState in eachSeq.intermediates:
                for eachProtonation in eachState.protonations:
                    fpHop.write("%-6s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
                fpHop.write("%10.3f\n" % eachState.energy)
            fpHop.write("\n")
            
        fpHop.close()
        
        
    def writeLowestHopSeq(self, fname=LOWESTHOPSEQ_FNAME):
        '''Write the lowest energy barrier hopping sequences to the file "fname".
        
        Now it's preferred to get this info from all the hopping sequences.
        
        '''
        fpLowE = open(fname, 'w')
        
        for eachSeq in self.hopSequences:
            if eachSeq.energyBarrier == self.lowestEnergyBarrier:
                for eachState in eachSeq.intermediates:
                    fpLowE.write("%-6s" % eachState.stateId)
                fpLowE.write("%10.3f\n" % eachSeq.energyBarrier)
        
                for eachState in eachSeq.intermediates:
                    for eachProtonation in eachState.protonations:
                        fpLowE.write("%-6s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
                    fpLowE.write("%10.3f\n" % eachState.energy)
                fpLowE.write("\n")
            
        fpLowE.close()
        
        
    def evaluateHopSeqEbarrier(self):
        '''Calculate the energy barriers of all the hopping sequences of this pathway.
        
        @note: The lowest energy barrier is calculated here as well.
        
        '''
        for eachSeq in self.hopSequences:
            eachSeq.getEBarrier()
            
        self.lowestEnergyBarrier = self.hopSequences[0].energyBarrier
        for eachSeq in self.hopSequences:
            if eachSeq.energyBarrier < self.lowestEnergyBarrier:
                self.lowestEnergyBarrier = eachSeq.energyBarrier
            
            
    def sortHopSeqByEbarrier(self):
        '''Sort the hop sequences in the list by their energy barrier.
        
        '''
        self.hopSequences = sorted(self.hopSequences, key=lambda seq: seq.energyBarrier)

            
    def readIntermediates(self, fname=INTERMEDIATES_FNAME):
        '''Load the protonation states from the file which has all the states.
        
        There has to be no residue already loaded into the pathway.
        
        '''
        fp = open(fname, 'r')
        
        headers = fp.readline().split()
        
        # if there are already key residues loaded, their names have to be the same as those in the file.
        if len(self.keyResidues) != 0:
            raise RuntimeError("There is already residue loaded in the pathway.")
        else:
            # No residues have been loaded into the pathway.
            for i in range(len(headers)-2):
                newRes = Residue()
                newRes.resName = headers[i+1]
                self.keyResidues.append(newRes)
                
        for eachLine in fp:
            fields = eachLine.split()
            newState = ProtonationState()
            newState.keyResidues = self.keyResidues
            newState.stateId = int(fields[0])
            newState.protonations = [CONVERT_SYMBOL_PROTONATION[eachCrg] for eachCrg in fields[1:-1]]
            newState.energy = float(fields[-1])
            self.protonationStates.add(newState)
        
        fp.close()
        
        
    def readHopSeqences(self, fname=HOPSEQUENCES_FNAME):
        '''Load all the hopping sequences from file.
        
        @note: The intermediate states have to be already loaded into the pathway.
         
        '''
        if len(self.keyResidues) == 0:
            raise RuntimeError("The intermediates have to be loaded first.")
        
        # a look up table to get the protonation state from state id number as show in the file.
        idToState = {}
        for eachState in self.protonationStates:
            idToState[eachState.stateId] = eachState

        fp = open(fname, 'r')
        allLines = fp.readlines()
        
        for i in range(len(allLines)):
            if i % (len(self.keyResidues)+2) != 0: continue
            fields = allLines[i].split()
            newHop = HopSequence()
            for j in fields[:-1]:
                newHop.intermediates.append(idToState[int(j)])
            newHop.energyBarrier = float(fields[-1])
            self.hopSequences.append(newHop)
            
        fp.close()
        
        
    def getHighEstate(self):
        '''Get the highest energy states among all the intermediate states.
        
        '''
        highestE = float("-inf")
         
        for eachState in self.protonationStates:
            if eachState.energy > highestE: highestE = eachState.energy
            
        highState = [] 
        for eachState in self.protonationStates:
            if eachState.energy == highestE: highState.append(eachState)
            
        return highState
        
        