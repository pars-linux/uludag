#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, string, os.path
from xml.dom import minidom, Node
import re


# This function parse the sgml files.


def readACKfile(parent):
    ackfile="ack"
    if os.path.exists(ackfile):
        for line in open(ackfile,'r').readlines():
            #print line
            parseSGML(parent, line)

    else:
        print "Ack file does not exist"


def parseSGML(parent, line):
    for node in parent.childNodes:
        if "testcase" in node.nodeName:
            for key in node.attributes.keys():
                if "order" in key:
                    if line.strip() in node.attributes.get(key).nodeValue:
                        #print node.attributes.get(key).nodeValue
                        for node in node.childNodes:
                            if "text" in node.nodeName:
                                print node.nodeValue
                            #if "command" in node.nodeName:
                            #    print node.nodeValue
                            #if "heritage" in node.nodeName:
                            #    print node.nodeValue
                    else:
                        for node in node.childNodes:
                            if "package" in node.nodeName and line.strip() in node.childNodes[0].nodeValue:
                                installationtestfile = open("installationtest", "a")
                                installationtestfile.write(line)


# Parsing start with this function and also the others
def run(inFileName):                                            # [5]
    doc = minidom.parse(inFileName)
    rootNode = doc.documentElement
    readACKfile(rootNode)

# the main function make a general loop for all sgml files created by splitsgmlfiles.py
def main():
    sgmlfile = "hardware-eng.sgml"
    if os.path.exists(sgmlfile):
        run(sgmlfile)
    else:
        print "SGML file does not exist"

if __name__ == '__main__':
    main()


