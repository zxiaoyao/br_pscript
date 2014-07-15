#!/usr/bin/env python
# encoding: utf-8
'''
write_gml -- write a graph in a gml file

write_gml is a description

It defines classes_and_methods

@author:     xzhu

@copyright:  2014. All rights reserved.

@license:    license

@contact:    zhuxuyu@gmail.com
@deffield    updated: Updated
'''

import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from xhbpathpy.hbNet import HbNet

__all__ = []
__version__ = 0.1
__date__ = '2014-06-16'
__updated__ = '2014-06-16'


HB_TXT = "hb.txt"
PDB_COOR = "step1_out.pdb"


def write_gml(fname=HB_TXT, pdbCoor=PDB_COOR, edgeCutoff=0.01, singleEdge=True, undirected=True, weighted=True):
    '''Write a gml file for the graph g.
    
    '''
    g = readHbNet(fname, edgeCutoff, singleEdge, undirected, weighted)
    
    print "graph ["
    
    counter = 1
    for eachNode in g.nodes():
        eachNode.id = counter
        
        eachNode.retrieveCorr(pdbCoor)
        eachNode.getResColor()
          
        print eachNode.convertToGml(),
        counter += 1    
        
    for u,v,edata in g.edges(data=True):
        # make the dangling edges dashed.
        if (g.degree(u) == 1 and g.degree(v) != 1) or (g.degree(u) != 1 and g.degree(v) == 1): edata["edata"].dashed = 1
        print edata["edata"].convertToGml(),
        
    
    print "]"
    
    

def readHbNet(fname=HB_TXT, edgeCutoff=0.01, singleEdge=True, undirected=True, weighted=True):
    '''Loat the hb network from file "hb.txt".
    
    Then convert it to another suitable kind of network.
    '''
    hbn = HbNet()
    hbn.readFromEdgeListFile(fname, weighted)
    
    return hbn.convertGraph(edgeCutoff, singleEdge, undirected, weighted)

    
def main(argv=None):
    '''Command line options.'''

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument("-f", help="text file to load the hb net", default=HB_TXT, nargs='?')
    parser.add_argument("-c", help="load edges with prob no less than this number", default=0.01, type=float, nargs='?')
        
    parser.add_argument("--singleedge", action="store_true", default=False, help="load at most one edge between two residues")
    parser.add_argument("--undirected", action="store_true", default=False, help="load the network as an undirected network")
    parser.add_argument("--weighted", action="store_true", default=False, help="load the network as an weighted network")
        
    parser.add_argument("-p", help="the pdb file to load the coordinates", default=PDB_COOR, nargs='?')

    # Process arguments
    args = parser.parse_args()

    write_gml(args.f, args.p, args.c, args.singleedge, args.undirected, args.weighted)
        
    return 0  


if __name__ == "__main__":
    sys.exit(main())