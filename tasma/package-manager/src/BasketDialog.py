#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

import string

from sets import Set as set
from qt import *
from kdecore import *
from khtml import *

import pisi
import Basket
from Icons import *

(UPDATE_BASKET, APPLY_OPERATION) = (100,101)

class SelectEventListener(DOM.EventListener):
    def __init__(self, parent):
        DOM.EventListener.__init__(self)
        self.parent = parent

    def handleEvent(self,event):
        target = event.target().nodeName().string()
        try:
            if target == "INPUT":
                inputElement = DOM.HTMLInputElement(event.target())
                name = inputElement.name().string()
                checked = inputElement.checked()
                if checked:
                    if name not in self.parent.basket.packages:
                        self.parent.basket.packages.append(str(name))
                else:
                    self.parent.basket.packages.remove(str(name))

                self.parent.updateTotals()
        except Exception, e:
            print e

class BasketDialog(QDialog):
    def __init__(self, parent, basket):
        QDialog.__init__(self,parent,str(i18n("Basket")),True)
        self.parent = parent
        self.basket = basket
        self.totalSize = 0

        self.setCaption(i18n("Basket"))

        layout = QGridLayout(self, 1, 1, 11, 6)

        self.pkgHBox = QHBox(self)
        layout.addMultiCellWidget(self.pkgHBox, 1, 1, 0, 2)

        if self.basket.state == Basket.remove_state:
            self.pkgLabel = QLabel(i18n("Selected package(s) for removal:"), self)
            self.extraLabel = QLabel(i18n("Reverse dependencies of the selected package(s) that are also going to be removed:"), self)
        elif self.basket.state == Basket.install_state:
            self.pkgLabel = QLabel(i18n("Selected package(s) for install:"), self)
            self.extraLabel = QLabel(i18n("Extra dependencies of the selected package(s) that are also going to be installed:"), self)
        elif self.basket.state == Basket.upgrade_state:
            self.pkgLabel = QLabel(i18n("Selected package(s) for upgrade:"), self)
            self.extraLabel = QLabel(i18n("Extra dependencies of the selected package(s) that are also going to be upgraded:"), self)

        layout.addWidget(self.pkgLabel, 0, 0)
        layout.addWidget(self.extraLabel, 2, 0)

        self.depHBox = QHBox(self)
        layout.addMultiCellWidget(self.depHBox, 3, 3, 0, 2)

        self.totalSizeLabel = QLabel(i18n("Total Size:"), self)
        layout.addWidget(self.totalSizeLabel, 4, 0)

        spacer = QSpacerItem(121, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer, 5, 0)

        self.updateBasketButton = QPushButton(self)
        self.updateBasketButton.setText(i18n("Update Basket"))
        self.updateBasketButton.setIconSet(loadIconSet("package"))
        layout.addWidget(self.updateBasketButton, 5, 1)

        self.applyButton = QPushButton(self)
        self.applyButton.setText(parent.operateAction.text())
        self.applyButton.setIconSet(parent.operateAction.iconSet())
        layout.addWidget(self.applyButton, 5, 2)

        self.connect(self.updateBasketButton, SIGNAL('clicked()'), self.updateBasket)
        self.connect(self.applyButton, SIGNAL('clicked()'), self.applyOperation)

        self.resize(QSize(574,503).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        # Read Css
        cssFile = file(str(locate("data","package-manager/layout.css"))).read()
        self.css = cssFile

        self.javascript = file(str(locate("data","package-manager/animation.js"))).read()

        self.pkgHtmlPart = KHTMLPart(self.pkgHBox)
        self.depHtmlPart = KHTMLPart(self.depHBox)

        self.createSelectedPackagesList()
        self.createExtraPackagesList()

        self.connect(self.pkgHtmlPart,SIGNAL("completed()"), self.registerEventListener)

    def updateBasket(self):
        self.createSelectedPackagesList()
        self.createExtraPackagesList()
        self.parent.updateStatusBar()

    def closeEvent(self, event):
        self.pkgHtmlPart = None
        self.depHtmlPart = None
        self.accept()

    def applyOperation(self):
        self.pkgHtmlPart = None
        self.depHtmlPart = None
        self.hide()
        self.done(APPLY_OPERATION)

    def registerEventListener(self):
        self.eventListener = SelectEventListener(self)
        node = self.pkgHtmlPart.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def updateTotals(self):
        self.setCursor(Qt.waitCursor)
        self.createExtraPackagesList()
        self.setCursor(Qt.arrowCursor)

    def createSelectedPackagesList(self):
        self.createHTML(self.basket.packages, self.pkgHtmlPart, True)

    def createExtraPackagesList(self):
        self.parent.basket.update()

        if self.basket.packages:
            self.applyButton.setEnabled(True)
        else:
            self.applyButton.setEnabled(False)

        if self.basket.extraPackages:
            self.extraLabel.show()
            self.depHBox.show()
            self.createHTML(self.basket.extraPackages, self.depHtmlPart, False)
        else:
            self.extraLabel.hide()
            self.depHBox.hide()

        tpl = pisi.util.human_readable_size(self.basket.getBasketSize())
        size = "%.1f %s" % (tpl[0], tpl[1])
        self.totalSizeLabel.setText(i18n("Total Size: <b>%1</b>").arg(size))

    def createHTML(self, packages, part=None, checkBox=False):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        '''

        if not part:
            part = self.htmlPart

        part.begin()
        part.write(head)
        part.write("<style type=\"text/css\">%s</style>" % self.css)
        part.write("<script language=\"JavaScript\">%s</script>" % self.javascript)
        part.write("</head><body>")
        part.write(self.createHTMLForPackages(packages, checkBox))
        part.write('''<body></html>''')
        part.end()

    def createHTMLForPackages(self, packages, checkBox):
        result = ''
        template ='''
        <!-- package start -->
        <div class="disabled">
        '''
        if checkBox:
            template += '''<div class="checkboks" style="%s"><input type="checkbox" checked name="%s"></div>'''

        template += '''
        <div class="package_title_disabled" style="%s">
        <img src="%s" style="float:left;" width="%dpx" height="%dpx">
        <b>%s</b><br><span style="color:#303030">%s%s<br>%s</span><br>
        </div></div>
        <!-- package end -->
        '''

        style = "background-color:%s" % KGlobalSettings.baseColor().name()
        packages.sort(key=string.lower)

        for app in packages:
            package = self.basket.getPackage(app)
            size = self.basket.getPackageSize(package)
            tpl = pisi.util.human_readable_size(size)
            size = "%.0f %s" % (tpl[0], tpl[1])
            iconPath = getIconPath(package.icon)
            summary = package.summary
            iconSize = getIconSize()
            if checkBox:
                result += template % (style,app,style,iconPath,iconSize,iconSize,app,i18n("Size: "),size,summary)
            else:
                result += template % (style,iconPath,iconSize,iconSize,app,i18n("Size: "),size,summary)

        return result
