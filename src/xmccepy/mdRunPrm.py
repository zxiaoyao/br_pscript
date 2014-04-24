#!/usr/bin/python

import sys

def mdRunPrm(dirPrm, ifile = 'run.prm'):
    '''
    Modify the run.prm file according to dirPrm.

    The dirPrm is a {key_string : value_string} dictionary
    "key_string" doesn't include the '()'
    "value_string" has to be a string object
    '''
    ilines = open(ifile, 'r').readlines()
    
    modifiedKeys = []
    for il in range(len(ilines)):
        for ky in dirPrm.keys():
            if ilines[il].find('(' + ky + ')') > -1:
                old_value_len = len(ilines[il].split()[0])
                ilines[il] = dirPrm[ky] + ilines[il][old_value_len:]
                modifiedKeys.append(ky)
                break
    
    for ky in dirPrm.keys():
        if ky in modifiedKeys: continue
        ilines.append("%s           (%s)\n" % (ky, dirPrm[ky]))

    open(ifile, 'w').writelines(ilines)


def fix_head3(fixList, ifile = 'head3.lst'):
    '''
    Fix ionization of states of conformers in head3.lst
    
    fixList: a list of lists each of which has keys to match the lines in head3.lst
    the conformer that matches the criterir will be fixed in head3.lst
    '''
    
    lines = open(ifile).readlines()
    for il in range(len(lines)):
        for keys in fixList:
            line_match = True
            for key in keys:
            	if lines[il].find(key) == -1:
                    line_match = False
                    break
            if line_match:
                # switch flag to 't'
                lines[il] = lines[il][:21] + 't' + lines[il][22:]
                break

    open(ifile, 'w').writelines(lines)


if __name__ == '__main__':
     #sampDir = {'DO_MONTE':'t'}
     #mdRunPrm(sampDir, sys.argv[1])
     fList = [['LYS', '0']]
     fix_head3(fList)
