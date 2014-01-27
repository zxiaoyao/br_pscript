#!/usr/bin/env python

import argparse
import os, subprocess

def mfePath():
    parser = argparse.ArgumentParser()
    parser.add_argument("res", nargs="+", help="all the conformers in the pathway")
    args = parser.parse_args()
    
    eSelf = 0.0
    for eachConf in args.res:
        p = subprocess.Popen(["grep", eachConf, "mc_out"], stdout=subprocess.PIPE)
        pout = p.communicate()[0]
        eSelf += float(pout.split()[2])
        print "%s\t%s" % (pout.split()[0], pout.split()[2])
    print "\t%15.3f" % eSelf
        
    ePair = 0.0
    for eachConf in args.res:
        p = subprocess.Popen(["/home/xzhu/bin/mcce++/lib/mfetest", eachConf, "-t", "5", "-s", "0.1"], stdout=subprocess.PIPE)
        pout = p.communicate()[0]
        print eachConf
        
        for eachLine in pout.split('\n')[3:]:
            if eachLine.startswith("SUM"): ePair += float(eachLine.split()[1])
            for eachCol in eachLine.split():
                print eachCol + '\t',
                
            print
    print 'mfe\t', ePair
    print 'Total\t', eSelf + 1.364 * ePair 
    
        
def main():
    mfePath()
    
if __name__ == "__main__":
    main()
    

