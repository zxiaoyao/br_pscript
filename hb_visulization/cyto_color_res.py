'''
Created on Jan 30, 2014

@author: xzhu
'''
import os


def color_res(fName="hb.txt"):
    '''Divide the residues in "hb.txt" into different groups by residue type.
    So that Cytoscape can read it and color the residues accordingly.
    
    e.g.
    HOH        0
    ASP GLU    1
    RSB ARG    2
    '''
    
    COLOR_SCHEME = {"HOH":0, "ASP":1, "GLU":1, "RSB":2, "ARG":2}
    allResidues = []
    for eachLine in open(fName):
        r1 = eachLine.split()[0]
        r2 = eachLine.split()[1]
        if r1 not in allResidues: allResidues.append(r1)
        if r2 not in allResidues: allResidues.append(r2)
        
    ouputFie = "color_res.txt"
    fp = open(ouputFie, 'w')
    for eachRes in allResidues:
        if eachRes[:3] not in COLOR_SCHEME: continue
        fp.write(eachRes + '\t' + str(COLOR_SCHEME[eachRes[:3]]) + '\n')
    fp.close()
 
    
def main():
    
    os.chdir("/Users/xzhu/sibyl/BR2/1C3W/crystal/def/raw_O")
    color_res()


if __name__ == '__main__':
    main()