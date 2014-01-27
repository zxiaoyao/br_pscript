#!/usr/bin/python

import os, sys
import networkx as nx

DUMMY_PROTONATION = 211
POSSIBLE_PROTONATIONS = {"ASP":[-1, 0], "GLU":[-1, 0], "ARG":[0, 1], "HOH":[-1, 0, 1], "TRP":[0],\
                         "LYS":[0, 1], "SER":[0], "THR":[0], "TYR":[-1, 0], "RSB":[0, 1], "GLN":[0],\
                         "ASN":[0], "MET":[0]}

def main():
    g = nx.Graph()
    
    resHbFile = "hb.txt"
    
    hbfp = open(resHbFile, 'r')
    weightThreshold = 0.01
    if len(sys.argv) == 2: weightThreshold = float(sys.argv[1])
    edges = []
    for eachLine in hbfp:
        fields = eachLine.split()
        weight = float(fields[2])
        
        # if there is only one possible protonation state of a residue, do not include.
        if (len(POSSIBLE_PROTONATIONS[fields[0][:3]]) == 1): continue
        if (len(POSSIBLE_PROTONATIONS[fields[1][:3]]) == 1): continue
        
        if weight >= weightThreshold:
            edges.append((fields[0], fields[1], float(fields[2])))
    hbfp.close()
                                      
    g.add_weighted_edges_from(edges)
    #print "number of edges: ", g.number_of_edges()
    
    sourceRes = "ASPA0085"
    targetRes = "GLUA0194"
    
    makeNewPathFolder = True
    if (sourceRes in g.nodes()) and (targetRes in g.nodes()) and (nx.has_path(g, sourceRes, targetRes)):
#         fpPath = open("shortestPaths.txt", 'w')
        fpPath = open("allPaths.txt", 'w')

        pathId = 1
        pathCutoff = 6
#         for eachPath in nx.all_shortest_paths(g, sourceRes, targetRes):
        for eachPath in sorted(nx.all_simple_paths(g, sourceRes, targetRes, pathCutoff), key=lambda p: len(p)):    
            print eachPath
            pathName = "path%d" % pathId
            fpPath.write("%-8s" % pathName)
            for eachRes in eachPath:
                fpPath.write("%10s" % eachRes)
            fpPath.write("\n")
            
            if makeNewPathFolder:
                if not os.path.isdir(pathName):
                    os.mkdir(pathName)
                os.chdir(pathName)
                
                # need to have "fixedProtonations.txt" in the upper level directory.
                if not os.path.isfile("../fixedProtonations.txt"):
                    os.chdir("..")
                    os.system("/home/xzhu/bin/pythonScript/fix_protonations.py")
                    os.chdir(pathName)
                    
                makePathInfoFile(eachPath)
                
                os.chdir("..")
                            
            pathId += 1
        fpPath.close()
                
    else:
        print "There is no pathway between %s and %s" % (sourceRes, targetRes)

def makePathInfoFile(pathResidues):
    
    resProtonatios = loadResProtonation("../fixedProtonations.txt")
    resProtonatios["ASPA0085"] = 0
    resProtonatios["ARGA0082"] = 1
    resProtonatios["GLUA0194"] = -1
    
    fp = open("pathinfo.txt", 'w')
    for eachRes in pathResidues:
        fp.write("%-10s" % eachRes)
        for eachProtonation in POSSIBLE_PROTONATIONS[eachRes[:3]]:
            fp.write("%4d" % eachProtonation)
        fp.write("\n")
    
    for eachRes in pathResidues:
        initialProtonation = resProtonatios[eachRes]
        # waters always have initial state 0.
        if eachRes[:3] == "HOH":
            initialProtonation = 0
        fp.write("%-4d" % initialProtonation)
    fp.write("\n")
        
    fp.close()
        
def loadResProtonation(fname="fixedProtonations.txt"): 
    resProtonatios = {}
    for eachLine in open(fname, 'r'):
        fields = eachLine.split()
        resProtonatios[fields[0]] = int(fields[1])
    return resProtonatios

if __name__ == "__main__":
    main()
