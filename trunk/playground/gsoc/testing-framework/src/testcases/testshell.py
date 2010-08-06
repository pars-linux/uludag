#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
from clcolorize import colorize


class TestShell:
    """This class is used to handle the testcase of shell, in which the user is
    told to run a certain command on and note down the output."""
    def __init__(self, element, report=None):
        self.element = element
        self.report = list()
        
    def test_shell_main(self):
        """Print the text and ask the user to run the commands."""
        packageList = []
        for package in self.element.getiterator('package'):
            packageList.append(package.text)
        print 'Package:      ', colorize(', '.join(packageList), 'bold')
        case = self.element.xpath('case')
        totalCases = len(case)
        counter = 0
        print ''
        while counter < totalCases:
            print 'Case {0} of {1}:'.format(counter+1, totalCases)
            for text in case[counter].getiterator('text'):
                print text.text
            for text in case[counter].getiterator('command'):
                print colorize(text.text, 'bold')
            # Get the observations
            answer = raw_input('Did the above test run as expected? (y / n): ')
            if answer in ('y', 'Y', 'yes', 'YES', ''):
                self.report.append('Case {0} of {1}: Success'.format(counter+1, totalCases))
            else:
                self.report.append('Case {0} of {1}: Failed'.format(counter+1, totalCases))
                observation = raw_input('Enter your observations: \n> ')
                if not observation == '':
                    self.report.append('\tCase {0} Observation: {1}'.format(counter+1,
                                                                    observation))
                else:
                    self.report.append('\tCase {0}: No observation entered.'.format(counter+1))
            print ''
            counter += 1