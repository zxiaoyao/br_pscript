#!/usr/bin/env python
import argparse

class Wat(object):
    '''Water class.
    
    '''
    def __init__(self, resName="", occ=0.0):
        ''' Initialization.
        
        Args:
            resName (str): name of the residue (water), like HOHA0403.
            occ (float, optional): occupancy of the dummy conformer of the water.
            
        '''
        self.resName = resName
        self.dummyOcc = occ
        
        
def getWaterOcc(fName="fort.38"):
    allWaters = []
    fp = open(fName, 'r')
    for eachLine in fp:
        if eachLine.startswith("HOHDM"):
            resName = eachLine[:3] + eachLine[5:10]
            occ = float(eachLine.split()[1])
            newWater = Wat(resName, occ)
            allWaters.append(newWater)
    
    fp.close()

    return allWaters
        
def dummy_wat(threshold=-1.0, inverse=False):
    
    allWaters = getWaterOcc()
    allWaters = sorted(allWaters, key=lambda w: w.dummyOcc)
    counter = 0
    if not inverse:
        for eachWat in allWaters:
            if eachWat.dummyOcc > threshold:
                counter += 1
                print "%-10s%6.3f" % (eachWat.resName, eachWat.dummyOcc)
    else:
        for eachWat in allWaters:
            if eachWat.dummyOcc <= threshold:
                counter += 1
                print "%-10s%6.3f" % (eachWat.resName, eachWat.dummyOcc)
#     print counter
    return allWaters

def cmpTwoOcc(file1, file2, cutoff=-1.0):
    water1 = getWaterOcc(file1)
    water2 = getWaterOcc(file2)
    
    allWaters = []
    for eachWat in water1:
        if not eachWat.resName in allWaters:
            allWaters.append(eachWat.resName)
    for eachWat in water2:
        if not eachWat.resName in allWaters:
            allWaters.append(eachWat.resName)
            
    for eachWat in allWaters:
        found = False
        for eachW1 in water1:
            if eachW1.resName == eachWat:
                found = True
                o1 = eachW1.dummyOcc
                break
        if not found: o1 = "na"
        
        found = False
        for eachW2 in water2:
            if eachW2.resName == eachWat:
                found = True
                o2 = eachW2.dummyOcc
                break
        if not found: o2 = "na"
        
        if o1 == "na" or o2 == "na":
            print "%s%10s%10s" % (eachWat, str(o1), str(o2))
        else:
            diff = o1 - o2
            if abs(diff) > cutoff:
                print "%s%10.3f%10.3f%10.3f" % (eachWat, o1, o2, diff)
  
def main():
    parser = argparse.ArgumentParser()    
    parser.add_argument("-t", dest="threshold", type=float, default=-1.0)
    parser.add_argument("-inverse", action="store_true", help="inversely select the waters")
    parser.add_argument("-c", nargs=2)
    args = parser.parse_args()
     
    if args.c:
        cmpTwoOcc(args.c[0], args.c[1], args.threshold)
    else:
        dummy_wat(args.threshold, args.inverse)

if __name__ == "__main__":
    main()
    
