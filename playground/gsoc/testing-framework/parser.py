#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob

try:
    from lxml import etree
except ImportError:
    sys.stderr.write('Error importing the \'lxml\' library.\nYou need the lxml library package installed to run this software.')
    sys.exit(1)

def showXMLFiles(path):
    
    print 'Listing XML files in \'{0}\': \n'.format(path)
    
    filePath = os.path.join(path, '*.xml')
    
    pathList = glob.glob(filePath)
    
    fileList = [os.path.basename(x) for x in pathList]
    
    if not fileList:
        sys.stderr.write('No XML files were found in the current location. Restart this program with the \'--help\' switch for more information.\n\n')
        sys.exit(1)
        
    fileListDict = dict((enumerate(fileList, 1)))
    
    for number, element in enumerate(fileList, 1):
        print number, element
    
    while True:
        
        try:
            choice = int(raw_input('\nEnter your choice > '))
        except ValueError:
            print 'Please enter a valid choice between (1 - {0})'.format(len(fileList))
            continue
                   
        if not (choice > 0 and choice <= len(fileList)):
            print 'Please enter a valid choice between (1 - {0})'.format(len(fileList))
            continue
        
        print 'Parsing file: {0}'.format(fileListDict[choice])
        sys.exit(1)
    
def argCheck():
    
    if len(sys.argv) == 1:
        showXMLFiles(os.getcwd())
    elif os.path.isdir(sys.argv[1]):
        currentDirectory = sys.argv[1]
        showXMLFiles(currentDirectory)
    elif sys.argv[1] == '--help':
        print """Usage: parser.py [path]
                
[path] is the path location where the XML files are saved.
If no argument is specified, the parser will use the current working directory.\n"""
    else:
        sys.stderr.write('Invalid directory. Restart this program with \'--help\' for more information.\n')
        sys.exit(1)

print '\nPardus GNU/ Linux Testing Framework.\n'

argCheck()    
