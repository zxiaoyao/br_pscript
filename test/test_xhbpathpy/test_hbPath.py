'''
Created on May 21, 2014

@author: xzhu
'''
import unittest
from xhbpathpy.hbPath import HbPath

class Test(unittest.TestCase):


    def setUp(self):
        self.p = HbPath()
        self.p.readIntermediates()
        self.p.readHopSeqences()

    def tearDown(self):
        pass


    def testGetAllHopSequences(self):
        assert(len(self.p.keyResidues) == 5)
        assert(len(self.p.protonationStates)==12)
#         assert(len(self.p.hopSequences) == 5)
        for eachHop in self.p.hopSequences:
            eachHop.printHop()
            
        for eachState in self.p.getHighEstate():
            print eachState, eachState.energy


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()