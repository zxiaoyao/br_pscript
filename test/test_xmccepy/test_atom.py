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
        
    
    def test_readStep1Line(self):
        sline = "ATOM      1  N   LYS _0001_000  24.966  -0.646  22.314   1.000       1.000      BK____M000"    
        self.a.readStep1Line(sline)
        
        self.assertEqual(self.a.groupId, "ATOM  ", "groupId doesn't match")
        self.assertEqual(self.a.atomSeq, 1, "atomSeq doesn't match")
        self.assertEqual(self.a.atomName, " N  ", "atomName not match")
        self.assertEqual(self.a.resName, "LYS", "resName")
        self.assertEqual(self.a.chainId, "_", "chainId")
        self.assertEqual(self.a.resSeq, 1, "resSeq")
        self.assertEqual(self.a.confSeq, 0, "confSeq")
        self.assertEqual(self.a.corr.x, 24.966, "corr.x")
        
        
    def test_fun(self):
        self.assertEqual(1, 1, "oK")
    
#     def runTest(self):
#         self.test_atom()
#         self.test_readStep1Line()
        
        
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(Test))
    
    return test_suite


        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_atom']
    unittest.main()