#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from clcolorize import colorize


class TestGUI:
    """class for the testcase gui."""
    def __init__(self, element, report=None):
        self.element = element
        self.report = list()
        
    def test_gui_main(self):
        """Execute the gui test case and display the commands."""
        case = self.element.xpath('case')
        totalCases = len(case)
        counter = 0
        while counter < totalCases:
            print colorize('- Case {0} of {1} -', 'bold').format(counter+1, totalCases)
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
            print '\nPress ENTER to continue ...'
            raw_input()
            counter += 1
            
    def download_file(self, file):
        """Download a file using wget."""
        downloadFile = ['wget'] + ['-m'] + ['-nd'] + file
        fileName = os.path.basename(''.join(file))
        startwget = subprocess.call(downloadFile, stderr=open(os.devnull, 'w'))
        if startwget == 0:
            print colorize('{0}', 'bold').format(fileName), " downloaded to: '{0}'".format(os.getcwd())
        else:
            print "The file specified for the download doesn't exist."