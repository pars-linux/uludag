#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import string

from pisi.api import list_installed
from pisi.api import list_available
from testcases import testinstall

try:
    from lxml import etree
except ImportError:
    sys.exit("Error importing the 'lxml' library.\nYou need the 'lxml' library package installed to run this software.")


class XMLParser:
    """The main parser class."""
    def __init__(self, xmlfile, custompackage, tree=None, rootelement=None):
        self.xmlfile = xmlfile
        try:
            self.tree = etree.parse(self.xmlfile)
        except etree.XMLSyntaxError, detail:
            print '\n[Error]: The testcase file cannot be executed due to an invalid syntax.'
            print '[Detail]:', detail
            print '[Solution]: Request the testcase author for a new file or fix it manually.'
            sys.exit(1)
        self.rootelement = self.tree.getroot()
        self.custompackage = custompackage
    
    def parser_main(self):
        """The entry point for normal execution."""
        totalTestcases = 0
        # Get the total number of testcases in the file
        for element in self.tree.getiterator('testcase'):
                totalTestcases += 1               
        counter = 0
        # If the -p option is true, parse only the packages present in that file
        # The ElementTree is modified at this stage, so as to ease the parsing
        if self.custompackage is not None:
            customCounter = 0
            while customCounter < totalTestcases:
                element = self.rootelement[customCounter]
                for custom in element.getiterator('package'):
                    if custom.text in self.custompackage:
                        pass
                    else:
                        element.remove(custom)
                customCounter += 1
        # Run each testcase
        while counter < totalTestcases:
            print '\n-- Running test [ {0} of {1} ] --'.format(counter+1, totalTestcases)
            element = self.rootelement[counter]
            elementtext = element.get('test')
            # Based on the type of testcase, call the appropriate one
            print "\t'{0}'\n".format(elementtext)
            dict(install=self.test_install, gui=self.test_gui)[elementtext](element)        # one line hack to call the appropriate method!
            counter += 1
    
    def test_install(self, element):
        """Call the module for testcase type INSTALL."""
        listInstall = []
        for text in element.getiterator('package'):
            listInstall.append(text.text)
        testinstall.test_install(listInstall, self.installed_packages(), self.available_packages())
    
    def test_gui(self, element):
        """Call the module for testcase type GUI."""
        print 'Yeah gui! You are next :)'

    def output_package_list(self, outfile):
        """Print the list of packages in the XML file to an output file."""
        packageList = self.print_package_list()
        outputFile = os.path.abspath(outfile)
        if os.path.isfile(outputFile):
            while True:
                choice = raw_input("The file '{0}' exists. Do you wish to overwrite (y / n)? : ".format(outputFile))
                if choice in ('y', 'Y', 'yes', 'YES'):
                    break
                else:
                    sys.exit('[Aborting]')
        try:
            writeFile = open(outputFile, 'w')
            output = string.join(packageList, '\n')
            writeFile.write(output)
            writeFile.close()
        except IOError:
            print '[Error]: An error occurred while trying to write the output package file.'
            print '[Solution]: Please ensure that the output file name and path is valid.'
            sys.exit(1)
        sys.exit("The list of packages has been written to: '{0}'".format(outputFile))
    
    def print_package_list(self):
        """Print the list of packages in the XML file."""
        packageList = []
        for element in self.tree.getiterator('package'):
            packageList.append(element.text)
        return packageList

    def installed_packages(self):
        """Use the Pisi API to fetch the list of installed packages."""
        return list_installed()     # Pisi API
    
    def available_packages(self):
        """Use the Pisi API to fetch the list of available packages."""
        return list_available()     # Pisi API