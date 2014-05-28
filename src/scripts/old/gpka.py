#!/usr/bin/python
import sys, os, math
import idtable


def pkadiff(e, c):      # diff of calculated (c) and experiment (e) pKa
    if c == 'titration': # titration curve too sharp
        return 0.0
     
    if len(e) > 1:
        er = float(e[1:])
    if len(c) > 1:
        cr = float(c[1:])

    if e.startswith('>'):        # requires no space between sign and value
        if c.startswith('>'):
            return 0.0
        if c.startswith('<'):
            return cr - er
        if float(c) >= er:
            return 0.0
        return float(c) - er

    if e.startswith('<'):
        if c.startswith('<'):
            return 0.0
        if c.startswith('>'):
            return cr - er
        if float(c) <= er:
            return 0.0
        return float(c) - er

    if c.startswith('>'):
        if float(e) >= cr:
            return 0.0
        return cr - float(e)

    if c.startswith('<'):
        if float(e) <= cr:
            return 0.0
        return cr -float(e)

    return float(c) -float(e)      # diff = (calculated pKa) - (experiment pKa)
        
def avg(list):
    sum = 0.0
    for i in range(len(list)):
        sum = sum + float(list[i])

    return sum/len(list)

def rmsd(list):
    """ sum(i2) / n """
    # list is a list of error of calculation

    sum = 0.0
    for i in range(len(list)):
        sum = sum + float(list[i]) * float(list[i])

    return math.sqrt(sum/len(list))

def std(list):
    # list is a list of measurement

    av = avg(list)
    sum = 0.0
    for i in range(len(list)):
        sum = sum + (float(list[i]) - av) * (float(list[i]) - av)

    return math.sqrt(sum/(len(list) - 1))

def distr(list):
    count1 = count2 = count3 = count4 = 0
    for i in range(len(list)):
        ab = math.fabs(list[i])
        if ab <= 1:         # [-1, 1]
            count1 = count1 + 1
        elif ab > 1 and ab <= 2:     # [-2, -1) and (1, 2]
            count2 = count2 + 1
        elif ab > 2:     # [-4, -2) and (2, 4]
            count3 = count3 + 1             # the others
            if ab > 4:
                count4 += 1

    edis = [count1, count2, count3, count4]   # error distribution of list                        
    
    return edis   

if __name__ == '__main__':
    ''' nothing is so special'''

    if len(sys.argv) <2:
        print 'Usage:'
        print '    gpka.py norelax quick e4 d_surf ~/BGM/list/D_list ~/BGM/mutant'
        sys.exit()

    if sys.argv[6].endswith('/'):
        pdir = sys.argv[6][:-1]
    else:
        pdir = sys.argv[6]

    wr = sys.argv[1] # relax or norelax 
    rt = sys.argv[2] # run type: quick default
    ep = sys.argv[3] # epsion: e4 e8
    st = sys.argv[4] # delphi type: d_surf d_self

    pka_err       = []  # pka err, predicted - experimetal
    pka_abs_err   = []  # here, acid append dpka, base append -dpka
    pka_shi       = []  # experimental pKa shift relative to the solution, exp. - sol.
    pka_abs_shi   = []  # "abs" experimental pKa shift relative to the solution
    cal_shi       = []  # predicted pKa shift relative to the solution, pre. -sol.
    cal_abs_shi   = []  # "abs" predicted pKa shift relative to the solution, pre. -sol.

    mfe           = {}
    mfe_keys      = ('vdw0', 'vdw1', 'tors', 'ebkb', 'dsol', 'offset', 'pHpK0', 'EhEm0', '-TS', 'residues', 'vdw', 'ele', 'total', 'abs_ebkb', 'tot_vdw', 'tot_ele')
    for key in mfe_keys:
        mfe[key]  = []
 
    print '                                                             vdw0    vdw1    tors    ebkb    dsol   offset  pHpK0   EhEm0    -TS   residues  vdw      ele     total    diff  shift tot_vdw tot_ele  a_d  a_ebkb'

    os.system('rm -f ~/bin/tqe')
    lines = open(sys.argv[5]).readlines()
    for line in lines:
        fields = line.split()
        pdb = fields[0]

        # find key word to grep the pKa line for that residue in pK.out
        keyn = int(fields[1][:-1])
        epka = fields[2]
        chainid = 'A'

        if sys.argv[1] == 'grom' or sys.argv[1] == 'relax' or rt.startswith('r') or rt.startswith('g'):
            n = idtable.ggid('/home/xzhu/BGM/pdbfiles/' + pdb+'.pdb', chainid, keyn)
        else :
            n = keyn
        if n < 100:
            keyw = '00' + str(n) + '_'
        else:
            keyw = '0' + str(n) + '_'

        ppath = pdir + '/' + pdb + '/' + wr + '/' + rt + '/' + ep + '/' + st + '/' + 'pK.out' 

        if os.path.exists(ppath):
#            try:
#                os.chdir(pdir + '/' + pdb + '/' + wr + '/' + rt + '/' + ep + '/' + st)
#                os.system('ctitr.sh')
#                os.system('occonf.py -c 0.1 | grep -v DM | grep HOH >> /home/xzhu/bin/hoh.t')
#            except:
#                pass
            for pl in open(ppath).readlines():
                if pl.find(keyw) > -1:
#                    os.system('/home/xzhu/bin/mocc.py -p 7')
                    pfields = pl.split()
                    resname = pfields[0]
