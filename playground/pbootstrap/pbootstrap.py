#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from optparse import OptionParser

def main():
    # Command-line parsing
    parser = OptionParser()

    parser.add_option("-r", "--release",
                      action="store",
                      dest="release",
                      help="Set target Pardus release (Corporate2|2011)")

    parser.add_option("-a", "--architecture",
                      action="store",
                      dest="architecture",
                      help="Set target architecture (x86_64|i686)")

    parser.add_option("-d", "--destdir",
                      action="store",
                      dest="destdir",
                      help="Set the target installation directory")



    (options, packages) = parser.parse_args()

    print options.release



if __name__ == "__main__":
    main()

