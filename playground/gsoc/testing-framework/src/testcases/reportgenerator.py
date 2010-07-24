#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from datetime import date 

 
class ReportGenerate:
    """class to generate and manage the outputs generated."""
    def __init__(self, totaltests, testreport, file, custom, report=None):
        self.totaltests = totaltests
        self.testreport = testreport
        self.file = file
        self.custom = custom
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
            if self.testreport[counter] is None:
                self.report.append('Testing was skipped. See output for details.')
                counter += 1
                continue
            self.report.extend(self.testreport[counter].report)
            counter += 1
        # Report generation
        output = '\n'.join(self.report)
        todayDate = date.today()
        # outFilename specifies the file name of the report. 
        outFilename = 'report-{0}'.format(todayDate)
        try:
            outFile = open(outFilename, 'w')
            outFile.write(output)
            outFile.close()
        except IOError:
            print '\nUnable to generate the report file. Failed.'
        print 'Report saved to: {0}'.format(os.path.join(os.getcwd(), outFilename))

