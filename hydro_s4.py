#!/usr/bin/python
from mdRunPrm import mdRunPrm 
from mdRunPrm import fix_head3
# from mccepy.alterprotonation import freeAllConformers
from alterprotonation import fixHead3ByNumberOfProtons, freeAllConformers
import os, sys, time, shutil
import networkx as nx
import numpy
import pylab
import subprocess
#from twisted.trial.test.test_loader import testNames
# use this script on my own computer or directly on sibyl
home_prefix = "/Users/xzhu/sibyl"

# home_dir = "/home/xzhu/BR_occ_water/"
home_dir = os.path.join(home_prefix, "BR2")
param_dir = home_dir + "paramFiles/"

BR_PROTONATION_TXT = os.path.join(home_prefix, "/pfile/protonation/br.txt")
O_PROTONATION_TXT = os.path.join(home_prefix, "/pfile/protonation/o.txt")

# Different types of pdb files used in the calculation.
# "crystal" refers to the pdb files with all the lipid removed from the original pdb files.
# "hydro" refers to the pdb files with added ipece waters to the "crystal" pdb files.
pdb_path = {"crystal":home_dir + "pdb/removeMem/", "hydro":home_dir + "pdb/ipece_wat/"}

# Depending on whether it's a quick run or default run,  change corresponding run.prm file.
run_prm_path = {"quick":(param_dir + "run.prm.quick"),  "def":(param_dir + "run.prm.default")}


# "raw" means vdw not scaled, "lj01" means vdw0, vdw1 and vdw are all scaled by 0.1 in step4.
# Different kinds of runs need different extra.tpl files which are both saved in the "param_dir" directory. 
extra_tpl_path = {"raw":os.path.join(home_prefix, "/pfile/extra.tpl"),
                  "lj01":os.path.join(home_prefix, "pfile/extra0.1.tpl")}

# path of the name.txt file, this file will be copied to each working directory.
name_txt_path = param_dir + "name.txt"
def retrieve_path_info():
    subprocess.check_call(["/home/xzhu/bin/pythonScript/deal_multi_paths.py", "-p"])
def submit_net_runs():
    subprocess.check_call(["/home/xzhu/bin/pythonScript/deal_multi_paths.py", "-s"])
    
def analyze_net(do_fix=True):
    if do_fix:
        subprocess.check_call("/home/xzhu/bin/pythonScript/fix_protonations.py")
    subprocess.check_call("/home/xzhu/bin/pythonScript/analyzeNetwork.py")
    
def checkStatus():
    if os.path.isfile("head3.lst"):
        print "STEP 3 done"
    if os.path.isfile("pK.out"):
        print "STEP 4 done"
        
def loadFixProtonation(fName):
    fixList = {}
    for eachLine in open(fName):
        if eachLine.strip().startswith('#'): continue
        fields = eachLine.split()
        fixList[fields[0]] = int(fields[1])
    return fixList

def runStep4():
    # pK.out already exists
    if os.path.isfile("pK.out"): return
    
    linkFiles = ["energies.opp", "hb.dat"]
    copyFiles = ["head3.lst", "run.prm", "ms_gold"]
    
    for eachFile in linkFiles:
        if not os.path.exists(eachFile):
            os.symlink(os.path.join("../raw", eachFile), eachFile)
        
    for eachFile in copyFiles:
        shutil.copy(os.path.join("../raw", eachFile), eachFile)
    
    changePrm = {'DO_PREMCCE':'f', \
                 'DO_ROTAMERS':'f', \
                 'DO_ENERGY':'f',   \
                 'DO_MONTE':'t', \
                 'TITR_PH0':'7.0', \
                 'TITR_STEPS':'1', \
                 'MONTE_RUNS':'6',\
                 'MONTE_NITER':'2000',\
                 'NSTATE_MAX':'-1'}
    mdRunPrm(changePrm)
    
    # extra.tpl
    extra_tpl = "/home/xzhu/pfile/extra.tpl"
    shutil.copy(extra_tpl, ".")
    
    # fix head3.lst
    freeAllConformers()
    fixList = loadFixProtonation(BR_PROTONATION_TXT)
    fixHead3ByNumberOfProtons(fixList, reverse=True)
    
    # submit job
