'''
Created on Dec 30, 2014

@author: xzhu
'''
import unittest
from xmccepy.protein import Protein

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        self.assertEqual("one", "oone", "not equal")
        
    
#     def runTest(self):
#         self.testName()

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(Test))
    
    return test_suite


if __name__ == "__main__":
    unittest.main()