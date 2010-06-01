#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from optparse import OptionParser

try:
    from lxml import etree
except ImportError:
    sys.exit("""Error importing the 'lxml' library.\nYou need the 'lxml' library package installed to run this software.""")

def check_xml_file(file):
    """Load a XML file and check for validity of the syntax."""
    fileExtension = os.path.splitext(file)
    fileAbsolutePath = os.path.abspath(file)
    
    if not os.path.isfile(file): 
        sys.exit('The file \'{0}\' is not a valid file or the file does not exist.'.format(file))
    if not '.xml' in fileExtension:
        sys.exit('Error: Only XML files are supported.\nThe file \'{0}\' has the extension \'{1}\' and \
is an invalid test case file.'.format(file, fileExtension[1]))
    
    # We have a proper XML file now, let us parse it!
    print '- Pardus GNU/ Linux Testing Framework -'
    print 'Parsing file:\t[{0}]'.format(fileAbsolutePath)

def main():
    """Handle the command line arguments."""
    parser = OptionParser(usage = 'usage: %prog [options] arguments')
    parser.add_option('-f', '--file',
                      dest='filename',
                      metavar='FILE',
                      help='Specifies the testcase XML file for input.')
    (options, args) = parser.parse_args()
    
    if not options.filename:
        parser.print_help()
        sys.exit(1)
    if len(args) != 0:
        parser.error('Invalid number of arguments.')
        sys.exit(1)
        
    check_xml_file(options.filename)
    
if __name__ == '__main__':
    main()