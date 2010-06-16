#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import string
from pisi.api import list_installed
try:
    from lxml import etree
except ImportError:
    sys.exit("Error importing the 'lxml' library.\nYou need the 'lxml' library package installed to run this software.")


class XMLParser:
    """The main parser class."""
    def __init__(self, xmlfile, tree=None):
        self.xmlfile = xmlfile
        try:
            self.tree = etree.parse(self.xmlfile)
        except etree.XMLSyntaxError, detail:
            print '[Error]: The testcase file cannot be executed due to an invalid syntax.'
            print '[Detail]:', detail
            print '[Solution]: Request the testcase author for a new file or fix it manually.'
            sys.exit(1)

    def installed_packages(self):
        """Use the Pisi API to fetch the list of installed packages."""
        installedPackageList = list_installed()
        return installedPackageList
        
    def output_package_list(self, outFile):
        """Print the list of packages in the XML file to an output file"""
        packageList = self.print_package_list()
        if os.path.isfile(outFile):
            while True:
                choice = raw_input("The file '{0}' exists. Do you wish to overwrite (y / n)? : ".format(os.path.abspath(outFile)))
                if choice in ('y', 'Y', 'yes', 'YES'):
                    break
                else:
                    sys.exit('[Aborting]')
        tempFile = open(os.path.abspath(outFile), 'w')
        output = string.join(packageList, '\n')
        tempFile.write(output)
        tempFile.close()
        sys.exit("The list of packages has been written to: '{0}'".format(os.path.abspath(outFile)))
    
    def selected_package_parse(self, inFile):
        """Parse only the selected packages from a given file"""
        try:
            customPackageList = [line.rstrip() for line in open(os.path.abspath(inFile))]
            print "[Custom Package Processing], using file '{0}'".format(os.path.abspath(inFile))
            print 'The following packages will be tested: {0}'.format(customPackageList)
        except IOError:
            print "[Error]: Invalid package input file: '{0}' or the file does not exist.".format(os.path.abspath(inFile))
            print '[Solution]: Make sure that the input file contains packages seperated by a newline.'
            sys.exit(1)
        
    def print_package_list(self):
        """Print the list of packages in the XML file"""
        packageList = []
        for element in self.tree.iter('package'):
            packageList.append(element.text)
        return packageList