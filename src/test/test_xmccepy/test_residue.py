'''
Created on Apr 1, 2014

@author: xzhu
'''
import unittest
from xmccepy.residue import Residue

class Test(unittest.TestCase):


    def setUp(self):
        self.r = Residue()
        self.r.resName = "ASP"


    def tearDown(self):
        pass


    def test_name(self):
        self.assertEqual(self.r.resName, "ASP", "residue name incorrect")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()