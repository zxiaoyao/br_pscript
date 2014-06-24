'''
Created on May 17, 2014

@author: xzhu
'''
from xutility.constant import CONVERT_RES_SYMBOL, CONVERT_PROTONATION_SYMBOL
from xmccepy.residue import Residue

class ProtonationState(object):
    '''An intermediate protonation state during proton hopping.
    
    '''    
    def __init__(self):
        '''Constructor.
        
        '''
        ## keyResidues is an array of Residue type.
        self.keyResidues = []
        
        ## an array of integers which are the protonation states.
        self.protonations = []
        self.energy = 0.0
        self.stateId = 0
        self.layer = 0       # which layer this state appears
        
    
    def convertToDirName(self):
        '''Get the name of the correspond directory running this protonation state.
        
        '''
        stateName = ""
        for i in range(len(self.keyResidues)):
            stateName += CONVERT_RES_SYMBOL[self.keyResidues[i].resName[:3]]
            stateName += self.keyResidues[i].resName[3]
            stateName += str(int(self.keyResidues[i].resName[4:]))
            stateName += CONVERT_PROTONATION_SYMBOL[self.protonations[i]]
        
        return stateName
    
    __repr__ = convertToDirName
    
    
    
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
        
        
    def getResProtonMap(self):
        '''Get a map of residue name to residue protonation.
        
        '''
        assert (len(self.keyResidues) == len(self.protonations)), "number of key residues and number of protonations don't match"
        
        res = {}
        for i in range(len(self.keyResidues)):
            res[self.keyResidues[i].resName] = self.protonations[i]
            
        return res
    
    
    def mfeState(self):
        '''Do mfe++ to all the residues in this protonation state.
        
        '''
        mfePath = "/Users/xzhu/sibyl/bin/mfe++"
        
        