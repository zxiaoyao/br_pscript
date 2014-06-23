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
    
    
    @staticmethod
    def shortenResName(resName):
        '''Make the residue name shorter.
        
        @Example: ASPA0085 -> D85
                : HOHX0234 -> x234
                : HOHA0405 -> w405
                : RSBA0216 -> Z216
                
        '''
        THREE_LETTERS_TO_ONE = {"ASP":"D", "GLU":"E", "LYS":"K", "ARG":"R",
                                "MET":"M", "TRP":"W", "TYR":"Y", "THR": "T",
                                "RSB":"Z", "GLN":"Q"}
        
        resType = resName[:3]
        chainId = resName[3]
        resSeq = int(resName[4:])
        
        # water is special. Crystal waters start with 'w', while ipece water start with 'x'.
        if resType == "HOH":
            if chainId == "A":
                return "w" + str(resSeq)
            elif chainId == "X":
                return "x" + str(resSeq)
        # schiff's base.
        elif resType == "RSB":
            return "SB"
        else:
            # residues other than waters are all in chain A.
            return THREE_LETTERS_TO_ONE[resType] + str(resSeq)
    
    
    def convertToGml(self):
        '''Write the node to a gml file.
        
        '''
        res = ""
        
        INDENT = " " * 5
        res += "%snode [\n"  % INDENT
        
        res += "%sid %d\n" % (INDENT, self.id)
        res += '%slabel "%s"\n' % (INDENT, HbResNode.shortenResName(self.residue.resName)) 
        
        res += "%sx %d\n" % (INDENT, self.x) 
        res += "%sy %d\n" % (INDENT, self.y) 
        res += "%sz %d\n" % (INDENT, self.z)
        
        res += "%scolor %d\n" % (INDENT, self.color)
        res += "%s]\n" % (INDENT)  
        
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
        
            self.x = int(float(eachLine[30:38]) * HbResNode.scale)
            self.y = int(float(eachLine[38:46]) * HbResNode.scale)
            self.z = int(float(eachLine[46:54]) * HbResNode.scale)
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