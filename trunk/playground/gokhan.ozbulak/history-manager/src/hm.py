#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QCursor, QColor, QBrush, QTextCharFormat
from PyQt4.QtCore import QDate


from pisi.db import historydb

from ui_hm_window import Ui_MainWindow

class HM(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.detailWidget.hide()

        self.populateCalendar()

    # Slots

    @QtCore.pyqtSignature("QDate")
    def on_calendarWidget_clicked(self):
        pos = self.mapFromGlobal(QCursor.pos())
        self.detailWidget.show()
        self.detailWidget.move(pos.x(), pos.y())

    @QtCore.pyqtSignature("bool")
    def on_widgetCloseButton_clicked(self):
        self.detailWidget.hide()


    # Helper functions

    def populateCalendar(self):
        histdb = historydb.HistoryDB()

        for operation in histdb.get_last():
            if operation.type == 'snapshot':
                frmt = self.setDateBackground(QColor(180, 190, 125))
            else:
                frmt = self.setDateBackground(QColor(165, 165, 165))

            opDate = operation.date.split("-")
            date = QDate(int(opDate[0]), int(opDate[1]), int(opDate[2]))

            self.calendarWidget.setDateTextFormat(date, frmt)

    def setDateBackground(self, color):
        brush = QBrush(color)

        frmt = QTextCharFormat()
        frmt.setBackground(brush)

        return frmt
