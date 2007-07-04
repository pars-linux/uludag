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
from progress_ui import *
from modules import *
from options import *

class Wizard(QWizard):
    def __init__(self):
        QWizard.__init__(self)
        self.resize(620, 420)
        self.setCaption(u"Pardus Göç Aracı")
        self.setTitleFont(QFont("DejaVu Sans", 12, QFont.Bold))
        # User page:
        self.userpage = UserWidget(self)
        self.addPage(self.userpage, u"1. Kullanıcının Seçilmesi")
        # Empty settings page:
        self.settingspage = QWidget(self)
        self.addPage(self.settingspage, u"2. Ayarların Seçilmesi")
        self.setHelpEnabled(self.settingspage, False)
        # Progress page:
        self.progresspage = ProgressWidget(self)
        self.addPage(self.progresspage, u"3. Değişikliklerin Uygulanması")
        
        self.setHelpEnabled(self.userpage, False)
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
            QWizard.next(self)
        
        # Get options from widget and apply changes
        elif self.currentPage() == self.settingspage:
            # Prepare for migration:
            QWizard.next(self)
            self.setFinishEnabled(self.progresspage, False)
            options, steps = self.settingspage.getOptionsSteps()
            self.migration.options = options
            self.progresspage.text.setText(u"Değişiklikler yapılırken lütfen bekleyiniz...")
            self.progresspage.bar.setTotalSteps(steps)
            self.progresspage.bar.setProgress(0)
            self.progresspage.log.clear()
            self.warning = False
            # Migrate user and display progress:
            def printwarning(text):
                self.progresspage.log.append("<b>WARNING: </b>" + text)
                self.progresspage.bar.setProgress(self.progresspage.bar.progress() + 1)
                self.warning = True
            def printlog(text):
                self.progresspage.log.append(text)
                self.progresspage.bar.setProgress(self.progresspage.bar.progress() + 1)
            self.migration.migrate(printwarning, printlog)
            # Finish:
            self.setFinishEnabled(self.progresspage, True)
            if steps == 0:
                self.progresspage.text.setText(u"Hiçbir değişiklik seçilmediği için işlem yapılmadı. Programdan çıkabilirsiniz...")
            elif self.warning:
                self.progresspage.text.setText(u"Değişiklikler yapıldı. Ancak bazı uyarılar var. Uyarılara göz atıp programdan çıkabilirsiniz...")
            else:
                self.progresspage.text.setText(u"İstenen tüm değişiklikler başarıyla yapıldı. Programdan çıkabilirsiniz...")
