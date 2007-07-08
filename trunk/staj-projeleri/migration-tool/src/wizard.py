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

from qt import *

from user import *
from modules import *
from options import *
from files import *
from progress_ui import *

class Wizard(QWizard):
    def __init__(self):
        QWizard.__init__(self)
        self.resize(620, 420)
        self.setCaption(u"Pardus Göç Aracı")
        self.setTitleFont(QFont("DejaVu Sans", 12, QFont.Bold))
        # User page:
        self.userpage = UserWidget(self)
        self.addPage(self.userpage, u"1. Kullanıcının Seçilmesi")
        self.setHelpEnabled(self.userpage, False)
        # Empty settings page:
        self.settingspage = QWidget(self)
        self.addPage(self.settingspage, u"2. Ayarların Seçilmesi")
        self.setHelpEnabled(self.settingspage, False)
        # Empty files page:
        self.filespage = QWidget(self)
        self.addPage(self.filespage, u"3. Dosyaların Seçilmesi")
        self.setHelpEnabled(self.filespage, False)
        # Progress page:
        self.progresspage = ProgressWidget(self)
        self.addPage(self.progresspage, u"4. Değişikliklerin Uygulanması")
        self.setHelpEnabled(self.progresspage, False)
    
    def next(self):
        if self.currentPage() == self.userpage:
            # Get user and collect information:
            user = self.userpage.users[self.userpage.usersBox.currentItem()]
            part, parttype, username, userdir = user
            self.migration = UserMigration(part, parttype, userdir)
            # Update old settings page with the new one:
            self.removePage(self.settingspage)
            self.settingspage = Options(self.migration.sources, self.migration.destinations)
            self.insertPage(self.settingspage, u"2. Ayarların Seçilmesi", 1)
            self.setHelpEnabled(self.settingspage, False)
            # Update old files page with the new one:
            self.removePage(self.filespage)
            self.filespage = FilesPage(self, self.migration.sources, self.migration.destinations)
            self.insertPage(self.filespage, u"3. Dosyaların Seçilmesi", 2)
            self.setHelpEnabled(self.filespage, False)
            
            QWizard.next(self)
        
        # Get options from widget and apply changes
        elif self.currentPage() == self.settingspage:
            QWizard.next(self)
        
        elif self.currentPage() == self.filespage:
            # Check Options:
            options, steps = self.settingspage.getOptionsSteps()
            self.migration.options = options
            # Check Files:
            filesteps = self.filespage.steps()
            if filesteps < 0:
                return
            else:
                steps += filesteps
            # Prepare for migration:
            QWizard.next(self)
            self.setFinishEnabled(self.progresspage, False)
            self.applythread = ApplyThread(self)
            self.applythread.steps = steps
            self.applythread.start()
            self.setFinishEnabled(self.progresspage, True)

class ApplyThread(QThread):
    def __init__(self, wizard):
        QThread.__init__(self)
        self._wizard = wizard
    def run(self):
        # Progress page configuration:
        self._wizard.progresspage.text.setText(u"Değişiklikler yapılırken lütfen bekleyiniz...")
        self.progress = 0
        self.updateProgress()
        self._wizard.progresspage.log.clear()
        self._wizard.warning = False
        def printwarning(text, steps):
            self._wizard.progresspage.log.append("<b>WARNING:</b> %s" % text)
            self.progress += steps
            self.updateProgress()
            self._wizard.warning = True
        def printlog(text, steps):
            self._wizard.progresspage.log.append(text)
            self.progress += steps
            self.updateProgress()
        # Migrate Settings:
        self._wizard.migration.migrate(printwarning, printlog)
        # Migrate Files:
        self._wizard.filespage.migrate(printwarning, printlog)
        if self.steps == 0:
            self._wizard.progresspage.text.setText(u"Hiçbir değişiklik seçilmediği için işlem yapılmadı. Programdan çıkabilirsiniz...")
        elif self._wizard.warning:
            self._wizard.progresspage.text.setText(u"Değişiklikler yapıldı. Ancak bazı uyarılar var. Uyarılara göz atıp programdan çıkabilirsiniz...")
        else:
            self._wizard.progresspage.text.setText(u"İstenen tüm değişiklikler başarıyla yapıldı. Programdan çıkabilirsiniz...")
        self.updateProgress()
    def updateProgress(self):
        if self.steps:
            self._wizard.progresspage.bar.setProgress(self.progress * 100 / self.steps)
        else:
            self._wizard.progresspage.bar.setProgress(0)
