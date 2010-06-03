#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from optparse import OptionParser

try:
    from lxml import etree
except ImportError:
    sys.exit("""Error importing the 'lxml' library.\nYou need the 'lxml' library package installed to run this software.""")
    
    
def parser(xmlfile):
    """Parse the XML file"""
    print 'Parsing file:\t[{0}]'.format(xmlfile)


def check_xml_file(file):
    """Load and check for a XML file."""
    fileExtension = os.path.splitext(file)
    fileAbsolutePath = os.path.abspath(file)
    # First check whether the file is valid and if yes, then check for the XML extension
    if not os.path.isfile(file): 
        sys.exit('The file \'{0}\' is not a valid file or the file does not exist.'.format(file))
    if not '.xml' in fileExtension:
        sys.exit('Error: Only XML files are supported.\nThe file \'{0}\' is an invalid test case file.'.format(file))
    # We have a proper XML file to parse
    print '- Pardus GNU/ Linux Testing Framework -'
    parser(fileAbsolutePath)
    
    
def main():
    """Handle the command line arguments."""
    parser = OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-f', '--file',
                      dest='filename',
                      metavar='FILE',
                      help='specifies the testcase XML file for input.')
    (options, args) = parser.parse_args()
    # If no arguments are passed just print the help message
    if not options.filename:
        parser.print_help()
        sys.exit(1)
    # This should be changed according to the number of options and arguments
    if len(args) != 0:
        parser.error('Invalid number of arguments.')
        sys.exit(1)

    check_xml_file(options.filename)
    
    
if __name__ == '__main__':
    main()