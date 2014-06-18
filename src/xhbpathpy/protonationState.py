'''
Created on May 17, 2014

@author: xzhu
'''
from xutility.constant import CONVERT_RES_SYMBOL, CONVERT_PROTONATION_SYMBOL
from xmccepy.residue import Residue

class ProtonationState(object):
        
    def __init__(self):
        '''Constructor.
        
        '''
        ## keyResidues is of Residue type.
        self.keyResidues = []
        
        self.protonations = []
        self.energy = 0.0
        self.stateId = 0
        self.layer = 0       # which layer this state appears
        
                
    def __repr__(self):
        stateName = ""
        for i in range(len(self.keyResidues)):
            stateName += CONVERT_RES_SYMBOL[self.keyResidues[i].resName[:3]]
            stateName += self.keyResidues[i].resName[3]
            stateName += str(int(self.keyResidues[i].resName[4:]))
            stateName += CONVERT_PROTONATION_SYMBOL[self.protonations[i]]
        
        return stateName
    
    
    def __eq__(self, other):
        return repr(self) == repr(other)
    
    
    def __hash__(self):
        return hash(repr(self))
    
    
    def quick_init(self):
        '''Quickly initialize a new protonation state.
        
        '''
        self.keyResidues = [Residue("ASPA0085"), Residue("HOHX0292"), Residue("ARGA0082"), Residue("HOHX0234"), Residue("GLUA0194")]
        
        self.protonations = [0,   0,   1,   0,   -1]
        
        self.keyResidues[0].possibleProtonations = [-1, 0]
        self.keyResidues[1].possibleProtonations = [0, 1]
        self.keyResidues[2].possibleProtonations = [0, 1]
        self.keyResidues[3].possibleProtonations = [0, 1]
        self.keyResidues[4].possibleProtonations = [-1, 0]
        
    def printState(self):
        '''Print this protonation state.
        
        '''
        for i in range(len(self.keyResidues)):
            print "%10s" % self.keyResidues[i].resName,
        print
        
        for i in range(len(self.keyResidues)):
            print "%10s" % self.protonations[i],
        print