#     subprocess.call(["qsub", "submit.sh"])
#     shutil.copy("resInHbNet.txt", "ms_gold")
    shutil.copy("/home/xzhu/pfile/submit_temp.sh", ".")
    subprocess.call(["qsub", "submit_temp.sh"])
    
def runStep4Lj():
    # pK.out already exists
    if os.path.isfile("pK.out"): return
    
    linkFiles = ["energies.opp", "hb.dat"]
    copyFiles = ["head3.lst", "run.prm", "ms_gold"]
    for eachFile in linkFiles:
        if not os.path.exists(eachFile):
            os.symlink(os.path.join("../raw", eachFile), eachFile)
        
    for eachFile in copyFiles:
        shutil.copy(os.path.join("../raw", eachFile), eachFile)
        
    changePrm = {'DO_PREMCCE':'f', \
                 'DO_ROTAMERS':'f', \
                 'DO_ENERGY':'f',   \
                 'DO_MONTE':'t', \
                 'TITR_PH0':'7.0', \
                 'TITR_STEPS':'1', \
                 'MONTE_RUNS':'6',\
                 'MONTE_NITER':'2000',\
                 'NSTATE_MAX':'-1',\
                 'MFE_CUTOFF':'5.0',\
                 'ALWAYS_SCALE_VDW':'f'}
    mdRunPrm(changePrm)
    
    # extra.tpl
    extra_tpl = "/home/xzhu/pfile/extra0.25.tpl"
    shutil.copy(extra_tpl, "extra.tpl")
    
    # fix head3.lst
    fixList = loadFixProtonation(O_PROTONATION_TXT)
    fixHead3ByNumberOfProtons(fixList, reverse=True)
    
    # submit job
    submitsh = "/home/xzhu/pfile/submit_temp.sh"
    shutil.copy(submitsh, ".")
    subprocess.call(["qsub", "submit_temp.sh"])
        
def rerun_s4(parentPath):
    '''
    Rerun step4.
    '''
    if os.path.isfile("pK.out"): return
    os.system("cp " + os.path.join(parentPath, "run.prm") + " .")
    os.system("cp " + os.path.join(parentPath, "head3.lst") + " .")
    os.system("cp " + os.path.join(parentPath, "submit_ms.sh") + " .")
    os.system("cp " + os.path.join(parentPath, "ms_gold") + " .")
    os.system("cp " + os.path.join(parentPath, "extra.tpl") + " .")

    os.system("ln -s " + os.path.join(parentPath, "energies.opp" + " ."))
    os.system("ln -s " + os.path.join(parentPath, "hb.dat" + " ."))
    
    changePrm = {'DO_PREMCCE':'f', \
                 'DO_ROTAMERS':'f', \
                 'DO_ENERGY':'f',   \
                 'DO_MONTE':'t', \
                 'TITR_PH0':'0.0', \
                 'TITR_STEPS':'15', \
                 'MONTE_RUNS':'6',\
                 'EXTRA':"./extra.tpl"}
    mdRunPrm(changePrm)
    
    freeAllConformers()
#     fList = [['ASP-1A0115'], ['ASP-1A0096'], ['GLU0', 'A0204'], ['RSB01A0216']]
#     fix_head3(fList)
    
#     os.system("cp /home/xzhu/pfile/submit.sh .")
    os.system('qsub submit_ms.sh')

def run_ms_s4():
    # if it's done already
#     if os.path.exists('pK.out'):
#          return
    changePrm = {'DO_PREMCCE':'f', \
                 'DO_ROTAMERS':'f', \
                 'DO_ENERGY':'f',   \
                 'DO_MONTE':'t', \
                 'TITR_PH0':'7.0', \
                 'TITR_STEPS':'1', \
                 'MONTE_RUNS':'6',\
                 'NSTATE_MAX':'-1'}
    mdRunPrm(changePrm)

    # fix the ionization states of some residues
    try:
        fList = [['ASP-1A0115'], ['ASP-1A0096'], ['GLU0', 'A0204'], ['RSB01A0216']]
        fix_head3(fList)

        #os.system('cp step1_out.pdb ms_gold')
        os.system('cp resInHbNet.txt ms_gold')
