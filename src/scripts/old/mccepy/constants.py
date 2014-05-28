'''
Created on Jun 19, 2013

@author: xzhu
'''

# Convert 1 letter code of a residue to the 3-letter code.
RESIDUENAME3TO1 = {
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
  '_CA' : 'B',
  'RSB' : 'U'
}


# RESIDUENAME3TO1 is just the reverse of RESIDUENAME1TO3.
RESIDUENAME1TO3 = {}
for k,v in RESIDUENAME3TO1.iteritems():
    RESIDUENAME1TO3[v] = k
    


# '-':-1, '0':0, '+':+1, 'm':Dummy

# POSS_IONI stores the various ionization states of residues.
# The symbols in the bracket are used to denote the sub protonation state.
POSS_IONI = {'ASP':['-', '0'], 'RSB':['+', '0'], 'ARG':['+', '0'], 'GLU':['-', '0'], 'HOH':['0', '-', '+'], 'HIS':['+', '0'], 'LYS':['+', '0'], 'TYR':['-', '0']}

# POSS_CRG stores the various charges that a residues could carry.
POSS_CRG = {'ASP':[-1, 0], 'RSB':[1, 0], 'ARG':[1, 0], 'GLU':[-1, 0], 'HOH':[0, -1, 1], 'HYD':[0, 1], 'HIS':[0, 1], 'LYS':[0, 1], 'TYR':[0, -1]}

# ION_HEAD controls how the symbol indicating the type of conformer in head3.lst converts to the symbol used in the sub protonation state.
ION_HEAD  = {'-':'-', '0':'0', '+':'+', 'm':'D'}

# SYMBOLTOINT converts the symbol of protonation state to the charge
SYMBOLTOINT = {'-':-1, '+':1, '0':0}

# INTTOSYMBOL is the reverse of SYMBOLTOINT
INTTOSYMBOL = {-1:'-', 1:'+', 0:'0'}
