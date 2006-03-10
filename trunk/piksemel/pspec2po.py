#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import re
import piksemel as iks

po_header = """# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2006-03-08 12:58+0200\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"""

po_entry = """
#: %(ref)s
msgid %(id)s
msgstr %(str)s
"""

class Message:
    def __init__(self):
        self.reference = None
        self.msgid = None
        self.msgstr = None


class Po:
    def __init__(self, messages = None):
        self.messages = []
        if messages:
            self.messages = messages
    
    def _escape(self, str):
        if not str:
            return '""'
        
        str = re.sub('"', '\\"', str)
        
        parts = str.split("\n")
        
        if len(parts) == 1:
            return '"%s"' % parts[0]
        
        return '""' + "".join(map(lambda x: '\n"%s\\n"' % x, parts))
    
    def save(self, filename):
        f = file(filename, "w")
        f.write(po_header)
        for msg in self.messages:
            dict = {}
            dict["ref"] = msg.reference
            dict["id"] = self._escape(msg.msgid)
            dict["str"] = self._escape(msg.msgstr)
            f.write(po_entry % dict)
        f.close()
    
    def load(self, filename):
        self.messages = []
        msg = None
        for line in file(filename):
            line = line.rstrip("\n")
            
            if len(line.split()) == 0:
                if msg:
                    self.messages.append(msg)
                msg = Message()
            
            if not msg:
                continue
            
            if line.startswith("#: "):
                msg.reference = line[3:]


def find_pspecs(path):
    paks = []
    for root, dirs, files in os.walk(path):
        if "pspec.xml" in files:
            paks.append(root)
        # dont walk into the versioned stuff
        if ".svn" in dirs:
            dirs.remove(".svn")
    return paks

def extract_pspecs(path, language):
    messages = []
    paks = find_pspecs(path)
    for pak in paks:
        msg = Message()
        msg.reference = pak[len(path):] + ":summary"
        doc = iks.parse(pak + "/pspec.xml")
        source = doc.getTag("Source")
        for item in source.tags("Summary"):
            lang = item.getAttribute("xml:lang")
            if not lang or lang == "en":
                msg.msgid = item.firstChild().data()
            elif lang == language:
                msg.msgstr = item.firstChild().data()
        messages.append(msg)
        
        msg = Message()
        msg.reference = pak[len(path):] + ":description"
        doc = iks.parse(pak + "/pspec.xml")
        source = doc.getTag("Source")
        for item in source.tags("Description"):
            lang = item.getAttribute("xml:lang")
            if not lang or lang == "en":
                msg.msgid = item.firstChild().data()
            elif lang == language:
                msg.msgstr = item.firstChild().data()
        messages.append(msg)
    
    return messages


def extract(path, language, output):
    po = Po()
    po.messages = extract_pspecs(path, language)
    po.save(output)

def update(pofile, path):
    po = Po()
    po.load(pofile)
    for m in po.messages:
        print m.reference


if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2], "lala.po")
    #update("lala.po", None)
