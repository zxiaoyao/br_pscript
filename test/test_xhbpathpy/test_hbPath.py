'''
Created on May 21, 2014

@author: xzhu
'''
import unittest
from xhbpathpy.hbPath import HbPath

class Test(unittest.TestCase):


    def setUp(self):
        self.p = HbPath()
        self.p.initialState.quick_init()
        self.p.keyResidues = self.p.initialState.keyResidues
        self.p.nResidues = len(self.p.keyResidues)


    def tearDown(self):
        pass


    def testGetAllHopSequences(self):
        self.p.getAllHopSequences()
        print len(self.p.hopSequences)
        for eachHop in self.p.hopSequences:
            eachHop.printHop()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()