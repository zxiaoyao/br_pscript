#!/usr/bin/env python

'''
Created on Jun 23, 2014

@author: xzhu
'''


'''Get the network of protonation states that can have proton hops.

Run in the directory of the pathway where the text files having path info reside.
'''


from xhbpathpy.hbPath import HbPath

def get_hop_seq_net():
    '''Get the tree structure of hopping sequences to draw in cytoscape.
    
    '''
    hbpath = HbPath()    
    hbpath.readIntermediates()
    hbpath.readHopSeqences()
    
    INDENT = " " * 5
    
    print "graph ["
    for eachState in hbpath.protonationStates:
        print "%snode [" % INDENT
        print "%sid %d" % (INDENT, eachState.stateId) 
        print '%slabel "%d"' % (INDENT, eachState.stateId)
        print "%senergy %.3f" % (INDENT, eachState.energy) 
        print "%s]" % (INDENT) 
        
    allEdges = set() 
    for eachSeq in hbpath.hopSequences:
        for i in range(len(eachSeq.intermediates)-1):
            allEdges.add((eachSeq.intermediates[i].stateId, eachSeq.intermediates[i+1].stateId))
            
    edgesInLowestE = set()
    for eachSeq in hbpath.getLowestHopSeq():
        for i in range(len(eachSeq.intermediates)-1):
            edgesInLowestE.add((eachSeq.intermediates[i].stateId, eachSeq.intermediates[i+1].stateId))        
    
    for eachEdge in allEdges:
        print "%sedge [" % INDENT
        print "%ssource %d" % (INDENT, eachEdge[0])
        print "%starget %d" % (INDENT, eachEdge[1])
        
        if eachEdge in edgesInLowestE:
            print "%swidth 8" % INDENT
        else:
            print "%swidth 2" % INDENT
            
        print "%s]" % INDENT
    
    print "]"

def main():
    get_hop_seq_net()   
    
        
if __name__ == '__main__':
    main()