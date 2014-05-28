#!/usr/bin/env python

import argparse

'''Count the number of occupied waters.'''

def get_occ_water(threshold=1.000):
    '''Read fort.38 to find the occupied waters.
   
    Waters which have occ of dummy conformers less than the threshold are occupied.

    '''
    fp = open("fort.38", 'r')
    fp.readline()

    occWaters = []
    for eachLine in fp:
        if eachLine[:5] != "HOHDM": continue

        fields = eachLine.split()

        occ = float(fields[1])
        if occ >= threshold: continue

        # this water is occupied
        resName = fields[0][:3] + fields[0][5:10]
        occWaters.append(resName)

    return occWaters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="the threshold to determine if a water is occupied", default=1.000, nargs='?', type=float)
    args = parser.parse_args()

    occWaters = get_occ_water(args.t)
    counter = [0, 0]
    for w in occWaters:
        if w[3] == 'A': counter[0] += 1
        elif w[3] == 'X': counter[1] += 1

    print "crystal: %d, ipece: %d" % (counter[0], counter[1])


if __name__ == "__main__":
    main()        
       
