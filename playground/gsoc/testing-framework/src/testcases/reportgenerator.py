#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from sys import exit

from clcolorize import colorize
 
 
class ReportGenerate:
    """class to generate and manage the outputs generated."""
    def __init__(self, totaltests, testreport, file, custom,
                                        rootelement, summary=None, report=None):   
        self.totaltests = totaltests
        self.testreport = testreport
        self.file = file
        self.custom = custom
        self.rootelement = rootelement
        self.summary = list()
        self.report = list()
    
    def main(self):
        """The method for report generation."""
        testerName = raw_input('Please enter your name:\n> ')
        self.summary.append('Summary\n')
        for lst in (self.report, self.summary):
            lst.append('Pardus Testing Framework')
            lst.append('Using testcase file: {0}'.format(self.file))
            if self.custom is not None:
                lst.append('Custom package parsing: ' \
                                            '{0}'.format(', '.join(self.custom)))
            if testerName == '':
                print ''
                lst.append('Tested by: No name/ID was given.\n')
            else:
                lst.append('Tested by: {0}\n'.format(testerName))
        counter = 0
        while counter < self.totaltests:
            testcaseNumber = 'Test {0} / {1}'.format(counter+1, self.totaltests)
            self.report.append(testcaseNumber)
            # get the type of test
            testType = self.rootelement[counter].get('test')
            self.report.append("Type of test: '{0}'".format(testType))
            if self.testreport[counter] is None:
                self.report.append('Testing was skipped. See output for details')
                self.summary.append('{0} - Skipped'.format(testcaseNumber))
                counter += 1
                continue
            self.report.extend(self.testreport[counter].report)
            self.summary.append('{0} \n' \
                                 '{1}'.format(testcaseNumber,
                                 '\n'.join(self.testreport[counter].summary)))
            for lst in (self.report, self.summary):
                lst.append('\n')
            counter += 1
        self.generate_list(self.report, 'report', testerName)
        self.generate_list(self.summary, 'summary', testerName)
    
    def generate_list(self, writelist, report_type, testername):
        """Write the report/ summary to a file."""
        output = '\n'.join(writelist)
        fullFileName = os.path.basename(self.file)
        fileName = os.path.splitext(fullFileName)[0]
        # outFileName specifies the file name of the report. 
        outFileName = '{0}-{1}-{2}'.format(report_type, testername, fileName)
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
        print "{0} saved to:".format(report_type.title()), 
        print "'{0}'".format(os.path.join(os.getcwd(), outFileName))