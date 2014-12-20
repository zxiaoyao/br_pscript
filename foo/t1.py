'''
Created on May 27, 2014

@author: xzhu

I'm really very happy that I found it.
Just one number in the ip address of localhost.
'''

import networkx as nx
import matplotlib.pyplot as plt   
import numpy as np
        
if __name__ == '__main__':
    g = nx.Graph()
    g.add_node(1)
    
    plt.subplot(1,1,1)
    plt.plot([1, 3, 4, 5], [2, 6, 8, 3])
    plt.title("example")
    plt.xlabel("x axis")
    plt.ylabel("y axis")
    
    t1 = plt.text(3, 4, "hello pycon")
    t1.set_fontsize(30)
    plt.figtext(0.8, 0.8, "fixed text")
    
    ax = plt.gca()
    ax.annotate("import", xy=(3,3), xytext=(4,4), arrowprops={'facecolor':'r'})
    
    major_locator = plt.MultipleLocator(1)
    ax.xaxis.set_major_locator(major_locator)
    
    fig = plt.gcf()
    fig.set_facecolor('g')
    
    plt.bar([1,2,3], [4,3,5])
    
    
    plt.show()
    
    