#         os.system("cp " + param_dir + "submit_ms.sh .")
#         os.system('qsub submit_ms.sh')
        shutil.copy("/home/xzhu/pfile/submit_temp.sh", ".")
        os.system("qsub submit_temp.sh")
    except:
        sys.stderr.write("Can't modify head3.lst in directory " + os.getcwd())



def run_hb():
    os.system("cp /home/xzhu/pfile/submit_hb.sh .")
    os.system("qsub submit_hb.sh")

def run_hmatrix(copybak=True):
    if copybak:
        if os.path.exists("bak_ms.dat"):
            os.rename("bak_ms.dat", "ms.dat")
        
    os.system('cp /home/xzhu/pfile/submit_hm.sh .')
    #os.system('/home/xzhu/bin/hb_3/hmatrix &')
    os.system('qsub submit_hm.sh')

def step123(pdb, pdb_type="crystal", run_type="quick", scale_type="raw"):
    # pdb source files, copy the pdb files according to the pdb file type has been chosen.
    os.system('cp ' + pdb_path[pdb_type] + pdb + '.pdb .')
       
#=====================   Modify run.prm =================================================================================
    changePrm = {'DO_PREMCCE':'t', 'DO_ROTAMERS':'t', 'DO_ENERGY':'t',"DO_MONTE":'f', 'INPDB':(pdb + '.pdb'), 'IPECE_ADD_MEM':'t'} 
    changePrm["TITR_PH0"] = "7.0"                 # initial ph
    changePrm["TITR_STEPS"] = "1"                 # steps of titration, only do it at ph 7
       

    # Optional
    changePrm["MINIMIZE_SIZE"] = "f"              # don't minimize the output file, ie. save all output files.
    changePrm["TERMINALS"] = "f"                  # Don't lable terminal
    #changePrm["TERMINALS"] = "t"

    # No relaxations at all
    changePrm["HDIRECTED"] = "f"                  # no h-bond directed rotamer making
    changePrm["HV_RELAX_NCYCLE"] = "0"            # 0 number of cycles to relax rotamer clash
    changePrm["RELAX_H"] = "f"                    # Do not do relaxation on hydrogens

    # cp name.txt and extra.tpl to the working directory.
    changePrm["MCCE_HOME"] = param_dir            # use the tpl files in the param_dir directory.
    changePrm["EXTRA"] = "./extra.tpl"            # always use the extra.tpl file in the current directory.       
    os.system("cp " + extra_tpl_path[scale_type]  + " .")

    changePrm["RENAME_RULES"] = "./name.txt"
    os.system("cp " + name_txt_path + " .")

    # for step4 to save micro states
    changePrm["MONTE_RUNS"] = "6"                 # number of independent monte carlo runs
    changePrm["NSTATE_MAX"] = "-1"                # change it to -1 to make sure monte calo
                                                  # simulation is carried out, rather than the analytic solution.
    changePrm["MFE_POINT"] = "7"                  # settings for mfe
    changePrm["MFE_CUTOFF"] = "-1.0"
 
    # The only difference between quick and default is whether do rotations.
    if run_type == "quick":
        changePrm["PACK"] = "f"
    elif run_type == "def":
        changePrm["PACK"] = "t"  
      
    os.system("cp " + run_prm_path[run_type] + " run.prm")
    mdRunPrm(changePrm)
#=======================================================================================================================         

    # Submit the job
    submit_file_path = param_dir + "submit.sh"
    os.system("cp " + submit_file_path + " .")
    os.system('qsub submit.sh')

    print pdb,  pdb_type, run_type, scale_type, ' finished'

def print_sorted_path_stat():
    fileName = "path_second_stat.txt"
    if os.path.exists(fileName):
        newLines = sorted(open(fileName).readlines(), key=lambda line: float(line.split()[-1]))
        sys.stdout.writelines(newLines)
    
def checkInfo():
    if os.path.exists("ms_crg"):
        sys.stdout.write("ms_crg in directory " + os.getcwd() + '\n')
    else:
        if os.path.exists("pK.out"):
            sys.stdout.write("ONLY pK.out in directory " + os.getcwd() + '\n')
        else:
            sys.stdout.write("NO pK.out or ms_crg in directory " + os.getcwd() + '\n')
    #if os.path.exists("fixMfe"):
    #    sys.stdout.write("fixMfe exists in " + os.getcwd() + '\n')
    #else:
    #    sys.stdout.write("fixMfe doesn't exists in " + os.getcwd() + '\n')
    
