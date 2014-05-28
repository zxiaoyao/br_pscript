#!/usr/bin/env python
import sys
import os

def count_pdb_water(pdbfile):
    '''Count number of waters in pdb file.

    There is no hydrogen atom in water in pdb file.
       
    '''
    # count number of crystal waters and ipece waters.
    counter = [0, 0]
    for eachLine in open(pdbfile):
        # find a water, only use the line of water contains oxygen.
        if eachLine[17:20] == "HOH" and eachLine[12:16] == " O  ":
            # crystal water.
            if eachLine[21] == 'A': counter[0] += 1
            # water added by IPECE, determined by chain id.
            elif eachLine[21] == 'X': counter[1] += 1

    return counter


def main():
    pdb = os.getcwd().split('/')[4] + ".pdb"
    pdb = "step1_out.pdb"
    n = count_pdb_water(pdb)
    print "Number of crystal water:%5d, ipece water:%5d, totol:%6d" % (n[0], n[1], n[0]+n[1])


if __name__ == "__main__":
    main()
