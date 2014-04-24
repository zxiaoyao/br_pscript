'''
A class for the coordinate of a position.

Created on Apr 1, 2014

@author: xzhu
'''

class Corr(object):
    '''
    Corrdinate class.
    '''


    def __init__(self, x=0.0, y=0.0, z=0.0):
        '''Constructor.
        '''
        
        self.x = x
        self.y = y
        self.z = z
        
    def set(self, x=0.0, y=0.0, z=0.0):
        ''' Set the x, y, z values of a coordinate.
        '''
        self.x = x
        self.y = y
        self.z = z
        