#!/usr/bin/env python
'''
Created on Aug 9, 2013

@author: xzhu
'''
import os, sys
import networkx as nx

def main(fName="cppzk.txt"):
    g = nx.Graph()
    for eachLine in open(fName):
        fields = eachLine.split()
        g.add_edge(fields[0], fields[1])
         
#     keyConns = [["ASPA0085", "ARGA0082"], ["ARGA0082", "GLUA0194"]]
    keyConns = [["ASPA0085", "GLUA0194"]]
#     keyConns = [["ASPA0085", "ARGA0082"], ["ARGA0082", "GLUA0194"], ["ASPA0085", "GLUA0194"]]

    keyAtoms = {"ASPA0085":["OD1", "OD2"], "ARGA0082":["NE", "NH1", "NH2"], "GLUA0194":["OE1", "OE2"]}
    
    for eachConn in keyConns:
        sourceRes = eachConn[0]
        targetRes = eachConn[1]
        
        for eachSourceAtom in keyAtoms[sourceRes]:
            sourceAtom = sourceRes + eachSourceAtom
            if sourceAtom not in g.nodes(): continue
            for eachTargetAtom in keyAtoms[targetRes]:
                targetAtom = targetRes + eachTargetAtom
                if targetAtom not in g.nodes(): continue
                
                if nx.has_path(g, sourceAtom, targetAtom):
                    print "Path between %13s%13s" % (sourceAtom, targetAtom),
                    print nx.shortest_path(g, sourceAtom, targetAtom)
#                 else:
#                     print "No path between %13s%13s" % (sourceAtom, targetAtom)
        
        
if __name__ == '__main__':
#     print os.getcwd()
    if len(sys.argv) == 1:
        main()
    else:
        main(sys.argv[1])
    