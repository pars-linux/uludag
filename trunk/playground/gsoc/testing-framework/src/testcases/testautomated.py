#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from clcolorize import colorize


class TestAutomated:
    """This class will perform an automated test, the purpose of which is to run
    a command, get its output and compare it with the expected output, which is
    already encoded in the testcase file."""
    def __init__(self, package, commandtext, expectedtext, report=None):
        self.package = package
        self.commandtext = commandtext.split()      
        self.expected = expectedtext
        self.report = list()

    def test_automated_main(self):
        """Entry point for the testcase type automated."""
        try:
            runCommand = subprocess.Popen(self.commandtext,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        except OSError:
            self.report.append('Invalid command or invalid option: {0}'.format(''.join(self.commandtext)))
            return
        output, error = runCommand.communicate()
        if error:
            self.report.append('Error: {0}'.format(error))
            return 
        self.report.append('Output: {0}'.format(output.rstrip()))
        self.report.append('Expected: {0}'.format(self.expected))