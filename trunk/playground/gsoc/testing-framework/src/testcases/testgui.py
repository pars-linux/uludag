#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

from PyQt4 import QtCore, QtGui

from ui_main import Ui_Dialog

from clcolorize import colorize


class Main(QtGui.QMainWindow):
    def __init__(self, element, package_list, check_code=None, case=None,
                            totalCounter=None, totalpackages=None, totalcases=None,
                            summary=None, report=None):
        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        
        self.check_code = 0
        
        self.element = element
        self.case = self.element.xpath('case')
        self.package_list = package_list
        
        self.totalCounter = 0
        self.totalPackages = len(self.package_list)
        self.caseCounter = 0
        self.totalCases = len(self.case)
        
        self.summary = list()
        self.report = list()
        
        packageList = 'Packages: {0}'.format(', '.join(package_list))
        for lst in (self.summary, self.report):
            lst.append(packageList)
            
        self.update_text()
        self.connect(self.ui.next_button, QtCore.SIGNAL("clicked()"), self.next_case)
        
    def update_text(self):
        self.ui.groupBox.setTitle('Case {0} of {1}'.format(self.caseCounter+1, self.totalCases))
        self.ui.package_label.setText('Package: {0}'.format(self.package_list[self.totalCounter]))
        # get the list of files to be downloaded
        self.ui.text_edit.setText('')
        filesDownloaded = []
        for files in self.case[self.caseCounter].getiterator('download'):
            filesDownloaded.append(files.text)
        if filesDownloaded:
            self.ui.text_edit.append("Using files in '{0}':\n".format(os.getcwd()))
            self.ui.text_edit.append("{0}".format(os.path.basename('\n'.join(filesDownloaded))))
        # get the links
        linkList = []
        for linkTag in self.case[self.caseCounter].getiterator('link'):
            linkList.append(linkTag.text)
        if linkList:
            self.ui.text_edit.append('')
            self.ui.text_edit.append('Open the following link(s) in your browser:')
            self.ui.text_edit.append('{0}'.join(linkList))
        # get the text
        textList = []
        for element in self.case[self.caseCounter].getiterator('text'):
            textList.append(element.text)
        if textList:
            self.ui.text_edit.append('')
            for number, element in enumerate(textList, 1):
                self.ui.text_edit.append('{0}. {1}'.format(number, element))
        self.get_text()
        self.caseCounter += 1
        
    def next_case(self):
        if self.caseCounter < self.totalCases and self.totalCounter < self.totalPackages:
            self.update_text()
            self.ui.text_observation.clear()
        else:
            self.ui.next_button.setEnabled(False)
            self.next_package()
    
    def next_package(self):
        if self.totalCounter < self.totalPackages:
            self.ui.next_button.setEnabled(True)
            self.caseCounter = 0
            self.totalCounter += 1
            self.next_case()
        else:
            self.check_code = 1
            self.ui.package_label.setText('')
            self.ui.text_observation.setPlainText('')
            self.ui.text_edit.setText('End of package testing. Press FINISH to exit.')
            self.ui.groupBox.setTitle('Finished')
            self.ui.text_observation.setEnabled(False)
            self.ui.yes_button.setEnabled(False)
            self.ui.no_button.setEnabled(False)
            self.ui.quit_button.setEnabled(True)
            
    def get_text(self):
        if self.ui.yes_button.isChecked():
            self.report.append('Case {0} of {1}: Success'.format(self.caseCounter+1,
                                                                 self.totalCases))
            self.summary.append('Case {0} of {1}: Success'.format(self.caseCounter+1,
                                                                  self.totalCases))
        if self.ui.unable_button.isChecked():
            failure_message = 'Case {0} of {1}: The user was unable to perform ' \
                              'this test.'.format(self.caseCounter+1, self.totalCases)
            for lst in (self.summary, self.report):
                lst.append(failure_message)
        if self.ui.no_button.isChecked():
            self.report.append('Case {0} of {1}: Failed'.format(self.caseCounter+1,
                                                                self.totalCases))
            self.summary.append('Case {0} of {1}: Failed'.format(self.caseCounter+1,
                                                                 self.totalCases))
            observation = self.ui.text_observation.toPlainText()
            if observation == '':
                self.report.append('\tCase {0}: No observation ' \
                                            'entered.'.format(self.caseCounter+1))
            else:
                self.report.append('\tCase {0} Observation: ' \
                                   '{1}'.format(self.caseCounter+1, observation))


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
        print colorize('Starting the GUI ...', 'yellow')
        # start the graphical user interface now
        app = QtGui.QApplication(sys.argv)
        window = Main(self.element, self.packagelist, self.summary, self.report)
        window.show()
        app.exec_()
        if window.check_code == 1:
            self.summary = window.summary
            self.report = window.report
        else:
            failMessage = 'No information was entered in the GUI test.'
            for lst in (self.summary, self.report):
                lst.append(failMessage)
            
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