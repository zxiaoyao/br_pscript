'''
Created on Jun 17, 2014

@author: xzhu
'''
from xmccepy.atom import Atom

class HbAtomNode(object):
    '''
    Node of hb network which represents a residue.
    '''
    PDB_COOR = "step1_out.pdb"
    scale = -50
    
    def __init__(self, resAtomName="", nid=0):
        '''
        Constructor
        '''
        self.id = nid
        
        self.atom = Atom()
        
        self.resAtomName = ""
                
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        
        self.color = 0
        
        
    def __hash__(self):
        '''A node has to be hashable.
        
        '''
        return hash(self.resAtomName)
                   
    
    
    def __cmp__(self, other):
        '''Compare node with another node.
        
        '''
        return self.resAtomName > other.resAtomName
    
    
    def __str__(self):
        return self.resAtomName
    
    
    @staticmethod
    def shortenResName(resAtomName):
        '''Make the residue name shorter.
        
        @Example: ASPA0085 -> D85
                : HOHX0234 -> x234
                : HOHA0405 -> w405
                : RSBA0216 -> Z216
                
        '''
        THREE_LETTERS_TO_ONE = {"ASP":"D", "GLU":"E", "LYS":"K", "ARG":"R",
                                "GLY":"G", "ALA":"A", "VAL":"V", "LEU":"L",
                                "ILE":"I", "PHE":"F", "PRO":"P", "CYS":"C",
                                "ASN":"N", 
                                "MET":"M", "TRP":"W", "TYR":"Y", "THR": "T",
                                "RSB":"Z", "GLN":"Q", "SER":"S", "ASN":"N"}
        
        resType = resAtomName[:3]
        chainId = resAtomName[3]
        resSeq = int(resAtomName[4:8])
        
        
        shortResName = ""
        # water is special. Crystal waters start with 'w', while ipece water start with 'x'.
        if resType == "HOH":
            if chainId == "A":
                shortResName = "w" + str(resSeq)
            elif chainId == "X":
                shortResName = "x" + str(resSeq)
        # schiff's base.
        elif resType == "RSB":
            shortResName = "SB"
        else:
            # residues other than waters are all in chain A.
            shortResName = THREE_LETTERS_TO_ONE[resType] + str(resSeq)
            
        return shortResName + resAtomName[8:]
    
    
    def convertToGml(self):
        '''Write the node to a gml file.
        
        '''
        res = ""
        
        INDENT = " " * 5
        res += "%snode [\n"  % INDENT
        
        res += "%sid %d\n" % (INDENT, self.id)
        res += '%slabel "%s"\n' % (INDENT, HbAtomNode.shortenResName(self.resAtomName)) 
        
        res += "%sx %d\n" % (INDENT, self.x) 
        res += "%sy %d\n" % (INDENT, self.y) 
        res += "%sz %d\n" % (INDENT, self.z)
        
        res += "%scolor %d\n" % (INDENT, self.color)
        res += "%s]\n" % (INDENT)  
        
        return res
    
    
    def retrieveCorr(self, fname=PDB_COOR):
        '''Get the x,y,z coordinates of the atom node.
    
        For the amino acid, use the coordinates of the atom of the first conformer.
        For water, use the coordinates of O.
        
        '''
        resName = self.resAtomName[:8]
        stripedAtomName = self.resAtomName[8:]
        
        for eachLine in open(fname):
            if eachLine[27:30] != "001": continue
            rName = eachLine[17:20] + eachLine[21:26]
            if rName != resName: continue
            aName = eachLine[12:16].strip()
            if resName[:3] == "HOH":
                if aName != "O": continue
            else:
                if aName != stripedAtomName: continue
        
            self.x = int(float(eachLine[30:38]) * HbAtomNode.scale)
            self.y = int(float(eachLine[38:46]) * HbAtomNode.scale)
            self.z = int(float(eachLine[46:54]) * HbAtomNode.scale)
            break
            
            
    def getAtomColor(self):
        '''Get the color code for the residue by the type of it.
        
        * neutral residue (unpolar)  0
        * waters                     1
        * acids                      2
        * bases                      3

        '''
        acids = ["ASP", "GLU"]
        bases = ["ARG", "LYS", "RSB"]
        
        resName = self.resAtomName[:8]
        if resName[:3] == "HOH": self.color = 1
        elif resName[:3] in acids: self.color = 2
        elif resName[:3] in bases: self.color = 3