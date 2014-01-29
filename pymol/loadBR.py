#!/usr/bin/env python
from pymol import cmd, util

def parseResidue(resName):
    resn = resName[:3]
    chainId = resName[3]
    resi = int(resName[4:])
    return ("resn %s and chain %c and resi %d" % (resn, chainId, resi))


def loadBR(pdb, saveName=None, color=None):
    if not saveName:
        saveName = pdb.split('.')[0]
   
    cmd.load(pdb, saveName)

    if color: cmd.color(color, saveName)
    cmd.hide("lines")
    cmd.hide("nonbonded")
    cmd.show("cartoon")

    cmd.set("cartoon_transparency", 0.7)
    keyResidues = ["ASPA0085", "ARGA0082", "GLUA0194", "GLUA0204", "LYSA0216", "RETA0301"]
    for eachRes in keyResidues:
        cmd.show("lines", parseResidue(eachRes))
        util.cbag(parseResidue(eachRes))

cmd.extend("loadBR", loadBR)
