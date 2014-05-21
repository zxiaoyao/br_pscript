'''
Created on May 17, 2014

@author: xzhu
'''
from protonationState import ProtonationState
from hopSequence import HopSequence
from xmccepy.residue import Residue
from collections import deque


class HbPath(object):
    PATH_INFO_FILE = "pathinfo.txt"
    
    def __init__(self):
        ## all the key residues in the pathway.
        self.keyResidues = []
        
        ## initial protonation state.
        self.initialState = ProtonationState()
        
        ## number of residues in the pathway.
        self.nResidues = 0
        
        ## all the possible hopping sequences.
        self.hopSequences = []
        
        ## all the possible protonation states.
        self.protonationStates = set()
        
        
    def loadPathInfo(self, fName = PATH_INFO_FILE):
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
        else:
            self.nResidues = len(self.keyResidues)
        
        
    def getAllHopSequences(self):
#         ProtonationState.keyResidues = self.keyResidues
#         HopSequence.possibleProtonations = self.possibleProtonations
        
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