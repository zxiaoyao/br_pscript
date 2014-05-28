#!/usr/bin/env python
import argparse

class WaterConf(object):
    def __init__(self):
        self.confName = ""
        self.desolv = 0.0
        
def retrieveWaters(fileName):
    allWaters = []
    for eachLine in open(fileName):
        if eachLine[6:9] == "HOH":
            newWater = WaterConf()
            newWater.confName = eachLine.split()[1]
            newWater.desolv = float(eachLine[84:92])
            allWaters.append(newWater)
            
    return allWaters

def compDesolv(file1, file2, cutoff=-1.0):
    water1 = retrieveWaters(file1)
    water2 = retrieveWaters(file2)
    
    allConfs = set([eachWat.confName for eachWat in water1]).union(set([eachWat.confName for eachWat in water2]))
    for eachConf in allConfs:
        found = False
        for eachWat in water1:
            if eachWat.confName == eachConf:
                d1 = eachWat.desolv
                found = True
                break
        if not found: 
            d1 = "na"
        
        found = False
        for eachWat in water2:
            if eachWat.confName == eachConf:
                d2 = eachWat.desolv
                found = True
                break
        if not found: 
            d2 = "na"
            
        if d1 == "na" or d2 == "na":
            print "%s%10s%10s" % (eachConf, str(d1), str(d2))
        elif abs(d1 - d2) > cutoff:
            print "%s%10.3f%10.3f%10.3f" % (eachConf, d1, d2, d1-d2)
            
        
            
                
                

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", nargs=2, metavar=("file1", "file2"))
    parser.add_argument("-t", dest="threshold", type=float, default=-1.0,
                        help="the threshold to show the conformer")
    args = parser.parse_args()
    
    compDesolv(args.c[0], args.c[1], args.threshold)
    
if __name__ == "__main__":
    main()
    