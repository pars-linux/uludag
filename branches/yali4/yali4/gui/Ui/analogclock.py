#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui


class AnalogClock(QtGui.QWidget):
    hourHand = QtGui.QPolygon([
        QtCore.QPoint(7, 8),
        QtCore.QPoint(-7, 8),
        QtCore.QPoint(0, -40)
    ])

    minuteHand = QtGui.QPolygon([
        QtCore.QPoint(7, 8),
        QtCore.QPoint(-7, 8),
        QtCore.QPoint(0, -70)
    ])

    hourColor = QtGui.QColor(127, 0, 127)
    minuteColor = QtGui.QColor(0, 127, 127, 191)

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("update()"))
        timer.start(1000)

        self.setWindowTitle(self.tr("Analog Clock"))
        self.resize(200, 200)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QtCore.QTime.currentTime()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)

        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()

        painter.setPen(AnalogClock.hourColor)

        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)

        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()

        painter.setPen(AnalogClock.minuteColor)

        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    clock = AnalogClock()
    clock.show()
    sys.exit(app.exec_())
