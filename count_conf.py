#!/usr/bin/python

def count_conf():
    ''' Count the number of conformers in step2_out.pdb."
    
    Assuming the atoms in a conformer are in consecutive lines.
    '''
    
   atoms = open("step2_out.pdb").readlines()
   for line in atoms:
      if line[:6] != 'ATOM  ' and line[:6] != 'HETATM': continue
      if line[27:30] == '000': continue
      confid_old = line[21:30]
      break
   count = 0
   for line in atoms:
      if line[:6] != 'ATOM  ' and line[:6] != 'HETATM': continue
      if line[27:30] == '000': continue
      confid_new = line[21:30]
      if confid_new == confid_old: 
         continue
      else:
         count = count + 1
         confid_old = confid_new
   count = count + 1

   return count

if __name__ == "__main__":
   counter = count_conf()
   print 'there are ', counter, 'confermers'
