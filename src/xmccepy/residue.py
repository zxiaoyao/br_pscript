'''
Created on Apr 1, 2014

@author: xzhu
'''
from xmccepy.conformer import Conformer
class Residue(object):
    '''Residue class.
    
    '''
    def __init__(self, resName=""):
        '''Constructor.
        
        '''
        ## name of this residue, like ASPA0085.
        self.resName = resName
        self.chainId = ""
        
        ## All the possible protonation states of this residue in interger number.
        self.possibleProtonations = []
        
        ## All the conformers this residues has. It's an array of conformer type.
        self.conformers = []
        
        
        
    def findFirstMostOccConf(self, fname="fort.38"):
        '''Find first most occupied conformer among all the conformer of this residue in fort.38.
        
        For now assume there is only one titration point in fort.38.
        If there are more than one conformer having the same largest occ, just return the first conformer.
        
        '''
        allLines = open(fname, 'r').readlines()
        
        mostOccConf = Conformer()
        for eachLine in allLines[1:]:
            fields = eachLine.split()
            confName = fields[0]
            rname = confName[:3] + confName[5:10]
            if rname == self.resName:
                occ = float(fields[1])
                if occ > mostOccConf.occ:
                    mostOccConf.confName = confName
                    mostOccConf.occ = occ
                    
        return mostOccConf
                    
            
            
        
        
        
    def loadAllConfFromFort38(self, fname="fort.38"):
        '''Get 
        
        '''
        pass
        
        