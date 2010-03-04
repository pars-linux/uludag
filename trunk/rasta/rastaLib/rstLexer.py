# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QMainWindow, QColor, QFont
from PyQt4.Qsci import QsciScintilla, QsciLexerCustom

class RstLexer(QsciLexerCustom):
    def __init__(self, parent):
        QsciLexerCustom.__init__(self, parent)
        self._styles = {
            0: 'Default',
            1: 'Comment',
            2: 'Key',
            3: 'Bullet'
            }
        for key,value in self._styles.iteritems():
            setattr(self, value, key)

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
        return QFont('Droid Sans Mono', 10)

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

