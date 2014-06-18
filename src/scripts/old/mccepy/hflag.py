#!/usr/bin/env python

#
DUMMY_PROTONATION = 211

def alterHead3Flag(rule, reversely=False, outfile="head3.lst", infile="head3.lst"):
    ''' Change flags of conformers in "head3.lst", according to some rules.
    
    
    "rule" is a dictionary specifying the protonation states of residues.
    The key is a residue name, and the values are a list of protonation states.
    
    Only the flags of the conformers with those protonation states are "f".
    If the "reversely" is true, then the flags of the conformers with those protonation states are "t".
    Residues that are not shown in the rules will not be affected.
    
    The outfile could be named differently from "head3.lst", if the "outfile" argument is provided.
    '''
    allLines = open(infile, 'r').readlines()
    headerLine = allLines[0]
    allLines.pop(0)
    
    newLines =[]
    newLines.append(headerLine)
    
    for eachLine in allLines:
        newConf = Conf(eachLine)
        newLines.append(newConf.applyRule(rule, reversely))
        
    open(outfile, 'w').writelines(newLines)
    
class Conf(object):
    def __init__(self, hline=None):
        self.confName = ""
        self.resName = ""
        self.h = 0
        self.flag = 'f'
        
        self.origLine = ""
        
        if hline:
            self.origLine = hline
            fields = hline.split()
            self.confName = fields[1]
            self.resName = self.confName[:3] + self.confName[5:10]
            
            self.h = int(fields[8])
            # for dummy conformer the protonation is not 0, but DUMMY_PROTONATION
            if self.confName[3:5] == "DM":
                self.h = DUMMY_PROTONATION
                
            self.flag = fields[2]
            
    def applyRule(self, rule, resersely=False):
        modifiedLine = self.origLine
        if self.resName not in rule:
            # no rule for this conformer, don't change it.
            pass
        else:
            if self.h in rule[self.resName]:
                if not resersely:
                    modifiedLine = self.origLine[:21] + 'f' + self.origLine[22:]
                else:
                    modifiedLine = self.origLine[:21] + 't' + self.origLine[22:]
            else:
                if not resersely:
                    modifiedLine = self.origLine[:21] + 't' + self.origLine[22:]
                else:
                    modifiedLine = self.origLine[:21] + 'f' + self.origLine[22:]
        
        return modifiedLine
                    
if __name__ == "__main__":
    rule = {"ARGA0007":[0]}
    alterHead3Flag(rule, False, "fun.txt")
     
     