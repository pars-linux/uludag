# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
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

import random
import yali4.gui.context as ctx

class windowTitle(QtGui.QFrame):
    def __init__(self, parent, closeButton=True):
        QtGui.QFrame.__init__(self, parent)
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

        if closeButton:
            self.pushButton = QtGui.QPushButton(self)
            self.pushButton.setFocusPolicy(Qt.NoFocus)
            self.pushButton.setObjectName("pushButton")
            self.pushButton.setStyleSheet("font:bold;")
            self.pushButton.setText("X")

            self.hboxlayout.addWidget(self.pushButton)

        self.dragPosition = None
        self.mainwidget = self.parent()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.mainwidget.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.mainwidget.move(event.globalPos() - self.dragPosition)
            event.accept()

class Dialog(QtGui.QDialog):
    def __init__(self, title, widget, parent = None, closeButton = True, keySequence = None):
        QtGui.QDialog.__init__(self, ctx.mainScreen)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.windowTitle = windowTitle(self, closeButton)
        self.windowTitle.label.setText(title)

        self.gridlayout.addWidget(self.windowTitle,0,0,1,1)

        self.content = widget
        self.gridlayout.addWidget(self.content,1,0,1,1)

        if closeButton:
            QObject.connect(self.windowTitle.pushButton,SIGNAL("clicked()"),self.reject)

        if keySequence:
            shortCut = QtGui.QShortcut(keySequence, self)
            QObject.connect(shortCut, SIGNAL("activated()"), self.reject)

        QMetaObject.connectSlotsByName(self)

        self.setStyleSheet("""
            QFrame#windowTitle {background-color:#984379;color:#FFF;border:1px solid #FFF;border-radius:4px;}
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
<p>This action will start installing Pardus on<br>
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

class RebootWidget(QtGui.QWidget):

    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        l = QtGui.QVBoxLayout(self)
        l.setSpacing(20)
        l.setMargin(10)

        warning = QtGui.QLabel(self)
        warning.setText(_('''<b>
<p>Press Reboot button to restart your system.</p>
</b>
'''))

        self.reboot = QtGui.QPushButton(self)
        self.reboot.setText(_("Reboot"))

        buttons = QtGui.QHBoxLayout(self)
        buttons.setSpacing(10)
        buttons.addStretch(1)
        buttons.addWidget(self.reboot)

        l.addWidget(warning)
        l.addLayout(buttons)

        self.connect(self.reboot, SIGNAL("clicked()"),
                     self.slotReboot)

    def slotReboot(self):
        self.emit(SIGNAL("signalOK"), ())

class InformationWindow(QtGui.QWidget):

    def __init__(self, message):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        self.setObjectName("InfoWin")
        self.resize(280,50)
        self.setStyleSheet("""
            QFrame#frame { border: 1px solid #CCC;
                           border-radius: 4px;
                           background-image:url(':/gui/pics/transBlack.png');}

            QLabel { border:none;
                     color:#FFFFFF;}

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
        self.move(ctx.mainScreen.width()/2 - self.width()/2,
                  ctx.mainScreen.height() - self.height()/2 - 26)
        if message:
            self.label.setText(message)
        ctx.mainScreen.processEvents()

    def updateAndShow(self, message, progress=False):
        self.updateMessage(message,progress)
        self.show()
        ctx.mainScreen.processEvents()

    def show(self):
        QtGui.QWidget.show(self)
        ctx.mainScreen.processEvents()

    def hide(self):
        QtGui.QWidget.hide(self)
        ctx.mainScreen.processEvents()

class Yimirta(QtGui.QWidget):

    def __init__(self, notifier):
        QtGui.QWidget.__init__(self, ctx.mainScreen)
        Pix = QtGui.QPixmap(':/gui/pics/working.png')
        Pix2= QtGui.QPixmap(':/gui/pics/core.png')
        self.setObjectName("Yimirta")
        self.resize(140,145)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(0)
        self.gridlayout.setObjectName("gridlayout")

        self.frame = QtGui.QFrame(self)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")

        self.gridlayout1 = QtGui.QGridLayout(self.frame)
        self.gridlayout1.setObjectName("gridlayout1")

        self.timer = QTimer(self)
        self.remain = 2000
        self.oldscore = 0
        QObject.connect(self.timer, SIGNAL("timeout()"),self.goturBeniGittiginYere)
        self.pix = QtGui.QLabel(self)
        self.pix.setObjectName("pix")
        self.pix.setAlignment(Qt.AlignCenter)
        self.pix.setPixmap(Pix)
        self.gridlayout1.addWidget(self.pix,0,0,1,1)
        self.gridlayout.addWidget(self.frame,0,0,1,1)
        self.score = 0
        self.notifier = notifier
        self.setMouseTracking(True)
        self.goturBeniGittiginYere()
        self.timer.start(self.remain)
        self.setCursor(QtGui.QCursor(Pix2))

    def goturBeniGittiginYere(self):
        self.timer.start(self.remain)
        self.remain -= 1
        x = random.randint(20, ctx.mainScreen.width() - 20 - self.width())
        y = random.randint(20, ctx.mainScreen.height() - 20 - self.height())
        self.move(x,y)
        if self.oldscore == self.score:
            self.score -= 10
        self.notifier.updateAndShow("Score : %d" % self.score)
        self.oldscore = self.score
        ctx.mainScreen.processEvents()

    def mouseReleaseEvent(self, event):
        self.score += 10
        self.goturBeniGittiginYere()

    def start(self):
        self.timer.start(self.remain)
        self.show()

    def stop(self):
        self.timer.stop()
        self.notifier.hide()
        self.hide()

    def show(self):
        QtGui.QWidget.show(self)
        ctx.mainScreen.processEvents()

    def hide(self):
        QtGui.QWidget.hide(self)
        ctx.mainScreen.processEvents()
