#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time

from sys import exit
from datetime import date 

 
class ReportGenerate:
    """class to generate and manage the outputs generated."""
    def __init__(self, totaltests, testreport, file, custom, rootelement, report=None):
        self.totaltests = totaltests
        self.testreport = testreport
        self.file = file
        self.custom = custom
        self.rootelement = rootelement
        self.report = list()
    
    def main(self):
        """The method for report generation."""
        self.report.append('Pardus Testing Framework')
        self.report.append('Using testcase file: {0}'.format(self.file))
        if self.custom is not None:
            self.report.append('Custom package parsing using list: {0}'.format(self.custom))
        counter = 0
        while counter < self.totaltests:
            self.report.append('\n')
            self.report.append('Test {0} / {1}'.format(counter+1, self.totaltests))
            # Get the type of test
            testType = self.rootelement[counter].get('test')
            self.report.append("Type of test: '{0}'".format(testType))
            if self.testreport[counter] is None:
                self.report.append('Testing was skipped. See output for details.')
                counter += 1
                continue
            self.report.extend(self.testreport[counter].report)
            counter += 1
        # Report generation
        output = '\n'.join(self.report)
        todayDate = date.today()
        # outFileName specifies the file name of the report. 
        outFileName = '{0}-{1}'.format(os.path.basename(self.file), todayDate)
        try:
            # if the file already exists, create a new file using time as the variable
            if os.path.isfile(os.path.join(os.getcwd(), outFileName)):
                currentTime = time.strftime('%H:%M:%S')
                outFileName += '-{0}'.format(currentTime)
            outFile = open(outFileName, 'w')
            outFile.write(output)
            outFile.close()
        except IOError:
            exit('Error: Unable to generate the report file.')
        print 'Report saved to: {0}'.format(os.path.join(os.getcwd(), outFileName))