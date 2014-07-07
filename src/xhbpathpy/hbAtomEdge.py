'''
Created on Jun 17, 2014

@author: xzhu
'''


class HbAtomEdge(object):
    '''
    Edge of an atom hb network.
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
        INDENT = " " * 5
        
        res = "%sedge [\n" % INDENT
    
        res += "%ssource %d\n" % (INDENT, self.sNode.id)
        res += "%starget %d\n" % (INDENT, self.tNode.id)
        res += "%sweight %.3f\n" % (INDENT, self.weight)
        res += "%swidth %.1f\n" % (INDENT, self.width)
        res += "%sdashed %d\n" % (INDENT, self.dashed)  
        
        res += "%s]\n" % INDENT
        
        return res
    
    
    
        