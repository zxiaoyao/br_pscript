'''
Created on May 16, 2013

@author: xzhu
'''

import os
import mcceutility as mu
import networkx as nx
    
class Parent(object):
    def __init__(self):
        self.keyPair = {"DO_PREMCCE":'f', 'TITR_TYPE':"ph"}
        
    def usedToUpdate(self, fileName="run.fun"):
        fp = open(fileName, 'w')
        for eachKey in self.keyPair:
            fp.write(self.keyPair[eachKey] + '\t' + eachKey + '\n')
        fp.close()
        
class Child(Parent):
    def __init__(self):
        super(Child, self).__init__()
        self.keyPair["DO_PREMCCE"] = 't'
        self.keyPair["DO_MONTE"] = 't'
        
        
def main():
    s = set()
    a = [1,2,4,7]
    b = (3, 7, 4,5)
    c = {'a':1, 'b':"bb"}
    
    p = Parent()
    c = Child()
    
    hb = mu.ResHbNetwork("/Users/xzhu/sibyl/BR/1C3W/hydro/def/lj01/hb.txt")
    #for eachPath in nx.all_simple_paths(hb.graph, "ASPA0085", "GLUA0194", nx.shortest_path_length(hb.graph, "ASPA0085", "GLUA0194")+1):
    #    print eachPath
    #for eachPath in hb.getSecondShortestPaths("ASPA0085", "GLUA0194"):
    #    print eachPath
    print hb.getNumberOfShortestPaths("ASPA0085", "GLUA0194")
    
    
if __name__ == '__main__':
    main()