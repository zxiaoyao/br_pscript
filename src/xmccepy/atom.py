'''
Created on Apr 1, 2014

@author: xzhu
'''
from corr import Corr


class Atom(object):
    '''
    Atom class
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.corr = Corr()
        self.atomName = ""