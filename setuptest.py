#!/usr/bin/env python

# Default setting:
# annealing: 100
# equalibration: 300
# sampling: 2000
# independent sampling: 6

import os, shutil, sys, time
import argparse
import numpy as np
import pylab as pl

from mdRunPrm import mdRunPrm

enerfp = open("energytraject.txt", 'w')

iPlot = 1
fig, axes = pl.subplots(nrows=4, ncols=3)

class MCRunType(object):
    def __init__(self, a=100, e=300, s=2000, i=6):
        self.annealing = a
        self.equilibration = e
        self.sampling = s
        self.indep = i
        
        self.runId = (a, e, s, i)
        self.name = "a%de%ds%di%d" % (self.annealing, self.equilibration, self.sampling, self.indep)
        self.nSubtest = 10
        
        self.avgEnergy = 0.0
        self.stdAvgEnergy = 0.0
        self.avgConfsg = 0.0
        
        
    def submitTest(self, parentPath, workPath):
#         nTest = 10
#         currentPath = os.getcwd()
        os.chdir(workPath)
#         linkFiles = ("head3.lst", "energies.opp", "extra.tpl", "ms_gold")
        linkFiles = ("head3.lst", "energies.opp", "extra.tpl")
        
        if not os.path.isdir(self.name):
            os.mkdir(self.name)
        os.chdir(self.name)
        
        for eachFile in linkFiles:
            os.symlink(os.path.join(parentPath, eachFile), os.path.join(".", eachFile))
            
        shutil.copy("/home/xzhu/pfile/submit.sh", ".")
#         shutil.copy(os.path.join(parentPath, "submit_temp.sh"), "submit.sh")
        
        
        shutil.copy(os.path.join(parentPath, "run.prm"), ".")
        changePrm = {"MONTE_NSTART":str(self.annealing), "MONTE_NEQ":str(self.equilibration),\
                     "MONTE_NITER":str(self.sampling), "MONTE_RUNS":str(self.indep)}
        mdRunPrm(changePrm)
        
        # the directory which all sub runs are in.
        subParentPath = os.getcwd()
        
        for i in range(self.nSubtest):
#             allFiles = ("head3.lst", "energies.opp", "extra.tpl", "submit.sh", "run.prm")
            subrunName = "sub" + str(i+1)
            if not os.path.isdir(subrunName):
                os.mkdir(subrunName)
            os.chdir(subrunName)
#             for eachFile in allFiles:
#                 os.symlink(os.path.join("..", eachFile), os.path.join(".", eachFile))
#             os.system("qsub submit.sh")
            newTestrun = Testrun(subrunName, self.annealing, self.equilibration, self.sampling, self.indep)
            newTestrun.submitRun(subParentPath)
            
            os.chdir(subParentPath)
        
        # need to go back to the current directory for other runs
        os.chdir(workPath)
        
    def checkFinishStatus(self, workPath):
        os.chdir(workPath)
        if not os.path.isdir(self.name):
            print "no directory %s in %s" % (self.name, workPath)
            return
        else:
            os.chdir(self.name)
            
        subParentPath = os.getcwd()
        for i in range(self.nSubtest):
            subrunName = "sub" + str(i+1)
            if not os.path.isdir(subrunName):
                print "no directory %s in %s" % (subrunName, subParentPath)
                return
            else:
                os.chdir(subrunName)
            
            newTestrun = Testrun(subrunName, self.annealing, self.equilibration, self.sampling, self.indep)
            if not newTestrun.isFinished(os.getcwd()):
                print "%s in %s is not finished" % (newTestrun.name, self.name)
                if not os.path.isfile("mc_out"):
                    print "mc_out doesn't exist"
                else:
                    print "mc_out last modified: ", time.ctime(os.path.getmtime("mc_out"))
                
            os.chdir(subParentPath)
            
    def getStat(self, workPath):
        '''Get a statistics of the runs.'''
        os.chdir(workPath)
        if not os.path.isdir(self.name):
            print "no directory %s in %s" % (self.name, workPath)
            return
        else:
            os.chdir(self.name)
            
        subParentPath = os.getcwd()
        allStds = []
        allLarges = []
        allSmalls = []
        allAvgs = []
        allsubstd = []
        
        print "%10d%10d%10d%10d" % (self.annealing, self.equilibration, self.sampling, self.indep)
        print "%10s%10s%10s%10s%10s" % ("avg samp", "largest", "samllest", "std samp", "confsgm")
        for i in range(self.nSubtest):
            subrunName = "sub" + str(i+1)
            if not os.path.isdir(subrunName):
                print "no directory %s in %s" % (subrunName, subParentPath)
                return
            else:
                os.chdir(subrunName)
            
            newTestrun = Testrun(subrunName, self.annealing, self.equilibration, self.sampling, self.indep)
            if not newTestrun.isFinished(os.getcwd()):
