#!/usr/bin/env python

from pymol import cmd
def showResidue(resName, repr="sticks"):
    rName = resName[:3]
    chainId = resName[3]
    seq = int(resName[4:])
    cmd.show(repr, "resn %s and chain %c and resi %d" % (rName, chainId, seq))

def hideUnoccupiedWater(fileName, threshold=-1.0):
    cmd.hide("lines")
    cmd.show("cartoon")
    cmd.set("cartoon_transparency", 0.8)
    keyResidues = ["ASPA0085", "ARGA0082", "GLUA0194"]
    for eachRes in keyResidues:
        showResidue(eachRes)

    cmd.set("sphere_scale", 0.4)

    keptWaters = []
    for eachLine in open(fileName):
        if not eachLine.startswith("HOHDM"): continue
    	fields = eachLine.split()
	confName = fields[0]
	occ = float(fields[1])
	if occ > float(threshold):
	    continue
	else:
	    keptWaters.append(confName[:3] + confName[5:10])

    print "number of kept waters: ", len(keptWaters)
    cmd.hide("everything", "resn HOH")
    for eachWat in keptWaters:
        chainId = eachWat[3]
	seq = int(eachWat[4:])
	cmd.show("spheres", "resn HOH and chain " + chainId + " and resi " + str(seq))

cmd.extend("hideUnoccupiedWater", hideUnoccupiedWater)
