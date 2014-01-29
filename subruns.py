#!/usr/bin/python
# This program splits a working directory into subdirctories that can run partial delphi
#8/21/06 changed executable from mcce2.2/mcce to mcce2.2/mcce_0720, Gail
import sys, os, zlib

def print_help():
   print "subruns.py [-s n_steps"
   print "   This program divides step 3 of MCCE into sub working directories, which"
   print "   contain partial delphi run setups, and prepare a condor submit script."
   print "   When the step 3 in sub directories are finished, thia program can combine"
   print "   the result into current directory.\n"
   print "   -s n_steps: split to sub directories which contain n_steps of delphi each"
   print "   -c: to collect all the sub runs"
   return

def count_conf():
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
         count += 1
         confid_old = confid_new
   count += 1
   return count
 
def split_dirs(n_steps):

   # try to read head2.lst first to get the conformer number
   try:
      n_confs = len(open("head2.lst").readlines()) - 1
   except:
      n_confs = count_conf()

   # create a run.prm template
   runprm = open("run.prm").readlines()
   lines = []
   for line in runprm:
      if   line.find("(DO_PREMCCE)") >=0:
         line = "f        step 1: pre-run, pdb-> mcce pdb                    (DO_PREMCCE)\n"
      elif line.find("(DO_ROTAMERS)") >=0:
         line = "f        step 2: make rotatmers                             (DO_ROTAMERS)\n"
      elif line.find("(DO_ENERGY)") >=0:
         line = "t        step 3: do energy calculations                     (DO_ENERGY)\n"
      elif line.find("(DO_MONTE)") >=0:
         line = "f        step 4: monte carlo sampling                       (DO_MONTE)\n"
      elif line.find("(DELPHI_START)") >=0:
         line = "#START#  delphi start conformer number, 0 based             (DELPHI_START)\n"
      elif line.find("(DELPHI_END)") >=0:
         line = "#END#    delphi end conformer number, self included         (DELPHI_END)\n"
   # for the mcce2.5, we change DELPHI to PBE
      elif line.find("(PBE_START)") >=0:
         line = "#START#  pbe start conformer number, 0 based             (PBE_START)\n"
      elif line.find("(PBE_END)") >=0:         
         line = "#END#    pbe end conformer number, self included         (PBE_END)\n"
         
      lines.append(line)

   # number of sub directories      
   n_dirs = n_confs/n_steps + 1
   
   # create sub directories, copy run.prm and step2_out.pdb
   sub_fp = open('sub_list', 'w')
   for i in range(n_dirs):
      dir_name = "sub%03d" % (i+1)
      sub_fp.write(dir_name + '\n')
      try:
         os.mkdir(dir_name)
      except:
         pass
      fp = open("%s/run.prm"%dir_name, "w")
      for line in lines:
         fp.write(line.replace("#START#", "%d" % (i*n_steps+1)).replace("#END#", "%d" % ((i+1)*n_steps)))
      fp.close()
      
      try:
         os.remove("%s/step2_out.pdb" % dir_name)
         os.remove("%s/new.tpl" % dir_name)
      except:
         pass
      os.symlink("../step2_out.pdb", "%s/step2_out.pdb" % dir_name);
      os.symlink("../new.tpl", "%s/new.tpl" % dir_name);


   # create condor_submit file
   # if the machine has condor on it
   if not os.system("which condor_submit > /dev/null"): 
      lines = []
      lines.append("Executable = /home/mcce/mcce2.4.4/mcce\n")
      lines.append("Universe = vanilla\n")
      lines.append("error   = condor.err\n")
      lines.append("output  = run.log\n")
      lines.append("Log     = condor.log\n")
      lines.append("getenv   = true\n")
      lines.append("Notification = never\n\n")
   
      for i in range(n_dirs):
         lines.append("Initialdir = sub%03d\n" % (i+1))
         lines.append("queue\n\n")
      open("submit", "w").writelines(lines)

   # creat a sge submit file "msubmit.sh"
   # if the machine has sge on it
   if not os.system("which qsub > /dev/null") :
      lines = []
      lines.append("#!/bin/bash\n")
      lines.append("curpath=`pwd`\n")
      lines.append("for sub in `ls -d sub*/`\n")
      lines.append("do\n")
      lines.append("    cd ${curpath}/${sub}\n")
      lines.append("    cp /home/xzhu/pfile/submit.sh .\n")
      lines.append("    qsub submit.sh\n")
      lines.append("done\n")
      open("msubmit.sh", "w").writelines(lines)
      os.chmod("msubmit.sh", 0755)
   return

def append_dirs(sub_fp):
    os.system('cp /home/xzhu/pfile/zopp_sub.sh .')
    opp_fp = open('zopp_sub.sh', 'a')
    opp_fp.write('/home/xzhu/bin/zopp -a ')

    dirs = []
    for line in open(sub_fp, 'r'):
        dirs.append(line.strip('\n'))

#    os.system('cp ' + dirs[0] + '/energies.opp .')

    
    for dir in dirs:
        opp_fp.write(dir + ' ')
    opp_fp.write('\n')
    os.system('qsub zopp_sub.sh')
        
if __name__ == "__main__":
   if len(sys.argv) < 3:
      print_help()
      sys.exit()
   
   if   sys.argv[1] == "-s":
      n_steps = int(sys.argv[2])
      split_dirs(n_steps)

   elif sys.argv[1] == '-c':
      append_dirs(sys.argv[2])

   else:
      print_help()
      sys.exit()
