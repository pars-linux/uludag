#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
 
class ReportGenerate:
    """class to generate and manage the outputs generated."""
    def __init__(testinstall=None, testgui=None, testautomated=None, testshell=None):
        self.testinstall = testinstall
        self.testgui = testgui
        self.testautomated = testautomated
        self.testshell = testshell

