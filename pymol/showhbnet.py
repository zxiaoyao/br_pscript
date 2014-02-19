#!/usr/bin/env python
from pymol import cmd
from pymol import util
import networkx as nx

def isShowing(g, resName):
    keyRes = ("ASPA0085", "ARGA0082", "GLUA0194", "GLUA0204")

    for eachRes in keyRes:
        if nx.shortest_path(g, resName, eachRes):
            return True

    return False

def showhbnet(hbFile="hb.txt"):
    
    g = nx.Graph()
    pathResidues = []
    for line in open(hbFile):
        
        r1 = line.split()[0]
        r2 = line.split()[1]
        if r1 not in pathResidues:
            pathResidues.append(r1)
        if r2 not in pathResidues:
            pathResidues.append(r2)
        g.add_edge(r1, r2)
        
    cmd.set("sphere_transparency", 0.7)
    cmd.set("line_width", 0.5)
    
    for eachRes in pathResidues:
        if not isShowing(g, eachRes): continue
        resName = eachRes[:3]
        chainId = eachRes[3]
        resSeq = int(eachRes[4:])
        
        if eachRes == "RSBA0216":
            selection = "(r. lys and c. a and i. 216) or (r. ret)"
            cmd.show("lines", selection)
            cmd.label("r. lys and c. a and i. 216 and name ca", '"RSB"')
            util.cbag(selection)
            continue
        
        
        selection = "(r. %s and c. %c and i. %d)" % (resName, chainId, resSeq)
        if resName == "HOH":
            cmd.show("spheres", selection)
            cmd.set("sphere_scale", 0.15)
            cmd.label(selection, "chain+resi")

        else:
            cmd.show("lines", selection)
            cmd.label(selection+" and name ca", "resn+resi")
            util.cbag(selection)
    cmd.hide("everything", "h.")

cmd.extend("showhbnet", showhbnet)