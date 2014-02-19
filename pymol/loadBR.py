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
#     cmd.show("cartoon")
    cmd.show("ribbon")

    cmd.set("cartoon_transparency", 0.7)
    keyResidues = ["ASPA0085", "ARGA0082", "GLUA0194", "GLUA0204", "LYSA0216", "RET", "ASPA0212"]
    for eachRes in keyResidues:
        # retinal's residue sequence id can vary in different pdbs.
        selection = ""
        if eachRes == "RET":
            selection = "resn ret"
        else:
            selection = parseResidue(eachRes)
        
        selection += " and not name c+o+n"
        cmd.show("sticks", selection)
        util.cbag(selection)

cmd.extend("loadBR", loadBR)
