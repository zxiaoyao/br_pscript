'''
Created on May 18, 2014

@author: xzhu
'''
import unittest
from xhbpathpy.protonationState import ProtonationState

class Test(unittest.TestCase):


    def setUp(self):
        self.p = ProtonationState()
        self.p.keyResidues.append("abc")


    def tearDown(self):
        pass


    def testKeyResidues(self):
        assert("abc" == self.p.keyResidues[0])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testProtonationState']
    unittest.main()