def actionInPath(fileOpened=None):
    #os.system("/home/xzhu/bin/pythonScript/fix_io.py -m f.txt all_states.txt")
    dirName = "."
    #dirName = "fixProtonation"
    #dirName = "fixMfe"
    if os.path.exists(dirName):
        os.chdir(dirName)
        #checkInfo()
        #os.system("/home/xzhu/bin/pythonScript/fix_io.py -s f.txt all_states.txt")
        #os.system("/home/xzhu/bin/pythonScript/fix_io.py -r f.txt all_states.txt")
        #os.system("/home/xzhu/gmcce/hbPath/hBondPath.py -e ener.txt init.txt")
        if not os.path.exists("paths.txt"):
            sys.stderr.write("NO paths.txt in " + os.getcwd() + '\n')
            return
        eBarrier = open("paths.txt").readline().split()[-1]
        fileOpened.write(eBarrier + '\n')


def setupFixProtonation(aPdb):
    print os.getcwd()
    dirName = "fixProtonation"
    os.system("rm -rf " + dirName)
    os.mkdir(dirName)
    os.chdir(dirName)
    os.system("cp ../head3.lst .")
    os.system("cp ../run.prm .")
    os.system("cp ../all_states.txt .")
    os.system("cp ../f.txt .")
    os.system("cp ../init.txt .")
    os.system("cp ../ms_gold .")
    
    os.system("ln -s ../energies.opp .")
    
    fixList = {}
    protonationLines = open(os.path.join(home_dir, aPdb, "protonation.txt")).readlines()
    for eachLine in protonationLines:
        fixList[eachLine.split()[0]] = int(eachLine.split()[1])
    fixHead3ByNumberOfProtons(fixList, reverse=True)
    

def actionForAllPaths(aPdb, pdbT, runT, scaleT):
    allPathFileName = "secondshortestpaths.txt"
    #allPathFileName = "allshortestpaths.txt"

    if "No connected pathway" in open(allPathFileName).read():
        sys.stderr.write("No connected pathway\n")
        return
    
    fp = None  
    #os.system("zopp -x energies")
    fileName = "path_second_stat.txt"
    fp = open(fileName, 'w')
    finalPath = os.path.join(home_dir, aPdb, pdbT, runT, scaleT)
    for eachLine in open(allPathFileName).readlines():
        fields = eachLine.split()
        pathwayName = fields[0]
        pathwayPath = os.path.join(finalPath, pathwayName)
        os.chdir(pathwayPath)

        fp.write(eachLine[:-1] + '\t')
        #setupFixProtonation(aPdb)
        actionInPath(fp)
    fp.close()
        
    #os.chdir(finalPath)
    #os.system("rm -rf energies")


def findSecondShortestpaths():
    from mccepy import ResHbNetwork

    source = "ASPA0085"
    target = "GLUA0194"
    
    allPathFileName = "secondshortestpaths.txt"
    hb = ResHbNetwork("hb.txt")
    fp = open(allPathFileName, 'w')
    pathIndex = hb.getNumberOfShortestPaths(source, target) + 1
    for eachPath in hb.getSecondShortestPaths(source, target):
        fp.write("path%d" % pathIndex)
        for eachResidue in eachPath:
            fp.write('%10s' % eachResidue)
        fp.write('\n')
        pathIndex += 1
    fp.close()        
               
def getRunTypeAbbreviation(pdbT, runT, scaleT):
    '''
    Get the abbreviation a particular type of run.
    '''
    
    firstLetter = ''     # for pdbT, "crystal" = 'c', "hydro" = 'h'
    secondLetter = ''    # for runT, "quick" = 'q', "def' = 'd'
    thirdLetter = ''     # for scaleT, "raw" = 'r', "lj01" = 'l'
    if pdbT == "crystal":
        firstLetter = 'c'
    elif pdbT == "hydro":
        firstLetter = 'h'
        
    if runT == "quick":
        secondLetter = 'q'
    elif runT == "def":
        secondLetter = 'd'
        
    if scaleT == "raw":
        thirdLetter = 'r'
    elif scaleT == "lj01":
        thirdLetter = 'l'
        
    return firstLetter + secondLetter + thirdLetter
                          
        
