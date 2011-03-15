#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4.QtCore import *

from PyKDE4 import kdeui
from PyKDE4 import kdecore

class PEditLabelIcon(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        self.parent = parent
        self.readOnlyIcon = "/usr/share/icons/oxygen/16x16/actions/edit-rename.png"
        self.editIcon = "/usr/share/icons/oxygen/16x16/actions/dialog-ok-apply.png"
        self.setIcon(self.readOnlyIcon)

        self.setMaximumSize(QtCore.QSize(self.pixmap().width(), self.pixmap().height()))
        self.setMinimumSize(QtCore.QSize(self.pixmap().width(), self.pixmap().height()))

        self.installEventFilter(self)

    def setIcon(self, icon):
        self.setPixmap(QtGui.QPixmap(icon))

    """def sizeHint(self):
        return QtCore.QSize(self.pixmap().width(), self.pixmap().height())"""

    def eventFilter(self, target, event):
        if(event.type() == QtCore.QEvent.MouseButtonPress):
            if self.parent.label.isVisible():
                self.parent.startEditing()
            else:
                self.parent.endEditing()

        return False

class PEditLabelLabel(QtGui.QLabel):
    def __init__(self, parent, text):
        QtGui.QLabel.__init__(self, text, parent)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))

        self.installEventFilter(self)
        #self.updateSize()

    """def updateSize(self):
        width = self.fontMetrics().width(self.text())+2
        height = self.fontMetrics().height()+4

        #self.setMaximumSize(QtCore.QSize(width, height))
        #self.setMinimumSize(QtCore.QSize(width, height))"""

    def setText(self, text):
        QtGui.QLabel.setText(self, text)
        width = self.fontMetrics().width(self.text())+2
        height = self.fontMetrics().height()+4
        self.setMaximumSize(QtCore.QSize(width, height))
        #self.setMinimumSize(QtCore.QSize(width, height))

    def eventFilter(self, target, event):
        if event.type() == QEvent.MouseButtonDblClick:
            self.parent.startEditing()

        return False

class PEditLabelLineEdit(QtGui.QLineEdit):

    extraWidth = 32

    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        self.parent = parent
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))

        self.updateSize()

        self.installEventFilter(self)
        self.connect(self, SIGNAL('textChanged(QString)'), self.editTextChanged)

    def editTextChanged(self, text):
        self.updateSize()
        self.parent.updateSize()

    def updateSize(self):
        width = self.fontMetrics().width(self.text())+PEditLabelLineEdit.extraWidth
        #if self.parent.width() <= width+2+self.parent.icon.width(): # !!!!!!!! hata veriyor, icon yok diyor
        if self.parent.width() <= width+32:
            width = self.parent.width()-32
            if width <= 0:
                width = PEditLabelLineEdit.extraWidth
        self.setMaximumSize(QtCore.QSize(width,self.height()))
        self.setMinimumSize(QtCore.QSize(width,self.height()))

    def setText(self, text):
        QtGui.QLineEdit.setText(self, text)
        self.updateSize()

    def eventFilter(self, target, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                self.parent.endEditing()
        return False

    """def sizeHint(self):
        return QtCore.QSize(self.parent.label.width(), self.parent.label.height())"""

class PEditLabel(QtGui.QWidget):
    def __init__(self, parent, text):
        self.parent = parent
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QHBoxLayout(self)
        layout.setSpacing(0)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum))
        self.label = PEditLabelLabel(self, "")
        layout.addWidget(self.label)
        self.edit = PEditLabelLineEdit(self)
        self.edit.hide()
        layout.addWidget(self.edit)
        self.icon = PEditLabelIcon(self)
        layout.addWidget(self.icon)
        layout.addWidget(QLabel("", self))
        #layout.insertStretch(-1)

        self.storedText = text

        self.label.setStyleSheet("background-color: rgb( 128,128,0 )")
        self.icon.setStyleSheet("background-color: rgb( 28,128,128 )")
        self.setStyleSheet("background-color: rgb( 255,255,255 )")

        #self.resize(QtCore.QSize(400,400))
        self.updateSize()

    def updateSize(self):
        pass
        #self.setMinimumSize(QtCore.QSize(self.edit.width()+self.icon.width(), self.edit.height()+4))
        #self.setMaximumSize(QtCore.QSize(self.edit.width()+self.icon.width(), self.edit.height()+4))

    def startEditing(self):
        self.icon.setIcon(self.icon.editIcon)
        self.label.hide()
        self.edit.setText(self.storedText)
        self.edit.show()

    def endEditing(self):
        self.icon.setIcon(self.icon.readOnlyIcon)
        self.edit.hide()
        self.edit.clearFocus()
        self.storedText = self.edit.text()
        self.label.setText(self.cropEditText())
        self.label.show()

    def cropEditText(self):
        textWidth = self.label.fontMetrics().width(self.edit.text())
        if textWidth + 32 > self.width():
            r1 = float(self.width())/(textWidth+32)
            r2 = int(float(len(self.edit.text()))*r1)-3
            return self.edit.text()[:r2]+"..."
        else:
            return self.edit.text()

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    """def sizeHint(self):
        return QtCore.QSize(self.label.width()+self.icon.width(), self.label.height())"""

    def resizeEvent(self, event):
        #self.label.updateSize()
        if self.edit.isVisible():
            self.endEditing()
        self.label.setText(self.cropLabelText())
        ret = QWidget.resizeEvent(self, event)
        return ret

    def cropLabelText(self):
        if not self.label.text():
            if not self.storedText:
                return
                raise
            else:
                self.label.setText(self.storedText)
        #oldLength = len(self.label.text())
        textWidth = self.label.fontMetrics().width(self.storedText)
        if textWidth + 32 >= self.width():
            r1 = float(self.width())/(textWidth+32)
            r2 = int(float(len(self.storedText))*r1)-3
            print r2
            """print self.width()
            print textWidth+32
            print r1
            print ''"""
            return self.storedText[:r2]+"..."
        else:
            return self.storedText

