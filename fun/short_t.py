'''
Created on Feb 18, 2014

@author: xzhu
'''

import os, sys
import glob
def _which(name):
    """Searches for name in exec path and returns full path"""
    
    paths = os.environ["PATH"]
    paths += (os.pathsep + "/opt/local/bin/")
    if os.name == "nt":
        exe = ".exe"
    else:
        exe = ""
    print paths, len(paths)
        
    for path in paths.split(os.pathsep):
        match=glob.glob(os.path.join(path, name+exe))
        if match:
            return match[0]
    raise ValueError("No prog %s in path."%name)

_which("ls")