#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import sys

from xmlparser import XMLParser
from clarguments import arguments_parse


def custom_package_parse(infile):
    """Parse only the selected packages from a given file"""
    try:
        return [line.rstrip() for line in open(os.path.abspath(infile))]   
    except IOError:
        print "[Error]: Invalid package input file: '{0}' or the file does not exist.".format(os.path.abspath(infile))
        print '[Solution]: Make sure that the input file contains packages seperated by a newline.'
        sys.exit(1)
    
    
def check_file(file):
    """Check for validity of the testcase file."""
    fileExtension = os.path.splitext(file)
    fileAbsolutePath = os.path.abspath(file)    
    if not os.path.isfile(file): 
        sys.exit("[Error]: The file '{0}' is not a valid file or the file does not exist.".format(file))
    if not '.xml' in fileExtension:
        sys.exit("[Error]: Only XML files are supported. The file '{0}' is an invalid testcase file.".format(file))
    print "[Parsing file]:\t'{0}'".format(fileAbsolutePath)


def main():
    """Call the command line and the parser modules."""
    # Print the welcome message
    welcomeMessage = 'Pardus Testing Framework'
    lineSeperate = len(welcomeMessage) * '-'
    print welcomeMessage, '\n', lineSeperate
    # Call the clarguments module
    filename, custompackages, allpackages = arguments_parse()
    # Check whether the file is valid or not
    check_file(filename)
    # Now check the conditions and create the object
    if custompackages is not None:
        customparsefile = XMLParser(os.path.abspath(filename), custom_package_parse(custompackages))
        print "Custom package parsing using file: '{0}'".format(os.path.abspath(custompackages))
        customparsefile.parser_main()
    else:
        parsefile = XMLParser(os.path.abspath(filename), None)
        if allpackages is not None:
            parsefile.output_package_list(os.path.abspath(allpackages))
        parsefile.parser_main()


if __name__ == '__main__':
    main()