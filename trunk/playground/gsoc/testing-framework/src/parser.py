#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import string
import sys
from pisi.api import list_installed
from optparse import OptionParser
try:
    from lxml import etree
except ImportError:
    sys.exit("Error importing the 'lxml' library.\nYou need the 'lxml' library package installed to run this software.")
    

def installed_packages():
    """Use the Pisi API to return the list of installed packages"""
    installedPackageList = list_installed()
    return installedPackageList


def selected_package_parse(file):
    """Parse only the selected packages from a given file"""
    try:
        customPackageList = [line.rstrip() for line in open(os.path.abspath(file))]
        print "[Custom Package Processing], using file '{0}'".format(os.path.abspath(file))
        print 'The following packages will be tested: {0}'.format(customPackageList)
    except IOError:
        print "[Error]: Invalid package input file: '{0}' or the file does not exist.".format(os.path.abspath(file))
        print '[Solution]: Make sure that the input file contains packages seperated by a newline.'
        sys.exit()
    
    
def print_package_list(tree):
    """Print the list of packages in the XML file"""
    packageList = []
    for element in tree.iter('package'):
        packageList.append(element.text)
    return packageList


def output_package_list(file, tree):
    """Print the list of packages in the XML file to an output file"""
    packageList = print_package_list(tree)
    if os.path.isfile(file):
        choice = raw_input("The file '{0}' exists. Do you wish to overwrite (y / n)? : ".format(os.path.abspath(file)))
        validChoices = ['y', 'Y', 'yes', 'YES', 'Yes']
        if choice in validChoices:
            tempFile = open(os.path.abspath(file), 'w')
            output = string.join(packageList, '\n')
            tempFile.write(output)
            tempFile.close()
            print "The list of packages has been written to: '{0}'".format(os.path.abspath(file))
            sys.exit()
        else:
            print '[Aborting]'
    else:
        tempFile = open(os.path.abspath(file), 'w')
        output = string.join(packageList, '\n')
        tempFile.write(output)
        tempFile.close()
        print "The list of packages has been written to: '{0}'".format(os.path.abspath(file))
        sys.exit()


def main():
    """Handle the command line arguments and check for XML file syntax."""
    parser = OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-f', '--file',
                      dest='filename',
                      metavar='FILE',
                      help='specify the input XML testcase file for testing')
    parser.add_option('-p', '--package',
                      dest='package',
                      metavar='FILE',
                      help='specify the input file for custom package processing')
    parser.add_option('-a', '--all',
                      dest='allpackage',
                      metavar='FILE',
                      help='specify the output file to print the list of packages in the input XML')
    (options, args) = parser.parse_args()
    # If no arguments are passed just print the help message
    if options.filename is None:
        parser.print_help()
        sys.exit(1)
    if len(args) != 0:
        parser.error('Invalid number of arguments.')
        sys.exit(1)
    # Print the welcome message
    welcomeMessage = 'Pardus Testing Framework'
    lineSeperate = len(welcomeMessage) * '-'
    print welcomeMessage, '\n', lineSeperate
    # First check whether the file is valid and if yes, then check for the XML extension
    file = options.filename
    fileExtension = os.path.splitext(file)
    fileAbsolutePath = os.path.abspath(file)    
    if not os.path.isfile(file): 
        sys.exit("[Error]: The file '{0}' is not a valid file or the file does not exist.".format(file))
    if not '.xml' in fileExtension:
        sys.exit("[Error]: Only XML files are supported. The file '{0}' is an invalid testcase file.".format(file))
    print "[Parsing file]:\t'{0}'\n".format(fileAbsolutePath)
    # Check the syntax
    try:
        documentTree = etree.parse(fileAbsolutePath)
    except etree.XMLSyntaxError, detail:
        print '[Error]: The testcase file cannot be executed due to an invalid syntax.'
        print '[Detail]:', detail
        print '[Solution]: Request the testcase author for a new file or fix it manually.'
        sys.exit()
    # Check the options here and call the respective functions
    if options.package:
        selected_package_parse(options.package)
    if options.allpackage and options.package is None:
        output_package_list(options.allpackage, documentTree)


if __name__ == '__main__':
    main()