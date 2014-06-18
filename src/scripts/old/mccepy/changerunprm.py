'''
Created on Jun 19, 2013

@author: xzhu
'''
def modifyRunprm(dirPrm, ifile = 'run.prm'):
    '''
    Modify the run.prm file according to dirPrm.

    dirPrm is a {key_string : value_string} dictionary
    "key_string" doesn't include the '()'
    "value_string" has to be a string object
    '''
    ilines = open(ifile, 'r').readlines()

    for il in range(len(ilines)):
        for ky in dirPrm.keys():
            if ilines[il].find('(' + ky + ')') > -1:
                old_value_len = len(ilines[il].split()[0])
                ilines[il] = dirPrm[ky] + ilines[il][old_value_len:]
                break

    open(ifile, 'w').writelines(ilines)

