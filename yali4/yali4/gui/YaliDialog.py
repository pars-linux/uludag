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
        self.setStyleSheet("""
            QFrame#windowTitle {background-color:#984379;color:#FFF;border:1px solid #FFF;border-radius:4px;}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.mainwidget.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.mainwidget.move(event.globalPos() - self.dragPosition)
            event.accept()

class Dialog(QtGui.QDialog):
    def __init__(self, title, widget = None, parent = None, closeButton = True, keySequence = None):
        QtGui.QDialog.__init__(self, ctx.mainScreen)

        self.gridlayout = QtGui.QGridLayout(self)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.windowTitle = windowTitle(self, closeButton)
        self.setTitle(title)
        self.gridlayout.addWidget(self.windowTitle,0,0,1,1)

        if widget:
            self.addWidget(widget)
            QObject.connect(widget, SIGNAL("finished(int)"), self.reject)

        if closeButton:
            QObject.connect(self.windowTitle.pushButton, SIGNAL("clicked()"), self.reject)

        if keySequence:
            shortCut = QtGui.QShortcut(keySequence, self)
            QObject.connect(shortCut, SIGNAL("activated()"), self.reject)

        QMetaObject.connectSlotsByName(self)

    def setTitle(self, title):
        self.windowTitle.label.setText(title)

    def addWidget(self, widget):
        self.content = widget
        self.gridlayout.addWidget(self.content,1,0,1,1)

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

class Tetris(QtGui.QFrame):
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.curPiece = Shape()
        self.nextPiece = Shape()
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

        self.nextPiece.setRandomShape()
        self._parent = parent

    def message(self, string):
        self._parent.setTitle(string)

    def shapeAt(self, x, y):
        return self.board[(y * Tetris.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Tetris.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() / Tetris.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() / Tetris.BoardHeight

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.message("Score : %s" % self.numLinesRemoved)
        self.newPiece()
        self.timer.start(Tetris.Speed, self)

    def pause(self):
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
            self.message("Paused")
        else:
            self.timer.start(Tetris.Speed, self)
            self.message("Score : %s" % self.numLinesRemoved)
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Tetris.BoardHeight * self.squareHeight()

        for i in range(Tetris.BoardHeight):
            for j in range(Tetris.BoardWidth):
                shape = self.shapeAt(j, Tetris.BoardHeight - i - 1)
                if shape != Tetrominoes.NoShape:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Tetris.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.curPiece.shape() == Tetrominoes.NoShape:
            QtGui.QWidget.keyPressEvent(self, event)
            return

        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)
        elif key == Qt.Key_Space:
            self.dropDown()
        elif key == Qt.Key_D:
            self.oneLineDown()
        else:
            QtGui.QWidget.keyPressEvent(self, event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def clearBoard(self):
        for i in range(Tetris.BoardHeight * Tetris.BoardWidth):
            self.board.append(Tetrominoes.NoShape)

    def dropDown(self):
        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        numFullLines = 0

        rowsToRemove = []

        for i in range(Tetris.BoardHeight):
            n = 0
            for j in range(Tetris.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoes.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:
            for k in range(m, Tetris.BoardHeight):
                for l in range(Tetris.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines

            self.message("Score : %s" % self.numLinesRemoved)
            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoes.NoShape)
            self.update()

    def newPiece(self):
        self.curPiece = self.nextPiece
        self.nextPiece.setRandomShape()
        self.curX = Tetris.BoardWidth / 2 + 1
        self.curY = Tetris.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetrominoes.NoShape)
            self.timer.stop()
            self.isStarted = False
            self.message("Game over")

    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            if x < 0 or x >= Tetris.BoardWidth or y < 0 or y >= Tetris.BoardHeight:
                return False
            if self.shapeAt(x, y) != Tetrominoes.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()
        return True

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QtGui.QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2, 
            self.squareHeight() - 2, color)

        painter.setPen(color.light())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.dark())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1, 
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

class Tetrominoes(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7

class Shape(object):
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Tetrominoes.NoShape

        self.setShape(Tetrominoes.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):
        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotatedLeft(self):
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotatedRight(self):
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result
