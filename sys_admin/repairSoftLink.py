'''
Created on Mar 10, 2014

@author: xzhu
'''

import os, time, sys

def abSoftLink(relativeLink):
    ''' Change the relative soft link to an absolute soft link.
    '''
    
    pointPath = relativeLink
    while os.path.islink(pointPath):
        pointPath = os.readlink(pointPath)
        
    if os.path.isabs(pointPath):
        return pointPath
    else:
        return os.path.abspath(os.path.join(os.path.dirname(relativeLink), pointPath))
    
if __name__ == '__main__':
#     for eachFile in os.listdir("/Users/xzhu/sibyl"):
#         abPath = os.path.join("/Users/xzhu/sibyl", eachFile)
#         print abPath
#         print os.stat(abPath).st_nlink, time.ctime(os.stat(abPath).st_ctime), os.stat(abPath).st_dev
#     for dirName, subDirs, subFiles in os.walk("/Users/xzhu/sibyl/BR2/1C3W/hydro/def"):
#         for eachFile in subFiles:
#             if os.path.islink(os.path.join(dirName, eachFile)):
#                 print os.path.join(dirName, eachFile)
#     print abSoftLink("/Users/xzhu/sibyl/test/sycTest/anotherfile")
    print abSoftLink(sys.argv[1])
    