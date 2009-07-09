#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

class DisplayItem(QtGui.QGraphicsRectItem):
    def __init__(self):
        QtGui.QGraphicsRectItem.__init__(self)

        self.setRect(0, 0, 200, 200)
        self.setPen(QtGui.QPen(QtCore.Qt.black))
        self.setBrush(QtGui.QColor(0, 255, 0, 128))

        self._text = QtGui.QGraphicsTextItem(self)
        font = kdeui.KGlobalSettings.generalFont()
        font.setPixelSize(48)
        self._text.setFont(font)

        btn = QtGui.QToolButton()
        btn.setIcon(kdeui.KIcon("arrow-right"))
        btn.setAutoRaise(True)
        btn.hide()
        proxy = QtGui.QGraphicsProxyWidget(self)
        proxy.setWidget(btn)
        self._swapButtonProxy = proxy

        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        self._outputs = []
        self._output = None
        self._pos = 0

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        for output in self._outputs:
            menu.addAction(output)

        menu.exec_(event.screenPos())

    def hoverEnterEvent(self, event):
        if self._pos != 0:
            self._swapButtonProxy.show()
        QtGui.QGraphicsRectItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        if self._pos != 0:
            self._swapButtonProxy.hide()
        QtGui.QGraphicsRectItem.hoverLeaveEvent(self, event)

    def setOutput(self, output, pos):
        self._output = output
        self._pos = pos

        if output is None:
            self.hide()
        else:
            if pos == -1:
                self.setPos(-102, 0)
                buttonRect = self._swapButtonProxy.rect()
                buttonRect.moveBottomRight(self.rect().bottomRight())
                buttonRect.adjust(-10, -10, -10, -10)
                self._swapButtonProxy.setGeometry(buttonRect)
            elif pos == 0:
                self.setPos(0, 0)
            else:
                self.setPos(102, 0)
                buttonRect = self._swapButtonProxy.rect()
                buttonRect.moveBottomLeft(self.rect().bottomLeft())
                buttonRect.adjust(10, -10, 10, -10)
                self._swapButtonProxy.setGeometry(buttonRect)

            self.__setText(output.name)
            self.show()

    def __setText(self, text):
        self._text.setPlainText(text)
        textRect = self._text.boundingRect()
        itemRect = self.rect()
        textRect.moveCenter(itemRect.center())
        self._text.setPos(textRect.left(), textRect.top())


class DisplayScene(QtGui.QGraphicsScene):
    def __init__(self, view, parent = None):
        QtGui.QGraphicsScene.__init__(self, parent)

        def resizeEvent(event):
            self.updateDisplays()
            QtGui.QGraphicsView.resizeEvent(view, event)

        view.setScene(self)
        hints = QtGui.QPainter.TextAntialiasing \
                | QtGui.QPainter.SmoothPixmapTransform
        view.setRenderHints(hints)
        view.resizeEvent = resizeEvent
        self._view = view

        self._left = DisplayItem()
        self._right = DisplayItem()
        self.addItem(self._left)
        self.addItem(self._right)
        self._left.hide()
        self._right.hide()

    def updateDisplays(self):
        bRect = self.itemsBoundingRect()
        bRect.setTop(bRect.top() - 50)
        bRect.setBottom(bRect.bottom() + 50)
        bRect.setLeft(bRect.left() - 50)
        bRect.setRight(bRect.right() + 50)
        self._view.fitInView(bRect, QtCore.Qt.KeepAspectRatio)

    def mouseReleaseEvent(self, mouseEvent):
        self.updateDisplays()

        QtGui.QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def setOutputs(self, allOutputs, leftOutputName, rightOutputName):
        self._left._outputs = []
        self._right._outputs = []

        for output in allOutputs:
            if output.name == leftOutputName:
                self._left.setOutput(output, -1 if rightOutputName else 0)
                self._left._outputs.append(output.name)
            elif output.name == rightOutputName:
                self._right.setOutput(output, 1)
                self._right._outputs.append(output.name)
            else:
                self._left._outputs.append(output.name)
                self._right._outputs.append(output.name)
