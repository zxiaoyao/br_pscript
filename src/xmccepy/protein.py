'''
Created on Dec 30, 2014

@author: xzhu
'''
from residue import Residue

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