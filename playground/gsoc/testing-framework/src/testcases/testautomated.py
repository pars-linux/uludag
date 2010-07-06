#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from clcolorize import colorize

from processmanager import CallProcess


class TestAutomated:
    """This class will perform an automated test, the purpose of which is to run
    a command, get its output and compare it with the expected output, which is
    already encoded in the testcase file."""
    def __init__(self, package, commandtext, expectedtext):
        self.package = package
        self.commandtext = commandtext.split()      
        self.expected = expectedtext

    def test_automated_main(self):
        """Entry point for the testcase type automated."""
        automatedProcess = CallProcess(self.package)
        automatedProcess.start_process()
        