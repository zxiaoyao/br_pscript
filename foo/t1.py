'''
Created on May 27, 2014

@author: xzhu

I'm really very happy that I found it.
Just one number in the ip address of localhost.
'''

import networkx as nx
import matplotlib.pyplot as plt   
        
if __name__ == '__main__':
    g = nx.Graph()
    g.add_node(1)
    
    plt.plot([1, 3, 4, 5], [2, 6, 8, 3])
    plt.title("example")
    plt.xlabel("x axis")
    plt.ylabel("y axis")
    
    plt.show()
    
    