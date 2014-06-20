#!/usr/bin/env python
'''
Created on Jun 19, 2013

@author: xzhu
'''
import sys
DUMMY_CONFORMER = 211

class Head3Lst(object):
    '''Head3.lst.
    
    '''
    def __init__(self):
        self.header = ""
        self.hlines = []
        
    
    def readFromFile(self, fname="head3.lst"):
        '''Read head3.lst file.
        
        '''
        fp = open(fname, 'r')
        self.header = fp.readline()
        self.hlines = fp.readlines()
        fp.close()
        
    
    def writeToFile(self, fp=sys.stdout):
        fp.write(self.header)
        for eachLine in self.hlines:
            fp.write(eachLine)
            
            
    def fixByNumberOfProtons(self, fixList, freeDummyWaterConf=False, reverse=False):  
        '''
        Change the flag of conformers in head3.lst.
    
        According to a residue name like "ASPA0085" and the number of protons (-1, 0, 1).
        "fixList" is a dictionary of residue name and number of protons.
        For example:
            fixList = {"ASPA0085":0, "ASPA0212":-1}
        
        if "reverse" is False, the conformers in the residue which have the same number of protons will be fixed.
        if "reverse" is True, it's opposite, only the conformers with the same number of protons are not fixed.

        "fixed" means free to move and the flag is 'f' in head3.lst.    

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
                            
            newLines.append(newLine)
        
        self.hlines = newLines
    
        

    def freeAllConformers(self, residues=None, headerFile="head3.lst"):
        '''
        Change the flag of all the conformers of some residues to 'f',
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
    

def read_fix_protonation_file(fname):
    '''Read the file which has info of fixed residue protonations.
    
    '''
    res_protonations = {}
    for eachLine in open(fname):
        fields = eachLine.split()
        res_protonations[fields[0]] = int(fields[1])
        
    return res_protonations
    
    
def change_hflag_according_to_file(fname, freeDummyWaterConf=False, hfile="head3.lst"):
    '''Change the flag of conformers in head3.lst.
    
    '''
    res_protonations = read_fix_protonation_file(fname)
    
    h3l = Head3Lst()
    h3l.readFromFile(hfile)
    
    h3l.fixByNumberOfProtons(res_protonations, freeDummyWaterConf=False, reverse=True)

    h3l.writeToFile()


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="file has residue protonations")
    parser.add_argument("--freeDummy", action="store_true", help="free all the dummy water conformer")
    
    args = parser.parse_args()

    resProtonfile = args.f
    freeDummyWaterConf = args.freeDummy

    change_hflag_according_to_file(resProtonfile, freeDummyWaterConf)        
        
        
if __name__ == '__main__':
    main()
