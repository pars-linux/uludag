#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a code sample of the XML test file creation that will be implemented fully under the GSoC 2010 project.
# Please note that this is a prototype and not the final code. 
# As expected, it is incomplete and lacks the required features. 
# You need the lxml package installed. 
# You can do that by compiling it, or installing easy_install and then issuing the command: easy_install lxml

try:
  from lxml import etree
except ImportError:
  print 'lxml not found, please install the lxml library.'
  sys.exit('Now quitting.')

print 'Pardus Testing Framework - Automated Test Creation'

print '1. Name of the test: '
testName = raw_input()

print '2. Package: '
package = raw_input()
if package == '':
    print 'No package selected.\n'

print '3. Display text: '
text = raw_input()

print '4. Command:  '
command = raw_input()

print '5. Expected Output: '
expected = raw_input()

print 'Enter the name of the XML file: '
fileName = raw_input()

# XML generation starts here

root = etree.Element('document')

testcaseElt = etree.SubElement(root, 'testcase', test = 'automated')

nameElt = etree.SubElement(testcaseElt, 'name')
nameElt.text = testName

if(package != ''):
    packageElt = etree.SubElement(testcaseElt, 'package')
    packageElt.text = package

textElt = etree.SubElement(testcaseElt, 'text')
textElt.text = text

commandElt = etree.SubElement(testcaseElt, 'command')
commandElt.text = command

expectedOutput = etree.SubElement(testcaseElt, 'expected')
expectedOutput.text = expected

# XML file output goes here

outFile = open(fileName, 'w')

rootTree = etree.ElementTree(root)

rootTree.write(outFile, pretty_print = True)

outFile.close()