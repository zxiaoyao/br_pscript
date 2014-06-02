#!/usr/bin/python
import os, sys
import networkx as nx

possibleIonization = {"ASP":['-', '0'], "ARG":['0', '+'], "GLU":['-', '0'], "RSB":['0', '+'], "HOH":['-', '0', '+']}
possibleIonization["TYR"] = ['-', '0']
possibleIonization["LYS"] = ['0', '+']

def isValidPath(path):
    '''Test if each residue in the pathway has a neutral protonation state.
    
    '''
    is_valid = True
    for eachResidue in path:
        if len(possibleIonization.get(eachResidue[:3], ['0'])) == 1:
            print eachResidue
            is_valid = False
            break
        
    return is_valid


def getAllPaths():
    '''Get all the pathways.
    
    Between ASPA0085 and GLUA0194.
    '''
    g = nx.read_weighted_edgelist("hb.txt")                
    fp = open("allpaths.txt", 'w')
    
    try:
        counter = 1
        for eachPath in nx.all_shortest_paths(g, u"ASPA0085", u"GLUA0194"):
            if not isValidPath(eachPath):
                continue
            
            fp.write("path%d" % counter)
            for eachResidue in eachPath:
                fp.write('%10s' % eachResidue)
            fp.write('\n')
            
            counter += 1
    except nx.exception.NetworkXNoPath:
        fp.write("No connected pathway\n")
    finally:
        fp.close()
        

def writeftxt(keyResidues):
    fp = open("f.txt", 'w')
    for eachResidue in keyResidues:
        fp.write(eachResidue + '\n')
    fp.close()
    
    
def getInitialStates(keyResidues):
    initStates = []
    
    defaultStates = {}
    sumLines = open("../sum_crg.out").readlines()[:-4]
    sumLines.pop(0)
    for eachLine in sumLines:
        fields = eachLine.split()
        resName = fields[0][:3] + fields[0][4:9]
        ionizationState = '0'
        if float(fields[1]) > 0.5:
            ionizationState = '+'
        elif float(fields[1]) < -0.5:
            ionizationState = '-'
        defaultStates[resName] = ionizationState
    
    
    for eachResidue in keyResidues:
        if eachResidue == "ASPA0085":
            initStates.append('0')
        elif eachResidue == "GLUA0194":
            initStates.append('-')
        elif eachResidue == "ARGA0082":
            initStates.append('+')
        else:
            initStates.append(defaultStates[eachResidue])
            
    return initStates


def writeinittxt(keyResidues):
    initStates = getInitialStates(keyResidues)
    
    fp = open("init.txt", 'w')
    for eachState in initStates:
        fp.write(' ' + eachState)
    fp.write('\n')
    fp.close()
    
    
def writePathInfo(keyResidues):
    
    fp = open("pathinfo.txt", 'w')
    for eachResidue in keyResidues:
        fp.write(eachResidue)
        for eachState in possibleIonization[eachResidue[:3]]:
            fp.write('  ' + eachState)
        fp.write('\n')
    
    initStates = getInitialStates(keyResidues)
    for eachState in initStates:
        fp.write(' ' + eachState)
    fp.write('\n')
    
    fp.close()
    
def setUpHbRun():
    #getAllPaths()
    allPathFileName = "secondshortestpaths.txt"
    if "No connected pathway" in open(allPathFileName).read():
        sys.stderr.write("No connected pathway\n")
        return
    
    for eachLine in open(allPathFileName).readlines():
        fields = eachLine.split()
        
        #os.system("rm -rf " + fields[0])
        if not os.path.exists(fields[0]):
            os.mkdir(fields[0])
        os.chdir(fields[0])
        keyResidues  = fields[1:]
        
        writeftxt(keyResidues)
        writeinittxt(keyResidues)
        writePathInfo(keyResidues)
        
        os.system("/home/xzhu/gmcce/hbPath/hBondPath.py -s pathinfo.txt")
        os.system("cp ../ms_gold .")
        os.system("cp ../head3.lst .")
        os.system("ln -s ../energies.opp .")
        os.system("cp ../run.prm .")
        
        os.system("/home/xzhu/bin/pythonScript/fix_io.py -s f.txt all_states.txt")
        os.chdir("..")

def retrieveHbRun():
    if not os.path.exists("allpaths.txt"):
        sys.stderr.write("No file allpaths.txt\n")
        return
    
    if "No connected pathway" in open("allpaths.txt").read():
        sys.stderr.write("No connected pathway\n")
        return
    
    for eachLine in open("allpaths.txt").readlines():
        fields = eachLine.split()
        os.chdir(fields[0])
        
        os.system("/home/xzhu/bin/pythonScript/fix_io.py -r f.txt all_states.txt")
        os.chdir("..")
        
def getEnergyBarrier():
    if not os.path.exists("allpaths.txt"):
        sys.stderr.write("No file allpaths.txt\n")
        return
    
    if "No connected pathway" in open("allpaths.txt").read():
        sys.stderr.write("No connected pathway\n")
        return
    
    fp = open("path_stat.txt", 'w')
    for eachLine in open("allpaths.txt").readlines():
        fields = eachLine.split()
        os.chdir(fields[0])
        
        #os.system("/home/xzhu/bin/hbondpath/hBondPath.py ener.txt init.txt")
        os.system("/home/xzhu/gmcce/hbPath/hBondPath.py -e ener.txt init.txt")
        eBarrier = open("paths.txt").readline().split()[-1]
        fp.write(eachLine[:-1] + '\t' + eBarrier + '\n')
        os.chdir("..")
    fp.close()    


def helpMessage():
    print "syntax: "
    print "  To setup:               setuphbrun.py -s"
    print "  To retrieve:            setuphbrun.py -r"
    print "  To get energy barriers: setuphbrun.py -e"
    
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        helpMessage()
    elif sys.argv[1] == "-s":
        setUpHbRun()
    elif sys.argv[1] == "-r":
        retrieveHbRun()
    elif sys.argv[1] == "-e":
        getEnergyBarrier()


