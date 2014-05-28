#!/usr/bin/env python
import os
import sys
import subprocess
from colorama import Fore, Back, Style

'''Use this script to run another command or script in multiple directories.'''

def prepare_dirs():
    '''Get all the directories in which the command needs to be run.

    '''
    allDirs = []

    base_folder = "/home/xzhu/BR2"

    pdbs = ["1C3W", "1C8R", "1KG9", "1DZE", "1KG8", "1C8S", "1F4Z"]
    pdb_types = ["crystal"]
    run_types = ["quick"]
    #run_types = ["quick", "def"]
    scale_types = ["raw"]

    for eachPdb in pdbs:
        for eachPdbType in pdb_types:
            for eachRun in run_types:
                for eachScale in scale_types:
                    finalPath = os.path.join(base_folder, eachPdb, eachPdbType, eachRun, eachScale)
                    allDirs.append(finalPath)

    return allDirs


def multi_run(comm):
    '''Run the command or script "comm" in multiple directories.

    '''
    allDirs = prepare_dirs()
    for eachPath in allDirs:
        os.chdir(eachPath)
        print(Fore.GREEN + eachPath + Fore.RESET)
        subprocess.check_call(comm)


def main():
    multi_run(sys.argv[1:])


if __name__ == "__main__":
    main()
     
