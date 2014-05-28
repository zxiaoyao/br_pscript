#!/usr/bin/python

import sys

def all_occupy(cutoff):

    flines = open('fort.38', 'r').readlines()
    flines.pop()
    for fl in flines:
        occs = fl.split()
        for i in range(len(occs)-1):
            if float(occs[i+1]) >= cutoff:
                print fl,
                break

    return

def ph_occupy(ph, cutoff):

    flines = open('fort.38', 'r').readlines()

    fheads = flines[0].split()
    found_point = False
    for i in range(len(fheads)-1):
        if float(fheads[i+1]) == float(ph):
            found_point = True
            titr_point = i
            break
    if not found_point:
        print 'Can not find the titration point'
        exit()
    
    flines.pop()
    for fl in flines:
        occs = fl.split()    
        if float(occs[i+1]) >= cutoff:
            print fl,

    return

if __name__ == '__main__':
    
    cutoff = 0.001
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-c':
            cutoff = float(sys.argv[i+1])
            break

    p_found = False
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-p':
            ph_occupy(sys.argv[i+1], cutoff)
            p_found = True
            break
      
    if p_found == False:
        all_occupy(cutoff)
