#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from lxml import etree
    
TESTCASE = {1: 'install', 2: 'gui', 3: 'shell', 4: 'automated'}


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
            options_cases = '1. install\t2. gui\n3. shell\t4. automated\n' \
                                '5. (Exit)\t6. (Save and Exit)'
            choice = self.get_number(options_cases, 6)
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
    
    def gui(self):
        """Input the packages for the testcase gui."""
        print '\nTest type: GUI'
        # get the package
        package_list, total_packages = self.get_packages()
        if total_packages == 0:
            print self.skip_message
            return
        guiPackageElt = etree.SubElement(self.root_element, 'testcase',
                                                             lang='en',
                                                             test='gui')
        counter = 0
        while counter < total_packages:
            packageElt = etree.SubElement(guiPackageElt, 'package')
            packageElt.text = package_list[counter]
            counter += 1
        cases = self.get_number('How many cases do you want?')
        if cases == 0:
            print 'There has to be at least ONE case in a gui testcase.'
            return
        print ''
        case_counter = 0
        case_list = list()
        tag_text = 'Select the tag you want to enter:\n' \
                     '1. <text>\t2. <download>\n3. <link>\t4. (END)'
        # create the elements
        guiCaseElt = etree.SubElement(guiPackageElt, 'case')
        textElt = etree.SubElement(guiCaseElt, 'text')
        downloadElt = etree.SubElement(guiCaseElt, 'download')
        linkElt = etree.SubElement(guiCaseElt, 'link')
        # now go over the cases
        while case_counter < cases:
            print 'Case {0} / {1}'.format(case_counter+1, cases)
            while True:
                tag_choice = self.get_number(tag_text, 4)
                if tag_choice == 1:
                    text = self.get_text('Enter the text:')
                    textElt.text = text
                    continue
                if tag_choice == 2:
                    download = self.get_text('Enter the download link text:')
                    downloadElt.text = download
                    continue
                if tag_choice == 3:
                    link = self.get_text('Enter the link text:')
                    linkElt.text = link
                    continue
                if tag_choice == 4:
                    break
                print ''                
            case_counter += 1

    def automated(self):
        """Input the packages for the testcase automated."""
        print 'Automated got called'
        
    def shell(self):
        """Input the packages for the testcase shell."""
        print 'Shell got called'
        
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
        # print etree.tostring(self.document_tree, pretty_print=True, xml_declaration=True)
            
            
if __name__ == '__main__':
    print 'Pardus Testing Framework - Testcase Writer\n'
    testcase_writer = XMLWriter()
    testcase_writer.main()