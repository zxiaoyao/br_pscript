#!/usr/bin/env python
'''
Created on Jun 19, 2013

@author: xzhu
'''
import sys
DUMMY_CONFORMER = 211

def fixHead3ByNumberOfProtons(fixList, freeDummyWaterConf=False, reverse=False, ifile = "head3.lst", ofile=sys.stdout):
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

    
    oldLines = open(ifile).readlines()

    newLines = []
    newLines.append(oldLines.pop(0))
    
    for eachLine in oldLines:
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
        
    ofile.writelines(newLines)
    

def fix_head3(fixList, ifile = 'head3.lst'):
    '''
    Fix ionization of states of conformers in head3.lst.
    
    fixList: a list of lists each of which has keys to match the lines in head3.lst
    the conformer that matches the criterir will be fixed in head3.lst
    '''

    lines = open(ifile).readlines()
    for il in range(len(lines)):
        for keys in fixList:
            line_match = True
            for key in keys:
                if lines[il].find(key) == -1:
                    line_match = False
                    break
            if line_match:
                # switch flag to 't'
                lines[il] = lines[il][:21] + 't' + lines[il][22:]
                break

    open(ifile, 'w').writelines(lines)


def freeAllConformers(residues=None, headerFile="head3.lst"):
    '''
    Change the flag of all the conformers of some residues to 'f',
    or change all the residues if "residues==None".
    '''
    
    oldLines = open(headerFile).readlines()
    newLines = []
    newLines.append(oldLines.pop(0))
    
    for eachLine in oldLines:
        resName = eachLine[6:9] + eachLine[11:16]
                
        newLine = eachLine
        if residues != None:
            if resName in residues:
                newLine = eachLine[:21] + 'f' + eachLine[22:]
        else:
            newLine = eachLine[:21] + 'f' + eachLine[22:]

        newLines.append(newLine)
        
    open(headerFile, 'w').writelines(newLines)
    

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
    fixHead3ByNumberOfProtons(res_protonations, freeDummyWaterConf, ofile=sys.stdout)
        


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
