'''
Created on Jun 18, 2014

@author: xzhu
'''
import unittest
from xhbpathpy.hbResNet import HbResNet

class Test(unittest.TestCase):


    def setUp(self):
        self.hbn = HbResNet()


    def tearDown(self):
        pass


    def testReadFromHbTxt(self):
        self.hbn.readFromHbTxt()
#         g = self.hbn.convertGraph(edgeCutoff=0.01, singleEdge=True, undirected=True)
#         print len(g.nodes())
            
#         counter = 1
#         for eachNode in self.hbn.graph.nodes():
#             eachNode.id = counter
#             print id(eachNode), eachNode, eachNode.id
#             counter += 1
            
        print "%d nodes:" % len(self.hbn.graph.nodes())
        for eachNode in self.hbn.graph.nodes():
            print eachNode, id(eachNode)
    
        print "\n%d edges:" % len(self.hbn.graph.edges(data=True))
         
        for u,v,edata in self.hbn.graph.edges(data=True):
            print u, id(u), v, id(v)
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()