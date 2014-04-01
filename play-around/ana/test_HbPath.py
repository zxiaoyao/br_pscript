'''
Created on Mar 26, 2014

@author: xzhu
'''
import unittest
import HbPath

class Test(unittest.TestCase):


    def setUp(self):
        self.k = HbPath.HbPath(3)


    def tearDown(self):
        pass


    def test_square(self):
        self.assertEqual(7, self.k.square(), "some")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()