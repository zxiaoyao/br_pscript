'''
Created on Jun 20, 2014

@author: xzhu
'''

class RunPrm(object):
    '''
    run.prm.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        ## all the lines in run.prm.
        self.rlines = []
        
    
    def readFromFile(self, fname="run.prm"):
        '''Get all the lines from a run.prm file.
        
        '''
        self.rlines = open(fname).readlines()
        
        
    def writeToFile(self, fname=None):
        '''Write all the lines to a run.prm file or print to the console.
        
        '''
        import sys
        
        if fname == None:
            fp = sys.stdout
        else:
            fp = open(fname, 'w')
            
        fp.writelines(self.rlines)
        
        fp.close()
        
        
    def mdRunPrm(self, dirPrm):
        '''Modify the run.prm file according to dirPrm.

        The dirPrm is a {key_string : value_string} dictionary
        "key_string" doesn't include the '()'
        "value_string" has to be a string.
        
        '''
        newLines = []
        
        for eachLine in self.rlines:
            newLine = eachLine
            for ky in dirPrm.keys():
                if eachLine.find('(' + ky + ')') > -1:
                    old_value_len = len(eachLine.split()[0])
                    newLine = dirPrm[ky] + eachLine[old_value_len:]
                    break
                
            newLines.append(newLine)
        
        self.rlines = newLines