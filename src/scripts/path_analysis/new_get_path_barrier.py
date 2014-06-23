#!/usr/bin/env python
# encoding: utf-8
'''
scripts.path_analysis.new_get_path_barrier -- Get the energy barrier of a pathway and more..

scripts.path_analysis.new_get_path_barrier is a description

It defines classes_and_methods

@author:     xzhu

@copyright:  2014. All rights reserved.

@license:    license

@contact:    zhuxuyu@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2014-06-20'
__updated__ = '2014-06-20'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


#===============================================================================
# The way I use this script:
# 1. In your working directory where you already have "head3.lst", "fort.38", "sum_crg.out",
#    generate a file called "fixedProtonations.txt", in which you need to specify the protonation
#    states of all the residues.
#    You can use -1, 0, 1, or 211. 211 denotes the residue in dummy.
#
# 2. Make a sub directory (e.g "pathdir") in working directory 
# 3. In the sub directory, generate a file called "pathinfo.txt".
#    Specify the residues in the pathway, all their possible protonation states, and the initial state.
#    Refer to the "loadPathInfo" method in class "HbPath" for the file format please.
#
# 3. Go to the working directory, use "get_path_barrier.py -s pathdir" to submit the jobs.
# 4. After all jobs are done, use "get_path_barrier.py -p pathdir" to retrieve the calculated path info.
#    There will be 3 output files in the "pathdir" directory, "hopSequences.txt",
#    "intermediates.txt", and "lowestHopSeq.txt".
#    You can find the lowest energy barrier of the path in the "lowestHopSeq.txt" file.
#===============================================================================
SUB_RUNS_FOLDER = "mSub"
PATH_INFO_FILE = "pathinfo.txt"
DUMMY_PROTONATION = 211

import os, sys, shutil
import copy
import argparse
from collections import deque

from xhbpathpy.hbPath import HbPath
from xhbpathpy.protonationState import ProtonationState
from xhbpathpy.hopSequence import HopSequence

CONVERT_RES_SYMBOL = {"ASP":'D', "GLU":'E', "ARG":'R', "HOH":'O', "TYR":'Y', "RSB":'U'}
CONVERT_PROTONATION_SYMBOL = {-1:'-', 0:'0', +1:'+'}
CONVERT_SYMBOL_PROTONATION = {'-':-1, '0':0, '+':1}


                
def getAllResProtonation(fnHead3="head3.lst", fnCrg="sum_crg.out", fnFort="fort.38"):
    '''Assuming residues are ordinary ones, which only can change their charges by lose or gain protons.
    
    First, get all residues to be considered from "head3.lst". 
    And all the residues are assigned a default protonation state 0.
    
    Then, look through "sum_crg.out".
        if charge >= 0.5, residue protonation state is 1.
        if 0.5 > charge > -0.5, residue protonation state is 0.
        if charge <= -0.5, residue protonation state is -1.
        
    At last look through "fort.38" for the dummy conformers.
    If the occupancy of the dummy conformer is greater than 0.5, the residue state is DUMMY_PROTONATION.
    '''
    
    allResidues = set()
    
    allHLines = open(fnHead3, 'r').readlines()
    allHLines.pop(0)
    for eachLine in allHLines:
        allResidues.add(eachLine[6:9] + eachLine[11:16])
        
    resProtonations = {}
    for eachRes in allResidues:
        resProtonations[eachRes] = 0
        
    allCLines = open(fnCrg, 'r').readlines()
    allCLines.pop(0)
    for eachLine in allCLines[:-4]:
        fields = eachLine.split()
        resName = fields[0][:3] + fields[0][4:9]
        crg = float(fields[1])
        if crg >= 0.5:
            resProtonations[resName] = 1
        elif crg > -0.5:
            resProtonations[resName] = 0
        else:
            resProtonations[resName] = -1
            
    allFLines = open(fnFort, 'r').readlines()
    allFLines.pop(0)
    for eachLine in allFLines:
        if eachLine[:5] == "HOHDM":   # deal with dummy conformers, only consider waters
            occ = float(eachLine.split()[1])
            if occ > 0.5:
                resProtonations[eachLine[:3] + eachLine[5:10]] = DUMMY_PROTONATION
            
    return resProtonations
 
        
def getConfProtonation(confName):
    '''
    Get the protonation state of a conformer ONLY by its name.
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


