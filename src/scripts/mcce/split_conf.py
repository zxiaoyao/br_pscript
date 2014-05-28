#!/usr/bin/env python
import sys, os, argparse

class Atom(object):
    def __init__(self):
        self.remark = ""
        self.atomId = 0
        self.alt = ""
        self.atomName = ""
        self.resName = ""
        self.chainId = ""
        self.resSeq = 0
        self.confSeq = 0
        self.coor = [0.0, 0.0, 0.0]
        self.confType = ""
        
        self.resIdName = ""
        self.confIdName = ""
        
        
    def parse_step2_line(self, line):
        self.remark = line[:6]
        self.atomId = int(line[6:11])
        self.atomName = line[12:16]
        self.alt = line[16]
        self.resName = line[17:20]
        self.chainId = line[21]
        self.resSeq = int(line[22:26])
        self.confSeq = int(line[27:30])
        self.coor = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
        self.confType = line[80:82]
        
        self.resIdName = self.resName + self.chainId + ("%04d" % self.resSeq)
        self.confIdName = self.resName + self.confType + self.chainId + ("%04d" % self.resSeq) + "_" + ("%03d" % self.confSeq)

        
    def write_pdb_line(self):
        return "%6s%5d %4s%s%3s %s%4d    %8.3f%8.3f%8.3f                  %4d"\
            % (self.remark, self.atomId, self.atomName, self.alt,\
               self.resName, self.chainId, self.resSeq, self.coor[0],\
               self.coor[1], self.coor[2], self.confSeq)
            
class Conformer(object):
    def __init__(self):
        self.confName = ""
        self.atoms = []
        self.confSeq = 0
        
class Residue(object):
    def __init__(self):
        self.resName = ""
        self.sidechains = []
        self.backbone = Conformer()
        
    def relabel_confSeq(self):
        iConf = 1
        self.sidechains = sorted(self.sidechains, key=lambda eachSidechain: eachSidechain.confSeq)
        for eachSidechain in self.sidechains:
            eachSidechain.confSeq = iConf
            eachSidechain.confName = eachSidechain.confName[:-3] + ("%03d" % eachSidechain.confSeq)
            iConf += 1
            
    def write_sidechain_pdb(self):
        for eachSidechain in self.sidechains:
            fp = open(eachSidechain.confName + '.pdb', 'w')
            for eachAtom in self.backbone.atoms:
                fp.write(eachAtom.write_pdb_line() + '\n')
            for eachAtom in eachSidechain.atoms:
                fp.write(eachAtom.write_pdb_line() + '\n')
            fp.close()
            
def split_conf(fName="step2_out.pdb"):
    '''Split all conformers in step2_out.pdb into individual pdb files.
    '''
    allResidues = []
    for eachLine in open(fName):
        newAtom = Atom()
        newAtom.parse_step2_line(eachLine)
        
        resFound = False
        for eachRes in allResidues:
            if eachRes.resName == newAtom.resIdName:
                if eachRes.backbone.confName == newAtom.confIdName:
                    resFound = True
                    eachRes.backbone.atoms.append(newAtom)
                    break
                for eachConf in eachRes.sidechains:
                    if eachConf.confName == newAtom.confIdName:
                        resFound = True
                        eachConf.atoms.append(newAtom)
                        break
                    
                # conformer not exist
                if not resFound: 
                    newConf = Conformer()
                    newConf.atoms.append(newAtom)
                    newConf.confName = newAtom.confIdName
                    newConf.confSeq = newAtom.confSeq
                    
                    eachRes.sidechains.append(newConf)
                    resFound = True
                    break
             
        # residue not exist   
        if not resFound:
            newRes = Residue()
            newRes.resName = newAtom.resIdName
            if newAtom.confType == "BK":
                newRes.backbone.confName = newAtom.confIdName
                newRes.backbone.atoms.append(newAtom)
            else:
                newConf = Conformer()
                newConf.atoms.append(newAtom)
                newConf.confName = newAtom.confIdName
                newConf.confSeq = newAtom.confSeq
                
                newRes.sidechains.append(newConf)
            allResidues.append(newRes)
            
    for eachRes in allResidues:
        eachRes.relabel_confSeq()
        
    if not os.path.isdir("testconfs"):
        os.mkdir("testconfs")
    os.chdir("testconfs")
    for eachRes in allResidues:
        eachRes.write_sidechain_pdb()
#         if eachRes.resName == "HOHX0478":
#         for eachConf in eachRes.sidechains:
#             print eachConf.confName
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName", default="step2_out.pdb", nargs='?')
    args = parser.parse_args()
    
    split_conf(args.fileName)
    
if __name__ == "__main__":
    main()