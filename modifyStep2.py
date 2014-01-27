#!/usr/bin/env python
import sys, argparse

def modifyStep2(cutoff=-1.0, outFile="step2_out.pdb", waterStatFile="water_stat.txt", step2File="step2_out.pdb"):
    '''Remove the unoccupied waters in step2_out.pdb
    '''
    
    removeWaters = []
    for eachLine in open(waterStatFile):
        resName = eachLine.split()[0]
        occ = float(eachLine.split()[1])
        if occ > cutoff:
            removeWaters.append(resName)
            
    newLines = []
    for eachLine in open(step2File):
        resName = eachLine[17:20] + eachLine[21:26]
        if resName not in removeWaters:
            newLines.append(eachLine)
    open(outFile, 'w').writelines(newLines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest="threshold", type=float, default=-1.0,
                        help="dummy occ cutoff to remove water from step2_out.pdb")
    parser.add_argument("-o", dest="output", default="test.pdb",
                        help="name of the new step2_out.pdb")
    parser.add_argument("-w", dest="water_stat", default="water_stat.txt",
                        help="file that contains occ of waters")
    parser.add_argument("-s", dest="step2", default="step2_out.pdb",
                        help="input file which should be step2_out.pdb")
    args = parser.parse_args()

    modifyStep2(args.threshold, args.output, args.water_stat, args.step2)

if __name__ == "__main__":
    main()
