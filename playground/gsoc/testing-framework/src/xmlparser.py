#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import string

from pisi.api import list_installed
from pisi.api import list_available

from testcases import testinstall

from clcolorize import colorize

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
            print colorize('Error: The testcase file cannot be executed due to an invalid syntax.', 'red')
            print 'Detail: {0}'.format(detail)
            print colorize('Solution: Request the testcase author for a new file or fix it manually.', 'green')
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
                    # if the text is not in the tag, remove the tag
                    if not custom.text in self.custompackage:
                        element.remove(custom)
                customCounter += 1
        # Run each testcase
        while counter < totalTestcases:
            print "[ Running test", colorize("{0} / {1}", 'bold').format(counter+1, totalTestcases), ']' 
            element = self.rootelement[counter]
            elementText = element.get('test')
            # Based on the type of testcase, call the appropriate one
            print "Type of test: '{0}'".format(elementText)
            # If no package tag is there, move on to the next testcase
            packageList = []
            for packageTag in element.getiterator('package'):
                packageList.append(packageTag.text)
            if not packageList:
                print 'No package specified for testing. Skipping test ...\n'
                counter += 1
                continue
            # one line hack to call the appropriate method
            dict(
                install=self.test_install,
                gui=self.test_gui,
                shell=self.test_shell,
                automated=self.test_automated
                )[elementText](element, packageList)   
            counter += 1
    
    def test_install(self, element, packagelist):
        """Call the module for testcase type INSTALL."""
        testcaseinstall = testinstall.TestInstall(packagelist, self.installed_packages(), self.available_packages())
        testcaseinstall.test_install_main()
    
    def test_gui(self, element, packagelist):
        """Call the module for testcase type GUI."""
        installedPackages = self.installed_packages()
        print packagelist
        
    def test_shell(self, element, packagelist):
        """Call the module for testcase type SHELL."""
        print 'SHELL'
        
    def test_automated(self, element, packagelist):
        """Call the module for testcase type AUTOMATED."""
        print 'AUTOMATED'
  

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
                    print colorize('Aborting', 'red')
                    sys.exit(1)
        try:
            writeFile = open(outputFile, 'w')
            output = string.join(packageList, '\n')
            writeFile.write(output)
            writeFile.close()
        except IOError:
            print colorize('Error: An error occurred while trying to write the output package file.', 'red')
            print colorize('Solution: Please ensure that the output file name and path is valid.', 'green')
            sys.exit(1)
        print colorize("The list of packages has been written to: '{0}'", 'green').format(outputFile)
        sys.exit()
    
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