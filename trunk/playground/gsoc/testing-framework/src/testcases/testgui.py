#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

import sys
from clcolorize import colorize


class TestGUI:
    """class for the testcase gui."""
    def __init__(self, element, packagelist, report=None):
        self.element = element
        self.packagelist = packagelist
        self.report = list()
        
    def test_gui_main(self):
        """Execute the gui test case and display the commands."""
        case = self.element.xpath('case')
        totalPackages = len(self.packagelist)
        totalCases = len(case)
        totalCounter = 0
        while totalCounter < totalPackages:
            counter = 0
            while counter < totalCases:
                print colorize('Case {0} of {1}',
                               'bold').format(counter+1, totalCases), 'package: {0}'.format(self.packagelist[totalCounter])
                linkList = []
                for linkTag in case[counter].getiterator('link'):
                    linkList.append(linkTag.text)
                if linkList:
                    print colorize('Open the following link in your browser: ', 'bold')
                    print ''.join(linkList)
                downloadList = []
                for downloadTag in case[counter].getiterator('download'):
                    downloadList.append(downloadTag.text)
                if downloadList:
                    self.download_file(downloadList)
                textList = []
                for element in case[counter].getiterator('text'):
                    textList.append(element.text)
                for number, element in enumerate(textList, 1):
                    print colorize('{0}. ', 'bold').format(number), element
                raw_input('> Press ENTER to continue \n')
                counter += 1
            totalCounter += 1
            print colorize('Enter your observation of the tests:', 'bold')
        observation = raw_input('> ')
        self.report.append(observation)
        
    def download_file(self, file):
        """Download a file using wget."""
        downloadFile = ['wget'] + ['-m'] + ['-nd'] + file
        fileName = os.path.basename(''.join(file))
        startwget = subprocess.call(downloadFile, stderr=open(os.devnull, 'w'))
        if startwget == 0:
            print colorize('{0}', 'bold').format(fileName), " downloaded to: '{0}'".format(os.getcwd())
            self.report.append('{0} downloaded to: {1}'.format(fileName, os.getcwd()))
        else:
            print "The file specified for the download does not exist."