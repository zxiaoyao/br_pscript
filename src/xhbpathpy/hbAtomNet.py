'''
Created on Jun 17, 2014

@author: xzhu
'''
import networkx as nx

from hbAtomNode import HbAtomNode
from hbAtomEdge import HbAtomEdge

class HbAtomNet(object):
    '''
    Hydrogen bond network.
    '''
    
    ## default name for the text file "hb.txt".
    HB_TXT = "atomreshb.txt"
    
    COOR_PDB = "step1_out.pdb"

    def __init__(self):
        '''
        Constructor
        '''
        ## The underlying structure of a res hb net is still directed.
        self.graph = nx.DiGraph()
        
    @staticmethod
    def weightToWidth(weight):
        '''Convert weight of edge to the width of edge in cytoscape.
        
        '''
        return 2.0 + 8.0 * weight
    
        
    def readFromHbTxt(self, fname=HB_TXT):
        '''Load the network from hb.txt file.
        
        '''        
        nameToNode = {}
        
        for eachLine in open(fname):
            fields = eachLine.split()
            
            if fields[0] in nameToNode:
                sNode = nameToNode[fields[0]]
            else:
                sNode = HbAtomNode(fields[0])
                nameToNode[fields[0]] = sNode
            
            if fields[1] in nameToNode:
                tNode = nameToNode[fields[1]]
            else:
                tNode = HbAtomNode(fields[1])
                nameToNode[fields[1]] = tNode
            
            eAttr = HbAtomEdge()
            eAttr.sNode = sNode
            eAttr.tNode = tNode
            eAttr.weight = float(fields[2])
            eAttr.width = HbAtomNet.weightToWidth(eAttr.weight)
            eAttr.dashed = 0
            
            self.graph.add_edge(sNode, tNode, edata=eAttr)
            
            
    def convertGraph(self, edgeCutoff=0.001, singleEdge=True, undirected=True):
        '''Convert the network into a undirected one with at most a single edge between two residues.
        
        '''
        if undirected:
            g = nx.Graph()
        else:
            g = nx.DiGraph()
            
        if singleEdge:
            for u,v,edata in self.graph.edges(data=True):
                if edata["edata"].weight < edgeCutoff: continue
                if g.has_edge(v, u):
                    if g[v][u]["edata"].weight > edata["edata"].weight: continue
                    else:
                        g.remove_edge(v, u)
                        g.add_edge(u, v, edata=self.graph[u][v]["edata"])
                else: 
                    g.add_edge(u, v, edata=self.graph[u][v]["edata"])
                    
        else:
            for u,v,edata in self.graph.edges(data=True):
                if edata["edata"].weight < edgeCutoff: continue
                g.add_edge(u, v, edata=edata["edata"])
            
        return g 
    

        