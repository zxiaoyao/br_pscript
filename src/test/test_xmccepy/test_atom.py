'''
Created on Apr 1, 2014

@author: xzhu
'''
import unittest
from xmccepy.atom import Atom

class Test(unittest.TestCase):


    def setUp(self):
        self.a = Atom()


    def tearDown(self):
        pass


    def test_atom(self):
        self.assertEqual(self.a.corr.x, 0.0, "initial corrdinate is not 0")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_atom']
    unittest.main()