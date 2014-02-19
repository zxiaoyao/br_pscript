#!/usr/bin/env python
from pymol import cmd
def showFullNameRes(resName, repr="sticks"):
    rName = resName[:3]
    chainId = resName[3]
    seq = int(resName[4:])
    cmd.show(repr, "resn %s and chain %c and resi %d" % (rName, chainId, seq))

def highLightWater(fName, threshold=0.999):
    for eachLine in open(fName):
        waterName = eachLine.split()[0]
	occ = eachLine.split()[1]
	if float(occ) <= threshold:
	    showFullNameRes(waterName, "spheres")
cmd.extend("highLightWater", highLightWater)
