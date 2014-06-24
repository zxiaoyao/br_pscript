'''
Created on Apr 1, 2014

@author: xzhu
'''

class Conformer(object):
    '''
    Conformer class.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.confName = ""
        
        
        ## for now assuming only one titration point.
        self.occ = 0.0
        
        
        
    def __str__(self):
        '''toString.
        
        '''
        return "%s%6.3f" % (self.confName, self.occ)
        