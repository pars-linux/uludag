#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import codecs
from qt import *
from qtext import *

def load(filename):
    f = codecs.open(filename, "r", "utf-8")
    data = f.read()
    f.close()
    return data

def save(filename, data):
    f = codecs.open(filename, "w", "utf-8")
    f.write(data)
    f.close()

class HTMLLexer(QextScintillaLexerHTML):
    def __init__(self):
        QextScintillaLexerHTML.__init__(self)
        self.myfont = QFont("Sans", 10)
    
    def font(self, style):
        return self.myfont


class PythonLexer(QextScintillaLexerPython):
    def __init__(self):
        QextScintillaLexerPython.__init__(self)
        self.myfont = QFont("Sans", 10)
    
    def font(self, style):
        return self.myfont


class TextEd(QextScintilla):
    def __init__(self, path, name, lexer=None):
        # standart setup
        QextScintilla.__init__(self)
        self.setUtf8(True)
        self.setAutoIndent(1)
        self.setIndentationWidth(4)
        self.setIndentationsUseTabs(0)
        self.textModified = False
        self.connect(self, SIGNAL("textChanged()"), self._modified)
        # try to load file
        self.filename = os.path.join(path, name)
        try:
            data = load(self.filename)
            self.setText(data)
            self.textModified = False
            self.loaded = True
        except:
            self.loaded = False
        # syntax highlighting
        self.mylexer = lexer
        if lexer:
            self.setLexer(lexer)
    
    def _modified(self):
        self.textModified = True
    
    def save_changes(self):
        if self.textModified:
            data = self.text()
            save(self.filename, unicode(data))
            self.textModified = False
