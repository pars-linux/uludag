#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Original code belongs to Kopete licensed under GPL v2

from qt import *
from kdeui import *
from kdecore import *

from subprocess import *

class KopeteBalloon(QWidget):
    def __init__(self,parent,text,pix):
        QWidget.__init__(self,None,"KopeteBalloon", Qt.WStyle_StaysOnTop | Qt.WStyle_Customize | Qt.WStyle_NoBorder | Qt.WStyle_Tool | Qt.WX11BypassWM)
        self.parent = parent

        self.setCaption("")
        self.mAnchor = QPoint()
        BalloonLayout = QVBoxLayout(self, 22, KDialog.spacingHint(), "BalloonLayout")

        # BEGIN Layout1
        Layout1 = QHBoxLayout(BalloonLayout, KDialog.spacingHint(), "Layout1")
        self.mCaption = KActiveLabel(text, self, "mCaption");
        self.mCaption.setPalette(QToolTip.palette())
        self.mCaption.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Minimum );

        if pix:
            mImage = QLabel(self,"mImage")
            mImage.setScaledContents(False);
            mImage.setPixmap(pix)
            Layout1.addWidget(mImage)

        Layout1.addWidget(self.mCaption)
        # END Layout1


        # BEGIN Layout2
        Layout2 = QHBoxLayout(BalloonLayout, KDialog.spacingHint(), "Layout2")
        self.mViewButton = QPushButton(i18n("Show Updates"), self, "mViewButton")
        self.mIgnoreButton = QPushButton(i18n("Ignore"), self, "mIgnoreButton")

        self.connect(self.mIgnoreButton,SIGNAL("clicked()"),self.parent.hide)
        self.connect(self.mViewButton,SIGNAL("clicked()"),self.startPackageManager)

        Layout2.addStretch()
        Layout2.addWidget(self.mViewButton)
        Layout2.addWidget(self.mIgnoreButton)
        Layout2.addStretch()
        # END Layout2

        self.setPalette(QToolTip.palette())
        self.setAutoMask(True)

        #self.connect(self.mViewButton, SIGNAL("clicked()"),SIGNAL("signalButtonClicked()"))
        self.connect(self.mViewButton, SIGNAL("clicked()"),self.deleteLater)
        #self.connect(self.mIgnoreButton, SIGNAL("clicked()"),SIGNAL("signalIgnoreButtonClicked()"))
        self.connect(self.mIgnoreButton, SIGNAL("clicked()"),self.deleteLater)

    def setAnchor(self,anchor):
        self.mAnchor = anchor
        self.updateMask()

    def updateMask(self):
        mask = QRegion(10, 10, self.width() - 20, self.height() - 20)

        corners = [
            QPoint(self.width() - 50, 10),
            QPoint(10, 10),
            QPoint(10, self.height() - 50),
            QPoint(self.width() - 50, self.height() - 50),
            QPoint(self.width() - 10, 10),
            QPoint(10, 10),
            QPoint(10, self.height() - 10),
            QPoint(self.width() - 10, self.height() - 10)
            ]

        for i in range (0,4):
            corner = QPointArray()
            corner.makeArc(corners[i].x(), corners[i].y(), 40, 40, i * 16 * 90, 16 * 90)
            corner.resize(corner.size() + 1)
            corner.setPoint(corner.size() - 1, corners[i + 4])
            mask -= QRegion(corner)

        # get screen-geometry for screen our anchor is on
        # (geometry can differ from screen to screen!
        deskRect = QRect(KGlobalSettings.desktopGeometry(self.mAnchor))

        bottom = (self.mAnchor.y() + self.height()) > ((deskRect.y() + deskRect.height()-48));
        right = (self.mAnchor.x() + self.width()) > ((deskRect.x() + deskRect.width()-48));

        arrow = QPointArray(4)
        if right:
            if bottom:
                arrow.setPoint(0, QPoint(self.width(), self.height()))
                arrow.setPoint(1, QPoint(self.width() - 10, self.height() - 30))
                arrow.setPoint(2, QPoint(self.width() - 30, self.height() - 10))
            else:
                arrow.setPoint(0, QPoint(self.width() , 0))
                arrow.setPoint(1, QPoint(self.width() - 10,30))
                arrow.setPoint(2, QPoint(self.width() - 30,10))
        else:
            if bottom:
                arrow.setPoint(0, QPoint(0, self.height()))
                arrow.setPoint(1, QPoint(10, self.height() - 30))
                arrow.setPoint(2, QPoint(30, self.height() - 10))
            else:
                arrow.setPoint(0, QPoint(0,0))
                arrow.setPoint(1, QPoint(10,30))
                arrow.setPoint(2, QPoint(30,10))

        point = QPoint(arrow.point(0)[0],arrow.point(0)[1])
        arrow.setPoint(3, point)
        mask += QRegion(arrow)
        self.setMask(mask);

        if right:
            if bottom:
                self.move(self.mAnchor.x() - self.width(), self.mAnchor.y() - self.height())
            else:
                if self.mAnchor.y() < 0:
                    self.move(self.mAnchor.x() - self.width(), 0)
                else:
                    self.move(self.mAnchor.x() - self.width(), self.mAnchor.y())
        else:
            if bottom:
                if self.mAnchor.x() < 0:
                    self.move(0, self.mAnchor.y() - self.height())
                else:
                    self.move(self.mAnchor.x(), self.mAnchor.y() - self.height())
            else:
                if self.mAnchor.x() < 0:
                    if self.mAnchor.y() < 0:
                        self.move(0,0)
                    else:
                        self.move(0,self.mAnchor.y())
                else:
                    if self.mAnchor.y() < 0:
                        self.move(self.mAnchor.x(),0)
                    else:
                        self.move(self.mAnchor.x(),self.mAnchor.y())

    def startPackageManager(self):
        Popen(["package-manager","--showupdates"])
        self.parent.hide()
