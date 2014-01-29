'''
Created on Nov 1, 2013

@author: xzhu
'''
from pymol import cmd
import networkx as nx

def fullname_to_selection(resName):
    return "resn %s and chain %s and resi %d" % (resName[:3], resName[3], int(resName[4:8]))

def colorWater(pathFile):
    '''Color the unoccupied waters in white, and color waters in network in purple.
    
    "resInHbNet.txt" and "fort.38" have to be in the current directory.
    '''
    
    resInHbFile = "reshbond.txt"
    occFile = "fort.38"
    
    # color the waters white if dummyocc > 0.999
    # color waters in hb network purple
    # don't change colors of the other waters.
    DUMMY_CUTOFF = 0.999
    COLOR_UNOCCUPIED = "white"
    COLOR_IN_HB_NET = "purple"
    RADIUS_UNOCCUPIED = 0.1
    RADIUS_IN_HB_NET = 0.15
    RADIUS_IN_PATH = 0.3
    
    waterDummyOcc = {}
    
    fp = open(occFile)
    fp.readline()
    for eachLine in fp:
        if eachLine.startswith("HOHDM"):
            fields = eachLine.split()
            resName = fields[0][:3] + fields[0][5:10]
            occ = float(fields[1])
            waterDummyOcc[resName] = occ
    fp.close()
    
    waterInHB = set()
    keyResidues = ("ASPA0085", "ARGA0082", "GLUA0194")
    g = nx.Graph()
    for eachLine in open(resInHbFile):
        sourceNode = eachLine.split()[0]
        targetNode = eachLine.split()[1]
        g.add_edge(sourceNode, targetNode)
    print "node number ", nx.number_of_nodes(g)
    
    for eachRes in keyResidues:
        if eachRes in g.nodes():
            for eachNei in nx.node_connected_component(g, eachRes):
                if eachNei[:3] == "HOH":
                    waterInHB.add(eachNei)
    print "water connected: ", len(waterInHB)
            
    waterInPath = set()
    for eachLine in open(pathFile):
        if not eachLine.startswith("path"): continue
        fields = eachLine.split()
        for eachField in fields:
            if eachField.startswith("HOH"):
                waterInPath.add(eachField)
                
    print "water in path: ", len(waterInPath)
#     for eachWater in waterInPath:
#         print eachWater
    
            
    cmd.set("sphere_scale", RADIUS_UNOCCUPIED)
    
    for eachWater, occ in waterDummyOcc.items():
        if occ > DUMMY_CUTOFF:
            cmd.color(COLOR_UNOCCUPIED, fullname_to_selection(eachWater))
            
        elif eachWater in waterInHB:
            cmd.color(COLOR_IN_HB_NET, fullname_to_selection(eachWater))
            if eachWater in waterInPath:
                cmd.set("sphere_scale", RADIUS_IN_PATH, fullname_to_selection(eachWater))
            else:
                cmd.set("sphere_scale", RADIUS_IN_HB_NET, fullname_to_selection(eachWater))
            
cmd.extend("colorWater", colorWater)
    