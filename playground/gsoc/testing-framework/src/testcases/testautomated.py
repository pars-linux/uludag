#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

from clcolorize import colorize


class TestAutomated:
    """This class will perform an automated test, the purpose of which is to run
    a command, get its output and compare it with the expected output, which is
    already encoded in the testcase file."""
    def __init__(self, package, element, report=None):
        self.package = package
        self.element = element
        self.report = list()

    def test_automated_main(self):
        """Entry point for the testcase type automated."""
        case = self.element.xpath('case')
        totalCases = len(case)
        counter = 0
        print ''
        while counter < totalCases:
            print colorize('Case {0} of {1}', 'bold').format(counter+1, totalCases)
            self.report.append('')
            self.report.append('Case {0} of {1}'.format(counter+1, totalCases))
            for text in case[counter].getiterator('text'):
                print text.text
            commandList = []
            for command in case[counter].getiterator('command'):
                commandList.append(command.text)
            totalCommands = len(commandList)
            self.report.append('Total Commands: {0}'.format(totalCommands))
            self.report.append('-')
            commandCounter = 0
            while commandCounter < totalCommands:
                self.report.append('Command {0}: {1}'.format(commandCounter+1,
                                                    commandList[commandCounter]))
                try:
                    runCommand = subprocess.Popen(commandList[commandCounter].split(),
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)
                except OSError:
                    self.report.append('Output: Invalid command or invalid option')
                    commandCounter +=1 
                    continue
                output, error = runCommand.communicate()
                if error:
                    self.report.append('Error: {0}'.format(error.rstrip()))
                    commandCounter +=1 
                    continue
                self.report.append('Output: {0}'.format(output.rstrip()))
                commandCounter += 1
            for expected in case[counter].getiterator('expected'):
                self.report.append('Expected: {0}'.format(expected.text))
            print ''
            counter += 1