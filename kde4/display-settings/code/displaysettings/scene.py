#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4 import QtGui

class DisplayItem(QtGui.QGraphicsPolygonItem):
    def __init__(self, offset):
        QtGui.QGraphicsPolygonItem.__init__(self)

        self.myPolygon = QtGui.QPolygonF()
        points = ((-100, -100),
                  ( 100, -100),
                  ( 100,  100),
                  (-100,  100),
                  (-100, -100))

        for point in points:
            self.myPolygon.append(QtCore.QPointF(point[0] + offset, point[1]))

        self.setPolygon(self.myPolygon)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

class DisplayScene(QtGui.QGraphicsScene):
    def __init__(self, view, parent = None):
        QtGui.QGraphicsScene.__init__(self, parent)

        def resizeEvent(event):
            self.updateDisplays()
            QtGui.QGraphicsView.resizeEvent(view, event)

        view.setScene(self)
        view.resizeEvent = resizeEvent
        self._view = view

        item = DisplayItem(-102)
        item2 = DisplayItem(+102)
        self.addItem(item)
        self.addItem(item2)

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
