#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

class DisplayItem(QtGui.QGraphicsRectItem):
    def __init__(self, scene):
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
        btn.clicked.connect(scene.swapClicked)
        btn.hide()
        proxy = QtGui.QGraphicsProxyWidget(self)
        proxy.setWidget(btn)
        self._swapButton = btn
        self._swapButtonProxy = proxy

        self.setAcceptHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        self._scene = scene
        self._outputs = []
        self._output = None
        self._pos = 0
        self._menu = None

    def contextMenuEvent(self, event):
        if self._menu is None:
            menu = QtGui.QMenu()
            actionGroup = QtGui.QActionGroup(self.scene())
            for output in self._outputs:
                action = QtGui.QAction(output, self.scene())
                action.setData(QtCore.QVariant(output))
                action.setCheckable(True)
                action.setActionGroup(actionGroup)
                if output == self._output.name:
                    action.setChecked(True)
                menu.addAction(action)
            self._menu = menu

        action = self._menu.exec_(event.screenPos())
        if action:
            selection = str(action.data().toString())
            self._scene.outputSelected.emit(self, selection)

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
        self._menu = None

        if output is None:
            self.hide()
        else:
            if pos == -1:
                self.setPos(-102, 0)
                self._swapButton.setIcon(kdeui.KIcon("arrow-right"))
                buttonRect = self._swapButtonProxy.rect()
                buttonRect.moveBottomRight(self.rect().bottomRight())
                buttonRect.adjust(-10, -10, -10, -10)
                self._swapButtonProxy.setGeometry(buttonRect)
            elif pos == 0:
                self.setPos(0, 0)
            else:
                self.setPos(102, 0)
                self._swapButton.setIcon(kdeui.KIcon("arrow-left"))
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

    outputsChanged = QtCore.pyqtSignal(str, str)
    swapClicked = QtCore.pyqtSignal()
    outputSelected = QtCore.pyqtSignal(DisplayItem, str)

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

        self._left = DisplayItem(self)
        self._right = DisplayItem(self)
        self.addItem(self._left)
        self.addItem(self._right)
        self._left.hide()
        self._right.hide()

        self.outputSelected.connect(self.slotOutputSelected)
        self.swapClicked.connect(self.slotOutputSelected)

    def updateDisplays(self):
        bRect = self.itemsBoundingRect()
        bRect.setTop(bRect.top() - 50)
        bRect.setBottom(bRect.bottom() + 50)
        bRect.setLeft(bRect.left() - 50)
        bRect.setRight(bRect.right() + 50)
        self._view.fitInView(bRect, QtCore.Qt.KeepAspectRatio)

    def slotOutputSelected(self, item=None, name=None):
        if item is None:
            self.outputsChanged.emit(self._right._output.name,
                                    self._left._output.name)
        else:
            if item._output == self._left._output:
                self.outputsChanged.emit(name, "")
            else:
                self.outputsChanged.emit("", name)

    def mouseReleaseEvent(self, mouseEvent):
        self.updateDisplays()

        QtGui.QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def setOutputs(self, allOutputs, leftOutput, rightOutput):
        self._left._outputs = []
        self._right._outputs = []

        for output in allOutputs:
            if leftOutput and output.name == leftOutput.name:
                self._left.setOutput(output, -1 if rightOutput else 0)
                self._left._outputs.append(output.name)
            elif rightOutput and output.name == rightOutput.name:
                self._right.setOutput(output, 1)
                self._right._outputs.append(output.name)
            else:
                self._left._outputs.append(output.name)
                self._right._outputs.append(output.name)

        if rightOutput is None:
            self._right.hide()
