'''
Created on May 28, 2014

@author: xzhu
'''
import networkx as nx
import matplotlib.pyplot as plt

def quick_graph(g):
    '''Add nodes to a graph g.
    
    '''
    g.add_node(1, time="now")
    g.add_nodes_from("spam")
    g.add_edge(2, 3)
    g.add_edges_from([(1,2), (2, 4)])
    g[1][2]['color'] = "white"
    
    g.graph["title"] = "hb network"
    


if __name__ == '__main__':
    g = nx.Graph()
    
    quick_graph(g)
    
    print nx.connected_components(g)
    
    nx.draw_graphviz(g)
    plt.show()
    