'''
Created on Mar 18, 2014

@author: xzhu
'''
from pymol import cmd


def getAllAtoms(sele):
    '''Get the names of all the atoms in the selection.
    '''
    
    myspace = {'names':[]}

    cmd.iterate(sele, "names.append(name)", space=myspace)
    
    return myspace['names']



def listAtoms(sele):
    print getAllAtoms(sele)
    
def hasHbond(atomName):
    '''Determine if an atom could be a hydrogen bond by its name.
    '''
    
    BACKBONE = ["N", "CA", "C", "O"]
    
    if atomName in BACKBONE:
        return False
    
    if atomName[0] == 'O' or atomName[0] == 'N':
        return True
    else:
        return False
    
    
def showHbBond(sele1, sele2, onlyShortest=True):
    '''Show hydrogen bond between two residues.
    '''
    
    atoms1 = getAllAtoms(sele1)
    atoms2 = getAllAtoms(sele2)
    
    smallestDist = 10000
    smallestDistObj = None
    
    for firstAtom in atoms1:
        if not hasHbond(firstAtom): continue
        firstSele = "name " + firstAtom + " and " + sele1 
        for secondAtom in atoms2:
            if not hasHbond(secondAtom): continue
            secondSele = "name " + secondAtom + " and " + sele2
#             print firstSele
#             print secondSele 
            distName = sele1+firstAtom+'-'+sele2+secondAtom
            tempDist = cmd.distance(distName, firstSele, secondSele)
            
            if tempDist < smallestDist:
                smallestDist = tempDist
                if smallestDistObj:
                    cmd.delete(smallestDistObj)
                smallestDistObj = distName
         
            else:
                cmd.delete(distName)

    
cmd.extend("listAtoms", listAtoms)    
cmd.extend("showHbBond", showHbBond)