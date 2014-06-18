'''
Created on Apr 1, 2014

@author: xzhu
'''

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
        
        