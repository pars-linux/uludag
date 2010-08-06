#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from clcolorize import colorize


class TestGUI:
    """class for the testcase gui."""
    def __init__(self, element, packagelist, summary=None, report=None):
        self.element = element
        self.packagelist = packagelist
        self.summary = list()
        self.report = list()
        
    def test_gui_main(self):
        """Execute the gui test case and display the commands."""
        case = self.element.xpath('case')
        totalPackages = len(self.packagelist)
        print ''
        totalCases = len(case)
        totalCounter = 0
        while totalCounter < totalPackages:
            counter = 0
            self.report.append('Package: {0}'.format(self.packagelist[totalCounter]))
            self.summary.append('Package: {0}'.format(self.packagelist[totalCounter]))
            while counter < totalCases:
                print 'Case {0} of {1}:'.format(counter+1, totalCases)
                print 'Package -',
                print colorize('{0}', 'bold').format(self.packagelist[totalCounter])
                downloadList = []
                for downloadTag in case[counter].getiterator('download'):
                    downloadList.append(downloadTag.text)
                if downloadList:
                    self.download_file(downloadList)    
                linkList = []
                for linkTag in case[counter].getiterator('link'):
                    linkList.append(linkTag.text)
                if linkList:
                    print 'Open the following link in your browser: '
                    print '{0}'.join(linkList)
                textList = []
                for element in case[counter].getiterator('text'):
                    textList.append(element.text)
                for number, element in enumerate(textList, 1):
                    print colorize('{0}. ', 'bold').format(number), element
                # Get the observations
                answer = raw_input('Did the above test run as expected? (y / n): ')
                if answer in ('y', 'Y', 'yes', 'YES', ''):
                    self.report.append('Case {0} of {1}: Success'.format(counter+1,
                                                                         totalCases))
                    self.summary.append('Case {0} of {1}: Success'.format(counter+1,
                                                                         totalCases))
                else:
                    self.report.append('Case {0} of {1}: Failed'.format(counter+1,
                                                                        totalCases))
                    self.summary.append('Case {0} of {1}: '.format(counter+1,
                                                                         totalCases))
                    observation = raw_input('Enter your observations: \n> ')
                    if not observation == '':
                        self.report.append('\tCase {0} Observation: {1}'.format(counter+1,
                                                                        observation))
                    else:
                        self.report.append('\tCase {0}: No observation entered.'.format(counter+1))
                counter += 1
                print ''
            totalCounter += 1
        
    def download_file(self, file):
        """Download a file using wget."""
        totalDownloads = len(file)
        counter = 0
        print 'Downloading files, please wait ...'
        while counter < totalDownloads:
            downloadFile = ['wget'] + ['-m'] + ['-nd'] + file[counter].split()
            fileName = os.path.basename(''.join(file[counter]))
            startwget = subprocess.call(downloadFile, stderr=open(os.devnull, 'w'))
            if startwget == 0:
                print colorize('{0}', 'bold').format(fileName)
                self.report.append('{0} downloaded to: {1}'.format(fileName,
                                                                   os.getcwd()))
            else:
                print "The file {0} does not exist.".format(''.join(file[counter]))
            counter += 1
        print ''
        print 'File(s) downloaded to: ', colorize('{0}', 'bold').format(os.getcwd())