#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from lxml import etree
    
TESTCASE = {1: 'install', 2: 'gui', 3: 'shell', 4: 'automated'}


class XMLWriter:
    """Create the ElementTree and write the XML file."""
    def __init__(self, rootelement=None, documentetree=None):
        self.root_element = etree.Element('document')
        self.document_tree = etree.ElementTree(self.root_element)
 
    def main(self):
        """Entry point for the script."""
        while True:
            print 'Choose the type of testcase (1 - 7): '
            print '1. install\t2. gui\n3. shell\t4. automated\n' \
                                '5. (Exit)\t6. (Save and Exit)'
            input_failure = '\nInvalid choice. Please enter a value between (1 - 7)\n'
            try:
                choice = int(raw_input('> '))
            except ValueError:
                print input_failure
                continue
            if choice not in range(1, 7):
                print input_failure
                continue
            # exit without saving anything
            if choice == 5:
                sys.exit('Quitting.')
            # save and exit 
            if choice == 6:
                self.write_xml()
                continue
            # call the appropriate testcase
            test_choice = TESTCASE[choice]
            dict(
                install=self.install,
                gui=self.gui,
                shell=self.shell,
                automated=self.automated
            )[test_choice]()
            print ''

    def install(self):
        """Input the packages for the testcase install."""
        print '\nTest type: INSTALL'
        print "Enter each package in a new line, use '*' as package name to end: "
        # get the package
        package_list = list()
        while True:
            package = raw_input('> ')
            if package == '*':      # '*' is the delimiter here
                break
            if package == '':
                continue
            package_list.append(package)
        total_packages = len(package_list)
        # Write the contents to the ElementTree
        testInstallElt = etree.SubElement(self.root_element,
                                          'testcase',
                                          lang='en',
                                          test='install'
                                          )
        counter = 0
        while counter < total_packages:
            packageElt = etree.SubElement(testInstallElt, 'package')
            packageElt.text = package_list[counter]
            counter += 1

    def automated(self):
        """Input the packages for the testcase automated."""
        print 'Automated got called'
        
    def shell(self):
        """Input the packages for the testcase shell."""
        print 'Shell got called'
        
    def gui(self):
        """Input the packages for the testcase gui."""
        print 'Gui got called'
    
    def write_xml(self):
        """Write the ElemenTree to the XML file."""
        if len(self.root_element) == 0:
            print '\nNothing to save. Please input some data and try again.\n'
            return
        while True:
            file_name = raw_input('\nEnter name of the output XML file:\n> ')
            # append the extension
            file_name += '.xml'
            file_path = os.path.join(os.getcwd(), file_name)
            if file_name == '':
                print 'Please enter a valid filename.'
                continue
            if os.path.isfile(file_path):
                print "The file '{0}' already exists.".format(file_path)
                answer = raw_input('Do you wish to overwrite? ( y / n): ')
                if answer in ('y', 'Y', 'yes', 'YES'):
                        break
                else:
                    continue
            break
        try:
            outFile = open(file_path, 'w')
            self.document_tree.write(outFile, xml_declaration=True, pretty_print=True)
            sys.exit("Testcase XML file saved to: '{0}'".format(file_path))
        except IOError:
            sys.exit('An error was encountered while trying to save the file.')
            
            
if __name__ == '__main__':
    print 'Pardus Testing Framework - Testcase Writer\n'
    testcase_writer = XMLWriter()
    testcase_writer.main()
