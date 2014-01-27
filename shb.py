#!/usr/bin/env python

# To get the sum charge of the residues shown in the hb network


def readHbTxt():
    try:
        lines = open("hb.txt", 'r').readlines()
    except IOError:
        print " Can't open hb.txt"
        exit()

    resInNet = []
    for line in lines:
    	fields = line.split()
	if resInNet.count(fields[0]) == 0:
	    resInNet.append(fields[0])
	if resInNet.count(fields[1]) == 0:
	    resInNet.append(fields[1])

    return resInNet

def writeCrgNet(resNet):
    lines = open("sum_crg.out", 'r').readlines()
    ofp = open("net.crg", 'w')
    for line in lines[1:-4]:
        fields = line.split()
	simpleName = fields[0][:3] + fields[0][4:-1]
	if resNet.count(simpleName) != 0:
	    ofp.write(simpleName + '\t' + fields[1] + '\t' + str(colorV(float(fields[1]))) + '\n')

    return	    

def colorV(crg):
    """ [-1.0, -0.9]    1
        (-0.9, -0.5]    2
        (-0.5, -0.1)    3
        [-0.1,  0.1]    4
        (0.1,   0.5)    5
        [0.5,   0.9)    6
        [0.9,   1.0]    7
    """

    if crg >= -1.0 and crg <= -0.9: return 1
    if crg >  -0.9 and crg <= -0.5: return 2
    if crg >  -0.5 and crg <  -0.1: return 3
    if crg >= -0.1 and crg <=  0.1: return 4
    if crg >   0.1 and crg <   0.5: return 5
    if crg >=  0.5 and crg <   0.9: return 6
    if crg >=  0.9 and crg <=  1.0: return 7


if __name__ == "__main__":
    ress = readHbTxt()
    writeCrgNet(ress)
