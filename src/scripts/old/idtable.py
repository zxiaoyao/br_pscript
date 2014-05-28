#!/usr/bin/python
import sys

wrl = ('norelax', 'relax', 'grom', 'grom2', 'water', 'water2', 'gwater')
rtl = ('quick', 'default', 'ga', 'rq', 'rd')
epl = ('e2', 'e4', 'e6', 'e8', 'e10', 'e12', 'e20', 'e40')
stl = ('d_surf', 'd_self', 'apbs')

eps = ['e2', 'e4', 'e6', 'e8', 'e10', 'e12', 'e20']
rts = ['quick', 'default']
wrs = ['norelax', 'relax']
exs = ['d_surf', 'extra0.5', 'extra0.25', 'extra0.1', 'extra0.05', 'extra0.01', 'extra0.001']


typedic = {'norelax':'nr', 'relax':'re', 'grom':'gr', 'grom2':'g2', 'water':'wa', 'water2':'w2', 'gwater':'gw',
           'quick':'qu', 'default':'de', 'ga':'ga', 'rq':'rq', 'rd': 'rd','iquick':'iq', 'wq':'wq', 'wd':'wd', 'wd0.5':'w5', 's2':'s2', 'q_gold':'qg',
           'e2':'02', 'e4':'04', 'e6':'06', 'e8':'08', 'e10':'10', 'e12':'12', 'e20':'20','e40':'40',
            'd_surf':'su', 'd_self':'se', 'apbs':'ap', 'extra0.5':'x1', 'extra0.25':'x2', 'extra0.1':'x3', 'extra0.05':'x4', 'extra0.01':'x5', 'extra0.001':'x6'}

selist = ('/home/xzhu/BGM/mutant', '/home/xzhu/BGM/mp', '/home/xzhu/BGM/wt')

#pka0 = {'GLU':4.75, 'ASP':4.75, 'LYS':10.5, 'ARG':12.0}
pka0 = {'GLU':4.3, 'ASP':3.9, 'LYS':10.5, 'ARG':12.0}

cav_center = {'GLU':' CD ', 'ASP':' CG ', 'LYS':' NZ ', 'ARG':' NE '}

r_1_3 = {
  'A': 'ALA', 
  'C': 'CYS', 
  'D': 'ASP', 
  'E': 'GLU', 
  'F': 'PHE', 
  'G': 'GLY', 
  'H': 'HIS', 
  'I': 'ILE', 
  'K': 'LYS', 
  'L': 'LEU', 
  'M': 'MET', 
  'N': 'ASN', 
  'P': 'PRO', 
  'Q': 'GLN', 
  'R': 'ARG', 
  'S': 'SER', 
  'T': 'THR', 
  'V': 'VAL', 
  'W': 'TRP', 
  'Y': 'TYR', 
}

r_3_1 = {
  'ALA' : 'A', 
  'CYS' : 'C', 
  'ASP' : 'D', 
  'GLU' : 'E', 
  'PHE' : 'F', 
  'GLY' : 'G', 
  'HIS' : 'H', 
  'ILE' : 'I', 
  'LYS' : 'K', 
  'LEU' : 'L', 
  'MET' : 'M', 
  'ASN' : 'N', 
  'PRO' : 'P', 
  'GLN' : 'Q', 
  'ARG' : 'R', 
  'SER' : 'S', 
  'THR' : 'T', 
  'VAL' : 'V', 
  'TRP' : 'W', 
  'TYR' : 'Y', 
  'NTR' : 'X',  # NTR and CTR and HOH
  'CTR' : 'Z',     
  'HOH' : 'O',
  '_CA' : 'B'
}


def ggid(pdbname, chainid, resid):

    og = {}   # original format to gromacs
    go = {}   # gromacs to original format

    lines = []
    for line in open(pdbname).readlines():
        if line.startswith('ATOM') or line.startswith('HETATM'):
            lines.append(line)

    gid = 1
    old_cid = lines[0][21]
    old_oid = int(lines[0][22:26])
    og = {(old_oid, old_cid) : gid}
    go = {gid : (old_oid, old_cid)}

    for line in lines:
        cid = line[21]
        oid = int(line[22:26])
        if cid == old_cid and oid == old_oid:
            continue
        else:
            gid = gid + 1
            og[(cid, oid)] = gid
            go[gid] = (cid, oid)
            old_cid = cid
            old_oid = oid

    return og[(chainid, resid)]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage:'
        print '   return the gromacs residue id'
        print '   idtable.py cpep.pdb A 7'

    ngid = ggid(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    print ngid