def alterHead3ByProtonation(resProtonations, hbPath, fName="head3.lst", keepDummy=False):
    newLines = []
    allLines = open(fName, 'r').readlines()
    newLines.append(allLines.pop(0))
        
    for eachLine in allLines:
        confName = eachLine[6:20]
        resName = eachLine[6:9] + eachLine[11:16]
        
        # only fix the protonations of residues in path
        # the other residues are free to change protonations, except those whose protonations are already fixed.
        
        # by default the protonation states of residues are fixed.
        # This can be changed by adding one option "fixed=False" at the end of the program arguments

#         if not resName in hbPath.keyResidues:
#             newLines.append(eachLine) 
#             continue
        
        fixedProtonation = resProtonations[resName]
        
        # special treat for the dummy water conformers.
        # if it's not fixed to be dummy then always keep the dummy conformers of waters not in the pathway.
        if (resName not in hbPath.keyResidues) and resName[:3] == "HOH":
            if keepDummy and fixedProtonation != DUMMY_PROTONATION:
                if getConfProtonation(confName) == DUMMY_PROTONATION:
                    newLines.append(eachLine[:21] + 'f 0.00' + eachLine[27:])
                    continue
                
        if getConfProtonation(confName) == fixedProtonation:
            newLines.append(eachLine[:21] + 'f 0.00' + eachLine[27:])
        else:
            newLines.append(eachLine[:21] + 't 0.00' + eachLine[27:])
            
    open("head3.lst", 'w').writelines(newLines)        


def write_ms_gold(keyResidues):
    ''' write the key residues into "ms_gold" file.
    '''
    
    fp = open("ms_gold", 'w')
    for eachRes in keyResidues:
        fp.write(eachRes + '\n')
    fp.close()
   
   
def loadResProtonation(fname="fixedProtonations.txt"):
    '''Return the protonation states of all residues in a dictionary.
    ''' 
    resProtonatios = {}
    for eachLine in open(fname, 'r'):
        fields = eachLine.split()
        resProtonatios[fields[0]] = int(fields[1])
    return resProtonatios
     
    
def submit_subruns(hbPath, parentPath, runPath):
    '''Submit all the sub runs for a pathway.
    
    Things done here:
    1. create a container folder to contain all the sub runs for each protonation state.
    2. create a folder for each sub run within the container folder.
    3. copy or link necessary files in the parent folder to the sub folder.
    4. modify head3.lst according to the protonation states in each sub run.
    5. submit the job to SGE.
    
    '''
    from xmccepy.runPrm import RunPrm
    from xmccepy.head3Lst import Head3Lst

    resProtonations = loadResProtonation(os.path.join(parentPath, "fixedProtonations.txt"))
    
    if not os.path.isdir(runPath):
        os.makedirs(runPath, 0755)
    os.chdir(runPath)
    
    for eachState in hbPath.protonationStates:            
        if not os.path.isdir(str(eachState)):
            os.mkdir(str(eachState))
            
        os.chdir(str(eachState))
        
        # calculation has already been done.
        if os.path.isfile("pK.out") and len(open("pK.out").readlines()) != 0:
            print "Already has pK.out in", os.getcwd()
            os.chdir("..")
            continue
        
        
        files_to_link = ["energies.opp", "extra.tpl"]
        for eachFile in files_to_link:
            if not os.path.islink(eachFile):
                os.system("ln -s " + os.path.join(parentPath, eachFile) + " .")
                
                
        files_to_copy = ["head3.lst", "run.prm"]
        for eachFile in files_to_copy:
            shutil.copy(os.path.join(parentPath, eachFile), ".")
            
            
        for i in range(len(hbPath.keyResidues)):
            resProtonations[hbPath.keyResidues[i].resName] = eachState.protonations[i]
            
        # copy head3.lst from parent directory and modify it accordingly.
        # modify the flags in head3.lst according to the protonation states of residues.
        h3l = Head3Lst()
        h3l.readFromFile()
        h3l.fixByNumberOfProtons(resProtonations, freeDummyWaterConf=True, reverse=True)
        h3l.writeToFile("head3.lst")
        
                
        write_ms_gold(hbPath.keyResidues)
        
        
        # modify the run.prm.
        rp = RunPrm()
        rp.readFromFile()
        changePrm = {"MFE_CUTOFF":"10.0", "MONTE_NITER":"2000"}
        rp.mdRunPrm(changePrm)
        rp.writeToFile("run.prm")
        
        
        shutil.copy("/home/xzhu/pfile/submit_temp.sh", ".")
        os.system("qsub submit_temp.sh")
    
        os.chdir("..")


