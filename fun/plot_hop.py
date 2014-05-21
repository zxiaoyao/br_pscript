'''
Created on Feb 18, 2014

@author: xzhu
'''

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
setPos = {}
for eachLine in open("hop_node"):
    fields = eachLine.split()
    G.add_node(fields[0], energy=fields[1])
    setPos[fields[0]] = (float(fields[2]), float(fields[3]))
    
for eachLine in open("hop_edge"):
    fields = eachLine.split()
    G.add_edge(fields[0], fields[1])
    
nx.write_dot(G,'test.dot')

# same layout using matplotlib with no labels
plt.title("draw_networkx")
pos=nx.graphviz_layout(G,prog='dot')
nx.draw(G,pos,with_labels=True,arrows=True)
# draw_attr = {'node_color':'green', 'edge_color':'yellow'}
# nx.draw_networkx(G, setPos, **draw_attr)
plt.show()