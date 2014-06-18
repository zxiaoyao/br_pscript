'''
Created on Jun 17, 2013

@author: xzhu
'''

from pymol import cmd
import os,sys

def highlightRes(resString, **args):
    resName = resString[:3]
    chainID = resString[3]
    resiID = int(resString[4:])
    
    sele = "resn " + resName + " and  resi " + str(resiID) + " and chain " + chainID
    
    highlightColor = args.get("color", "red")
    cmd.color(highlightColor, sele)
    cmd.show("sticks", sele) 

def loadHbTxt(filePath):
    import networkx as nx
    
    g = nx.Graph()
    for eachLine in open(filePath):
        fields = eachLine.split()
        sourceNode = fields[0]
        targetNode = fields[1]
        hbPossibility = float(fields[2])
        g.add_edge(sourceNode, targetNode, weight=hbPossibility)
        
    return g

def testFun(filePath):
    import networkx as nx
    cmd.delete("all")
    
    cmd.fetch("1C3W")
    cmd.hide("lines", "all")
    cmd.show("cartoon", "1C3W")
    cmd.color("green", "all")
    
    #------------------------------ cmd.color("yellow", "resi 194 and resn GLU")
    #------------------------------- cmd.show("sticks", "resi 194 and resn GLU")
    highlightRes("GLUA0194", color="yellow")
    highlightRes("GLUA0204", color="yellow")
    
        
    g = loadHbTxt(filePath)
    allNodes = nx.node_connected_component(g, "GLUA0194")
    #===========================================================================
    # print allNodes
    #===========================================================================
    
    accRes = {}
    for line in open("/Users/xzhu/sibyl/BR/1C3W/hydro/def/raw/acc.res"):
        fields = line.split()
        resString = fields[1] + fields[2]
        acc = float(fields[4])
        accRes[resString] = acc
    
    colorThreshold = 0.02
    for eachResidue in accRes.keys():
        if accRes[eachResidue] > colorThreshold:
            if eachResidue in allNodes:
                print eachResidue
                highlightRes(eachResidue)
        
    

cmd.extend("tfun", testFun)
