#!/usr/bin/env python
import os, shutil

threeDir = ["/home/xzhu/test/more_wat_ASP7/1C3W/aspglu/occwater/lj01",
            "/home/xzhu/test/more_wat_ASP7/1C8R/aspglu/occwater/lj01",
            "/home/xzhu/test/more_wat_ASP7/1KG9/aspglu/occwater/lj01"]
        
def subCommand(*args, **kwargs):
    movingFiles = ["fixedProtonations.txt", "allPaths.txt"]
    
    if not os.path.isdir("extra01"):
        os.mkdir("extra01")
        os.system("mv path* extra01/.")
        for eachFile in movingFiles:
            os.system("mv " + eachFile + " extra01/.")
    os.remove("extra.tpl")
    os.system("qsub submit_temp.sh")

def sub_hmatrix():
    if os.path.isfile("bak_ms.dat"):
        os.rename("bak_ms.dat", "ms.dat")
    os.system("qsub submit_hm.sh")
    os.system("/home/xzhu/bin/pythonScript/fix_protonations.py")
    
def analyzenet():
    os.system("/home/xzhu/bin/pythonScript/analyzeNetwork.py")
    
def run_net():
    os.system("/home/xzhu/bin/pythonScript/deal_multi_paths.py -s")
    
def collect_net():
    os.system("/home/xzhu/bin/pythonScript/deal_multi_paths.py -p")
    
def main():
    for eachDir in threeDir:
        os.chdir(eachDir)
        print eachDir
#         sub_hmatrix()  
#         analyzenet()
#         run_net()
#         collect_net()
        os.system("cat pathStatistics.txt")
             
if __name__ == "__main__":
    main()