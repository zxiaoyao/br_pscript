#!/usr/bin/python

# remove sge jobs from sys.argv[1] to sys.argv[2]

import os, sys

for i in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    print i 
    os.system('qdel -f ' + str(i))    
