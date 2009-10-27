# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.gui.context as ctx

class windowTitle(QtGui.QFrame):
    def __init__(self, *args):
        QtGui.QFrame.__init__(self, *args)
        self.setMaximumSize(QSize(9999999,26))
        self.setObjectName("windowTitle")
        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0,0,4,0)

        self.label = QtGui.QLabel(self)
        self.label.setObjectName("label")
        self.label.setStyleSheet("padding-left:4px; font:bold 11px; color: #FFFFFF;")

        self.hboxlayout.addWidget(self.label)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setFocusPolicy(Qt.NoFocus)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("font:bold;")
        self.pushButton.setText("X")

        self.hboxlayout.addWidget(self.pushButton)

        self.move = 0
        self.mainwidget = self.parent()

    def mousePressEvent(self, event):
        self.move = 1
        self.start_x = event.globalPos().x()
        self.start_y = event.globalPos().y()
        wpos = self.mainwidget.mapToGlobal(QPoint(0,0))
        self.w_x = wpos.x()
        self.w_y = wpos.y()

    def mouseReleaseEvent(self, event):
        self.move = 0

    def mouseMoveEvent(self, event):
        if self.move:
            pos = event.globalPos()
            newpos = QPoint()
            newpos.setX(self.w_x + pos.x() - self.start_x)
            newpos.setY(self.w_y + pos.y() - self.start_y)
            self.mainwidget.move(newpos)

class Dialog(QtGui.QDialog):
    def __init__(self, t, w, parent=None):
        QtGui.QDialog.__init__(self, ctx.mainScreen.ui)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.windowTitle = windowTitle(self)
        self.windowTitle.label.setText(t)

        self.gridlayout.addWidget(self.windowTitle,0,0,1,1)

        self.content = w
        self.gridlayout.addWidget(self.content,1,0,1,1)

        QObject.connect(self.windowTitle.pushButton,SIGNAL("clicked()"),self.reject)
        QMetaObject.connectSlotsByName(self)

        self.setStyleSheet("""
            QFrame#windowTitle {background-color:#E75F10;color:#FFF;border:1px solid #FFF;border-radius:1px;}
        """)

class WarningDialog(Dialog):

    def __init__(self, w, parent):
        self.warning_widget = w
        Dialog.__init__(self, _("Warning"), self.warning_widget, parent)

        self.connect(self.warning_widget, SIGNAL("signalOK"),
                     self.slotOK)
        self.connect(self.warning_widget, SIGNAL("signalCancel"),
                     self.slotCancel)

    def slotOK(self):
        self.done(1)

    def slotCancel(self):
        self.done(0)

class WarningWidget(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        l = QtGui.QVBoxLayout(self)
        l.setSpacing(20)
        l.setMargin(10)

        self.warning = QtGui.QLabel(self)
        self.warning.setScaledContents(True)
        self.warning.setText(_('''<b>
<p>This action will start installing Pardus on
your system formatting the selected partition.</p>
</b>
'''))

        self.cancel = QtGui.QPushButton(self)
        self.cancel.setText(_("Cancel"))

        self.ok = QtGui.QPushButton(self)
        self.ok.setText(_("O.K. Go Ahead"))

        buttons = QtGui.QHBoxLayout(self)
        buttons.setSpacing(10)
        buttons.addStretch(1)
        buttons.addWidget(self.cancel)
        buttons.addWidget(self.ok)

        l.addWidget(self.warning)
        l.addLayout(buttons)

        self.connect(self.ok, SIGNAL("clicked()"),
                     self.slotOK)
        self.connect(self.cancel, SIGNAL("clicked()"),
                     self.slotCancel)

    def setMessage(self,msg):
        self.warning.setText(msg)

    def slotOK(self):
        self.emit(SIGNAL("signalOK"), ())

    def slotCancel(self):
        self.emit(SIGNAL("signalCancel"), ())


class InformationWindow(QtGui.QWidget):

    def __init__(self, message):
        QtGui.QWidget.__init__(self, ctx.mainScreen.ui)
        self.setObjectName("InfoWin")
        self.resize(280,50)
        self.setStyleSheet("""
            QFrame#frame { border: 1px solid #CCC;
                           border-radius: 4px;
                           background-image:url(':/gui/pics/transBlack.png');}

            QLabel { border:none;
                     color:#FFFFFF;
                     font:bold; }

            QProgressBar { border: 1px solid white;}

            QProgressBar::chunk { background-color: #F1610D;
                                  width: 0.5px;}
        """)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setObjectName("gridlayout")

        self.frame = QtGui.QFrame(self)
        self.frame.setObjectName("frame")

        self.gridlayout1 = QtGui.QGridLayout(self.frame)
        self.gridlayout1.setMargin(2)
        self.gridlayout1.setSpacing(3)
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName("message")
        self.hboxlayout.addWidget(self.label)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)

        self.progressBar = QtGui.QProgressBar(self.frame)
        self.progressBar.setMaximumSize(QSize(16777215,6))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value",QVariant(-1))
        self.progressBar.setObjectName("progressBar")
        self.gridlayout1.addWidget(self.progressBar,1,0,1,1)
        self.gridlayout.addWidget(self.frame,0,0,1,1)

        self.updateMessage(message)

    def updateMessage(self, message=None, progress=False):
        self.progressBar.setVisible(progress)
        self.move(ctx.mainScreen.ui.width()/2 - self.width()/2,
                  ctx.mainScreen.ui.height() - self.height()/2 - 26)
        if message:
            self.label.setText(message)
        ctx.mainScreen.processEvents()

    def updateAndShow(self, message, progress=False):
        self.updateMessage(message,progress)
        self.show()

    def show(self):
        QtGui.QWidget.show(self)
        ctx.mainScreen.processEvents()

    def hide(self):
        QtGui.QWidget.hide(self)
        ctx.mainScreen.processEvents()

