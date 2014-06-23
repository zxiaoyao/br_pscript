'''
Created on Jun 20, 2014

@author: xzhu
'''
import sys

DUMMY_CONFORMER = 211

class Head3Lst(object):
    '''
    head3.lst
    '''


    def __init__(self):
        '''
        Constructor
        '''
        ## the header line of head3.lst.
        self.header = ""
        
        ## all the other lines for the conformers.
        self.hlines = []
        
        
        
    def readFromFile(self, fname="head3.lst"):
        '''Read head3.lst file.
        
        '''
        fp = open(fname, 'r')
        self.header = fp.readline()
        self.hlines = fp.readlines()
        fp.close()
        
    
    def writeToFile(self, fname=None):
        '''Write all the lines into file stream fp.
        
        '''
        if fname == None:
            fp = sys.stdout
        else:
            fp = open(fname, 'w')
            
        fp.write(self.header)
#         for eachLine in self.hlines:
#             fp.write(eachLine)

        fp.writelines(self.hlines)
        fp.close()
        
            
    def fixByNumberOfProtons(self, fixList, freeDummyWaterConf=False, reverse=False):  
        '''
        Change the flag of conformers in head3.lst.
    
        According to a residue name like "ASPA0085" and the number of protons (-1, 0, 1).
        "fixList" is a dictionary of residue name and number of protons.
        For example:
            fixList = {"ASPA0085":0, "ASPA0212":-1}
        
        if "reverse" is False, the conformers in the residue which have the same number of protons will be fixed.
        if "reverse" is True, it's opposite, only the conformers with the same number of protons are not fixed.

        If freeDummyWaterConf is true, all the dummy conformers of water are fixed to be 'f'.    

        '''
    
        def isDummy(hline):
            '''Check a head3.lst line to see if it's a dummy conformer.
            '''
            return hline[9:11] == "DM"

    
        newLines = []
    
        for eachLine in self.hlines:
            resName = eachLine[6:9] + eachLine[11:16]
            nH = int(eachLine[49:52])
        
            newLine = eachLine
            
            if resName in fixList:
                if not reverse:
                    if isDummy(eachLine):
                        if fixList[resName] == DUMMY_CONFORMER:
                            newLine = eachLine[:21] + 't' + eachLine[22:]
                    elif fixList[resName] == nH:
                        newLine = eachLine[:21] + 't' + eachLine[22:]
                elif reverse:
                    if isDummy(eachLine):
                        if fixList[resName] != DUMMY_CONFORMER:
                            newLine = eachLine[:21] + 't' + eachLine[22:]
                    elif fixList[resName] != nH:
                        newLine = eachLine[:21] + 't' + eachLine[22:]
            
            if freeDummyWaterConf and eachLine[6:11] == "HOHDM":
                newLine = eachLine[:21] + 'f' + eachLine[22:]
                
                
            newLines.append(newLine)
        
        self.hlines = newLines
    
        

    def freeAllConformers(self, residues=None):
        '''
        Change the flag of all the conformers of some specified residues to 'f',
        or change all the residues if "residues==None".
        '''
    
        newLines = []
    
        for eachLine in self.hlines:
            resName = eachLine[6:9] + eachLine[11:16]
                
            newLine = eachLine
            if residues:
                if resName in residues:
                    newLine = eachLine[:21] + 'f' + eachLine[22:]
            else:
                newLine = eachLine[:21] + 'f' + eachLine[22:]

            newLines.append(newLine)
        
        self.hlines = newLines