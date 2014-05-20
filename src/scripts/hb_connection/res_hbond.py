#!/usr/bin/env python
import sys
import networkx as nx
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fName", help="hb network file name")
    parser.add_argument("-t", dest="threshold", help="threshold to add an edge", type=float, default=-1.0)
    parser.add_argument("-source", help="source node", default="ASPA0085")
    parser.add_argument("-target", help="target node", default="GLUA0194")
    parser.add_argument("-lenLessThan", help="longest length a path has", default=6)
    args = parser.parse_args()
    
    fName = args.fName
    edgeCutoff = args.threshold
    pathCutoff = args.lenLessThan
    
    MIDDLE_RES = "ARGA0082"
    
    g = nx.Graph()
    for eachLine in open(fName):
        fields = eachLine.split()
        if len(fields) == 3 and float(fields[2]) < edgeCutoff:
            continue
        g.add_edge(fields[0], fields[1])
        
    sourceRes = args.source
    targetRes = args.target
    
    if (sourceRes in g.nodes()) and (targetRes in g.nodes()) and (nx.has_path(g, sourceRes, targetRes)):
        for eachPath in sorted(nx.all_simple_paths(g, sourceRes, targetRes, pathCutoff), key=lambda p: len(p)):
            print eachPath
    else:
        print "No path"
        
        if (sourceRes in g.nodes()) and (targetRes in g.nodes()):
            print "Both %s and %s in the network but are not connected" % (sourceRes, targetRes)
            
        if sourceRes in g.nodes():
            print "%s in: " % sourceRes, nx.node_connected_component(g, sourceRes)
            if MIDDLE_RES in nx.node_connected_component(g, sourceRes):
                print "%s connecting with %s" % (MIDDLE_RES, sourceRes)
                
        if targetRes in g.nodes():
            print "%s in: " % targetRes, nx.node_connected_component(g, targetRes) 
            if MIDDLE_RES in nx.node_connected_component(g, targetRes):
                print "%s connecting with %s" % (MIDDLE_RES, targetRes)
                
        if MIDDLE_RES in g.nodes():
            print "%s in: " % MIDDLE_RES, nx.node_connected_component(g, MIDDLE_RES) 
        
if __name__ == "__main__":
    main()