#! /usr/bin/python

import os, subprocess
import networkx as nx

def main():
    
    g = nx.read_weighted_edgelist("/home/xzhu/BR/1DZE/hydro/def/lj01/hb.txt")
    allNodes = nx.node_connected_component(g, "GLUA0194")
    
    #print allNodes
    #print 
    for eachPath in nx.all_simple_paths(g, "ASPA0085", "GLUA0194"):
        if len(eachPath) == nx.shortest_path_length(g, "ASPA0085", "GLUA0194") + 2:
            print eachPath
        
    
    accRes = {}
    for line in open("/home/xzhu/BR/1DZE/hydro/def/raw/acc.res"):
        fields = line.split()
        resName = fields[1] + fields[2]
        acc = float(fields[4])
        accRes[resName] = acc
        
    #for eachNode in allNodes:
    #    print eachNode, accRes[eachNode]
    
        
    #print lines[0]
    
    
def fun():
    import subprocess, os
    
    p = subprocess.Popen(["qstat", "-u", "xzhu"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    allLines = out.split('\n')[2:-1]
    for eachLine in allLines:
        jobid = eachLine.split()[0]
        subp = subprocess.Popen(["qstat", "-j", jobid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subout, suberr = subp.communicate()
        print jobid
        for line in subout.split('\n'):
            if line.startswith("cwd:"):
                subdir = line.split()[1]
            if line.startswith("script_file:"):
                subscript = line.split()[1]
        print subdir
        #os.system("qdel " + jobid)
        #os.system("qsub " + os.path.join(subdir, subscript))
        
def getRunTypeAbbreviation(pdbT, runT, scaleT):
    
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
    
def foo():
    print getRunTypeAbbreviation("crysta", "quick", "raw")
         
if __name__ == "__main__":
    print [i for i+1 in ]        
