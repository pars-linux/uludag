#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Pardus Package Testing Framework 
# 
# Copyright (C) 2010, Sukhbir Singh and Semen Cirit
# Copyright (C) 2005 - 2009, TUBITAK/ UEKAE
# 
# This program is free software; you can redistribute it and/ or modify it under
# the terms of the GNU General Public License (GNU GPL) as published by the Free
# Software Foundation; either version 2 of the License, or (at your option) any
# later version
# 
# Please read the COPYING file

import os
import sys

from lxml import etree
    

class XMLWriter:
    """Create the ElementTree and write the XML file."""
    skip_message = 'There has to be at least ONE package in a testcase.\n' \
                   'Please try again ...'
    def __init__(self, rootelement=None, documentetree=None):
        self.root_element = etree.Element('document')
        self.document_tree = etree.ElementTree(self.root_element)
 
    def main(self):
        """Entry point for the script."""
        while True:
            print 'Choose the type of testcase (1 - 6): '
            options_cases = '1. install  2. gui  3. shell  4. automated\n' \
                                '5. (Exit)   6. (Save and Exit)'
            choice = self.get_number(options_cases, 6)
            # exit without saving anything
            if choice == 5:
                sys.exit('Quitting.')
            # save and exit 
            if choice == 6:
                self.write_xml()
                continue
            # call the appropriate testcase
            testcase = {1: 'install', 2: 'gui', 3: 'shell', 4: 'automated'}
            test_choice = testcase[choice]
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
        # get the package
        package_list, total_packages = self.get_packages()
        if total_packages == 0:
            print self.skip_message
            return
        # Write the contents to the ElementTree
        testPacakgeElt = etree.SubElement(self.root_element,
                                          'testcase',
                                          lang='en',
                                          test='install'
                                          )
        counter = 0
        while counter < total_packages:
            packageElt = etree.SubElement(testPacakgeElt, 'package')
            packageElt.text = package_list[counter]
            counter += 1
        print 'Finished'
    
    def gui(self):
        """Input the packages for the testcase gui."""
        print '\nTest type: GUI'
        # get the package
        package_list, total_packages = self.get_packages()
        if total_packages == 0:
            print self.skip_message
            return
        # there has to be least one case tag in a GUI test case
        cases = self.get_number('How many cases do you want?')
        if cases == 0:
            print 'There has to be at least ONE case in a gui testcase.'
            return
        print ''
        guiPackageElt = etree.SubElement(self.root_element, 'testcase',
                                                             lang='en',
                                                             test='gui')
        counter = 0
        while counter < total_packages:
            packageElt = etree.SubElement(guiPackageElt, 'package')
            packageElt.text = package_list[counter]
            counter += 1
        case_counter = 0
        case_list = list()
        tag_text = 'Select the tag you want to enter:\n' \
                     '1. <text>   2. <download>   3. <link>\t4. (END)'     
        # now go over the cases
        while case_counter < cases:
            print 'Case {0} / {1}'.format(case_counter+1, cases)
            guiCaseElt = etree.SubElement(guiPackageElt, 'case')
            while True:
                tag_choice = self.get_number(tag_text, 4)
                if tag_choice == 1:
                    text = self.get_text('Enter the text:')
                    textElt = etree.SubElement(guiCaseElt, 'text')
                    textElt.text = text
                    continue
                if tag_choice == 2:
                    download = self.get_text('Enter the download link text:')
                    downloadElt = etree.SubElement(guiCaseElt, 'download')
                    downloadElt.text = download
                    continue
                if tag_choice == 3:
                    link = self.get_text('Enter the link text:')
                    linkElt = etree.SubElement(guiCaseElt, 'link')
                    linkElt.text = link
                    continue
                if tag_choice == 4:
                    if len(guiCaseElt) == 0:
                        print 'No data for <case> tag was entered.'
                        self.root_element.remove(guiPackageElt)
                    break
            case_counter += 1
        print 'Finished'
            
    def shell(self):
        """Input the packages for the testcase shell."""
        print '\nTest type: SHELL'
        package_list, total_packages = self.get_packages()
        if total_packages == 0:
            print self.skip_message
            return
        cases = self.get_number('How many cases do you want?')
        if cases == 0:
            print 'There has to be at least ONE case in a shell testcase.'
            return
        print ''
        shellPackageElt = etree.SubElement(self.root_element, 'testcase',
                                                              lang='en',
                                                              test='shell')
        counter = 0
        while counter < total_packages:
            packageElt = etree.SubElement(shellPackageElt, 'package')
            packageElt.text = package_list[counter]
            counter += 1
        case_counter = 0
        case_list = list()
        tag_text = 'Select the tag you want to enter:\n' \
                     '1. <text>\t2. <command>\t3. (END)'
        while case_counter < cases:
            print 'Case {0} / {1}'.format(case_counter+1, cases)
            shellCaseElt = etree.SubElement(shellPackageElt, 'case')
            while True:
                tag_choice = self.get_number(tag_text, 3)
                if tag_choice == 1:
                    text = self.get_text('Enter the text:')
                    textElt = etree.SubElement(shellCaseElt, 'text')
                    textElt.text = text
                    continue
                if tag_choice == 2:
                    download = self.get_text('Enter the command text:')
                    downloadElt = etree.SubElement(shellCaseElt, 'command')
                    downloadElt.text = download
                    continue
                if tag_choice == 3:
                    if len(shellCaseElt) == 0:
                        print 'No data for <case> tag was entered.'
                        self.root_element.remove(shellPackageElt)
                    break
            case_counter += 1
        print 'Finished'

    def automated(self):
        """Input the packages for the testcase automated."""
        print '\nTest type: AUTOMATED'
        package_list, total_packages = self.get_packages()
        if total_packages == 0:
            print self.skip_message
            return
        cases = self.get_number('How many cases do you want?')
        if cases == 0:
            print 'There has to be at least ONE case in a automated testcase.'
            return
        print ''
        automatedPackageElt = etree.SubElement(self.root_element, 'testcase',
                                                                 lang='en',
                                                                 test='automated')
        counter = 0
        while counter < total_packages:
            packageElt = etree.SubElement(automatedPackageElt, 'package')
            packageElt.text = package_list[counter]
            counter += 1
        case_counter = 0
        case_list = list()
        tag_text = 'Select the tag you want to enter:\n' \
                     '1. <command>  2. <expected>  3. (END)'
        while case_counter < cases:
            print 'Case {0} / {1}'.format(case_counter+1, cases)
            automatedCaseElt = etree.SubElement(automatedPackageElt, 'case')
            while True:
                tag_choice = self.get_number(tag_text, 3)
                if tag_choice == 1:
                    download = self.get_text('Enter the command text:')
                    downloadElt = etree.SubElement(automatedCaseElt, 'command')
                    downloadElt.text = download
                    continue
                if tag_choice == 2:
                    expected = self.get_text('Enter the expected text:')
                    expectedElt = etree.SubElement(automatedCaseElt, 'expected')
                    expectedElt.text = expected
                    continue
                if tag_choice == 3:
                    if len(automatedCaseElt) == 0:
                        print 'No data for <case> tag was entered.'
                        self.root_element.remove(automatedPackageElt)
                    break
            case_counter += 1
        print 'Finished'
        
    def get_packages(self):
        """Input the list of packages."""
        package_list = list()
        print "Enter each package in a new line, use '*' as package name to end: "
        while True:
            package = raw_input('> ')
            if package == '*':      # '*' is the delimiter here
                break
            if package == '':
                continue
            package_list.append(package)
        total_packages = len(package_list)
        return package_list, total_packages
    
    def get_number(self, text, boundary=None):
        """Returns a number after validating it."""
        if boundary is not None:
            input_failure = '\nInvalid choice. Please enter a value between ' \
                                                  '(1 - {0})\n'.format(boundary)
            while True:
                try:
                    number = int(raw_input('{0}\n> '.format(text)))
                except ValueError:
                    print input_failure
                    continue
                if number not in range(1, boundary+1):
                    print input_failure
                    continue
                break
            return number
        while True:
            try:
                    number = int(raw_input('{0} > '.format(text)))
            except ValueError:
                    print 'Please enter a valid number.'
                    continue
            break
        return number
    
    def get_text(self, text):
        """Returns text after validating it."""
        while True:
            text_input = raw_input('{0}\n> '.format(text))
            if text_input == '':
                print 'No text was entered. Please try again.'
                continue
            break
        return text_input
    
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
                answer = raw_input('Do you wish to overwrite? ( y / n ): ')
                if answer in ('y', 'Y', 'yes', 'YES'):
                    break
                else:
                    continue
            break
        try:
            outFile = open(file_path, 'w')
            self.document_tree.write(outFile,
                                     xml_declaration=True,
                                     encoding='utf-8',
                                     pretty_print=True)
            sys.exit("Testcase XML file saved to: '{0}'".format(file_path))
        except IOError:
            sys.exit('An error was encountered while trying to save the file.')

            
if __name__ == '__main__':
    print 'Pardus Testing Framework - Testcase Writer\n'
    test_case_writer = XMLWriter()
    test_case_writer.main()