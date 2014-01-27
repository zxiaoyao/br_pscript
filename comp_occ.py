#!/usr/bin/env python
import argparse

class Conf(object):
    def __init__(self, resName="", occ=0.0):
        self.confName = resName
        self.occ = occ
        

    
def getConfOcc(fName="fort.38"):
    allConfs = []
    allLines = open(fName).readlines()
    allLines.pop(0)
    
    for eachLine in allLines:
        if eachLine.startswith("HOH"): continue
        newConf = Conf()
        fields = eachLine.split()
        newConf.confName = fields[0]
        newConf.occ = float(fields[1])
        allConfs.append(newConf)
        
    return allConfs



def cmpTwoOcc(file1, file2, cutoff=-1.0):
    confs1 = getConfOcc(file1)
    confs2 = getConfOcc(file2)
    
    allConfs = []
    for eachConf in confs1:
        if not eachConf.confName in allConfs:
            allConfs.append(eachConf.confName)
    for eachConf in confs2:
        if not eachConf.confName in allConfs:
            allConfs.append(eachConf.confName)
            
    for eachConf in allConfs:
        found = False
        for eachConf1 in confs1:
            if eachConf1.confName == eachConf:
                found = True
                o1 = eachConf1.occ
                break
        if not found: o1 = "na"
        
        found = False
        for eachConf2 in confs2:
            if eachConf2.confName == eachConf:
                found = True
                o2 = eachConf2.occ
                break
        if not found: o2 = "na"
        
        
        if o1 == "na" or o2 == "na":
            print "%s%10s%10s" % (eachConf, str(o1), str(o2))
        else:
            diff = o1 - o2
            if abs(diff) > cutoff:
                print "%s%10.3f%10.3f%10.3f" % (eachConf, o1, o2, diff)
  
def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("-t", dest="threshold", type=float, default=-1.0)
    parser.add_argument("-c", nargs=2)
    args = parser.parse_args()
     
    if args.c:
        cmpTwoOcc(args.c[0], args.c[1], args.threshold)

    else:
        dummy_wat(args.threshold)

if __name__ == "__main__":
    main()
    