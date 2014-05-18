#!/usr/bin/env python
import pylab
import numpy as np

class EnergyTraject(object):
    def __init__(self):
        self.steps = []
        self.energies = []
        self.mcId = 0
        
    def addStep(self, eachLine):
        fields = eachLine.split()
        self.steps.append(int(fields[1][:-1]))
        self.energies.append(float(fields[-1]))
        
    def plot(self):
        pylab.plot(self.steps, self.energies, label="MC"+str(self.mcId))
        

def main():
    allLines = []
    allMC = []

    START_TAG = "Doing MC"

    END_TAG = "The average running energy"

    fp = open("mc_out", 'r')
    beginSave = False
    for eachLine in fp:
        if eachLine.startswith(START_TAG):
            newMC = EnergyTraject()
            newMC.mcId = int(eachLine.split()[2])
            beginSave = True
            continue
    
        if beginSave and (not eachLine.startswith(END_TAG)):
            newMC.addStep(eachLine)
        
        elif beginSave and eachLine.startswith(END_TAG):
            allMC.append(newMC)
            beginSave = False
        
    for eachMC in allMC:
        eachMC.plot()
    pylab.legend(loc=1)
    pylab.show()
    
if __name__ == "__main__":
    main()
        
         
    
        
    
        