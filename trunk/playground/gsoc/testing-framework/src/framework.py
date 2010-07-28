#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from xmlparser import XMLParser

from clarguments import arguments_parse

from clcolorize import colorize


def custom_package_parse(infile):
    """Parse only the selected packages from a given file."""
    try:
        return [line.rstrip() for line in open(os.path.abspath(infile))]   
    except IOError:
        print colorize("Invalid package input file: \'{0}' " \
                       "or the file does not exist.", 'red').format(os.path.abspath(infile))
        print colorize("Make sure that the input file "
                       "contains packages seperated by a newline.", 'green')
        sys.exit(1)
    
    
def check_file(file):
    """Check for validity of the testcase file."""
    fileExtension = os.path.splitext(file)
    fileAbsolutePath = os.path.abspath(file)    
    if not os.path.isfile(file): 
        print colorize("The file '{0}' is not a valid input file " \
                       "or the file does not exist.", 'red').format(file)
        sys.exit(1)
    if not '.xml' in fileExtension:
        print colorize("Only XML files are supported. The file '{0}' " \
                       "is an invalid testcase file.", 'red').format(file)
        sys.exit(1)
    print 'Parsing file:  {0}\n'.format(fileAbsolutePath)


def main():
    """Call the command line and the parser modules."""
    print colorize('Pardus Testing Framework\n', 'bold')
    # Call the clarguments module
    filename, custompackages, allpackages = arguments_parse()
    # Check whether the file is valid or not
    check_file(filename)
    # Now check the conditions and create the object
    if custompackages is not None:
        customparsefile = XMLParser(os.path.abspath(filename),
                                    custom_package_parse(custompackages))
        print "Custom parsing:\t'{0}'\n".format(os.path.abspath(custompackages))
        customparsefile.parser_main()
    else:
        parsefile = XMLParser(os.path.abspath(filename), None)
        if allpackages is not None:
            parsefile.output_package_list(os.path.abspath(allpackages))
        parsefile.parser_main()


if __name__ == '__main__':
    main()