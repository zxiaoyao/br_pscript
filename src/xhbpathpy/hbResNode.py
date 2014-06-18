'''
Created on Jun 17, 2014

@author: xzhu
'''
from xmccepy.residue import Residue

class HbResNode(object):
    '''
    Node of hb network which represents a residue.
    '''
    PDB_COOR = "step1_out.pdb"
    scale = -50
    
    def __init__(self, resName="", nid=0):
        '''
        Constructor
        '''
        self.id = nid
        
        self.residue = Residue(resName)

                
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
    
    
    def retrieveCorr(self, fname=PDB_COOR):
        '''Get the x,y,z coordinates of the residue node.
    
        For the amino acid, use the coordinates of CB atom.
        For water, use the coordinates of O.
        
        '''
        resName = self.residue.resName
        for eachLine in open(fname):
            rName = eachLine[17:20] + eachLine[21:26]
            if rName != resName: continue
            aName = eachLine[12:16]
            if resName[:3] == "HOH":
                if aName != " O  ": continue
            else:
                if aName != " CB ": continue
        
            self.x = float(eachLine[30:38]) * HbResNode.scale
            self.y = float(eachLine[38:46]) * HbResNode.scale
            self.z = float(eachLine[46:54]) * HbResNode.scale
            break
            
            
    def getResColor(self):
        '''Get the color code for the residue by the type of it.
        
        * neutral residue (unpolar)  0
        * waters                     1
        * acids                      2
        * bases                      3

        '''
        acids = ["ASP", "GLU"]
        bases = ["ARG", "LYS", "RSB"]
        
        resName = self.residue.resName
        if resName[:3] == "HOH": self.color = 1
        elif resName[:3] in acids: self.color = 2
        elif resName[:3] in bases: self.color = 3