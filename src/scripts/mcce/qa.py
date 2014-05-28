#!/usr/bin/env python
import argparse
import subprocess, sys, os

def getJobDirectory(jobId):
    p = subprocess.Popen(["qstat", "-j", str(jobId)], stdout=subprocess.PIPE)
    output = p.communicate()[0]
    for eachLine in output.split("\n")[:-1]:
        if eachLine.startswith("sge_o_workdir:"):
            return eachLine.split()[1]
        
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-command", "--command")
    args = parser.parse_args()
    
    p1 = subprocess.Popen(["qstat", "-u", "xzhu"], stdout=subprocess.PIPE)
    output = p1.communicate()[0]
    for eachLine in output.split('\n')[2:-1]:
        print eachLine,
        workDir = getJobDirectory(eachLine.split()[0]) 
        print workDir
        if args.command:
            os.chdir(workDir)
            subprocess.call(args.command.split())
            print
    
if __name__ == "__main__":
    main()
    