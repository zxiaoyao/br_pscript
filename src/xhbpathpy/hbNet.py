'''
Created on Jun 17, 2014

@author: xzhu
'''
import networkx as nx

from hbNode import HbNode
from hbEdge import HbEdge

class HbNet(object):
    '''
    Hydrogen bond network.
    
    This is directed network with all the edges stored. 
    It then could be converted a undirected network with a single edge.
    '''
    
    ## default name for the text file "hb.txt".
    HB_TXT = "hb.txt"
    
    COOR_PDB = "step2_out.pdb"

    def __init__(self):
        '''
        Constructor
        '''
        ## The underlying structure of a hb net is still directed.
        self.graph = nx.DiGraph()
        
    @staticmethod
    def weightToWidth(weight):
        '''Convert weight of edge to the width of edge in cytoscape.
        
        '''
        return 2.0 + 8.0 * weight
    
        
    def readFromEdgeListFile(self, fname=HB_TXT, weighted=True):
        '''Load the network from a file.
        
        The network is represented by all the edges in a text file.
        The edge could be weighted or unweighted.
        
        
        
        '''        
        nameToNode = {}
        
        for eachLine in open(fname):
            fields = eachLine.split()
            
            if fields[0] in nameToNode:
                sNode = nameToNode[fields[0]]
            else:
                sNode = HbNode(fields[0])
                nameToNode[fields[0]] = sNode
            
            if fields[1] in nameToNode:
                tNode = nameToNode[fields[1]]
            else:
                tNode = HbNode(fields[1])
                nameToNode[fields[1]] = tNode
            
            eAttr = HbEdge()
            eAttr.sNode = sNode
            eAttr.tNode = tNode
            
            if weighted:
                eAttr.weight = float(fields[2])
            
            eAttr.width = HbNet.weightToWidth(eAttr.weight)
            eAttr.dashed = 0
            
            self.graph.add_edge(sNode, tNode, edata=eAttr)
            
            
    def convertGraph(self, edgeCutoff=0.001, singleEdge=True, undirected=True, weighted=True):
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
                if weighted and edata["edata"].weight < edgeCutoff: continue
                g.add_edge(u, v, edata=edata["edata"])
            
        return g 
    

        