def outputPathStat(fname="pathStatistics.txt"):
    class HbPath(object):
        def __init__(self, line=None):
            self.pathName = ""
            self.residues = []
            self.eBarrier = 0.0
            
            self.hops = []
            if line: self.initFromLine(line)
            
        def initFromLine(self, line):
            fields = line.split()
            self.pathName = fields[0]
            self.residues = fields[1:-1]
            self.eBarrier = float(fields[-1])
            
        def loadHopInfo(self, fname="lowestHopSeq.txt"):
            lines = open(fname).readlines()
            lines = lines[:(1+len(self.residues))]
            for eachLine in lines:
                self.hops.append(eachLine)
            
        
        def __str__(self):
            str = ""
            for eachRes in self.residues:
                str += "%10s" % eachRes
            str += '\n'
            for eachHop in self.hops:
                for eachCol in eachHop.split():
                    str += "%10s" % eachCol
                str += '\n'
            return str
            
    
    class PathStat(object):
        def __init__(self):
            self.length = 0
            self.nPath = 0
            self.lowestEBarrier = 0.0
            self.paths = []
        
        def addFirstPath(self, hbPath):
            self.length = len(hbPath.residues)
            self.nPath = 1
            self.lowestEBarrier = hbPath.eBarrier
            self.paths.append(hbPath)
            
        def hasPath(self, hbPath):
            return self.length == len(hbPath.residues)
        
        def addPath(self, hbPath):
            self.nPath += 1
            if self.lowestEBarrier > hbPath.eBarrier:
                self.lowestEBarrier = hbPath.eBarrier
            self.paths.append(hbPath)
            
    if not os.path.exists(fname):
        print "No %s in %s" % (fname, os.getcwd())
        return
    
    allPathStat = []
    for eachLine in open(fname, 'r'):
        newPath = HbPath(eachLine)
        newPath.loadHopInfo(newPath.pathName + "/lowestHopSeq.txt")
        isNewPathType = True
        for eachPathStat in allPathStat:
            if eachPathStat.hasPath(newPath):
                eachPathStat.addPath(newPath)
                isNewPathType = False
                break
        if isNewPathType:
            newPathStat = PathStat()
            newPathStat.addFirstPath(newPath)
            allPathStat.append(newPathStat)
            
    allPathStat = sorted(allPathStat, key=lambda s: s.length)
    for eachStat in allPathStat:
        eachStat.paths = sorted(eachStat.paths, key=lambda p: p.eBarrier)
        
    for eachStat in allPathStat:
        sys.stdout.write("barrier: %10.2f, npath: %4d, length: %4d\n" % (eachStat.lowestEBarrier, eachStat.nPath, eachStat.length)) 
        print eachStat.paths[0]
#     allLines = open(fname, 'r').readlines()
#     allLines.sort(key=lambda eachLine: float(eachLine.split()[-1]))
#     print "barrier: %10.2f, npath: %4d, length: %4d" % (float(allLines[0].split()[-1]), len(allLines), len(allLines[0].split())-2)
#     for eachLine in allLines:
#         print eachLine,
     
 
def tempRemove():
    dirNames = ["fixProtonationSurroundingHb001", "fixProtonationSurroundingHb01", "freeSurroundingHb001", "freeSurroundingHb01"] 
    removeFiles = ["energies.opp", "ms.dat", "hah.txt", "hb.dat"]
    for eachDir in dirNames:
        os.chdir(eachDir)
        for eachFile in removeFiles:
            if os.path.isfile(eachFile):
                os.remove(eachFile)
                os.symlink(os.path.join("..", eachFile), eachFile)
        os.chdir("..")
        
def rmWatRun(pdb, pdb_type="crystal", run_type="quick", scale_type="raw"):
    sourceDir = "/home/xzhu/BR_orig/"
    water_occ = "water_stat.txt"
    
    fileToCopy = ["extra.tpl", "submit.sh", "run.prm", water_occ]
    
    fileFromRaw = ["step2_out.pdb"]
    
    for eachFile in fileToCopy:
        shutil.copy(os.path.join(sourceDir, pdb, pdb_type, run_type, scale_type, eachFile), ".")
        
    for eachFile in fileFromRaw:
        shutil.copy(os.path.join(sourceDir, pdb, pdb_type, run_type, "raw", eachFile), ".")
        
    os.system("/home/xzhu/bin/pythonScript/modifyStep2.py -w " + water_occ + " -t 0.999 -o step2_out.pdb")

        
