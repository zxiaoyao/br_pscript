#!/usr/bin/env python

N_RES = 6

def lineToString(line, n=6):
    fields = line.split()
    s = ""
    for i in range(n):
        s += fields[i]
    return s

def main(subName, hopName):
    subStrings = []
    for eachLine in open(subName):
        subStrings.append(lineToString(eachLine))

    allLines = open(hopName).readlines()
    for i in range(len(allLines)-len(subStrings)+1):
        if not allLines[i].strip(): continue
        found = True
        for j in range(N_RES):
            if subStrings[j] != lineToString(allLines[i+j]):
                found = False
                break
        if found:
            for j in range(N_RES+1):
                print allLines[i-1+j],
            for j in range(N_RES+1):
                print allLines[i-1+j].split()[-1]
            break

if __name__ == "__main__":
    import sys
    main(sys.argv[1], sys.argv[2])
            
        