#                 print "%s/%s is not finished" % (self.name, newTestrun.name)
                print "na"
            else:
#                 print "working in %s/%s," % (self.name, newTestrun.name),
                newTestrun.read_mc_out()
                subavg = np.average(newTestrun.allMCEnergies)
                submax = max(newTestrun.allMCEnergies)
                submin = min(newTestrun.allMCEnergies)
                substd = np.std(newTestrun.allMCEnergies)
                 
                print "%10.3f%10.3f%10.3f%10.3f%10.3f" % (subavg, submax, submin, substd, newTestrun.largeststd)
                enerfp.write("%.3f\n" % subavg)
                allStds.append(newTestrun.largeststd)
                allLarges.append(submax)
                allSmalls.append(submin)
                allAvgs.append(subavg)
                allsubstd.append(substd)
                
            os.chdir(subParentPath)
#         print "\n========%s largeststd: %.3f, std of it: %.3f\n" % (self.name, np.average(allStds), np.std(allStds))
        print "%10s%10s%10s%10s%10s" % ("avg samp", "max large", "min samll", "avg stdE", "avg confsg")
        print "%10.3f%10.3f%10.3f%10.3f%10.3f\n" % (np.average(allAvgs), max(allLarges), min(allSmalls), np.average(allsubstd), np.average(allStds))
        self.avgEnergy = np.average(allAvgs)
        self.stdAvgEnergy = np.std(allAvgs)
        self.avgConfsg = np.average(allStds)
            
class Conf(object):
    def __init__(self):
        self.name = ""
        self.flag = ''
        self.E_self = 0.0
        self.mcs = []
        self.occ = 0.0
        self.sgm = 0.0
        
    def initFromLine(self, line):
        fields = line.split()
        self.name = fields[0]
        self.flag = fields[1]
        self.E_self = float(fields[2])
        self.mcs = [float(mc) for mc in fields[3:-2]]
        self.occ = float(fields[-2][-5:])
        self.sgm = float(fields[-1][-5:])
               
               
class EnergyTraject(object):
    def __init__(self):
        self.steps = []
        self.energies = []
        self.mcId = 0

    def addStep(self, eachLine):
        fields = eachLine.split()
        self.steps.append(int(fields[1][:-1]))
        self.energies.append(float(fields[-1]))

    def plot(self):
        pylab.plot(self.steps, self.energies, label="MC"+str(self.mcId))


class Testrun(object):
    def __init__(self, name, a=100, e=300, s=2000, i=6):
        self.annealing = a
        self.equilibration = e
        self.sampling = s
        self.indep = i
        self.name = name
        
        self.avgEnergies = []
        self.allMCEnergies = []
        
        self.mcSamplings = []
        self.conformers = []
        
        
        self.largeststd = 0.0
        
    def submitRun(self, parentPath):
#         allFiles = ("head3.lst", "energies.opp", "extra.tpl", "submit.sh", "run.prm", "ms_gold")
        allFiles = ("head3.lst", "energies.opp", "extra.tpl", "submit.sh", "run.prm")
        for eachFile in allFiles:
            os.symlink(os.path.join(parentPath, eachFile), os.path.join(".", eachFile))
            
        os.system("qsub submit.sh")
        
    def read_mc_out(self, fname="mc_out", **kwargv):
        MC_START_TAG = "Doing MC"
        MC_END_TAG = "The average running energy"
        CONF_START_TAG = "Conformer"
        
        fp = open(fname, 'r')
        
        sgThres = 0.1
        if "sgThreshold" in kwargv:
            sgThres = kwargv["sgThreshold"]
        
        beginSampling = False
        beginConf = False
        for eachLine in fp:
            if eachLine.startswith(MC_START_TAG):
                newMC = EnergyTraject()
                newMC.mcId = int(eachLine.split()[2])
                beginSampling = True
                continue
            if beginSampling and (not eachLine.startswith(MC_END_TAG)):
                self.allMCEnergies.append(float(eachLine.split()[-1]))
                newMC.addStep(eachLine)
            elif beginSampling and eachLine.startswith(MC_END_TAG):
                self.avgEnergies.append(float(eachLine.split()[-2]))
                self.mcSamplings.append(newMC)
                
                beginSampling = False
            
            if eachLine.startswith(CONF_START_TAG):
                beginConf = True
                continue
            
            if beginConf:
                # avoid empty line.
                if len(eachLine) > 14:
                    newConf = Conf()
                    newConf.initFromLine(eachLine)
                    if newConf.sgm > self.largeststd: self.largeststd = newConf.sgm
                    if newConf.sgm >= sgThres:
                        self.conformers.append(newConf)
                
    def isFinished(self, workPath):
        '''Check whether this run is finished.'''
        if os.path.isfile(os.path.join(workPath, "pK.out")):
            return True
        else:
            return False      
    
