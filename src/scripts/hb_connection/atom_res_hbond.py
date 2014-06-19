#!/usr/bin/env python
'''
Created on Jun 18, 2014

@author: xzhu
'''

def atomBasedResHb(fname="hah.txt"):
    '''Get the residue hb net from atom connections.
    
    The weight is 0.1.
    
    '''
    edges = set()
    for eachLine in open(fname):
        edges.add((eachLine[:3]+eachLine[5:10], eachLine[15:18]+eachLine[20:25]))
        
    for eachEdge in edges:
        print eachEdge[0], eachEdge[1], "0.1"
        
if __name__ == '__main__':
    atomBasedResHb()