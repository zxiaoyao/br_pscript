'''
Created on Mar 18, 2014

@author: xzhu
'''
import networkx as nx


if __name__ == '__main__':
    g = nx.Graph()
    g.add_edge('a', 'b')
    g.add_edge('a', 'c')
    g.add_edge('a', 'd')
    g.add_edge('c', 'd')
    
    print g.nodes()
    
    