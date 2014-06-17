'''
Created on Jun 17, 2014

@author: xzhu
'''
from xmccepy.residue import Residue

class HbResNode(object):
    '''
    Node of hb network which represents a residue.
    '''


    def __init__(self, resName=None):
        '''
        Constructor
        '''
        self.id = 0
        
        if resName:
            self.residue = Residue(resName)
        else:
            self.residue = Residue()
                
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        self.color = 0
        
        
    def __hash__(self):
        '''A node has to be hashable.
        
        '''
        return hash(self.residue.resName)
    
    
    def __cmp__(self, other):
        '''Compare node with another node.
        
        '''
        return self.residue.resName > other.residue.resName
    
    
    def __str__(self):
        return self.residue.resName
    
    
    def convertToGml(self):
        '''Write the node to a gml file.
        
        '''
        res = ""
        
        res += "\tnode [\n"
        res += "\tid %d\n" % self.id
        res += '\tlabel "%s"\n' % self.residue.resName 
        
        res += "\tx %10.3f\n" % self.x 
        res += "\ty %10.3f\n" % self.y 
        res += "\tz %10.3f\n" % self.z
        
        res += "\tcolor %d\n" % self.color
        res += "\t]\n"  
        
        return res