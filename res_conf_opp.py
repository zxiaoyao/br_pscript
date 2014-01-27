#!/usr/bin/env python
import sys

def res_conf_opp(res1, res2):
    conf1 = []
    conf2 = []
    
    fp = open("fort.38", 'r')
    fp.readline()
    for eachLine in fp:
        confName = eachLine.split()[0]
        resName = confName[:3] + confName[5:10]
        if resName == res1:
            conf1.append(confName)