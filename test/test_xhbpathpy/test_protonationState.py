'''
Created on May 18, 2014

@author: xzhu
'''
import unittest
from xhbpathpy.protonationState import ProtonationState
from xmccepy.residue import Residue

class Test(unittest.TestCase):


    def setUp(self):
        self.p = ProtonationState()
        self.p.keyResidues.append(Residue("ASPA0085"))
        self.p.protonations = [0]


    def tearDown(self):
        pass


    def testKeyResidues(self):
        assert("ASPA0085" == self.p.keyResidues[0].resName)
        assert("DA850" == str(self.p))
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testProtonationState']
    unittest.main()