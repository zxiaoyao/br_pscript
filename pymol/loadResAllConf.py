#!/usr/bin/env python
from pymol import cmd
import os

def loadResAllConf(resName, confDir):
    ''' Load all the conformers of a residue in a directory.
    
    The conformers are obtained by splitting the conformers in step2_out.pdb.
    '''
    if not os.path.isdir(confDir):
        raise Exception("conformer directory doesn't exist!")
    
    allConfs = []
    for eachFile in os.listdir(confDir):
        if not os.path.isfile(os.path.join(confDir, eachFile)):
            continue
        
        confName = eachFile[:-4]
#         print confName
        confResName = confName[:3] + confName[5:10]
        
        if resName == confResName:
            allConfs.append(confName)
            
    allConfs = sorted(allConfs, key=lambda x: int(x[-3:]))
    for eachConf in allConfs:
        cmd.load(os.path.join(confDir, eachConf+".pdb"))
            
            
cmd.extend("loadResAllConf", loadResAllConf)
    
    