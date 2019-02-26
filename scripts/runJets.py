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
    parser.add_option('--output', dest='output_file', help='Output file. Override parameters specifications.',default=None)
    parser.add_option('--params','-p', dest='params', action='append', help='Override something in the parameters. Can be used multiplet times. Example calibration:do:True',default=[])
    #parser.add_option('--cfg', dest='parameter_file', help='Python file containing definition of parameters',default="hgc_tpg.jets.parameters")
    (opt, args) = parser.parse_args()
    if not opt.input_file:
        parser.print_help()
        print 'Error: Missing input file name'
        sys.exit(1)

    #parameters = importlib.import_module(re.sub('.py$','',opt.parameter_file)).parameters
    from hgc_tpg.jets.parameters import parameters
    par = parameters()
    for pstr in opt.params:
        sec = pstr.split(':')[0]
        sub = pstr.split(':')[1]
        if len(pstr.split(':')) >=3 :
            val = pstr.split(':')[2]
            print "* overriding setting:",sec + '["'+ sub+'"] = ' +val
            exec('par.'+sec + '["'+ sub+'"] = ' +val )
        else:
            print "* overriding setting:",sec + '=' + sub
            exec('par.'+sec + '=' + sub )

    if opt.output_file:
        par.output["file"]=opt.output_file

    main(opt.input_file,par)

