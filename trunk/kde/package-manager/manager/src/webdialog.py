#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from pds.gui import *
from pmutils import *

from ui_webdialog import Ui_WebDialog
from pds.qprogressindicator import QProgressIndicator

class WebDialog(PAbstractBox, Ui_WebDialog):
    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)
        self.setupUi(self)

        # PDS Settings
        self._animation = 1
        self._duration = 400
        self.enableOverlay()
        self._disable_parent_in_shown = True

        self.registerFunction(IN, lambda: parent.statusBar().hide())
        self.registerFunction(FINISHED, lambda: parent.statusBar().setVisible(not self.isVisible()))
        self._as = 'http://appinfo.pardus.org.tr'
        self.cancelButton.clicked.connect(self._hide)

        # Hide Scrollbars and context menu in webview
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)

        self.tabWidget.removeTab(0)

        self.busy = QProgressIndicator(self, "white")
        self.busy.setMaximumSize(QSize(48, 48))
        self.webLayout.addWidget(self.busy)
        self.busy.hide()

        self.noconnection.hide()

    def showPage(self, addr):
        self.webView.load(QUrl(addr))
        self.animate(start = BOTCENTER, stop = MIDCENTER)

    def _sync_template(self, status, package, summary, description):
        def _replace(key, value):
            self.webView.page().mainFrame().evaluateJavaScript(\
                    '%s.innerHTML="%s";' % (key, value))

        self.busy.hide()
        self.busy.stopAnimation()

        if status:
            _replace('title', package)
            _replace('summary', summary)
            _replace('description', description)
            self.webView.show()
            self.noconnection.hide()
        else:
            self.noconnection.show()
            self.webView.hide()

    def showPackageDetails(self, package, summary='', description='', files=[]):
        self.packageName.setText(package)

        self.webView.hide()
        self.busy.show()
        self.busy.startAnimation()

        self.webView.load(QUrl('%s/?p=%s' % (self._as, package)))
        self.webView.loadFinished.connect(lambda x: \
                self._sync_template(x, package, summary, description))

        self.tabWidget.insertTab(0, self.filesList, i18n('Package Files'))
        if files:
            print files
        else:
            self.tabWidget.removeTab(0)

        self.animate(start = BOTCENTER, stop = MIDCENTER)

    def _hide(self):
        self.busy.stopAnimation()
        self.webView.loadFinished.disconnect()
        self.animate(start = MIDCENTER, stop = BOTCENTER, direction = OUT)

