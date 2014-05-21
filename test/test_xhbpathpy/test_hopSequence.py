'''
Created on May 20, 2014

@author: xzhu
'''
import unittest
from xhbpathpy.hopSequence import HopSequence
from xhbpathpy.protonationState import ProtonationState

class Test(unittest.TestCase):


    def setUp(self):
        self.p = ProtonationState()
        self.p.quick_init()
        self.h = HopSequence(self.p)


    def tearDown(self):
        pass


    def testNextHop(self):
        assert(len(self.h.hopHistory) == 5)
        assert(self.h.energyBarrier == 0.0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()