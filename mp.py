#!/usr/bin/python

from constants import *
from tpl import *

class ATOM:
    def __init__(self):
        self.serial      = -1
        self.name        = ''
        self.altLoc      = ''
        self.resName     = ''
        self.chainID     = ''
        self.resSeq      = -1
        self.iCode       = ''
        self.xyz         = []
        self.rad         = 0.0 
        self.crg         = 0.0
        self.history     = ''  

        return
 
    def loadStepLine(self, line):
        self.serial      = int(line[6:11])
        self.name        = line[12:16]
        self.altLoc      = line[16]
        self.resName     = line[17:20]
        self.chainID     = line[21]
        self.resSeq      = int(line[22:26])
        self.iCode       = line[26]

        if self.iCode == " ": self.iCode = "_"

        self.xyz         = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
        self.rad         = float(line[54:62]))
        self.crg         = float(line[68:74])
        self.history     = line[80:90]

        return
         
class CONFORMER:
    def __init__(self):
        self.atoms = []

        self.resName = ''
        self.resSeq = -1
        self.confName = ''
        self.iCode = ''

        self.iConf = -1
        self.crg = 0.0
        self.Em0 = 0.0
        self.pKa0 = 0.0
        self.ne = 0
        self.nH = 0
        self.FL = ''
        self.occ = 0.0 

        self.E_vdw0 = 0.0
        self.E_vdw1 = 0.0
        self.E_tors = 0.0
        self.E_epol = 0.0
        self.E_dsolv = 0.0
        self.extra  = 0.0
        self.history = ''
       
        self.focc = [] 

        return
         
    def initial_by_h3(line):
        self.iConf = int(line[:5])
        self.confName = line[6:20]
        self.FL    = line[21]
        self.occ   = float(line[22:27])
        self.crg   = float(line[27:34])
        self.Em0   = float(line[34:40])
        self.pKa0  = float(line[40:46])
        self.ne    = int(line[46:49])
        self.nH    = int(line[49:52])
        self.E_vdw0= float(line[52:60])
        self.E_vdw1= float(line[60:68])
        self.E_tors= float(line[68:76])
        self.E_epol= float(line[76:84])
        self.E_dsolv=float(line[84:92])
        self.E_extra=float(line[92:100])
        self.history=line[101:112]

        self.resName = self.confName[:3]
        self.resSeq  = int(self.confName[6:10])
        self.iConf   = int(self.confName[-3:]

        return

    def inRes(resName):
        if resName == self.resName:
            return True
        else:
            return False

    def load_occ(line):
        fields = line.split()[1:]
        for occ in fields:
            self.focc.append(float(occ))

        return
             
class RESIDUE:
   def __init__(self):
      self.confs=[]
      return
   
class PROTEIN:
   def __init__(self):
      self.ress=[]
      
      return
   
   def readPDB(self, fname):
      lines = [line for line in open(fname).readlines() if line[:6] == "ATOM  " or line[:6] == "HETATM"]
      lines = [line for line in lines if line[13] != "H"]
      for line in lines:
         atom = ATOM()
         atom.loadline(line)

         # search if this atom belongs to an existing residue. Reverse order makes search faster
         Found = False
         for i_res in range(len(self.ress)-1, -1, -1):
            if self.ress[i_res].resName == atom.resName and \
               self.ress[i_res].chainID == atom.chainID and \
               self.ress[i_res].resSeq  == atom.resSeq  and \
               self.ress[i_res].iCode   == atom.iCode:
               Found = True
               break

         # If not found, add a new residue
         if not Found:
            res = RESIDUE()
            res.resName = atom.resName
            res.chainID = atom.chainID
            res.resSeq  = atom.resSeq
            res.iCode   = atom.iCode

            # Insert a backbone conformer regardless of atoms
            conf = CONFORMER()
            conf.confName = atom.resName+"BK"
            conf.history  = "BK________"
            
            res.confs.append(conf)
            self.ress.append(res)
            i_res = len(self.ress)-1
            # at this point, the current atom must be in the residue i_res
            
         # load this atom to a condormer of residue i_res
         if (len(line) == 90 and line[80:82]) == "BK" or atom.name in BackboneAtoms[atom.resName]:
            self.ress[i_res].confs[0].atoms.append(atom)
         else:
            All_have_it = True
            for i_conf in range(len(self.ress[i_res].confs)-1, 0, -1):
               if atom.name not in [x.name for x in self.ress[i_res].confs[i_conf].atoms]:
                  # Add to the first conformer found in the reversed order regardless of conformer type
                  self.ress[i_res].confs[i_conf].atoms.append(atom)
                  All_have_it = False
                  break

            if All_have_it:
               conf = CONFORMER()
               # Since this atom is in a new conformer, we have to decide if it belongs to a predefined conformer
               if len(line) == 90:
                  conf.confName = atom.name+line[80:82] # from pdb file
                  conf.history  = line[80:90]
               else:
                  conf.confName = ConfTypes[self.ress[i_res].resName][0] # from conformer list
                  conf.history  = conf.confName[3:5]+"________"
               self.ress[i_res].confs.append(conf)
               self.ress[i_res].confs[len(self.ress[i_res].confs)-1].atoms.append(atom)
      return
               
   def writePDB(self):
      output_lines=[]
      c = 0
      for res in self.ress:
         iConf = -1     # count from 0, -1 to compensate += 1
         for conf in res.confs:
            iConf += 1
            for atom in conf.atoms:
               c += 1
               line = "ATOM  %5d %4s%c%3s %c%04d%c%03d%8.3f%8.3f%8.3f %7.3f      %6.3f      %-10s\n" % (
                            c, atom.name,
                            atom.altLoc,
                            res.resName,
                            res.chainID,
                            res.resSeq,
                            res.iCode,
                            iConf,
                            atom.xyz[0],
                            atom.xyz[1],
                            atom.xyz[2],
                            atom.rad,
                            atom.crg,
                            conf.history)

               output_lines.append(line)
      return output_lines
