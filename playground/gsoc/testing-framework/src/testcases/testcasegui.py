#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys

from PyQt4 import QtCore, QtGui

from ui_main import Ui_Dialog


class Main(QtGui.QMainWindow):
    test_type = 'Shell Test'
    def __init__(self, element, package_list, checkCode=None, case=None,
                                              totalCounter=None, totalcases=None,
                                              summary=None, report=None):
        QtGui.QMainWindow.__init__(self)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        
        self.checkCode = 0
    
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
        
        self.ui.text_edit.setText("Press 'Start' to begin testing ...")
        self.connect(self.ui.next_button, QtCore.SIGNAL("clicked()"), self.next_case)
        self.connect(self.ui.save_button, QtCore.SIGNAL("clicked()"), self.get_text)
        
    def update_text(self):
        self.ui.text_observation.clear()
        self.ui.group_box.setTitle('Case {0} of {1}'.format(self.caseCounter+1, self.totalCases))
        self.ui.package_label.setText('Package(s): {0}'.format(', '.join(self.package_list)))
        self.ui.text_edit.setText('')
        # get the text
        textList = []
        for element in self.case[self.caseCounter].getiterator('text'):
            textList.append(element.text)
        if textList:
            for number, element in enumerate(textList, 1):
                self.ui.text_edit.append('{0}. {1}'.format(number, element))
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
            self.ui.text_edit.setEnabled(True)
            self.ui.label.setEnabled(True)
            self.ui.yes_button.setEnabled(True)
            self.ui.no_button.setEnabled(True)
            self.ui.unable_button.setEnabled(True)
            self.ui.save_button.setEnabled(True)
            self.ui.next_button.setText('N&ext')
            self.update_text()
            self.ui.next_button.setEnabled(False)
        else:
            self.ui.quit_button.setEnabled(True)
            
            self.ui.text_observation.setEnabled(False)
            self.ui.label.setEnabled(False)
            self.ui.yes_button.setEnabled(False)
            self.ui.clear_button.setEnabled(False)
            self.ui.no_button.setEnabled(False)
            self.ui.label_observation.setEnabled(False)
            self.ui.unable_button.setEnabled(False)
            self.ui.next_button.setEnabled(False)
            self.ui.next_button.setEnabled(False)
            
            self.checkCode = 1
            
            self.ui.package_label.setText('')
            self.ui.text_observation.setPlainText('')
            self.ui.text_edit.setText("End of package testing. Press 'Finish' to exit.")
            self.ui.group_box.setTitle('Finished')

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
            self.report.append('Case {0} of {1}: ' \
                               'No information entered'.format(self.caseCounter+1,
                                                                self.totalCases))
            self.summary.append('Case {0} of {1}: Failed'.format(self.caseCounter+1,
                                                                 self.totalCases))
        self.ui.save_button.setEnabled(False)
        self.ui.next_button.setEnabled(True)
        self.caseCounter += 1