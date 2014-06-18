'''
Created on Jun 17, 2014

@author: xzhu
'''
import networkx as nx

class Name(object):
    def __init__(self, resName=""):
        self.resName = resName

class Node(object):
    def __init__(self, resName="", x=0.0):
        if resName:
            self.name = Name(resName)
        else:
            self.name = Name()
        self.x = x
        
    def __hash__(self):
        return hash(self.name.resName)
    
    def __cmp__(self, other):
        return self.name.resName > other.name.resName
    
# class Edge(object):
#     def __init__(self):
    
if __name__ == '__main__':
    g = nx.Graph()
    
    n1 = Node("a")
    n2 = Node("a")
    n3 = Node("b")
    n4 = Node("c")
    n5 = Node("d")
    n1.x = 10
    n2.x = 100
    
    allNodes = set()
    allNodes.add(n1)
    allNodes.add(n2)
    allNodes.add(n3)
    allNodes.add(n4)
    allNodes.add(n5)
    
    g.add_edge(n3, n1, weight=1.0)
    g.add_edge(n4, n2, weight=0.1)
    
    g.add_edge(n4, n5, weight=0.5)
    
    print "%d nodes:" % len(g.nodes())
    for eachNode in g.nodes():
        print id(eachNode)
    
    print "\n%d edges:" % len(g.edges(data=True))
#     for eachNode in g.nodes():
#         eachNode.x = 999
#         
    for u,v,edata in g.edges(data=True):
        print u.x, v.x, id(u), id(v)
        print edata["weight"]
