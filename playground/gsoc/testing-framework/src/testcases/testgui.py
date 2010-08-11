#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from PyQt4 import QtCore, QtGui

from interface import Main


class TestGUI:
    """class for the testcase gui."""
    def __init__(self, element, packagelist, summary=None, report=None):
        self.element = element
        self.packagelist = packagelist
        self.summary = list()
        self.report = list()
        
    def test_gui_main(self):
        """Execute the gui test case and display the commands."""
        # download the required files
        downloadList = []
        for downloadTag in self.element.getiterator('download'):
            downloadList.append(downloadTag.text)
        if downloadList:
            self.download_file(downloadList)
        # start the graphical user interface now
        totalPackages = len(self.packagelist)
        counter = 0
        while counter < totalPackages:
            app = QtGui.QApplication(sys.argv)
            window = Main(self.element, self.packagelist, self.summary, self.report)
            window.show()
            app.exec_()
            if window.checkcode == 1:
                self.summary.extend(window.summary)
                self.report.extend(window.report)
            else:
                failMessage = 'No information was entered in the GUI test.'
                for lst in (self.summary, self.report):
                    lst.extend(failMessage)
            counter += 1
            
    def download_file(self, file):
        """Download a file using wget."""
        totalDownloads = len(file)
        counter = 0
        print 'Downloading files, please wait ...'
        while counter < totalDownloads:
            downloadFile = ['wget'] + ['-N'] + file[counter].split()
            fileName = os.path.basename(''.join(file[counter]))
            startwget = subprocess.call(downloadFile, stderr=open(os.devnull, 'w'))
            if startwget == 0:
                print colorize('{0}', 'bold').format(fileName)
                self.report.append('{0} downloaded to: {1}'.format(fileName,
                                                                   os.getcwd()))
            else:
                print "The file {0} does not exist.".format(''.join(file[counter]))
            counter += 1