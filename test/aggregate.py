'''
Created on Dec 30, 2014

@author: xzhu
'''
import unittest
import test_xmccepy.test_protein
import test_xmccepy.test_atom

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(test_xmccepy.test_atom.suite())
    test_suite.addTest(test_xmccepy.test_protein.suite())

    return test_suite


if __name__ == "__main__":
    test_runner = unittest.TextTestRunner()
    
    test_suite = suite()
    
    
    test_runner.run(test_suite)