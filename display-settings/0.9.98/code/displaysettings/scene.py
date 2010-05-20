#!/usr/bin/python
# -*- coding: utf-8 -*-

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

from displaysettings.device import Output

class DisplayItem(QtGui.QGraphicsRectItem):
    def __init__(self, scene):
        QtGui.QGraphicsRectItem.__init__(self)

        self.setRect(0, 0, 260, 200)

        self.pen = QtGui.QPen(QtGui.QColor(84, 116, 138))
        self.pen.setWidth(1)
        self.setPen(self.pen)

        self.gradient = QtGui.QLinearGradient(0, 200, 50, 0)
        self.gradient.setColorAt(1, QtGui.QColor(160, 230, 255))
        self.gradient.setColorAt(0, QtGui.QColor(42, 153, 229))
        self.setBrush(self.gradient)

        self._text = QtGui.QGraphicsTextItem(self)
        font = kdeui.KGlobalSettings.generalFont()
        font.setPixelSize(48)
        self._text.setDefaultTextColor(QtGui.QColor(40, 40, 40, 255))
        self._text.setFont(font)

        btn = QtGui.QToolButton()
        btn.setIcon(kdeui.KIcon("arrow-right"))
        btn.setAutoRaise(True)
        btn.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
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
            self._scene.outputChanged.emit(self, selection)

        self.setSelected(True)

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
                self.setPos(-133, 0)
                self._swapButton.setIcon(kdeui.KIcon("arrow-right"))
                buttonRect = self._swapButtonProxy.rect()
                buttonRect.moveBottomRight(self.rect().bottomRight())
                buttonRect.adjust(-10, -10, -10, -10)
                self._swapButtonProxy.setGeometry(buttonRect)
            elif pos == 0:
                self.setPos(0, 0)
            else:
                self.setPos(133, 0)
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

        font = self._text.font()
        size = 48
        while textRect.width() > itemRect.width():
            size -= 8
            if size < 0:
                break
            font.setPixelSize(size)
            self._text.setFont(font)
            textRect = self._text.boundingRect()

        textRect.moveCenter(itemRect.center())
        self._text.setPos(textRect.left(), textRect.top())


class DisplayScene(QtGui.QGraphicsScene):

    outputsChanged = QtCore.pyqtSignal(str, str)
    swapClicked = QtCore.pyqtSignal()
    outputChanged = QtCore.pyqtSignal(DisplayItem, str)
    outputSelected = QtCore.pyqtSignal(Output)

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
        self._left.setSelected(True)

        self._selectedItem = self._left

        self.outputChanged.connect(self.slotOutputChanged)
        self.swapClicked.connect(self.slotOutputChanged)
        self.selectionChanged.connect(self.slotSelectionChanged)

    def updateDisplays(self):
        bRect = self.itemsBoundingRect()
        bRect.setTop(bRect.top() - 50)
        bRect.setBottom(bRect.bottom() + 50)
        bRect.setLeft(bRect.left() - 30)
        bRect.setRight(bRect.right() + 30)
        self._view.fitInView(bRect, QtCore.Qt.KeepAspectRatio)

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

        #self.selectionChanged.emit()

    def slotOutputChanged(self, item=None, name=None):
        if item is None:
            self.outputsChanged.emit(self._right._output.name,
                                    self._left._output.name)

        elif item._output == self._left._output:
            self.outputsChanged.emit(name, "")
        else:
            self.outputsChanged.emit("", name)

    def slotSelectionChanged(self):
        items = self.selectedItems()
        if items:
            selected = items.pop(-1)
            for item in items:
                item.setSelected(False)

            self._selectedItem = selected
            self.outputSelected.emit(selected._output)

    def selectedOutput(self):
        return self._selectedItem._output
