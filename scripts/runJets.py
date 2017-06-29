#! /usr/bin/env python

import sys
sys.path.insert(0,'.')

import rootpy.ROOT as ROOT
from hgc_tpg.jets.jets import jet_clustering


def main(input_file,parameters):
    jc = jet_clustering(input_file,parameters)
    jc.loop()

    return


if __name__=='__main__':
    import sys
    import optparse
    import importlib
    import re
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--input', dest='input_file', help='Input file',default=None)
    #parser.add_option('--cfg', dest='parameter_file', help='Python file containing definition of parameters',default="hgc_tpg.jets.parameters")
    (opt, args) = parser.parse_args()
    if not opt.input_file:
        parser.print_help()
        print 'Error: Missing input file name'
        sys.exit(1)

    #parameters = importlib.import_module(re.sub('.py$','',opt.parameter_file)).parameters
    from hgc_tpg.jets.parameters import parameters
    par = parameters()

    main(opt.input_file,par)

