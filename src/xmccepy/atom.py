'''
The atom data structure for MCCE.

Created on Apr 1, 2014

@author: xzhu
'''
from corr import Corr


class Atom(object):
    '''Atom class.
    '''

    def __init__(self):
        '''Constructor
        '''
        ## ATOM or HETATM        
        self.groupId = ""
        self.atomSeq = 0

        ## Four letter standard name as in tpl file.
        self.atomName = ""
        self.resName = ""
        self.chainId = ""
        self.resSeq = 0
        self.confSeq = 0
        
        self.corr = Corr()
        
        self.radius = 0.0
        self.charge = 0.0
        self.history = ""
        
        ## The trailing part of a pdb line which is not parsed.
        self.pdbRest = ""
        
        
    def setCorr(self, x=0.0, y=0.0, z=0.0):
        ''' Set the coordinate of the atom.
        '''
        self.corr.set(x, y, z)
        
        
    def readStep1Line(self, sline):
        ''' Read a line in step1_out.pdb.
        
        A line in step1_out.pdb represents an atom with extra info about the conformer.
        @param sline A line from step1_out.pdb.
        '''
        self.groupId = sline[:6]
        self.atomSeq = int(sline[7:11])
        self.atomName = sline[12:16]
        self.resName = sline[17:20]
        self.chainId = sline[21]
        self.resSeq = int(sline[22:26])
        self.confSeq = int(sline[27:30])
        
        self.setCorr(float(sline[30:38]), float(sline[38:46]), float(sline[46:54]))
        
        self.radius = float(sline[56:62])
        self.charge = float(sline[67:74])
        self.history = sline[80:90]
        

        
    def writeStep1Line(self):
        ''' Write atom like a line in step1_out.pdb.
        
        @return A line of atom for step1_out.pdb.
        '''
        return "%-6s %4d %s %s %s%04d_%03d%8.3f%8.3f%8.3f  %6.3f     %7.3f      %s" %\
            (self.groupId, self.atomSeq, self.atomName, self.resName, self.chainId, self.resSeq, self.confSeq,\
             self.corr.x, self.corr.y, self.corr.z, self.radius, self.charge, self.history)
            
    
    def readPdbLine(self, pline):
        ''' Read a line in a standard pdb file.
        @param pline A line in pdb file.
        '''
        self.groupId = pline[:6]
        self.atomSeq = int(pline[7:11])
        self.atomName = pline[12:16]
        self.resName = pline[17:20]
        self.chainId = pline[21]
        self.resSeq = int(pline[22:26])
        
        self.setCorr(float(pline[30:38]), float(pline[38:46]), float(pline[46:54]))
        
        self.radius = float(pline[54:60])
        self.charge = float(pline[60:66])
        self.pdbRest = pline[66:80]
        
        
    def writePdbLine(self):
        ''' Write atom like a line in standard pdb file.
        @return A line of atom for pdb file.
        '''
        if self.chainId != "_":
            return "%-6s %4d %s %s %s%4d    %8.3f%8.3f%8.3f%6.2f%6.2f%s" %\
                (self.groupId, self.atomSeq, self.atomName, self.resName, self.chainId, self.resSeq,\
                 self.corr.x, self.corr.y, self.corr.z, self.radius, self.charge, self.pdbRest)
        else:
            return "%-6s %4d %s %s  %4d    %8.3f%8.3f%8.3f%6.2f%6.2f%s" %\
                (self.groupId, self.atomSeq, self.atomName, self.resName, self.resSeq,\
                 self.corr.x, self.corr.y, self.corr.z, self.radius, self.charge, self.pdbRest)