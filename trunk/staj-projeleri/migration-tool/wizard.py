# -*- coding: utf-8 -*-

from qt import *

from user import *
from modules import *
from options import *

class Wizard(QWizard):
    def __init__(self):
        QWizard.__init__(self)
        self.resize(620, 420)
        self.setCaption(u"Pardus Göç Aracı")
        self.setTitleFont(QFont("DejaVu Sans", 12, QFont.Bold))
        
        # Generate UI
        self.userpage = UserWidget(self)
        self.addPage(self.userpage, u"1. Kullanıcının Seçilmesi")
        
        self.lastpage = QWidget(self)
        self.lastpage.layout = QVBoxLayout(self.lastpage)
        self.addPage(self.lastpage, u"3. Değişikliklerin Uygulanması")
        
        self.setHelpEnabled(self.userpage, False)
        self.setHelpEnabled(self.lastpage, False)
        self.setFinishEnabled(self.lastpage, False)
    
    def next(self):
        if self.currentPage() == self.userpage:
            user = self.userpage.users[self.userpage.usersBox.currentItem()]
            part, parttype, username, userdir = user
            self.migration = UserMigration(part, parttype, userdir)
            self.settingspage = Options(self.migration.sources)
            self.insertPage(self.settingspage, u"2. Ayarların Seçilmesi",1)
            self.setHelpEnabled(self.settingspage, False)

        
        # Ayarlar sayfasindaki seceneklere bakip options sozlugunu olustur:
        elif self.currentPage() == self.settingspage:
            self.migration.options = self.settingspage.options
            self.migration.migrate()
            self.setFinishEnabled(self.lastpage, True)
        
        QWizard.next(self)