#!/usr/bin/env python
from pymol import cmd
from pymol import util
import networkx as nx

def isShowing(g, resName):
    ''' Check if a has a hydrogen bonded pathway to any of the key residues.
    '''
    
    KEY_RESIDUES = ("ASPA0085", "ARGA0082", "GLUA0194", "GLUA0204")

    for eachRes in KEY_RESIDUES:
        if nx.shortest_path(g, resName, eachRes):
            return True

    return False

def loadHbNet(hbFile="hb.txt"):
    '''Load the hb.txt file into a network.
    '''
    
    g = nx.Graph()

    for line in open(hbFile):
        
        r1 = line.split()[0]
        r2 = line.split()[1]

        g.add_edge(r1, r2)
        
    return g


def showhbnet(hbFile="hb.txt"):
    
    
    g = loadHbNet(hbFile)
            
    cmd.set("sphere_transparency", 0.7)
    cmd.set("line_width", 0.5)
    
    for eachRes in g.nodes():
        # only show the residues in the network that have connection with the key residues.
        if not isShowing(g, eachRes): continue
        resName = eachRes[:3]
        chainId = eachRes[3]
        resSeq = int(eachRes[4:])
        
        # the schiff's base is specail, it's a combination of Lys216 and the retinal.
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
    
    # hide all the hydrogens.        
    cmd.hide("everything", "h.")

cmd.extend("showhbnet", showhbnet)