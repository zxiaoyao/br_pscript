#!/usr/bin/env python
import os
class Water:
    def __init__(self, name="", occ=[]):
        self.resName = name
        self.occ = occ
    
def occu():
    f1 = "occuwater.txt"
    f2 = "neutral/occuwater.txt"
    f3 = "ionize/occuwater.txt"
    os.system("/home/xzhu/bin/pythonScript/water_stat.py -t 0.999 -inverse >occuwater.txt")
    os.chdir("neutral")
    os.system("/home/xzhu/bin/pythonScript/water_stat.py -t 0.999 -inverse >occuwater.txt")
    os.chdir("../ionize")
    os.system("/home/xzhu/bin/pythonScript/water_stat.py -t 0.999 -inverse >occuwater.txt")
    os.chdir("..")
    allWater = []
    for eachLine in open(f1):
        fields = eachLine.split()
        newWater = Water()
        newWater.resName = fields[0]
        newWater.occ.append(fields[1])
        allWater.append(newWater)

    for eachLine in open(f2):
        resName = eachLine.split()[0]
        found = False
        for eachWater in allWater:
            if resName == eachWater.resName:
            	eachWater.occ.append(eachLine.split()[1])
                found = True
                break
        if not found:
            newWater = Water()
            newWater.resName = resName
            newWater.occ.extend(["na", eachLine.split()[1]])
            allWater.append(newWater)

    for eachLine in open(f3):
        resName = eachLine.split()[0]
        found = False
        for eachWater in allWater:
            if resName == eachWater.resName:
                eachWater.occ.append(eachLine.split()[1])
                found = True
                break
        if not found:
            newWater = Water()
            newWater.resName = resName
            newWater.occ.extend(["na", "na", eachLine.split()[1]])
            allWater.append(newWater)

    #for eachWater in allWater:
    #    print "%10s%8s%8s%8s" % (eachWater.resName, eachWater.occ[0], eachWater.occ[1], eachWater.occ[2])

    return allWater

def grepout():
    allWater = occu()
    for eachLine in open("out.pdb"):
        resName = eachLine[17:20] + eachLine[21] + ("%04d" % int(eachLine[22:26]))
        for eachWater in allWater:
            if eachWater.resName == resName:
                print eachLine[:21] + 'Y' + eachLine[22:],
                break

def main():
    grepout()
 
if __name__ == "__main__":
    main()
