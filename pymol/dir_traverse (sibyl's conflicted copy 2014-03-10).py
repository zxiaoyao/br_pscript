'''
Created on Feb 5, 2014

@author: xzhu
'''
import os, time

def main():
    for root, dirs, files in os.walk("."):
        for eachFile in files:
            joinedPath = os.path.join(os.path.abspath(root), eachFile)
            st = os.stat(joinedPath)
            fz = int(st.st_size)

            if fz > 1024**3: print"%-9.2fGB" % float(fz)/(1024**3),
            elif fz > 1024**2: print"%-9.2fMB" % float(fz)/(1024**2),
            elif fz > 1024: print "%9.1fKB" % (float(fz)/1024),
            else: print "%10dB" % fz,
            
            print "%15s" % time.ctime(st.st_mtime),
            print joinedPath
            
if __name__ == '__main__':
    main()