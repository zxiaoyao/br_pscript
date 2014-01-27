#!/usr/bin/python
import os, sys
# get the target residues in the parameter directory
def tar_res():
    all_tpl = os.listdir('.')
    res = []
    for tpl in all_tpl:
        if tpl.endswith('.tpl'):
            res.append(tpl[:-4])
    
    return res

def split_pdb(pdb):
    pdb_lines =[]
    for line in open(pdb).readlines():
        if line.startswith('ATOM'):
            pdb_lines.append(line)
   
    all_res = []
    res     = []

    old_res = pdb_lines[0][17:20]
    old_chainID = pdb_lines[0][21]
    old_resSeq  = int(pdb_lines[0][22:26])
       
    for line in pdb_lines:
        new_res = line[17:20]
        new_chainID = line[21]
        new_resSeq  = int(line[22:26])

        if old_res == new_res and old_chainID == new_chainID and old_resSeq == new_resSeq:
            res.append(line)
        else:
            found = False 
            for i in range(len(all_res)):
                if old_res == all_res[i][0]:
                    found = True
                    all_res[i].append(res)
                    break
            if found == False:
                all_res.append([old_res, res])

            res = []
            res.append(line)
            old_res = new_res
            old_chainID = new_chainID
            old_resSeq = new_resSeq
   
    return all_res
        
def set_tpl_zero(all_res):
    for res in all_res:
        flines = open(res[0].lower() + '.tpl', 'r').readlines()
        fp     = open(res[0].lower() + '.tpl', 'w')
        for line in flines:
            if line.startswith('RXN'):
                line = line[:20] + '0.00\n'
            fp.write(line)

    return
   
def write_pdb(res, i):
    fp = open('prot.pdb', 'w')
    fp.writelines(res[i+1])
    fp.close()

    return
     
def submit_runs(all_res):
    for res in all_res:
        os.mkdir(res[0])
        os.chdir(res[0])
        for i in range(len(res)-1):
            os.mkdir('re_' + str(i+1))
            os.chdir('re_' + str(i+1))
            os.system('cp /home/xzhu/pfile/submit.sh .')
            os.system('cp ../../run.prm .')
            write_pdb(res, i)
            os.system('qsub submit.sh')
            os.chdir('../')          
        os.chdir('../')

    return


def res_conftype(all_res):
    conf_type = {}
    for res in all_res:
        lines = open(res[0].lower() + '.tpl').readlines()
        for line in lines:
            if line.startswith('CONFLIST'):
                fields = line.split()
                conf_type[res[0]] = fields[2:]
                break
    
    return conf_type 
        
def collect_runs(all_res):
    dsol = {}
    # types: a dictionary of all conformer types of the residues, {'GLU':['GLU01', 'GLU-1']}
    types = res_conftype(all_res)
    for res in all_res:
        os.chdir(res[0])
        for type in types[res[0]]:
            dsol[type] = []
            for i in range(len(res)-1): 
                for line in open('re_' + str(i+1) + '/head3.lst', 'r').readlines():
                    if line.find(type) > -1:
                       dsol[type].append(float(line[84:92]))
        os.chdir('..')

    for key in dsol.keys():
        if len(dsol[key]) == 0:
            del dsol[key]
            continue

        sum = 0.0
        for i in range(len(dsol[key])):
            sum = sum + dsol[key][i]
        dsol[key] = sum/len(dsol[key])

          
    for res in all_res:
        flines = open(res[0].lower() + '.tpl', 'r').readlines()
        fp     = open(res[0].lower() + '.tpl', 'w')       
        for line in flines:
            if line.startswith('RXN'):
                print line,
                fields = line.split()
                for type in types[res[0]]:
                    if dsol.has_key(type):
                        if fields[1] == type:
                            line = line[:20] + str('%.2f' % dsol[type]) + '\n'
                
            fp.write(line)
    
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage:'
        print 'e_param.py -s 3BDC.pdb'
        print 'To collect the dsol data:'
        print 'e_param.py -c 3BDC.pdb'
        exit()

    pdir = os.getcwd() 
    pdb = sys.argv[2]

    tar_res = tar_res()
    #split the pdb file into small ones with only one residue in it
    all_res = split_pdb(pdb)
    for res in all_res:
        print res[0], len(res)
        if sys.argv[1] == '-r':
            os.system('rm -rf ' + res[0]) 

    if sys.argv[1] == '-s':
        set_tpl_zero(all_res)
        submit_runs(all_res) 

    elif sys.argv[1] == '-c':
        os.chdir(pdir)
        
        set_tpl_zero(all_res)
        collect_runs(all_res)
