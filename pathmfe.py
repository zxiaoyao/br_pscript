#!/usr/bin/env python
import os
import subprocess

def main():
    if not os.path.islink("energies"):
        os.system("ln -s ../../../../energies .")
    if os.path.isfile("bak_ms.dat"):
        os.system("mv bak_ms.dat ms.dat")
    os.system("/home/xzhu/gmcce/serialte/te -s")
    p = subprocess.Popen(["tail", "-1", "ms_out"], stdout=subprocess.PIPE)
    pout = p.communicate()[0]
    confs = pout.split()[:6]
    sconf = "/home/xzhu/bin/pythonScript/simpletest.py"
    for eachConf in confs:
        sconf += (" " + eachConf)
    print confs
    os.system(sconf)
    
if __name__ == "__main__":
    main()
