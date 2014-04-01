'''
Created on Mar 19, 2014

@author: xzhu
'''

"""Check the directories and files that may eat up the disk space."""

import argparse
import os
import sys



def main():
    
    # arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("direct", help="root directory of the search")
    parser.add_argument("-f", help="the searching file name")
    parser.add_argument("-d", help="the searching directory name")
    parser.add_argument("--delete", help="delete the searched directories and files", action="store_true")
    args = parser.parse_args()
    
    for root, dirs, files in os.walk(args.direct):
        if args.d:
            for eachDir in dirs:
                if eachDir == args.d:
                    os.system("sudo du -hs " + os.path.join(root, eachDir))
                    if args.delete:
                        os.system("sudo rm -rf " + os.path.join(root, eachDir))
                    
        if args.f:
            for eachFile in files:
                if eachFile == args.f:
                    os.system("sudo du -hs " + os.path.join(root, eachFile))
                    if args.delete:
                        os.system("sudo rm -f " + os.path.join(root, eachFile))
    
if __name__ == '__main__':
    main()