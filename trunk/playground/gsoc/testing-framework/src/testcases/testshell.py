#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
from clcolorize import colorize


class TestShell:
    """This class is used to handle the testcase of shell, in which the user is
    told to run a certain command on and note down the output."""
    def __init__(self, element, text, report=None):
        self.element = element
        self.textlist = text
        self.report = list()
        
    def test_shell_main(self):
        """Print the text and ask the user to run the commands."""
        case = self.element.xpath('case')
        totalCases = len(case)
        counter = 0
        while counter < totalCases:
            print colorize('Case {0} of {1}', 'bold').format(counter+1, totalCases)
            print ''.join(self.textlist)
            for text in self.element.getiterator('command'):
                print colorize(text.text, 'yellow')
            raw_input('> Press ENTER to continue ')
            counter += 1
        print colorize('Enter your observation of the tests:', 'bold')
        observation = raw_input('> ')
        self.report.append(observation)