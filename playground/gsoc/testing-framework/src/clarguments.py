#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from optparse import OptionParser


def arguments_parse():
    """Handle the command line arguments."""
    parser = OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-f', '--file',
                      dest='filename',
                      metavar='FILE',
                      help='specify the input XML testcase file for testing (REQUIRED)')
    parser.add_option('-p', '--packages',
                      dest='custompackages',
                      metavar='FILE',
                      help='specify the input file for custom package processing')
    parser.add_option('-a', '--all',
                      dest='allpackages',
                      metavar='FILE',
                      help='specify the output file to print the list of packages in the input XML')
    (options, args) = parser.parse_args()
    # If no arguments are passed just print the help message
    if options.filename is None:
        print "The input file (specified by the '-f' option) is mandatory."
        parser.print_help()
        sys.exit(1)
    if len(args) != 0:
        parser.error('Invalid number of arguments.')
        sys.exit(1)
    # Either call -p or -a, but not both
    if options.custompackages and options.allpackages:
        print "[Error]: Specify either the '-p' or the '-a' option, but not both."
        sys.exit(1)
    # Since both cannot be true, check which is and return accordingly
    return options.filename, options.custompackages, options.allpackages