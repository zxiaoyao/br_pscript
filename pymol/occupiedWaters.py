#!/user/bin/env python
from pymol import cmd
import os
DUMMY_WATER = 211
def occupiedWaters(sele=None, fName="fixedProtonations.txt"):
    '''Color the occupied waters in a different color.
    '''
    WAT_COLOR = {"IPE_UNOCC":"white", "IPE_OCC":"blue", "CRY_UNOCC":"yellow", "CRY_OCC":"red"}
    
    extra = ""
    if sele: extra = " and %s" % sele
    
    cmd.color(WAT_COLOR["IPE_UNOCC"], "resn hoh and chain x" + extra)
    cmd.set("sphere_scale", "0.1", "resn hoh and chain x" + extra)
    cmd.color(WAT_COLOR["CRY_UNOCC"], "resn hoh and chain a" + extra)
    cmd.set("sphere_scale", "0.2", "resn hoh and chain a" + extra)
    cmd.show("spheres", "resn hoh" + extra)
    
    cmd.set("label_position", (0,-1.5,0))
    
    if os.path.exists(fName):
        counter = 0
        for eachLine in open(fName):
            fields = eachLine.split()
            if fields[0][:3] != "HOH": continue
            chainId = fields[0][3]
            resSeq = int(fields[0][-4:])
            selection = ("resn hoh and chain %c and resi %d" % (chainId, resSeq)) + extra
            
            if int(fields[1]) != DUMMY_WATER:
                cmd.set("sphere_scale", "0.3", selection)
                if chainId == 'A':
                    cmd.color(WAT_COLOR["CRY_OCC"], selection)
                    cmd.label(selection, '"A" + resi')
                elif chainId == 'X':
                    cmd.color(WAT_COLOR["IPE_OCC"], selection)
                    cmd.label(selection, '"X" + resi')
                counter += 1
        print "%d occupied waters colored" % counter
    
cmd.extend("occupiedWaters", occupiedWaters)