def showStat(allRuns, parameter1s, parameter2s, parameter3s, parameter4s, quantities):
    global iPlot
    for q in quantities:
        print q
        for p1 in parameter1s:
            for p2 in parameter2s:
                for p3 in parameter3s:
                    print "(%d_%d_%d)" % (p1, p2, p3),
                    stat = []
                    for p4 in parameter4s:
                        for eachRun in allRuns:
                            # all p1, p2, p3, p4 has to be different from each other
                            if sorted((p1, p2, p3, p4)) == sorted(eachRun.runId):
                                if q == "avgConfsg": 
                                    print "\t%10.3f" % eachRun.avgConfsg,
                                    stat.append(eachRun.avgConfsg)
                                elif q == "avgEnergy":
                                    print "\t%10.3f" % eachRun.avgEnergy,
                                    stat.append(eachRun.avgEnergy)
                                elif q == "stdAvgEnergy":
                                    print "\t%10.3f" % eachRun.stdAvgEnergy,
                                    stat.append(eachRun.stdAvgEnergy)
                                break
                    print
                    pl.subplot(4, 3, iPlot)
                    if iPlot == 1:
                        pl.title("maxconfstd")
                        pl.ylabel("independent run")
                    if iPlot == 2:
                        pl.title("average energy")
                    if iPlot == 3:
                        pl.title("std energy")
                    if iPlot == 4:
                        pl.ylabel("sampling")
                    if iPlot == 7:
                        pl.ylabel("annealing")
                    if iPlot == 10:
                        pl.ylabel("equilibration")
                    pl.plot(pl.array(parameter4s), pl.array(stat))
                    pl.xticks(parameter4s)
        iPlot += 1
           
def main():
    global fig
    parser = argparse.ArgumentParser(description="Test mc convergence")
    parser.add_argument("-s", action="store_true", help="submit all test runs")
    parser.add_argument("-r", action="store_true", help="get a statistics of all runs")
    parser.add_argument("-c", action="store_true", help="check job finish status")
    args = parser.parse_args()
    
    # folder which contains files like "head3.lst", "energies.opp" which we need to copy from.
#     parentPath = "/home/xzhu/BR2/1C3W/hydro/quick/lj01"
#     parentPath = "/home/xzhu/BR2/1C3W/crystal/def/lj01/testconvergence"
    parentPath = "/home/xzhu/BR_occ_water/1C3W/hydro/def/lj01/testHOH"

    
    # the folder in which the calculations will be done.
    workPath = os.getcwd()
    
    annealing_options = [100, 1000]
    equilibration_options = [300, 3000]
    sampling_options = [2000, 20000]
    indep_options = [6, 20, 40, 60]
#     annealing_options = [100]
#     equilibration_options = [300]
#     sampling_options = [2000]
#     indep_options = [6]
    
    allRuns = []
    for a in annealing_options:
        for e in equilibration_options:
            for s in sampling_options:
                for i in indep_options:
                    newRun = MCRunType(a, e, s, i)
                    if args.c:
                        newRun.checkFinishStatus(workPath)
                    if args.s:
                        newRun.submitTest(parentPath, workPath)
                    if args.r:
                        newRun.getStat(workPath)
                        allRuns.append(newRun)
    
    if args.r:
        showStat(allRuns, annealing_options, equilibration_options, sampling_options, indep_options, ["avgConfsg", "avgEnergy", "stdAvgEnergy"])
        showStat(allRuns, annealing_options, equilibration_options, indep_options, sampling_options, ["avgConfsg", "avgEnergy", "stdAvgEnergy"])
        showStat(allRuns, equilibration_options, sampling_options, indep_options, annealing_options, ["avgConfsg", "avgEnergy", "stdAvgEnergy"])
        showStat(allRuns, annealing_options, sampling_options, indep_options, equilibration_options, ["avgConfsg", "avgEnergy", "stdAvgEnergy"])
        fig.tight_layout()
        pl.show()
                    
                    
if __name__ == "__main__":
    main()
    
