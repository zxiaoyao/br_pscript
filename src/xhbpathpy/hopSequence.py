'''
Created on May 17, 2014

@author: xzhu
'''
import copy
class HopSequence(object):
    
    def __init__(self, initialState=None):
        ## Each element is a list of all possible protonation states of a residue.
        self.possibleProtonations = []
        
        ## Save the number of times the protonation state of the residue has been changed. 
        self.hopHistory = []
        self.energyBarrier = 0.0
        
        ## intermediate states during this hopping sequence.
        self.intermediates = []
        
        # if the initial protonation state is given.
        if initialState:
            self.intermediates.append(initialState)
            for i in range(len(initialState.protonations)):
                self.hopHistory.append(0)
                
                
    def nextHop(self):
        '''Get all the hopping sequences from the current one by one proton hop.
        
        '''
        allNewHopSequence = []
        if len(self.intermediates) == 0: 
            raise RuntimeError("Hop sequence has to have initial state to propagate.")
        
        lastState = self.intermediates[-1]
        
        for i in range(len(self.hopHistory) - 1):
            # if the protonation hasn't been changed.
            if self.hopHistory[i] == 0:
                # if this residue can lose a proton.
                if (lastState.protonations[i] - 1) in lastState.keyResidues[i].possibleProtonations:
                    # if the next residue can accept an extra proton.
                    if (lastState.protonations[i+1] + 1) in lastState.keyResidues[i+1].possibleProtonations:
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
        '''Get the energy barrier of this hop sequence.
        
        It's the difference between the highest energy and the energy of the initial state.
        The field energyBarrier will be reset to it.
        '''
        highestE = self.intermediates[0].energy
        for eachState in self.intermediates:
            if eachState.energy > highestE:
                highestE = eachState.energy
                
        self.energyBarrier = highestE - self.intermediates[0].energy
        
        return self.energyBarrier 
    
    
    def printHop(self):
        '''Print this hop sequence.
        
        '''
        self.intermediates[0].printState()
        for eachState in self.intermediates[1:]:
            for i in range(len(eachState.keyResidues)):
                print "%10s" % eachState.protonations[i],
            print
                         
 
        