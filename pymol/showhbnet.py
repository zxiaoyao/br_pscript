#!/usr/bin/env python
from pymol import cmd
from pymol import util
from sets import Set

pdb = "1KG9"
cmd.load("../raw/"+pdb+".pdb", pdb)
cmd.hide("lines")
cmd.hide("nonbonded")
cmd.show("cartoon")
cmd.color("wheat", "all")
pathResidues = []
for line in open("hb.txt"):
    r1 = line.split()[0]
    r2 = line.split()[1]
    if r1 not in pathResidues:
        pathResidues.append(r1)
    if r2 not in pathResidues:
        pathResidues.append(r2)

#for line in open("pathStatistics.txt"):
#    for eachRes in line.split()[1:-2]:
#        if eachRes not in pathResidues:
#            pathResidues.append(eachRes)
cmd.set("stick_radius", 0.1)
selection = ""
for eachRes in pathResidues:
    print eachRes
    resName = eachRes[:3]
    chainId = eachRes[3]
    resSeq = int(eachRes[4:])
  
    selection += "(r. %s and c. %c and i. %d)" % (resName, chainId, resSeq)
    selection += " or "

    if resName == "HOH":
        cmd.show("spheres", "resn %s and chain %c and resi %d and %s" % (resName, chainId, resSeq, pdb))
        cmd.show("lines", "resn %s and chain %c and resi %d and %s" % (resName, chainId, resSeq, pdb))
    else:
        cmd.show("sticks", "%s and resn %s and chain %c and resi %d and not name c+ca+n+o" % (pdb, resName, chainId, resSeq))
        cmd.label("%s and resn %s and chain %c and resi %d and name cb" % (pdb, resName, chainId, resSeq), "resn+resi")
        util.cbag("%s and resn %s and chain %c and resi %d and not name c+ca+n+o" % (pdb, resName, chainId, resSeq))
