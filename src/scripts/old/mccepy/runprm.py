'''
Created on Jun 25, 2013

@author: xzhu
'''

class RunprmBase(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.keypair = {}
        
        self.keypair["DO_PREMCCE"] = 'f'
        self.keypair["DO_ROTAMERS"] = 'f'
        self.keypair["DO_ENERGY"] = 'f'
        self.keypair["DO_MONTE"] = 'f'
        
        self.keypair["MINIMIZE_SIZE"] = 't'
        