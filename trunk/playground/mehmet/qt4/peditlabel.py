#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt4 import QtGui
from PyQt4 import QtCore

from PyKDE4 import kdeui
from PyKDE4 import kdecore

class PEditLabelIcon(QtGui.QLabel):
    def __init__(self, parent):
        QtGui.QLabel.__init__(self, parent)
        self.readOnlyIcon = "/usr/share/icons/oxygen/16x16/actions/edit-rename.png"
        self.editIcon = "/usr/share/icons/oxygen/16x16/actions/dialog-ok-apply.png"
        self.setIcon(self.readOnlyIcon)

        self.parent = parent

        self.setMaximumSize(QtCore.QSize(self.pixmap().width(), self.pixmap().height()))
        self.setMinimumSize(QtCore.QSize(self.pixmap().width(), self.pixmap().height()))

        self.installEventFilter(self)

    def setIcon(self, icon):
        self.setPixmap(QtGui.QPixmap(icon))

    def sizeHint(self):
        return QtCore.QSize(self.pixmap().width(), self.pixmap().height())


    def eventFilter(self, target, event):
        if(event.type() == QtCore.QEvent.MouseButtonPress):
            if self.parent.label.isVisible():
                self.setIcon(self.editIcon)
                self.parent.label.hide()
                self.parent.edit.setText(self.parent.label.text())
                self.parent.edit.show()
            else:
                self.setIcon(self.readOnlyIcon)
                self.parent.edit.hide()
                self.parent.label.setText(self.parent.edit.text())
                self.parent.label.show()

        return False

class PEditLabelLabel(QtGui.QLabel):
    def __init__(self, parent, text):
        QtGui.QLabel.__init__(self, text, parent)

        width = self.fontMetrics().width(self.text())+2
        height = self.fontMetrics().height()+4

        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))

    def setText(self, text):
        QtGui.QLabel.setText(self, text)
        width = self.fontMetrics().width(self.text())+2
        height = self.fontMetrics().height()+4

        self.setMaximumSize(QtCore.QSize(width, height))
        self.setMinimumSize(QtCore.QSize(width, height))

class PEditLabelLineEdit(QtGui.QLineEdit):
    def __init__(self, parent):
        QtGui.QLineEdit.__init__(self, parent)
        self.parent = parent
        self.updateSize()

        self.installEventFilter(self)

    def updateSize(self, width=None):
        if width:
            self.setMaximumSize(QtCore.QSize(self.width()+width,self.height()))
            self.setMinimumSize(QtCore.QSize(self.width()+width,self.height()))
        else:
            self.setMaximumSize(QtCore.QSize(self.parent.label.width()+32,self.parent.label.height()+4))
            self.setMinimumSize(QtCore.QSize(self.parent.label.width()+32,self.parent.label.height()+4))

    def setText(self, text):
        QtGui.QLineEdit.setText(self, text)
        self.updateSize()

    def eventFilter(self, target, event):
        if(event.type() == QtCore.QEvent.KeyPress):
            if event.key() >= 32 or event.key() <= 127:
                self.updateSize(self.fontMetrics().width(event.text()))

        return False

    def sizeHint(self):
        return QtCore.QSize(self.parent.label.width(), self.parent.label.height())

class PEditLabel(QtGui.QWidget):
    def __init__(self, parent, text):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QHBoxLayout(self)
        layout.setSpacing(2)
        self.label = PEditLabelLabel(self, text)
        layout.addWidget(self.label)
        self.edit = PEditLabelLineEdit(self)
        self.edit.hide()
        layout.addWidget(self.edit)
        self.icon = PEditLabelIcon(self)
        layout.addWidget(self.icon)
        layout.insertStretch(3)

        #self.label.setStyleSheet( "background-color: rgb( 128,128,0 )" )
        #self.icon.setStyleSheet( "background-color: rgb( 128,128,128 )" )
        #self.setStyleSheet( "background-color: rgb( 128,18,18 )" )

        #self.resize(QtCore.QSize(400,400))


    def sizeHint(self):
        return QtCore.QSize(self.label.width()+self.icon.width(), self.label.height())


