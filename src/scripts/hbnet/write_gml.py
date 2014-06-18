#!/usr/bin/env python
# encoding: utf-8
'''
write_gml -- write a graph in a gml file

write_gml is a description

It defines classes_and_methods

@author:     xzhu

@copyright:  2014. All rights reserved.

@license:    license

@contact:    zhuxuyu@gmail.com
@deffield    updated: Updated
'''

import sys
import os

import networkx as nx

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from xhbpathpy.hbResNet import HbResNet

__all__ = []
__version__ = 0.1
__date__ = '2014-06-16'
__updated__ = '2014-06-16'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

HB_TXT = "hb.txt"
PDB_COOR = "step1_out.pdb"

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def write_gml(fname=HB_TXT, pdbCoor=PDB_COOR, edgeCutoff=0.01, singleEdge=True, undirected=True):
    '''Write a gml file for the graph g.
    
    '''
    g = readHbNet(fname, edgeCutoff, singleEdge, undirected)
    
    print "graph ["
    
    counter = 1
    for eachNode in g.nodes():
        eachNode.id = counter
        
        eachNode.retrieveCorr(pdbCoor)
        eachNode.getResColor()
          
        print eachNode.convertToGml(),
        counter += 1    
        
    for u,v,edata in g.edges(data=True):
#         print edata["edata"].sNode.id, edata["edata"].tNode.id
        if (g.degree(u) == 1 and g.degree(v) != 1) or (g.degree(u) != 1 and g.degree(v) == 1): edata["edata"].dashed = 1
        print edata["edata"].convertToGml(),
        
    
    print "]"
    
    

def readHbNet(fname=HB_TXT, edgeCutoff=0.01, singleEdge=True, undirected=True):
    '''Loat the hb network from file "hb.txt".
    
    '''
    hbn = HbResNet()
    hbn.readFromHbTxt(fname)
    
    return hbn.convertGraph(edgeCutoff, singleEdge, undirected)

    
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by xzhu on %s.
  Copyright 2014 . All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        parser.add_argument("-f", help="text file to load the hb net", default=HB_TXT, nargs='?')
        parser.add_argument("-c", help="load edges with prob no less than this number", default=0.01, type=float, nargs='?')
        
        parser.add_argument("--singleedge", action="store_true", default=True, help="load at most one edge between two residues")
        parser.add_argument("--undirected", action="store_true", default=True, help="load the network as an undirected network")
        
        parser.add_argument("-p", help="the pdb file to load the coordinates", default=PDB_COOR, nargs='?')

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose
        if verbose > 0:
            print("Verbose mode on")

#         print args.f, args.c, args.singleedge, args.undirected, args.p
#         write_gml()
        write_gml(args.f, args.p, args.c, args.singleedge, args.undirected)
        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    sys.exit(main())