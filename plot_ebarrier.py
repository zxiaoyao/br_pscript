#!/usr/bin/env python

from hbnet import HbPath
import pylab as plt

        
hbpath = HbPath()
hbpath.load_calculated_path()

x = []
maxState = hbpath.hopSequences[0].intermediates[0]

for eachState in hbpath.hopSequences[0].intermediates:
    x.append(eachState.energy)
    if eachState.energy > maxState.energy:
        maxState = eachState

# maxState.fine_output()
for i in range(len(maxState.keyResidues)):
    print "%10s" % maxState.keyResidues[i],
print "%10.3f" % maxState.energy
        
for i in range(len(maxState.keyResidues)):
    print "%10s" % maxState.protonations[i],
print "%10.3f" % hbpath.hopSequences[0].energyBarrier
# print max(eachState.energy for eachState in hbpath.hopSequences[0].intermediates)
# plt.xticks(range(len(x)))
# plt.plot(x)
plt.show()
    