def run_step3():
    changePrm = {'DO_PREMCCE':'f', \
                 'DO_ROTAMERS':'f', \
                 'DO_ENERGY':'t',   \
                 'DO_MONTE':'f'}
    mdRunPrm(changePrm)
    os.system("qsub submit.sh")

def runStep4Test(testName):
    if not os.path.isdir(testName): os.mkdir(testName)
    os.chdir(testName)
    linkFiles = ["energies.opp", "head3.lst", "extra.tpl", "run.prm", "submit.sh"]
    for eachFile in linkFiles:
        os.symlink(os.path.join("..", eachFile), eachFile)
    subprocess.call(["qsub", "submit.sh"])
    os.chdir("..")
    
def setupPathFolder(dirName):
    os.system("rm -rf HB01")
    if not os.path.isdir(dirName):
        os.mkdir(dirName)
    os.chdir(dirName)
    filesToCopy = ["fixedProtonations.txt", "hb.txt", "head3.lst", "run.prm"]
    filesToLink = ["energies.opp", "extra.tpl"]
    for eachFile in filesToCopy:
        shutil.copy(os.path.join("..", eachFile), eachFile)
    for eachFile in filesToLink:
        os.symlink(os.path.join("..", eachFile), eachFile)
    os.system("/home/xzhu/bin/pythonScript/analyzeNetwork.py 0.1")
    
def neat_path_output(pathFile="pathStatistics.txt"):
    ''' Sort the paths in pathStatistics.txt first by the length of the path, 
    then by the energy barrier.
    '''
    
    if not os.path.exists(pathFile):
        print "No %s in %s" % (pathFile, os.getcwd())
        return
    
    allLines = sorted(open(pathFile).readlines(), key=lambda eachLine: (len(eachLine.split()), float(eachLine.split()[-1])))
    for eachLine in allLines:
        print eachLine,
    
    
def setup_keepDummy():
    files_to_copy = ["extra.tpl", "run.prm", "allPaths.txt", "fixedProtonations.txt",\
                     "hb.txt", "head3.lst", "submit_temp.sh"]
    files_to_link = ["energies.opp", "hb.dat"]
    for eachFile in files_to_copy:
        if not os.path.exists(eachFile):
            shutil.copy(os.path.join("..", eachFile), eachFile)
    for eachFile in files_to_link:
        if not os.path.exists(eachFile):
            os.symlink(os.path.join("..", eachFile), eachFile)
        
            
def main():
#     pdbs = ["1C3W", "1C8R", "1KG9"]
#     pdbs = ["1DZE", "1KG8", "1C8S", "1F4Z"]
    pdbs = ["1C3W", "1C8R", "1KG9", "1DZE", "1KG8", "1C8S", "1F4Z"]
#     pdbs = ["1C3W"]
    pdb_types = ["hydro"]
#     pdb_types = ["crystal"]
#     run_types = ["quick", "def"]
    run_types = ["quick"]
    scale_types = ["raw_O"]
    #scale_types = ["raw", "lj01"]
#     scale_types = ["lj01_keep_999"]
    #scale_types = ["lj01_keep_999", "lj025_keep_999"]
    
    for aPdb in pdbs:
        for pdbT in pdb_types:
            for runT in run_types:
                for scaleT in scale_types:
                    finalPath = os.path.join(home_dir, aPdb, pdbT, runT, scaleT)
#                     if not os.path.exists(finalPath):
#                         os.makedirs(finalPath, 0755)

                    if not os.path.exists(finalPath):
                        sys.stderr.write("%s doesn't exist\n" % finalPath)
                        continue
                    os.chdir(finalPath)
                    
                    sys.stdout.write("%s\n" % finalPath)
                    sys.stdout.flush()
                    if os.path.exists("hb.txt"):
                        os.system(" ~/Dropbox/eclipse_workspace/br/hb_connection/res_hbond.py -source ASPA0085 -target GLUA0204 -lenLessThan 10 hb.txt | grep -v A0082")

                    
if __name__ == '__main__':
    main()
