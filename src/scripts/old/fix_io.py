#!/usr/bin/python

import os, sys
from mcceutility.constants import RESIDUENAME3TO1, POSS_IONI, POSS_CRG, ION_HEAD, SYMBOLTOINT, INTTOSYMBOL
from mcceutility.alterprotonation import freeAllConformers

'''The very first script to perform analysis and submit jobs.
It's not being used any more.
'''

def load_key_res(ifile):
    """ 
    Load residue names from a file, such as "ASPA0085".
    """

    if not os.path.exists(ifile):
        sys.stderr.write("Can't find " + ifile + '  in ' + os.getcwd() + '\n')
        sys.exit()

    key_res = []
    lines = open(ifile).readlines()
    for line in lines:
        if line.strip()[0] != '#':
            key_res.append(line[:-1])

    return key_res

def com_list(lst1, lst2):
    """
    Combine two lists of strings, to get all the combinations of the two lists.
    Example:
          input  : lst1 = ['-', '0'], lst2 = ['0', '+']
          output : all_state = ['-0', '-+', '00', '0+']
    """

    # if one list is empty, return the other one
    if not lst1: return lst2
    if not lst2: return lst1

    all_state = [a+b for a in lst1 for b in lst2]

    return all_state

def set_runs(residues, all_state):
    short_res_name = []
    sub_state = all_state       			# all the possible ionization states of the residues
            
                                                # during the first iteration
    for res in residues:			# res: ASPA0085
        short_name = RESIDUENAME3TO1[res[:3]]             # short_name : D

        short_name += res[3]                    # short_name : DA
        short_name += str(int(res[4:]))         # short_name : DA85
        short_res_name.append(short_name)       # short_res_name : ['DA85']

        #sub_state = com_list(sub_state, POSS_IONI[res[:3]])   # sub_state = ['-', '0']
    
    # all the subruns are in mSub directory.
    sub_run_dir = 'mSub'
    if not os.path.exists(sub_run_dir):
        os.mkdir(sub_run_dir)
    os.chdir(sub_run_dir)
        
    # If there are 6 residues, sub looks like '-00+00' denoting a protonation state of the 6 residues.
    for sub in sub_state:
        # Get the directory name for a sub protonation state, which looks like 'DA850OA402-OA4060RA82+OA403+EA194-'.
        dir_name = ''
        for i in range(len(residues)):
            dir_name += short_res_name[i]
            dir_name += sub[i]

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        os.chdir(dir_name) 

        # The calculation for this sub state is already finished.
        if os.path.exists('pK.out'):
            if os.path.exists('ms_crg'):
                print 'Have "pK.out" and "ms_crg" in ', dir_name
            else:
                print 'Only have "pK.out in ', dir_name
            os.chdir('..')
            continue

	# link files in the parent dirctory.
        os.system('ln -s ../../energies.opp .')
        os.system('ln -s ../../run.prm .')

        if os.path.exists("../../extra.tpl"):
            os.system('ln -s ../../extra.tpl .')
        elif os.path.exists("../../../extra.tpl"):
            os.system('ln -s ../../../extra.tpl .')


        # Modify ms_gold to include only the key residues in it.
        os.system('cp ../../ms_gold .')
        alterMsGold(residues, "ms_gold")

        # alter head3.lst, fixing the protonation states of the key residues, according to the sub protonation state
        os.system('cp ../../head3.lst .')
        freeAllConformers(residues)
        alterHead3(short_res_name, sub)

        os.system('cp /home/xzhu/pfile/submit_ms.sh .')
        os.system('qsub submit_ms.sh')

        os.chdir('..')
     
def alterMsGold(residues, msGoldFile):
    newLines = []
    for eachLine in open(msGoldFile).readlines():
        resName = eachLine[17:20] + eachLine[21:26]
        if resName in residues:
            newLines.append(eachLine)

    open(msGoldFile, 'w').writelines(newLines)