#                    os.system('grep ' + resname[-6:] + ' head3.lst | wc -l >> /home/xzhu/bin/tqe')
                    # get mfe energy terms
                    mfe['vdw0'].append(float(pl[43:53]))
                    mfe['vdw1'].append(float(pl[53:61]))
                    mfe['tors'].append(float(pl[61:69]))
                    mfe['ebkb'].append(float(pl[69:77]))
                    mfe['dsol'].append(float(pl[77:85]))
                    mfe['offset'].append(float(pl[85:93]))
                    mfe['pHpK0'].append(float(pl[93:101]))
                    mfe['EhEm0'].append(float(pl[101:109]))
                    mfe['-TS'].append(float(pl[109:117]))
                    mfe['residues'].append(float(pl[117:125]))
                    mfe['vdw'].append(float(pl[125:133]))
                    mfe['ele'].append(float(pl[133:141]))
                    mfe['total'].append(float(pl[141:151]))
 
                    # total vdw and ele
                    # tot_vdw = vdw0 + vdw1 + vdw
                    mfe['tot_vdw'].append(float(pl[43:53]) + float(pl[53:61]) + float(pl[125:133]))

                    # tot_ele = ebkb + ele + dsol
                    mfe['tot_ele'].append(float(pl[69:77]) + float(pl[133:141]) + float(pl[77:85]))      # including the desolvation energy

                    # old format of pK.out
                    if pl.find('more') > -1:
                        cpka = '>14.0'
                    elif pl.find('less') > -1: 
                        cpka = '<0.0'
                    else :
                        cpka = pfields[1]
                    
                    # pKa error = calculated - experiment
                    dpka = pkadiff(epka, cpka)
                    pka_err.append(dpka)

                    # for the null model, pka_shi = solution - experiment
                    pka0 = idtable.pka0[pl[:3]]    
                    spka = pkadiff(str(pka0), epka)
                    i_cal_shi = pkadiff(str(pka0), cpka)
                    pka_shi.append(spka)                 
                    cal_shi.append(i_cal_shi)

                    # if base, then reverse the sign
                    if resname.find('+') > -1:
                        pka_abs_err.append(-1 * dpka)
                        pka_abs_shi.append(-1 * spka)
                        cal_abs_shi.append(-1 * i_cal_shi)

                        mfe['abs_ebkb'].append(-1 * float(pl[69:77]))
                    else :
                        pka_abs_err.append(dpka)
                        pka_abs_shi.append(spka)
                        cal_abs_shi.append(i_cal_shi)
                        mfe['abs_ebkb'].append(float(pl[69:77]))

                    # print the whole line in pK.out
                    print "%s/%s/%s/%s" % (idtable.typedic[wr], idtable.typedic[rt], idtable.typedic[ep], idtable.typedic[st]),
                    print pl[:-1],          # '-1' to remove endline sign

                    # append pka error and pka shift to that line
                    print "%6.1f" % dpka,    
                    print "%6.1f" % spka,
                    print "%6.1f" % mfe['tot_vdw'][-1],
                    print "%6.1f" % mfe['tot_ele'][-1],
                    print "%7.1f" % pka_abs_err[-1],
                    print "%6.1f" % mfe['abs_ebkb'][-1]
                    break    # only get pKa from the first chain
        else:
            sys.stderr.write('no' + ppath + '\n')
            

    # pKa statistics
    
    # no such type of run
    if len(pka_err) == 0:
        exit()

    print '  type      #pka  rmsd  avg   [0,1]  (1,2]    >2     >4    s_avg s_rmsd   pka_abs_avg s_abs_avg  s_b_2      s_abs_std  cal_abs_avg  cal_abs_std '

    print "%s/%s/%s/%s" % (idtable.typedic[wr], idtable.typedic[rt], idtable.typedic[ep], idtable.typedic[st]),

    print "%3d%6.1f%6.1f" % (len(pka_err), rmsd(pka_err), avg(pka_err)), 

    print "%6.1f%%%6.1f%%%6.1f%%%6.1f%%" % \
          (float(distr(pka_err)[0])/len(pka_err)*100, float(distr(pka_err)[1])/len(pka_err)*100, float(distr(pka_err)[2])/len(pka_err)*100, float(distr(pka_err)[3])/len(pka_err)*100),

    print "%6.1f%6.1f%11.1f%12.1f%9.1f%%%12.1f%12.1f%12.1f " % (avg(pka_shi), rmsd(pka_shi), avg(pka_abs_err), avg(pka_abs_shi), float(distr(pka_shi)[2])/len(pka_err)*100, std(pka_abs_shi), avg(cal_abs_shi), std(cal_abs_shi) )

    # mfe statistics
    print '  type           vdw0    vdw1      tors    ebkb     dsol     offset   pHpK0    EhEm0     TS   residues     vdw      ele     total  abs_ebkb tot_vdw  tot_ele'
    
    # mfe average
    print "%s/%s/%s/%s" % (idtable.typedic[wr], idtable.typedic[rt], idtable.typedic[ep], idtable.typedic[st]),
    for key in mfe_keys:
        print "%8.1f" % avg(mfe[key]),
    print

    # mfe std
    print "%s/%s/%s/%s" % (idtable.typedic[wr], idtable.typedic[rt], idtable.typedic[ep], idtable.typedic[st]),
    for key in mfe_keys:
        print "%8.1f" % std(mfe[key]),

