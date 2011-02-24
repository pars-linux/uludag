#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import date

try:
    from lxml import etree
except ImportError:
    print "Error: The 'lxml' library was not found"
    sys.exit("Please install the package 'lxml' to continue")

from pisi.api import list_installed
from pisi.api import list_available

from testcases import testinstall
from testcases import testgui
from testcases import testautomated
from testcases import testshell

from testcases import reportgenerator

from clcolorize import colorize


class XMLParser(object):
    """The main parser class."""
    testreport = list()
    def __init__(self, xmlfile, custompackage, tree=None, rootelement=None):
        self.xmlfile = xmlfile
        try:
            self.tree = etree.parse(self.xmlfile)
        except etree.XMLSyntaxError, detail:
            print colorize('Error: The testcase file cannot be executed ' \
                           'due to an invalid syntax.', 'red')
            print colorize('Detail: {0}', 'bold').format(detail)
            print colorize('Solution: Request the testcase author ' \
                           'for a new file or fix it manually.', 'green')
            sys.exit(1)
        self.rootelement = self.tree.getroot()
        self.custompackage = custompackage
    
    def parser_main(self):
        """The entry point for normal execution."""
        totalTestcases = 0
        # Get the total number of testcases in the file
        for element in self.tree.iter('testcase'):
                totalTestcases += 1               
        counter = 0
        # If the -p option is true, parse only the packages present in that file
        # The ElementTree is modified at this stage, so as to ease the parsing
        if self.custompackage is not None:
            customCounter = 0
            while customCounter < totalTestcases:
                element = self.rootelement[customCounter]
                for custom in element.iter('package'):
                    # if the text is not in the tag, remove the tag
                    if not custom.text in self.custompackage:
                        element.remove(custom)
                customCounter += 1
        # Run each testcase
        while counter < totalTestcases:
            element = self.rootelement[counter]
            # Based on the type of testcase, call the appropriate one
            elementText = element.get('test')
            print "Running test: ", colorize("{0} / {1}", 'bold').format(counter+1,
                                                                    totalTestcases)
            print 'Type of test:  {0}'.format(elementText)
            packageList = []
            for packageTag in element.iter('package'):
                packageList.append(packageTag.text)
            # If no package tag is there, move on to the next testcase
            if not packageList:
                print colorize('Package testing skipped ...', 'red')
                print colorize('-', 'bold')
                self.testreport.append(None)
                counter += 1
                continue
            # One line hack to call the appropriate method
            dict(
                install=self.test_install,
                automated=self.test_automated,
                gui=self.test_gui,
                shell=self.test_shell,
                )[elementText](element, packageList, counter)
            print colorize('Finished', 'green')
            print colorize('-', 'bold')
            counter += 1
        self.generate_report(totalTestcases)
        
    def test_install(self, element, packagelist, counter):
        """Call the module for testcase type INSTALL."""
        self.testreport.append(testinstall.TestInstall(packagelist,
                                                self.installed_packages(),
                                                self.available_packages()))
        self.testreport[counter].test_install_main()
    
    def test_gui(self, element, packagelist, counter):
        """Call the module for testcase type GUI."""
        caseList = self.testcase_tag_parse(element, 'case')
        if not caseList:
            print colorize('No <case> tag found. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        testgui_install = testinstall.TestInstall(packagelist,
                                                  self.installed_packages(),
                                                  self.available_packages())
        testgui_install.test_install_main()
        # Get the list of packages to parse
        packagelist = testgui_install.packagelist
        if testgui_install.failcode == 0:
            print colorize('Unable to install packages. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        self.testreport.append(testgui.TestGUI(element, packagelist))
        self.testreport[counter].report.extend(testgui_install.report)
        # Add the install report to the final report
        self.testreport[counter].test_gui_main()
        
    def test_automated(self, element, packagelist, counter):
        """Call the module for testcase type AUTOMATED."""
        expectedTextList = self.testcase_tag_parse(element, 'expected')
        if not expectedTextList:
            print colorize('No <expected> tag found. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        # Do the same for the <command> tag
        commandTextList = self.testcase_tag_parse(element, 'command')
        if not commandTextList:
            print colorize('No <command> tag found. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        testautomated_install = testinstall.TestInstall(packagelist,
                                                  self.installed_packages(),
                                                  self.available_packages())
        testautomated_install.test_install_main()
        packagelist = testautomated_install.packagelist
        if testautomated_install.failcode == 0:
            print colorize('Unable to install packages. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        self.testreport.append(testautomated.TestAutomated(packagelist, element))
        self.testreport[counter].report.extend(testautomated_install.report)
        self.testreport[counter].test_automated_main()
        
    def test_shell(self, element, packagelist, counter):
        """Call the module for testcase type SHELL."""
        commandList = self.testcase_tag_parse(element, 'command')
        if not commandList:
            print colorize('No <command> tag found. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        testshell_install = testinstall.TestInstall(packagelist,
                                                  self.installed_packages(),
                                                  self.available_packages())
        testshell_install.test_install_main()
        packagelist = testshell_install.packagelist
        if testshell_install.failcode == 0:
            print colorize('Unable to install packages. Skipping test ...', 'red')
            self.testreport.append(None)
            return
        self.testreport.append(testshell.TestShell(element, packagelist))
        self.testreport[counter].report.extend(testshell_install.report)
        self.testreport[counter].test_shell_main()

    def output_package_list(self, outfile):
        """Print the list of packages in the XML file to an output file."""
        packageList = self.print_package_list()
        outputFile = os.path.abspath(outfile)
        if os.path.isfile(outputFile):
            while True:
                choice = raw_input("The file '{0}' exists. Do you wish to " \
                                   "overwrite (y / n)? : ".format(outputFile))
                if choice in ('y', 'Y', 'yes', 'YES'):
                    break
                else:
                    print colorize('Aborting', 'red')
                    sys.exit(1)
        try:
            writeFile = open(outputFile, 'w')
            output = '\n'.join(packageList)
            writeFile.write(output)
            writeFile.close()
        except IOError:
            print colorize('Error: An error occurred while trying to write ' \
                           'the output package file.', 'red')
            print colorize('Solution: Please ensure that the output ' \
                           'file name and path is valid.', 'green')
            sys.exit(1)
        print colorize("The list of packages has been written to: " \
                       "'{0}'", 'green').format(outputFile)
        sys.exit(1)
    
    def testcase_tag_parse(self, element, tag):
        """Parse the element and get the text in tag."""
        # Note that this just uses iter() method to walk through the element,
        # the actual handling is done in the method that called this method
        # Also note that this is valid ony for the testcases and not for any
        # other method or function. This is to simplify the code.
        tagTextList = []
        for tagParse in element.iter(tag):
            tagTextList.append(tagParse.text)
        return tagTextList
    
    def print_package_list(self):
        """Print the list of packages in the XML file."""
        packageList = []
        for element in self.tree.iter('package'):
            packageList.append(element.text)
        return packageList

    def installed_packages(self):
        """Use the Pisi API to fetch the list of installed packages."""
        return list_installed()     # Pisi API
    
    def available_packages(self):
        """Use the Pisi API to fetch the list of available packages."""
        return list_available()     # Pisi API
        
    def generate_report(self, totaltests):
        """Call the report generator module."""
        report = reportgenerator.ReportGenerate(totaltests, self.testreport,
                            self.xmlfile, self.custompackage, self.rootelement)
        report.main()