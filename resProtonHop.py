#!/usr/bin/env python

import argparse

def resProtonHop(sourceRes, targetRes, hbFile="hah.txt"):
    ''' Find all the conformers of two residues that can have proton hopping.

    Need to have the file "hah.txt".
    '''
    
    for eachLine in open(hbFile):
        fields = eachLine.split()
        res1 = fields[0][:3] + fields[0][5:10]
        res2 = fields[1][:3] + fields[1][5:10]
        
        if res1 == sourceRes and res2 == targetRes:
            print eachLine,
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sourceRes", help="hbond donor")
    parser.add_argument("targetRes", help="hbond acceptor")
    parser.add_argument("hbFile", default="hah.file", nargs='?')
    args = parser.parse_args()
    
    resProtonHop(args.sourceRes, args.targetRes, args.hbFile)
    
if __name__ == "__main__":
    main()