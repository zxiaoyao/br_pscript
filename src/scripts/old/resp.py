#!/usr/bin/python
import sys, os

def loadKeyGroup(fileName):
    keyGroups = [line.strip() for line in open(fileName)]
    return keyGroups

    
def main():
    fixedGroups = ['RSBA0216', 'GLUA0204']
    keyGroups = loadKeyGroup('f.txt')
    surroundGroups = []

    lines = open('respair.lst').readlines()
    lines.pop(0)

    for line in lines:
        fields = line.split()

        if abs(float(fields[4])) > float(sys.argv[1]):
            resName = fields[0][:3] + fields[0][4:9]
            surroundName = fields[1][:-1]
            
            if resName in keyGroups or surroundName in keyGroups:
                if not (resName in keyGroups and surroundName in keyGroups):
                    print line, 

                    if surroundName not in surroundGroups:
                        if surroundName not in keyGroups and surroundName not in fixedGroups:
                            surroundGroups.append(surroundName)
                    if resName not in surroundGroups:
                        if resName not in keyGroups and resName not in fixedGroups:
                            surroundGroups.append(resName)
    
    if len(surroundGroups) != 0:
        fortlines = open('fort.38').readlines()
        fortlines.pop(0)

        print '\nResidues surrounding: '
        for res in surroundGroups:
            print res
            for line in fortlines:
                fortName = line[:3] + line[5:10]
                if fortName == res:
                    if float(line.split()[1]) > 0.1:
                        print line,
               
                  

def usage():
    print 'Syntax:'
    print '	res.py cutoff'


if __name__ == '__main__':
     if len(sys.argv) == 2:
         pdbs   = ["1C8R", "1C3W", "1KG9", "1DZE", "1KG8", "1C8S"]
         for pdb in pdbs:
             os.chdir('/home/xzhu/BR_ipe_mem/' + pdb + '/hydro/implictWat/def/lj0.1')
             print pdb
             main()
             print 
     else:
         usage()
