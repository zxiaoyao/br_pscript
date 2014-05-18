'''
Created on May 17, 2014

@author: xzhu
'''

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