#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Rasta RST Editor
    2010 - Gökmen Göksel <gokmen:pardus.org.tr> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# RstTextEdit Widget based on John Schember 's (2009) SpellText Edit
# which has MIT license

import re
import sys

import enchant

from PyQt4.Qt import *
from PyQt4.QtCore import pyqtSignal

class RstTextEdit(QPlainTextEdit):

    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)

        # Default dictionary based on the current locale.
        self.dict = enchant.Dict()
        self.highlighter = RstHighlighter(self.document())
        self.highlighter.setDict(self.dict)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            event = QMouseEvent(QEvent.MouseButtonPress, event.pos(),
                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QPlainTextEdit.mousePressEvent(self, event)

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()

        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)

        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if self.textCursor().hasSelection():
            text = unicode(self.textCursor().selectedText())
            if not self.dict.check(text):
                spell_menu = QMenu('Spelling Suggestions')
                for word in self.dict.suggest(text):
                    action = SpellAction(word, spell_menu)
                    action.correct.connect(self.correctWord)
                    spell_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                if len(spell_menu.actions()) != 0:
                    popup_menu.insertSeparator(popup_menu.actions()[0])
                    popup_menu.insertMenu(popup_menu.actions()[0], spell_menu)

        popup_menu.exec_(event.globalPos())

    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        cursor = self.textCursor()
        cursor.beginEditBlock()

        cursor.removeSelectedText()
        cursor.insertText(word)

        cursor.endEditBlock()

class RstHighlighter(QSyntaxHighlighter):

    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)

        self.dict = None

    def setDict(self, dict):
        self.dict = dict

    def highlightBlock(self, text):
        if not self.dict:
            return

        text = unicode(text)

        format = QTextCharFormat()
        format.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

        format.setUnderlineColor(Qt.green)
        start = 0
        for line in text.splitlines():
            if line.lstrip(' ').startswith('*'):
                self.setFormat(start, start + len(line), format)
            start = len(line)

        format.setUnderlineColor(Qt.red)
        for word_object in re.finditer(self.WORDS, text):
            if not self.dict.check(word_object.group()):
                self.setFormat(word_object.start(),
                    word_object.end() - word_object.start(), format)


class SpellAction(QAction):

    '''
    A special QAction that returns the text in a signal.
    '''

    correct = pyqtSignal(unicode)

    def __init__(self, *args):
        QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(
            unicode(self.text())))

