#!/usr/bin/python
# -*- coding: utf-8 -*-

# Rasta RST Editor
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom

class RstLexer(QsciLexerCustom):
    def __init__(self, parent, font=None):
        QsciLexerCustom.__init__(self, parent)
        self._styles = {
            0: 'Default',
            1: 'Comment',
            2: 'Key',
            3: 'Bullet'
            }
        for key,value in self._styles.iteritems():
            setattr(self, value, key)
        if font:
            if font is QVariant:
                font = font.toString()
            self.dfont = QFont(font)
        else:
            self.dfont = QFont('Droid Sans Mono', 10)

    def language(self):
        return 'Rst Files'

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QColor('#000000')
        elif style == self.Comment:
            return QColor('#A0A0A0')
        elif style == self.Bullet:
            return QColor('#CC6600')
        elif style == self.Key:
            return QColor('blue')
        return QsciLexerCustom.defaultColor(self, style)

    def defaultPaper(self, style):
        return QsciLexerCustom.defaultPaper(self, style)

    def defaultEolFill(self, style):
        return QsciLexerCustom.defaultEolFill(self, style)

    def defaultFont(self, style):
        return self.dfont

    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        SCI = editor.SendScintilla
        set_style = self.setStyling

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            source = bytearray(end - start)
            SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return

        index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)

        state = self.Default

        self.startStyling(start, 0x1f)

        for line in source.splitlines(True):
            length = len(line)
            if length == 1:
                state = self.Default
            else:
                firsttwo = line[0:2]
                if firsttwo == '..':
                    state = self.Comment
                elif line.find('--') > -1 or line.find('==') > -1 :
                    state = self.Key
                elif chr(line[0]) in ('*','-'):
                    state = self.Bullet
                else:
                    state = self.Default
            set_style(length, state)