def alterHead3(short_res_name, sub):       
    lines = open('head3.lst').readlines()
    new_line = []
    new_line.append(lines[0])
    lines.pop(0)
    for line in lines:
        if line[6:9] not in POSS_IONI.keys():
            new_line.append(line)
            continue
           
        buff_name = RESIDUENAME3TO1[line[6:9]] + line[11] + str(int(line[12:16]))
        if (buff_name in short_res_name) and (line[9] != ION_HEAD[sub[short_res_name.index(buff_name)]]):
            new_line.append(line[:21] + 't' + line[22:])
        else:
            new_line.append(line)

    open('head3.lst', 'w').writelines(new_line)


def retrieve_runs(residues, all_state):
    short_res_name = []
    sub_state = all_state       # all the possible ionization states of the residues
    f_collt = open('ener.txt', 'w')
    head_str = ''
    for res in residues:
        head_str += ('%-10s' % res)
    head_str += '%-9s%-9s%-9s%-9s' % ('Avg', 'std', 'occ', 'Nms')
    f_collt.write(head_str + '\n')   

    for res in residues:
        short_name = RESIDUENAME3TO1[res[:3]]
        short_name += res[3]
        short_name += str(int(res[4:]))
        short_res_name.append(short_name)

        #sub_state = com_list(sub_state, POSS_IONI[res[:3]])

    if not os.path.exists('mSub'):
        print 'NO directory mSub'
        exit()
    os.chdir('mSub')

    for sub in sub_state:
        dir_name = ''
        for i in range(len(residues)):
            dir_name += short_res_name[i]
            dir_name += sub[i]
        if not os.path.exists(dir_name):
            print "no directory: " + dir_name
            continue
        os.chdir(dir_name)
        
        if not os.path.exists('pK.out'):
            sys.stderr.write('not finished yet ' + dir_name + '\n')
            os.chdir('..')
            #exit()
            continue

        if not os.path.exists('ms_crg'):
            #os.system('/home/xzhu/bin/e_crg/te -f ../../f.txt')
            os.system('mpiexec -n 8 ~/bin/e_crg/te -f ../../f.txt')
        else:
            sys.stdout.write("ms_crg already exists in " + os.getcwd() + '\n')
        
        try:
            print "now in directory: %s" % dir_name
            ms_fields = (open('ms_crg').readlines()[1]).split()
        except IOError:
            print 'no ms_crg ', dir_name
            
        line_to_write = ''
        n_res = len(residues)
        print "n_res = ", n_res
        for i in range(n_res):
            line_to_write += ('%-10s' % INTTOSYMBOL[int(ms_fields[i])])
        line_to_write += ('%-9.3f%-9.3f%-9.3f%-9d' % (float(ms_fields[n_res+3]), float(ms_fields[n_res+4]), \
                       #   float(ms_fields[n_res+5][:-1]) / 100, int(ms_fields[n_res+6])))
                      1, 200000))
        f_collt.write(line_to_write + '\n')
        
        os.chdir('..') 
        
