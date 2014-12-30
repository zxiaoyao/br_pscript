'''
Created on Dec 30, 2014

@author: xzhu
'''
from residue import Residue
from conformer import Conformer


STEP1_OUT_PDB = "step1_out.pdb"

class Protein(object):
    '''
    The protein class.
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        ## all the residues in protein
        residues = []
        
    
    def load_step1_out_pdb(self, fname=STEP1_OUT_PDB):
        '''Load info of protein from step1_out.pdb.
        
        '''
        