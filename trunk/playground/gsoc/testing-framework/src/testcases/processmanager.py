#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from clcolorize import colorize


class CallProcess:
    """class to handle process management from the framework."""
    def __init__(self, process):
        self.process = process
    
    def start_process(self):
        """Start the process and return the output and the error messages."""
        try:
            startProcess = subprocess.Popen(self.process, shell=False,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            processOutput, processError = startProcess.communicate()
            if processError:
                print colorize('Invalid command', 'red')
                return
        except OSError:
            print colorize('Invalid process.', 'red')
 
