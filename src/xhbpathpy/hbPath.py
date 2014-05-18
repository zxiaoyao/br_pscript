'''
Created on May 17, 2014

@author: xzhu
'''

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