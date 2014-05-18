'''
Created on May 17, 2014

@author: xzhu
'''

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
                         
 
        