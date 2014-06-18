'''
Created on Jun 25, 2013

@author: xzhu
'''

import networkx as nx

class ResHbNetwork(object):
    '''
    classdocs
    '''


    def __init__(self, fileName=None):
        '''
        Constructor
        '''
        self.graph = nx.Graph()
        
        if fileName != None:
            self.loadFromFile(fileName)
            
    def loadFromFile(self, fileName):
        '''
        Load network from a text file, e.g. "hb.txt"
        '''
        self.graph = nx.read_weighted_edgelist(fileName)
        
    def getAllShortestPaths(self, source, target):
        return nx.shortest_path(self.graph, source, target)
    
    def getSecondShortestPaths(self, source, target):
        allPaths = []
        shortestPathLength = nx.shortest_path_length(self.graph, source, target)
        for eachPath in nx.all_simple_paths(self.graph, source, target, shortestPathLength+2):
            if len(eachPath) ==  shortestPathLength + 2:
                allPaths.append(eachPath)
        return allPaths
    
    def getNumberOfShortestPaths(self, source, target): 
        
        return sum(1 for p in nx.all_shortest_paths(self.graph, source, target)) #@UnusedVariable
        
    
        