def mfe_fix(residues):
    '''
    use mfe++ to calculate the pairwise interaction between conformer of key residues 
    and the background resdiues, excluding the key residues.
    program to use /home/xzhu/bin/mcce++/lib/mfetest.

    This function doesn't submit the mcce
    '''

    from mdRunPrm import fix_head3

    if os.path.exists('fixMfe'):
        os.system('rm -rf fixMfe')
    os.mkdir('fixMfe')
    os.chdir('fixMfe')

    os.system('cp ../../head3.lst .')
    os.system('ln -s ../../energies.opp .')
    #os.system('ln -s ../energies .')
    os.system('cp ../../extra.tpl .')
    os.system('cp ../../run.prm .')
    os.system('ln -s ../../fort.38 .')
    os.system('cp ../f.txt .')
    os.system("cp ../all_states.txt .")
    os.system("cp ../init.txt .")
    os.system("ln -s ../../energies .")

    #os.system('cp -s ../fullRes.txt .')
    

    os.mkdir('mfeDetails')
    os.system('ln -s ../ms_gold .')

    hlines = open('head3.lst').readlines()
    hlines.pop(0)

    # all the key conformers and their extra energy term 
    key_confs = []
    extras = []

    for line in hlines:
        confID = line[6:20]
        if confID [3:5] == 'DM': continue
        if (confID[:3] + confID[5:10]) in residues:
            key_confs.append(confID)

    for cf in key_confs:
        #print "conf ID ", cf
        os.system('/home/xzhu/bin/mcce++/lib/mfetest ' + cf + ' -s 0.1 -t 5 -f f.txt > mfeDetails/' + cf + '.mfe++')
        os.system('mv res_sum.out mfeDetails/' + cf + '_res_sum.out')

        mlines = open('mfeDetails/' + cf + '.mfe++').readlines()
        extras.append(float(mlines[-1].split()[1]))
        print cf, ' done: ', extras[-1]

    newhlines = []
    for line in open('head3.lst').readlines():
        if line[6:20] in key_confs:
            #newhlines.append(line[:92] + ('%8.3f' % extras.pop(0)) + line[100:])
            # at the beginning, all conformers of free residues should be free to sample
            newhlines.append(line[:21] + 'f' + line[22:92] + ('%8.3f' % extras.pop(0)) + line[100:])
            key_confs.pop(0)
        else:
            confID = line[6:20]
            if (confID[:3] + confID[5:10]) in residues:
                newhlines.append(line)
            else:
                newhlines.append(line[:21] + 't' + line[22:])
             
    open('head3.lst', 'w').writelines(newhlines)


def modify_ms_gold(residues):
    '''
    Modify the "ms_gold" file in current directory.

    Append all the lines in step1_out.pdb that belong to the "residues".
    '''

    if not os.path.exists("ms_gold"):
        print "NO ms_gold file found"
        #exit()

    #lines = open("ms_gold").readlines()
    lines = open("../../step1_out.pdb").readlines()
    new_lines = []

    for line in lines:
        if line[17:20] + line[21:26] in residues:
            new_lines.append(line)

    open("ms_gold", 'w').writelines(new_lines)
    
def load_state(stateFile):
    all_state = []
    for eachLine in open(stateFile).readlines():
        all_state.append(eachLine.split())

    return all_state
    


def main(run_mode, resFile, stateFile):
    all_res = load_key_res(resFile)
    all_state = load_state(stateFile)

    # submit all the sub runs
    if run_mode == '-s':
        set_runs(all_res, all_state)

    # get the "ener.txt" file from all the sub runs
    elif run_mode == '-r':
        retrieve_runs(all_res, all_state) 

    # get the extra term of conformers of residues in "f.txt"
    elif run_mode == '-m':
        mfe_fix(all_res)

    
    # modify the ms_gold file to only include lines of the kye residues
    elif run_mode == '-g':
        modify_ms_gold(all_res)

    elif run_mode == '-c':
       comp_fort(all_res)

    elif run_mode == '-l':
        list_fort(all_res)

    elif run_mode == '-crg':
        list_crg(all_res)

    elif run_mode == '-res_crg':
        res_crg(all_res)


def help():
    ''' message to print when there is no argument  '''
    print 'Run it in the parent directory' 
    print 'To setup all the runs,    		syntax fix_io.py -s pathresidues.txt allstates.txt'
    print 'To retrieve all the runs, 		syntax fix_io.py -r pathresidues.txt allstates.txt'
    print 'To use mfetest to get extra energy,  syntax fix_io.py -m pathresidues.txt allstates.txt'

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == "-h": 
        help()
    else:
        #resFile = 'f.txt'
        #stateFile = "allstates.txt"
        main(sys.argv[1], sys.argv[2], sys.argv[3])
