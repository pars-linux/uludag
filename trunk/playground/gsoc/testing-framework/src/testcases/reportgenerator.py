#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from sys import exit
from datetime import date 

from clcolorize import colorize
 
 
class ReportGenerate:
    """class to generate and manage the outputs generated."""
    def __init__(self, totaltests, testreport, file, custom, rootelement, summary,
                                                                    report=None):   
        self.totaltests = totaltests
        self.testreport = testreport
        self.file = file
        self.custom = custom
        self.rootelement = rootelement
        self.summary = summary
        self.report = list()
    
    def main(self):
        """The method for report generation."""
        testerName = raw_input('Please enter your name/ ID:\n> ')
        self.summary.append('\nTesting information:\n')
        for lst in (self.report, self.summary):
            lst.append('Pardus Testing Framework')
            lst.append('Using testcase file: {0}'.format(self.file))
            if self.custom is not None:
                lst.append('Custom package parsing: ' \
                                            '{0}'.format(', '.join(self.custom)))
            if testerName == '':
                lst.append('Tested by: No name/ID was given.')
            else:
                lst.append('Tested by: {0}'.format(testerName))
        counter = 0
        while counter < self.totaltests:
            self.report.append('\n')
            self.report.append('Test {0} / {1}'.format(counter+1, self.totaltests))
            # get the type of test
            testType = self.rootelement[counter].get('test')
            self.report.append("Type of test: '{0}'".format(testType))
            if self.testreport[counter] is None:
                self.report.append('Testing was skipped. See output for details.')
                counter += 1
                continue
            self.report.extend(self.testreport[counter].report)
            counter += 1
        self.generate_list(self.report, 'report')
        self.generate_list(self.summary, 'summary')
    
    def generate_list(self, writelist, report_type):
        """Write the report/ summary to a file."""
        output = '\n'.join(writelist)
        todayDate = date.today()
        # outFileName specifies the file name of the report. 
        outFileName = '{0}-{1}-{2}'.format(report_type,
                                         os.path.basename(self.file), todayDate)
        try:
            # if the file already exists, create a new file
            # using time as the variable. Append time to the filename
            if os.path.isfile(os.path.join(os.getcwd(), outFileName)):
                currentTime = time.strftime('%H:%M:%S')
                outFileName += '-{0}'.format(currentTime)
            outFile = open(outFileName, 'w')
            outFile.write(output)
            outFile.close()
        except IOError:
            exit('Error: Unable to generate the {0} file.'.format(report_type))
        print '{0} saved to:'.format(report_type.title()), 
        print '{0}'.format(os.path.join(os.getcwd(), outFileName))