#!/usr/bin/python
'''
Created on Aug 1, 2013

@author: xzhu
'''
import networkx as nx
#import matplotlib.pyplot as plt
from time import time
import os, sys

class ResNode(object):
    def __init__(self, rName="", aName=""):
        self.resName  = rName
        self.atomName = aName
    
    def isSame(self, other):   
        if self.resName == other.resName and self.atomName == other.atomName:
            return True
        else:
            return False
        
    def __repr__(self):
        return self.resName + self.atomName
    
    def __eq__(self, other):
        return (repr(self) == repr(other))
                
    def __hash__(self):
        return hash(repr(self))

class ResEdge(object):
    def __init__(self, dRes=None, aRes=None):
        self.dRes = dRes
        self.aRes = aRes
        
    def isSame(self, other):
        if self.dRes.isSame(other.dRes) and self.aRes.isSame(other.aRes):
            return True
        else:
            return False
    
    def fetchNodes(self):
        return (self.dRes, self.aRes)
        
class Hbond(object):
    def __init__(self, donorConf="", donorAtom="", hAtom="", acceptorConf="", acceptorAtom="", dist=0.0, angle=0):
        self.donorConf = donorConf
        self.donorAtom = donorAtom
        self.hAtom = hAtom
        self.acceptorConf = acceptorConf
        self.acceptorAtom = acceptorAtom
        self.dist = dist
        self.angle = angle;
        
        if self.donorConf:
            self.donorRes = Hbond.confToRes(self.donorConf)
            
        if self.acceptorConf:
            self.acceptorRes = Hbond.confToRes(self.acceptorConf)
    
    @staticmethod
    def confToRes(confName):
        resName = confName[:3] + confName[5:10]
        return resName
     
    def initFromLine(self, line):
        self.donorConf = line[:14]
        self.acceptorConf = line[15:29]
        self.donorAtom = line[30:34]
        self.hAtom = line[35:39]
        self.acceptorAtom = line[41:45]
        self.dist = float(line[46:50])
        self.angle = int(line[51:54])
        
        self.acceptorRes = Hbond.confToRes(self.acceptorConf)
        self.donorRes = Hbond.confToRes(self.donorConf)
        
    def convertToResEdge(self):
        dRes = ResNode(self.donorRes, self.donorAtom)
        aRes = ResNode(self.acceptorRes, self.acceptorAtom)
        
        return ResEdge(dRes, aRes)
    
    def convertToResNodes(self):
        dRes = ResNode(self.donorRes, self.donorAtom)
        aRes = ResNode(self.acceptorRes, self.acceptorAtom)
        
        return (dRes, aRes)
    
class AtomNet(object):
    def __init__(self):
        self.g = nx.DiGraph()
        
    def obtainNetworkFromFile(self, fName="hah.txt"):
        '''
        Get the atom network from "hah.txt" file.
        '''
        for eachline in open("hah.txt", 'r'):        
            newBond = Hbond()
            newBond.initFromLine(eachline)
            self.g.add_edge(*newBond.convertToResNodes())
            
    def obtainNetworkWithOcc(self, fName="hah.txt", occFile="fort.38"):
        pass
            
    def storeInFile(self, fName="atomhb.txt"):
        '''
        Store the atom network in a file named "atomhb.txt".
        '''
        fp = open(fName, 'w')
        for eachEdge in self.g.edges():
            fp.write("%8s%4s%10s%4s\n" % (eachEdge[0].resName, eachEdge[0].atomName, eachEdge[1].resName, eachEdge[1].atomName))
        fp.close()
        
    def store_atomreshb(self, fName="atomhb.txt"):
        '''
        Store the atom network in a file named "atomhb.txt".
        '''
        fp = open(fName, 'w')
        for eachEdge in self.g.edges():
            fp.write("%s%s\t%s%s\n" % (eachEdge[0].resName, eachEdge[0].atomName.strip(), eachEdge[1].resName, eachEdge[1].atomName.strip()))
        fp.close()
            
            
    def loadGraph(self, fName="atomhb.txt"):
        '''
        Get the atom network from "atomhb.txt" file, which has been written to store an atom network.
        '''
        for eachLine in open(fName):
            sourceNode = ResNode(eachLine[:8], eachLine[8:12])
            targetNode = ResNode(eachLine[14:22], eachLine[22:26])
            self.g.add_edge(sourceNode, targetNode)
    
    def printShortestPath(self, sourceNode, targetNode):
        
        print sourceNode.resName, sourceNode.atomName, targetNode.resName, targetNode.atomName,            
        try:
            print len(nx.shortest_path(self.g, sourceNode, targetNode))
#             print len(nx.shortest_path(self.g, sourceNode, targetNode)), nx.shortest_path(self.g, sourceNode, targetNode)

        except:
            print "na"
            
    def shortestPathBetweenResidues(self, sourceRes, targetRes):
        '''
        Get a shortest pathway between each donor atom in sourceRes and each acceptor atom in targetRes,
        if there exists.
        '''
        
        resAtoms = {"ASP":[" OD1", " OD2"], "RSB":[" NZ "], "GLU":[" OE1", " OE2"], "ARG":[" NE ", " NH1", " NH2"]}
        
        sourceNodes = []
        for eachAtom in resAtoms[sourceRes[:3]]:
            sourceNodes.append(ResNode(sourceRes, eachAtom))
            
        targetNodes = []
        for eachAtom in resAtoms[targetRes[:3]]:
            targetNodes.append(ResNode(targetRes, eachAtom))
                        
        for sAtom in sourceNodes:
            for tAtom in targetNodes:
                self.printShortestPath(sAtom, tAtom)
    

def main():   
    time_start = time()
    atomNet = AtomNet()
    atomNet.obtainNetworkFromFile()
#     atomNet.loadGraph()    
    atomNet.store_atomreshb("atomreshb.txt")

#     atomNet.shortestPathBetweenResidues(sys.argv[1], sys.argv[2])
#     atomNet.shortestPathBetweenResidues("ASPA0085", "ARGA0082")
#     atomNet.shortestPathBetweenResidues("ARGA0082", "GLUA0194")
#     atomNet.shortestPathBetweenResidues("ASPA0085", "GLUA0194")
#     
#     atomNet.shortestPathBetweenResidues("RSBA0216", "ASPA0085")
#     atomNet.shortestPathBetweenResidues("ASPA0096", "RSBA0216")
    
    print "Total time: ", time() - time_start
    
if __name__ == '__main__': 
    main()
