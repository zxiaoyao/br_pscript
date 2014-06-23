#!/usr/bin/env python
'''
Created on Jun 19, 2013

@author: xzhu
'''
from xmccepy.head3Lst import Head3Lst
    
HEAD3_LST = "head3.lst"

def read_fix_protonation_file(fname):
    '''Read the file which has info of fixed residue protonations.
    
    '''
    res_protonations = {}
    for eachLine in open(fname):
        fields = eachLine.split()
        res_protonations[fields[0]] = int(fields[1])
        
    return res_protonations
    
    
def change_hflag_according_to_file(hname, fname, freeDummyWaterConf=False, reverse=True, ofile=None):
    '''Change the flag of conformers in head3.lst.
    
    '''
    res_protonations = read_fix_protonation_file(fname)
    
    h3l = Head3Lst()
    h3l.readFromFile(hname)
    
    h3l.freeAllConformers()
    h3l.fixByNumberOfProtons(res_protonations, freeDummyWaterConf, reverse)

    h3l.writeToFile(ofile)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-hl", help="head.lst", default=HEAD3_LST, nargs='?')
    parser.add_argument("-f", help="file has residue protonations")
    parser.add_argument("--freeDummy", action="store_true", help="free all the dummy water conformer")
    parser.add_argument("--reverse", action="store_true", default=False, help="reversely fix the protonation states")
    parser.add_argument("-o", help="output file name of new head3.lst", default=None, nargs='?')
    args = parser.parse_args()

    change_hflag_according_to_file(hname=args.hl, fname=args.f, freeDummyWaterConf=args.freeDummy, reverse=args.reverse, ofile=args.o)        
        
        
if __name__ == '__main__':
    main()
