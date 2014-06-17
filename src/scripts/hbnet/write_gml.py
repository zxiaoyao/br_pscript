#!/usr/local/bin/python2.7
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

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg


def write_gml():
    '''Write a gml file for the graph g.
    
    '''
    g = readHbNet()
    
    print "graph ["
    
    counter = 1
    for eachNode in g.nodes():
        eachNode.id = counter
        print eachNode.convertToGml(),
        counter += 1
        
    for u,v,edata in g.edges(data=True):
        edata["edata"].source = u.id
        edata["edata"].target = v.id
        print edata["edata"].convertToGml(),
        
#     for u,v,edata in g.edges(data=True):
#         print u.id, v.id, edata["edata"].weight, edata["edata"].width
    
    print "]"
    
def readHbNet(fname=HB_TXT):
    '''Loat the hb network from file "hb.txt".
    
    '''
    hbn = HbResNet()
    hbn.readFromHbTxt(fname)
    
    return hbn.convertGraph(edgeCutoff=0.001, singleEdge=True, undirected=True)

    
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

        # Process arguments
        args = parser.parse_args()

        verbose = args.verbose


        if verbose > 0:
            print("Verbose mode on")

        write_gml()
        
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