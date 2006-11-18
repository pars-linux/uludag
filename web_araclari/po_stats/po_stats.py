#!/usr/bin/python
#-*- coding: utf-8 -*-

#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

"""

  A basic script to creates HTML statistics from PO files (see po_files.py and pstemplates.py).

  Usage: /path/to/po_stats.py -l output_lang

"""

import os
import sys
import getopt
from urlparse import urlparse
from operator import itemgetter

sys.path.append('.')

try:
    from pstemplates import *
    from po_files import *
except ImportError, e:
    print >> sys.stderr, e
    sys.exit(0)


__version__ = "0.1"


def usage():
    print >> sys.stderr, __doc__
    sys.exit(1)

def processPOFile(poPath, proName = 'Noname'):
    """Returns a dictionary filled up with some information about the po file"""
    ID, STR = range(1, 3)

    fileInfo = {}

    headerFields = ["Project-Id-Version", "POT-Creation-Date", "PO-Revision-Date", "Last-Translator", "Language-Team"]

    for k in ['Untranslated', 'Translated', 'Fuzzy', 'Total', 'pU', 'pF', 'pT']:
        fileInfo[k] = 0

    fileInfo['Project-Name'] = proName

    if not poPath:
        for h in headerFields + ['File-Name', 'File-Path']:
            fileInfo[h] = "#"
        return fileInfo

    fileInfo['File-Name'] = os.path.basename(poPath)
    fileInfo['File-Path'] = poPath

    if urlparse(poPath)[0] == "http" or urlparse(poPath)[0] == "https":
        from urllib2 import urlopen
        try:
            fileObj = urlopen(poPath)
        except:
            print >> sys.stderr, "Unable to read file: '%s'" % poPath
            sys.exit(1)
    elif urlparse(poPath)[0] == "":
        try:
            fileObj = open(poPath)
        except IOError, msg:
            print >> sys.stderr, "Unable to read file: '%s'" % poPath
            sys.exit(1)
    else:
        print >> sys.stderr, "Unknown url: '%s'" % poPath

    lines = fileObj.readlines()

    def processEntry(msgid, msgstr, fuzzy):
        if (not msgid) and msgstr:
            # We're in the header section of the PO.
            _ = lambda x: x.split(':')[1].strip()
            for e in msgstr.split('\n'):
                for i in headerFields:
                    if e.startswith(i):
                        fileInfo[i] = _(e)
                        continue
        if not msgstr:
            fileInfo['Untranslated'] += 1
        if fuzzy:
            fileInfo['Fuzzy'] += 1
        if (msgid and msgstr) and (not fuzzy):
            fileInfo['Translated'] += 1

    section = None
    fuzzy = 0
    lno = 0

    # Parse the catalog
    for l in lines:
        lno += 1
        # new entry
        if l[0] == '#' and section == STR:
            processEntry(msgid, msgstr, fuzzy)
            section = None
            fuzzy = 0
        # fuzzy
        if l[:2] == '#,' and 'fuzzy' in l:
            fuzzy = 1
        # Skip comments
        if l[0] == '#':
            continue
        # Now we are in a msgid section, output previous section
        if l.startswith('msgid'):
            if section == STR:
                processEntry(msgid, msgstr, fuzzy)
            section = ID
            l = l[5:]
            msgid = msgstr = ''
        # Now we are in a msgstr section
        elif l.startswith('msgstr'):
            section = STR
            l = l[6:]
        # Skip empty lines
        l = l.strip()
        if not l:
            continue

        l = eval(l)
        if section == ID:
            msgid += l
        elif section == STR:
            msgstr += l
        else:
            print >> sys.stderr, 'Syntax error on %s:%d' % (infile, lno), \
                  'before:'
            print >> sys.stderr, l
            sys.exit(1)
    # last entry
    if section == STR:
        processEntry(msgid, msgstr, fuzzy)

    for k in ['Untranslated', 'Translated', 'Fuzzy']:
        fileInfo['Total'] += fileInfo[k]

    fileInfo['pU'] = 100 * fileInfo['Untranslated'] / fileInfo['Total']
    fileInfo['pT'] = 100 * fileInfo['Translated'] / fileInfo['Total']
    fileInfo['pF'] = 100 * fileInfo['Fuzzy'] / fileInfo['Total']

    return fileInfo


def createHTML(files, po_lang, html_lang = 'en'):
    body, dlist = [], []

    for f in files:
        dlist.append(processPOFile(files[f], f))

    for d in sorted(dlist, key=itemgetter('pT'), reverse=True):
        body.append(htmlBodyTemplate[html_lang] % (d))

    try:
        of = open("stats-%s.html" % po_lang, "w")
    except IOError:
        print >> sys.stderr, "Unable to open file for writing: '%s'" % (outFile)
        sys.exit(1)

    of.write(htmlHeaderTemplate[html_lang] % (po_lang))
    of.writelines(body)
    of.write(htmlFooterTemplate[html_lang])

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:')
    except getopt.error:
        usage()

    if (args) or (not opts) or (len(opts) != 1):
        usage()

    html_lang = opts[0][1]

    for t in ['htmlHeaderTemplate', 'htmlBodyTemplate', 'htmlFooterTemplate']:
        if not eval(t).get(html_lang):
            print "There is no HTML template for language '%s'" % html_lang
            sys.exit(1)

    for po_lang in po_files.keys():
        createHTML(po_files[po_lang], po_lang, html_lang)

if __name__ == '__main__':
    main()
