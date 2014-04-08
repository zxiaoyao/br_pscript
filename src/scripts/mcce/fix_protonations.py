#!/usr/bin/python

DUMMY_PROTONATION = 211

def getAllResProtonation(fnHead3="head3.lst", fnCrg="sum_crg.out", fnFort="fort.38"):
    '''Assuming residues are ordinary ones, which only can change their charges by lose or gain protons.
    
    The default protonation states of residues are 0.
    Determine the protonation states of residues, first from the "sum_crg.out", then from "fort.38".
    '''
    
    # Get all the residues from "head3.lst".
    allResidues = set()
    
    allHLines = open(fnHead3, 'r').readlines()
    allHLines.pop(0)
    for eachLine in allHLines:
        allResidues.add(eachLine[6:9] + eachLine[11:16])
        
    # Default protonations of all the residues are 0.
    resProtonations = {}
    for eachRes in allResidues:
        resProtonations[eachRes] = 0
        
    # Get the actual protonation states of residues from their charges.
    # 1:  if charge >= 0.5
    # -1: if charge <= -0.5
    # 0:  otherwise.
    allCLines = open(fnCrg, 'r').readlines()
    allCLines.pop(0)
    for eachLine in allCLines[:-4]:
        fields = eachLine.split()
        resName = fields[0][:3] + fields[0][4:9]
        crg = float(fields[1])
        if crg >= 0.5:
            resProtonations[resName] = 1
        elif crg <= -0.5:
            resProtonations[resName] = -1
        else:
            resProtonations[resName] = 0
            
    # deal with dummy conformers, only consider waters
    # if dummy conformer is more than half occupied, the protonation state of a residue is DUMMY_PROTONATION.
    allFLines = open(fnFort, 'r').readlines()
    allFLines.pop(0)
    for eachLine in allFLines:
        if eachLine[3:5] == "DM":   
            occ = float(eachLine.split()[1])
            if occ > 0.5:
                resProtonations[eachLine[:3] + eachLine[5:10]] = DUMMY_PROTONATION
      
    # Sort all the residues first by chain Id, then by sequence number.      
    allResidues = sorted(allResidues, key= lambda res: (res[3], int(res[4:])))
    fpFixProtonation = open("fixedProtonations.txt", 'w')
    for eachRes in allResidues:
        fpFixProtonation.write("%s%5d\n" % (eachRes, resProtonations[eachRes]))
    fpFixProtonation.close()
    
    return resProtonations
        
        
def getConfProtonation(confName):
    '''Get the protonation state of a conformer ONLY by its name.
    '''
    
    if confName[3] == '0':
        return 0
    elif confName[3] == '-':
        return -1
    elif confName[3] == '+':
        return 1
    elif confName[3:5] == "DM":
        return DUMMY_PROTONATION
    else:
        return 0

def main():
    getAllResProtonation()
    
if __name__ == "__main__":
    main()