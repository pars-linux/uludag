#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from PyQt4.QtGui import *
from PyQt4.QtCore import QUrl

from PyKDE4.kdecore import *

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        self.setWindowIcon(QIcon(":/icons/help.png"))
        self.setWindowTitle(i18n("Information"))
        self.layout = QGridLayout(self)
        self.htmlpart = QTextBrowser(self)
        self.resize(500, 300)
        self.layout.addWidget(self.htmlpart, 0, 0)
        self.lang_code = os.environ['LANG'][:5].split('_')[0].lower()

        if os.path.isfile(KStandardDirs.locate("data", ("history-manager/help/%s/main_help.html" % self.lang_code))):
            self.htmlpart.setSource(QUrl(KStandardDirs.locate('data', 'history-manager/help/%s/main_help.html'%self.lang_code)))
        else:
            self.htmlpart.setSource(QUrl(KStandardDirs.locate('data', 'history-manager/help/en/main_help.html')))
