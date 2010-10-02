#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui

from interface import Main


class TestShell(object):
    """This class is used to handle the testcase of shell, in which the user is
    told to run a certain command on and note down the output."""
    def __init__(self, element, packagelist, summmary=None, report=None):
        self.element = element
        self.packagelist = packagelist
        self.summary = list()
        self.report = list()
        
    def test_shell_main(self):
        """Print the text and ask the user to run the commands."""
        # start the gui
        app = QtGui.QApplication(sys.argv)
        window = Main(self.element, self.packagelist, self.summary, self.report)
        window.show()
        app.exec_()
        
        if window.checkcode:
            self.summary = window.summary
            self.report = window.report
        else:
            failMessage = 'No information was entered in the SHELL test.'
            for lst in (self.summary, self.report):
                lst.append(failMessage)