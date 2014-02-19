#!/usr/bin/env python

from pymol import cmd
def showFullNameRes(resName, repr="sticks"):
    rName = resName[:3]
    chainId = resName[3]
    seq = int(resName[4:])
    cmd.show(repr, "resn %s and chain %c and resi %d" % (rName, chainId, seq))

cmd.extend("showFullNameRes", showFullNameRes)