def run_te():
    shutil.copy("/home/xzhu/pfile/submit_te.sh", ".")
    os.system("qsub submit_te.sh")

    
def retrieve_info_from_microstate(hbPath, subFolder):
    '''Get energy of the protonation state from the microstates.
    '''
    
    os.chdir(subFolder)
    te_program_path = "/home/xzhu/gmcce/serialte/te"
    
    for eachState in hbPath.protonationStates:
        os.chdir(str(eachState))
        if os.path.isfile("respair.lst"):
            os.remove("respair.lst")

        if not os.path.isfile("ms_crg") :
            run_te()
        elif len(open("ms_crg").readlines()) != 2:
            run_te()
        
        os.chdir("..")
        
        
def obtain_path_info(hbPath, pathFolder, subRunFolder):
    os.chdir(subRunFolder)
    for eachState in hbPath.protonationStates:
        os.chdir(str(eachState))
        eachState.energy = float(open("ms_crg").readlines()[-1].split()[-4])
        if os.path.isfile("ms.dat"):
            os.remove("ms.dat")
        os.chdir("..")
        
        
    # sort all the intermediate states, first by layer, then by energy. 
    hbPath.protonationStates = sorted(hbPath.protonationStates, key=lambda state: (state.layer, state.energy)) 
    for i in range(len(hbPath.protonationStates)):
        hbPath.protonationStates[i].stateId = i + 1
     
    os.chdir(pathFolder)
    # output of all the intermediate states.      
    fpIntermediates = open("intermediates.txt", 'w')
    fpIntermediates.write("%-6s" % "id")
    for res in hbPath.keyResidues:
        fpIntermediates.write("%9s" % res)
    fpIntermediates.write("%10s\n" % "E")
    
    for eachState in hbPath.protonationStates:
        fpIntermediates.write("%-6s" % eachState.stateId)
        for eachProtonation in eachState.protonations:
            fpIntermediates.write("%9s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
        fpIntermediates.write("%10.3f\n" % eachState.energy)
    fpIntermediates.close()
    
    # sort all the possible hopping sequences, by the energy barrier
    for eachSeq in hbPath.hopSequences:
        eachSeq.getEBarrier()
#         highestE = eachSeq.intermediates[0].energy
#         for eachState in eachSeq.intermediates:
#             if eachState.energy > highestE:
#                 highestE = eachState.energy
#         eachSeq.energyBarrier = highestE - eachSeq.intermediates[0].energy        
    hbPath.hopSequences = sorted(hbPath.hopSequences, key=lambda seq: seq.energyBarrier)
    
    # output all the possible hopping sequences.
    lowestEnergyBarrier = hbPath.hopSequences[0].energyBarrier
    for eachSeq in hbPath.hopSequences:
        if eachSeq.energyBarrier < lowestEnergyBarrier:
            lowestEnergyBarrier = eachSeq.energyBarrier
            
    fpHop = open("hopSequences.txt", 'w')
    fpLowE = open("lowestHopSeq.txt", 'w')
    for eachSeq in hbPath.hopSequences:
        for eachState in eachSeq.intermediates:
            fpHop.write("%-6s" % eachState.stateId)
        fpHop.write("%10.3f\n" % eachSeq.energyBarrier)
        
        for eachState in eachSeq.intermediates:
            for eachProtonation in eachState.protonations:
                fpHop.write("%-6s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
            fpHop.write("%10.3f\n" % eachState.energy)
        fpHop.write("\n")
        
        if eachSeq.energyBarrier == lowestEnergyBarrier:
            for eachState in eachSeq.intermediates:
                fpLowE.write("%-6s" % eachState.stateId)
            fpLowE.write("%10.3f\n" % eachSeq.energyBarrier)
        
            for eachState in eachSeq.intermediates:
                for eachProtonation in eachState.protonations:
                    fpLowE.write("%-6s" % CONVERT_PROTONATION_SYMBOL[eachProtonation])
                fpLowE.write("%10.3f\n" % eachState.energy)
            fpLowE.write("\n")
            
    fpHop.close()
    fpLowE.close()
    
    
def load_path_energy_info(hbPath):
    '''
    Get the energies of intermediate states and energy barriers of different hopping sequences,
    by reading the files "intermediates.txt", "hopSequences.txt".
    '''
    allLines = open("intermediates.txt", 'r').readlines()
    allLines.pop(0)
    
    for eachLine in allLines:
        fields = eachLine.split()
        newState = ProtonationState()
        newState.stateId = fields[0]
        newState.protonations = [CONVERT_SYMBOL_PROTONATION[eachCrg] for eachCrg in fields[1:-1]]
        newState.energy = float(fields[-1])
        
        for eachState in hbPath.protonationStates:
            if eachState.protonations == newState.protonations:
                eachState.stateId = newState.stateId
                eachState.energy = newState.energy
                break
            
    for eachSeq in hbPath.hopSequences:
        eachSeq.getEBarrier()
      

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

    Created by xzhu on %s.
    Copyright 2014 . All rights reserved.

    Licensed under the Apache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0

    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.

    USAGE
    ''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        parser.add_argument("-s", action="store_true", 
                        help="submit the jobs of the sub runs")
        parser.add_argument("-r", action="store_true",
                        help="retrieve the results of the sub runs")
        parser.add_argument("-p", action="store_true", 
                        help="obtain the path information")
        parser.add_argument("-l", action="store_true", 
                        help="print the highest energy state in the lowest energy barrier hopping sequence")
        parser.add_argument("pathName", default="path1", nargs='?',
                        help="name of the path")
#         parser.add_argument("subFolder", default=SUB_RUNS_FOLDER, nargs='?',
#                         help="sub directory name where sub runs are in")
        
        args = parser.parse_args()   
        
        verbose = args.verbose
        if verbose > 0:
            print("Verbose mode on")
            
        pathName = args.pathName
        subRunName = SUB_RUNS_FOLDER
    
        parentPath = os.getcwd()

        pathFolder = os.path.join(parentPath, pathName)

        subRunFolder = os.path.join(pathFolder, subRunName)
        
        pathInfoFile = "pathinfo.txt"
    
        hbPath = HbPath()
        hbPath.loadPathInfo(os.path.join(pathFolder, pathInfoFile))
        hbPath.getAllHopSequences()
    
        
        if args.s:
            submit_subruns(hbPath, parentPath, subRunFolder)
        elif args.r:
            retrieve_info_from_microstate(hbPath, subRunFolder)
        elif args.p:
            obtain_path_info(hbPath, pathFolder, subRunFolder)
        elif args.l:
            pass

        

        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    sys.exit(main())