# -*- coding: utf-8 -*-

import gettext
__trans = gettext.translation('ranimator', fallback=True)
i18n = __trans.ugettext

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimeLine, QObject, SIGNAL

B = " <span style='margin-left: %s;font-size:%spt;'>%s</span> "
C = "%s"

minFontSize = 9
maxFontSize = 11

class Animator:

    def __init__(self, titles, label):
        self.timeLine = QTimeLine(350)
        self.timeLine.setUpdateInterval(10)

        # get titles
        self.titles = titles

        # get  label widget
        self.label = label

        self.cpos = 0
        self.font = maxFontSize / 2

        self.move(0, self.font)

        QObject.connect(self.timeLine, SIGNAL("valueChanged(qreal)"), self.draw)
        QObject.connect(self.timeLine, SIGNAL("finished()"), self.finished)

    def running(self):
        return self.timeLine.state() == QTimeLine.Running

    def draw(self):
        if self.running():
            self.move(self.cpos, self.font)
            self.font += 1
            if self.font >= maxFontSize:
                self.font = maxFontSize

    def finished(self):
        self.font = maxFontSize / 2

    def move(self, pos, maxf):
        i = 0
        text = ""
        ratio = (maxf - minFontSize) / 2
        for title in self.titles:
            if i == pos:
                size = maxf
            elif i == pos - 1 or i == pos + 1:
                size = maxf - ratio
            else:
                size = minFontSize
            text += B % (size,size, title)
            i += 1

        self.label.setText(C % text)
        self.cpos = pos

    def next(self):
        self.cpos += 1
        self.timeLine.start()

    def prev(self):
        self.cpos -= 1
        self.timeLine.start()

