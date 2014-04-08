#!/usr/bin/python

import sys
import argparse

class Conf(object):
    '''Conformer class.
    '''
    
    def __init__(self, f_line, t_col):
        f_fields = f_line.split()
        self.confid = f_fields[0]
        self.occ    = float(f_fields[t_col])
        self.resid  = self.confid[:3]+self.confid[5:10]
        self.chainid = self.resid[3]
        self.resseq  = int(self.resid[4:])
        self.x2      = 0.0
        self.s_head  = []
        self.cor     = [] 

    def load_s2(self, s_line):
        '''Load the info of the conformer from a line in "step2_out.pdb".
        
        One atom of the conformer is loaded.
        '''
        
        self.s_head.append(s_line[:17])
        self.cor.append(s_line[30:54])


    def write_pdb(self, fp):
        '''Write the conformer to a pdb file.
        
        All the atoms of this conformer need to be written.
        '''
         
        for i in range(len(self.s_head)):
            pdb_line = self.s_head[i] + self.resid[:3] + ' ' + self.chainid + '%4d' % self.resseq + '%28s' % self.cor[i] + '%6.2f' % self.occ + '\n'
            fp.write(pdb_line)


def get_max_conf(all_conf):
    '''Get all the most occupied conforemers for each residue.
    
    Args:
        all_conf: all the conformers.
    
    Returns:
        a list of all the most occupied conformers for each residue.
    '''
    
    all_res = {}
    resid = all_conf[0].resid
    
    # the first element is the occ which is the largest among all the conformers,
    # followed by the conformers in this residue.
    occ = all_conf[0].occ   
    all_res[resid] = [occ]      
 
    # conformers need to be listed in order
    for conf in all_conf:  
        if conf.resid == resid:
            all_res[resid].append(conf)
            if conf.occ > occ:
                occ = conf.occ
                all_res[resid][0] = occ
        else:
            occ = conf.occ
            resid = conf.resid
            all_res[resid] = [occ]
            all_res[resid].append(conf)
            
    res_occ = {}
    for res in all_res.keys():
        for i in range(len(all_res[res])-1):
            if all_res[res][i+1].occ >= all_res[res][0]:
                res_occ[res] = all_res[res][i+1]
                # if the first most occupied conformer found, break
                break  

    # the most occupied conformers of each residue.
    reduced_conf = []
    for conf in all_conf:
        for res in res_occ.keys():
            if conf.confid == res_occ[res].confid:
                reduced_conf.append(conf)
 
    return reduced_conf


def most_occ(tp, f3='fort.38', s2='step2_out.pdb'):
    ''' Get the most occupied conformers from "fort.38" and "step2_out.pdb".
    
    Args:
        tp: the titration point.
        f3: fort.38.
        s2: step2_out.pdb.
    '''
    
    def float_equal(f1, f2, tol=0.00001):
        '''Test if two floating point numbers are equal.
        
        Args:
            f1: first floating point number.
            f2: second floating point number.
            tol: tolerance to test equality.
        '''
        return abs(f1-f2) < tol
    
    
    # load fort.38
    f_lines = open(f3).readlines()
    f_head  = f_lines[0].split()
    for i in range(len(f_head)-1):
        if float_equal(f_line[i+1], tp, tol):
            t_col = i+1                # the titration point column
            break
    del f_lines[0]

    # load all conf in fort.38
    all_conf = []
    for f_line in f_lines:
        all_conf.append(Conf(f_line, t_col))

    # most occupied conformers
    max_conf = get_max_conf(all_conf)

    # update conf from step2_out.pdb
    s_lines = open(s2).readlines()
    for conf in max_conf:
        for s_line in s_lines:
            if s_line[17:20]+s_line[21:26] == conf.resid:
                if s_line[80:82] == 'BK':            # backbone
                    conf.load_s2(s_line)
                elif s_line[26:30] == conf.confid[-4:]:
                    conf.load_s2(s_line)             # it's the sidechain
    
    # output pdb
    outfp = open('mocc_'+tp, 'w')
    for conf in max_conf:
        conf.write_pdb(outfp)
                    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="the titration point", type=float)
    args = parser.parse_args()
    
    most_occ(args.t)
    
    
if __name__ == '__main__':
    main()
