#!/usr/bin/env python
import argparse

'''Remove the occupied waters in step2_out.pdb.
The "fort.38" and "step2_out.pdb have to be in the current directory.
'''

def getUnoccupiedWater(threshold=1.000):
    '''Get all the unoccupied waters according to fort.38.
     
    @note Assuming there is only one titration point.
    @param threshold a water is unoccupied if the occ of dummy conformer is larger than or equal to the threshold.

    '''
    unoccupied_waters = []

    fp = open("fort.38", 'r')
    fp.readline()
    
    for eachLine in fp:
        if eachLine[:5] != "HOHDM": continue
        fields = eachLine.split()
        occ = float(fields[1])
        if occ < threshold: continue
        resName = fields[0][:3] + fields[0][5:10]
        unoccupied_waters.append(resName)

    return unoccupied_waters

        
def remove_unoccupied_water(threshold):
    '''Remove the unoccupied waters from step2_out.pdb.

    The result will be printed to the stdout.
 
    '''
    unoccupied_waters = getUnoccupiedWater(threshold)
    
    fp = open("step2_out.pdb", 'r')
    for eachLine in fp:
        # only consider waters here. 
        if eachLine[17:20] != "HOH": 
            print eachLine,
            continue
        resName = "HOH" + eachLine[21:26]
        if resName not in unoccupied_waters:
            print eachLine,  


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help="The threshold to determine if a water is unoccupied", default=1.000, nargs='?')
    args = parser.parse_args()

    remove_unoccupied_water(args.t)


if __name__ == "__main__":
    main()
    
