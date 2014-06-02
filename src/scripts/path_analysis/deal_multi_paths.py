#!/usr/bin/python
import os, sys, shutil, argparse

GET_PATH_BARRIER_CMD = "/home/xzhu/bin/br_pscript/src/scripts/path_analysis/get_path_barrier.py"

def submit_multi_paths(pathInfoFile="allPaths.txt"):
    if os.path.exists(pathInfoFile):
        for eachLine in open(pathInfoFile):
            fields = eachLine.split()
            pathName = fields[0]
            os.system(GET_PATH_BARRIER_CMD + " -s " + pathName)

def retrieve_multi_paths(pathInfoFile="allPaths.txt", outputFile="pathStatistics.txt"):
    if os.path.exists(pathInfoFile):
        for eachLine in open(pathInfoFile):        
            fields = eachLine.split()
            pathName = fields[0]
            os.system(GET_PATH_BARRIER_CMD + " -r " + pathName)
        
def obtain_multi_paths(pathInfoFile="allPaths.txt", outputFile="pathStatistics.txt"):
    if os.path.exists(pathInfoFile):
        fp = open(outputFile, 'w')
        for eachLine in open(pathInfoFile):
            fields = eachLine.split()
            pathName = fields[0]
            os.system(GET_PATH_BARRIER_CMD + " -p " + pathName)
            path_energy_fp = open(os.path.join(pathName, "lowestHopSeq.txt"), 'r')
            energyBarrier = float(path_energy_fp.readline().split()[-1])
            initEnergy = float(path_energy_fp.readline().split()[-1])
            fp.write(eachLine[:-1] + ("%10.3f%10.3f\n" % (initEnergy, energyBarrier)))
        fp.close()

def archive_run(parentPath, archiveFolder, pathInfoFile="allPaths.txt"):
    if not os.path.isdir(archiveFolder):
        os.mkdir(archiveFolder)
    filesToCopy = ["head3.lst", "run.prm", "ms.dat", "fort.38", "sum_crg.out", "ms_run.log",\
                   "pK.out", "hb.txt", "fixedProtonations.txt", "allPaths.txt", "pathStatistics.txt",\
                   "ms_gold", "hb.dat", "hah.txt", "energies.opp", "extra.tpl"]
    for eachFile in filesToCopy: 
        if os.path.islink(eachFile):
            linkto = os.readlink(eachFile)
            while os.path.islink(linkto):
                linkto = os.readlink(linkto)
            os.symlink(os.path.abspath(linkto), os.path.join(parentPath, archiveFolder, eachFile))
        elif os.path.isfile(eachFile):
            shutil.copy(os.path.join(parentPath, eachFile), os.path.join(parentPath, archiveFolder))
    
    
    if os.path.exists(pathInfoFile):
        for eachLine in open(pathInfoFile):        
            fields = eachLine.split()
            pathName = fields[0]
            
            # remove the "mSub" directory in each sub run
            shutil.rmtree(os.path.join(pathName, "mSub"))
            
            shutil.copytree(os.path.join(parentPath, pathName), os.path.join(parentPath, archiveFolder, pathName), symlinks=True)

def removeAllPathFolder(pathInfoFile="allPaths.txt"):
    if os.path.exists(pathInfoFile):
        for eachLine in open(pathInfoFile):
            fields = eachLine.split()
            pathName = fields[0]
            shutil.rmtree(pathName)
            
def getLowEHop(pathInfoFile="allPaths.txt"):
    if os.path.exists(pathInfoFile):
        for eachLine in open(pathInfoFile):
            fields = eachLine.split()
            pathName = fields[0]
            if os.path.isfile(os.path.join(pathName, "lowestHopSeq.txt")):
                print os.path.join(os.getcwd(), pathName)
                os.system("cat " + os.path.join(pathName, "lowestHopSeq.txt"))
            
def helpMessage():
    print "deal_multi_path.py -s: to submit jobs to run all sub runs form all paths"
    print "                   -r: to retrieve energy barriers of all paths"
    print "                   -p: to get the statistics of all the paths"
    print "                   -a parentPath archiveFolder: to archive all the file a type of run into the archiveFolder"
    print "                   -rm: remove all the path folders"
    print "                   -l: print hopping sequence of lowest energy barrier"
    
def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-s", action="store_true", help="submit jobs to run all sub runs for all paths")
    parse.add_argument("-r", action="store_true", help="retrieve energy barriers of all paths")
    parse.add_argument("-p", action="store_true", help="get the statistics of all the paths")
    parse.add_argument("-a", nargs=2, metavar=("parentPath", "archiveFolder"),
                       help="archive all the file a type of run into the archiveFolder")
    parse.add_argument("-rm", action="store_true", help="remove all the path folders")
    parse.add_argument("-l", action="store_true", help="print hopping sequence of lowest energy barrier")
    args = parse.parse_args()
    
    if args.s: submit_multi_paths()
    if args.r: retrieve_multi_paths()
    if args.p: obtain_multi_paths()
    if args.a: archive_run(args.a[0], args.a[1])
    if args.rm: removeAllPathFolder()
    if args.l: getLowEHop()
    
    
if __name__ == "__main__":
    main()
        
