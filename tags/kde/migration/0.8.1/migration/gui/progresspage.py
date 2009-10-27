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
        lay = QVBoxLayout(self, 11, 6, "lay")
        # Top Label:
        self.label = QLabel(self, "label")
        self.label.setText(i18n("Please wait while applying changes..."))
        self.label.setAlignment(self.label.alignment() | Qt.WordBreak)
        lay.addWidget(self.label)
        # Progress Bar Grid Layout:
        progresslay = QGridLayout(None, 1, 1, 15, 5, "progresslay")
        lay.addLayout(progresslay)
        # Progress 1:
        self.label1 = QLabel(self, "label1")
        self.label1.setText(i18n("Prepare: "))
        progresslay.addWidget(self.label1, 0, 0)
        self.progressbar1 = QProgressBar(self, "progressbar1")
        progresslay.addWidget(self.progressbar1, 0, 1)
        # Progress 2:
        self.label2 = QLabel(self, "label2")
        self.label2.setText(i18n("Apply: "))
        progresslay.addWidget(self.label2, 1, 0)
        self.progressbar2 = QProgressBar(self, "progressbar2")
        progresslay.addWidget(self.progressbar2, 1, 1)
        ## Status Label:
        #self.statuslabel = QLabel(self, "statuslabel")
        #self.statuslabel.setText(i18n("Status: "))
        #self.statuslabel.setAlignment(self.label.alignment() | Qt.WordBreak)
        #lay.addWidget(self.statuslabel)
        # Operation Lines:
        self.oplines = QVBoxLayout(None, 0, 0, "oplines")
        lay.addLayout(self.oplines)
        # Spacer:
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lay.addItem(spacer)
        # Progress Variables:
        self.steps1 = 0
        self.steps2 = 0
        self.progress1 = 0
        self.progress2 = 0
        self.active = 0
        self.operations = []
        self.updateProgress()
    
    def updateProgress(self):
        "Updates status of progress bars"
        if self.steps1 == 0:
            self.progressbar1.setProgress(0)
        else:
            self.progressbar1.setProgress(100 * self.progress1 / self.steps1)
        if self.steps2 == 0:
            self.progressbar2.setProgress(0)
        else:
            self.progressbar2.setProgress(100 * self.progress2 / self.steps2)
    
    def addProgress(self, number, bar=1):
        "Adds steps to progress bars"
        if bar == 1:
            self.steps1 += number
        else:
            self.steps2 += number
        self.updateProgress()
    
    def makeProgress(self, number, bar=1):
        "Makes progress bar step"
        if bar == 1:
            self.progress1 += number
        else:
            self.progress2 += number
        self.updateProgress()
    
    def addOperation(self, name, steps):
        "Adds a new operation to the progress page"
        op = Operation(self, name, steps)
        self.oplines.addLayout(op)
        self.operations.append(op)
        self.steps2 += steps
    
    def customEvent(self, event):
        # Show Warning Box:
        if event.type() == 65456:
            self.warning = QMessageBox.warning(self, i18n("Warning!"), event.message, QMessageBox.Ok, QMessageBox.Cancel, QMessageBox.NoButton)
    
    def go(self, log, stat, steps):
        "increments progressbar, logs changes and modify icons"
        activeop = self.operations[self.active]
        if activeop.progress + steps > activeop.steps:
            self.makeProgress(activeop.steps - activeop.progress, 2)
        else:
            self.makeProgress(steps, 2)
        if activeop.go(log, stat, steps):
            self.active += 1
            if self.active < len(self.operations):
                self.operations[self.active].start()
            else:
                self.active -= 1


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
            if log:
                print i18n("OK:"), log
            self.OKs += 1
        elif stat == ProgressPage.WARNING:
            if log:
                print i18n("WARNING:"), log
            self.warnings += 1
        elif stat == ProgressPage.ERROR:
            if log:
                print i18n("ERROR:"), log.__class__, "(", log.__doc__, ") :", log
            self.errors += 1
        if self.progress >= self.steps:
            if self.errors > 0:
                pix = KGlobal.iconLoader().loadIcon("cancel", KIcon.Toolbar)
            elif self.warnings > 0:
                pix = KGlobal.iconLoader().loadIcon("messagebox_warning", KIcon.Toolbar)
            else:
                pix = KGlobal.iconLoader().loadIcon("apply", KIcon.Toolbar)
            self.icon.setPixmap(pix)
            return True
        else:
            return False



