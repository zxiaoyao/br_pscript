#!/usr/bin/env python

'''Divide all the residues in the hbond network into 3 groups.

For all the residues in the hbond network represented in "hb.txt":
    group1: all the waters.
    group2: all the key residues in the pathway.
    group0: the rest of the residues in the network.
'''

residues = set()
for eachLine in open("hb.txt"):
    res1, res2, occ = eachLine.split()
    residues.add(res1)
    residues.add(res2)

keyResidues = ["ASPA0085", "ARGA0082", "GLUA0194", "GLUA0204", "RSBA0216"]
for eachRes in residues:
    if eachRes.startswith("HOH"):
        print eachRes, '\t', 1
    elif eachRes in keyResidues:
        print eachRes, '\t', 2
    else:
        print eachRes, '\t', 0
