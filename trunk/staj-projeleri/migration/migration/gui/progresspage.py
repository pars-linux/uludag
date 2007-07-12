#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *


class ProgressPage(QWidget):
    OK, WARNING, ERROR = xrange(3)
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.lay = QVBoxLayout(self, 11, 6, "lay")
        
        self.label = QLabel(self, "label")
        self.label.setText(i18n("Please wait while applying changes..."))
        self.label.setAlignment(self.label.alignment() | Qt.WordBreak)
        self.lay.addWidget(self.label)
        
        self.progress = 0
        self.steps = 0
        self.progressbar = QProgressBar(self)
        self.progressbar.setProgress(0)
        self.lay.addWidget(self.progressbar)
        
        #self.progresslist = QListBox(self)
        #self.lay.addWidget(self.progresslist)
        #self.progresslist.setSelectionMode(QListBox.NoSelection)
        
        self.operations = []
        self.warning = False
        self.log = []
        self.active = -1
        self.oplay = QVBoxLayout(None)
        self.lay.addLayout(self.oplay)
        
        self.spacer = QSpacerItem(1,1,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.lay.addItem(self.spacer)
        self.log = QTextEdit(self,"log")
        self.log.setTextFormat(QTextEdit.LogText)
        self.log.hide()
        self.lay.addWidget(self.log)
        self.detailsButton = QCheckBox(i18n("Click here to see details..."), self, "deneme")
        self.detailsButton.hide()
        self.lay.addWidget(self.detailsButton)
        self.connect(self.detailsButton, SIGNAL("toggled(bool)"), self.log, SLOT("setShown(bool)"))
    
    def addOperation(self, name, steps):
        "adds a new operation to the process page"
        op = Operation(self, name, steps)
        self.oplay.addLayout(op)
        self.operations.append(op)
        self.operations[0].start()
        self.steps += steps
        self.active = 0
    
    def go(self, log, stat, steps):
        "increments progressbar, logs changes and modify icons"
        self.progress += steps
        if self.steps:
            self.progressbar.setProgress(100 * self.progress / self.steps)
        if stat == ProgressPage.WARNING:
            self.warning = True
        activeop = self.operations[self.active]
        if stat == ProgressPage.OK:
            self.log.append(log)
        elif stat == ProgressPage.WARNING:
            self.log.append(unicode(i18n("<b>WARNING: %s</b>")) % log)
        elif stat == ProgressPage.ERROR:
            self.log.append(unicode(i18n("<b>ERROR: %s</b>")) % log)
        if activeop.go(log, stat, steps):
            self.active += 1
            if self.active < len(self.operations):
                self.operations[self.active].start()
            else:
                self.detailsButton.show()


class Operation(QHBoxLayout):
    def __init__(self, parent, title, steps):
        QHBoxLayout.__init__(self, None)
        self.title = title
        self.steps = steps
        self.mother = parent
        self.progress = 0
        self.warnings = 0
        self.errors = 0
        self.OKs = 0
        self.icon = QLabel(parent)
        self.icon.show()
        self.icon.setMinimumSize(QSize(30, 30))
        self.icon.setMaximumSize(QSize(30, 30))
        self.addWidget(self.icon)
        self.text = QLabel(parent)
        self.text.setText(title)
        self.text.show()
        self.addWidget(self.text)
    
    def start(self):
        pix = KGlobal.iconLoader().loadIcon("1rightarrow", KIcon.Toolbar)
        self.icon.setPixmap(pix)
    
    def go(self, log, stat, steps):
        self.progress += steps
        if stat == ProgressPage.OK:
            self.OKs += 1
        elif stat == ProgressPage.WARNING:
            self.warnings += 1
        elif stat == ProgressPage.ERROR:
            self.errors += 1
        if self.progress >= self.steps:
            if self.errors > 0:
                pix = KGlobal.iconLoader().loadIcon("cancel", KIcon.Toolbar)
            elif self.warnings > 0:
                pix = KGlobal.iconLoader().loadIcon("messagebox_warning", KIcon.Toolbar)
            else:
                pix = KGlobal.iconLoader().loadIcon("apply", KIcon.Toolbar)
                #self.detailsButton.setText("deneme")
            self.icon.setPixmap(pix)
            return True
        else:
            return False
