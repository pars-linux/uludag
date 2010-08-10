#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

from ui_main import Ui_Dialog

from clcolorize import colorize


class Main(QtGui.QMainWindow):
    test_type = 'Shell Test'
    def __init__(self, element, package_list, check_code=None, case=None,
                                            totalCounter=None, totalcases=None,
                                            summary=None, report=None):
        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        
        self.check_code = 0
    
        self.element = element
        self.case = self.element.xpath('case')
        self.package_list = package_list
                
        self.caseCounter = 0
        self.totalCases = len(self.case)
        
        self.summary = list()
        self.report = list()
        
        packageList = 'Packages: {0}'.format(', '.join(package_list))
        for lst in (self.summary, self.report):
            lst.append(packageList)
        
        self.ui.type_label.setText(self.test_type)
    
        self.connect(self.ui.next_button, QtCore.SIGNAL("clicked()"), self.next_case)
        self.connect(self.ui.save_button, QtCore.SIGNAL("clicked()"), self.get_text)
        
    def update_text(self):
        self.ui.text_observation.clear()
        self.ui.groupBox.setTitle('Case {0} of {1}'.format(self.caseCounter+1, self.totalCases))
        self.ui.package_label.setText('Packages: {0}'.format(', '.join(self.package_list)))
        # get the text
        textList = []
        for element in self.case[self.caseCounter].getiterator('text'):
            textList.append(element.text)
        if textList:
            for number, element in enumerate(textList, 1):
                self.ui.text_edit.setText('{0}. {1}'.format(number, element))
        # get the commands
        commandList = []
        for element in self.case[self.caseCounter].getiterator('command'):
            commandList.append(element.text)
        if commandList:
            self.ui.text_edit.append('')
            self.ui.text_edit.append('{0}'.format('\n'.join(commandList)))
            
    def next_case(self):
        if self.caseCounter < self.totalCases:
            self.ui.next_button.setEnabled(True)
            self.ui.yes_button.setEnabled(True)
            self.ui.no_button.setEnabled(True)
            self.ui.unable_button.setEnabled(True)
            self.ui.save_button.setEnabled(True)
            self.ui.next_button.setText('N&ext')
            self.update_text()
            self.ui.next_button.setEnabled(False)
        else:
            self.ui.quit_button.setEnabled(True)
            self.ui.next_button.setEnabled(False)
            self.ui.next_button.setEnabled(False)
            self.check_code = 1
            self.ui.package_label.setText('')
            self.ui.text_observation.setPlainText('')
            self.ui.text_edit.setText('End of package testing. Press FINISH to exit.')
            self.ui.groupBox.setTitle('Finished')
            self.ui.text_observation.setEnabled(False)
            self.ui.yes_button.setEnabled(False)
            self.ui.no_button.setEnabled(False)
            self.ui.unable_button.setEnabled(False)

    def get_text(self):
        if self.ui.yes_button.isChecked():
            self.report.append('Case {0} of {1}: Success'.format(self.caseCounter+1,
                                                                 self.totalCases))
            self.summary.append('Case {0} of {1}: Success'.format(self.caseCounter+1,
                                                                  self.totalCases))
        elif self.ui.unable_button.isChecked():
            failure_message = 'Case {0} of {1}: The user was unable to perform ' \
                              'this test.'.format(self.caseCounter+1, self.totalCases)
            for lst in (self.summary, self.report):
                lst.append(failure_message)
            observation = self.ui.text_observation.toPlainText()
            if observation == '':
                self.report.append('\tCase {0}: No observation ' \
                                            'entered.'.format(self.caseCounter+1))
            else:
                self.report.append('\tCase {0} Observation: ' \
                                   '{1}'.format(self.caseCounter+1, observation))
        elif self.ui.no_button.isChecked():
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
        else:
            self.report.append('Case {0} of {1}: No information entered'.format(self.caseCounter+1,
                                                                self.totalCases))
            self.summary.append('Case {0} of {1}: Failed'.format(self.caseCounter+1,
                                                                 self.totalCases))
        self.ui.save_button.setEnabled(False)
        self.ui.next_button.setEnabled(True)
        self.caseCounter += 1
                
class TestShell:
    """This class is used to handle the testcase of shell, in which the user is
    told to run a certain command on and note down the output."""
    def __init__(self, element, summmary=None, report=None):
        self.element = element
        self.summary = list()
        self.report = list()
        
    def test_shell_main(self):
        """Print the text and ask the user to run the commands."""
        packageList = []
        for package in self.element.getiterator('package'):
            packageList.append(package.text)
        app = QtGui.QApplication(sys.argv)
        window = Main(self.element, packageList, self.summary, self.report)
        window.show()
        app.exec_()
        if window.check_code == 1:
            self.summary = window.summary
            self.report = window.report
        else:
            failMessage = 'No information was entered in the SHELL test.'
            for lst in (self.summary, self.report):
                lst.append(failMessage)