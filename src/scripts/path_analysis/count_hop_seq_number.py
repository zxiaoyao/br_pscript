'''
Created on Jun 18, 2014

@author: xzhu
'''
from xhbpathpy.hbPath import HbPath
'''Count the number of different hopping sequence of a pathway.'''

def countHopSeqNumber():
    '''Count number of hopping sequences.
    
    Have to be in a folder where all the files need to get the pathway are there.
    
    '''
    hbp = HbPath() 
    hbp.readIntermediates()
    hbp.readHopSeqences()
    
    return len(hbp.hopSequences)
    
if __name__ == '__main__':
    print countHopSeqNumber()