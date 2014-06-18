'''
Created on Jun 17, 2014

@author: xzhu
'''


class HbResEdge(object):
    '''
    Edge of a hb network.
    '''


    def __init__(self, sNode=None, tNode=None):
        '''
        Constructor.
        '''
        self.sNode = sNode
        self.tNode = tNode
        
        self.weight = 0.0
        self.width = 0.0
        self.dashed = 0
        
    def convertToGml(self):
        '''Write the edge to gml file.
        
        '''
        res = "\tedge[\n"
    
        res += "\tsource %d\n" % self.sNode.id
        res += "\ttarget %d\n" % self.tNode.id
        res += "\tweight %10.3f\n" % self.weight
        res += "\twidth %10.3f\n" % self.width
        res += "\tdashed %d\n" % self.dashed  
        
        res += "\t]\n"
        
        return res