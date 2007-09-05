#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *

from summaryDialogUI import SummaryDialogUI
from summaryWidgetUI import SummaryWidgetUI

class SummaryDialog(SummaryDialogUI):
    def __init__(self, languages, activeLanguage = None, parent = None, name = None):
        SummaryDialogUI.__init__(self, parent, name)
        self.summaries = []
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        for lang in languages:
            wdg = QWidget(self.tbLanguage)
            lo = QHBoxLayout(wdg, 6, 6)
            lo.setAutoAdd(True)
            self.tbLanguage.addItem(wdg, "Language %s:" % lang[0])
            sumWidgt = SummaryWidgetUI(wdg)
            sumWidgt.leLanguage.setText(lang[0])
            sumWidgt.leSummary.setText(lang[1])
            sumWidgt.teDescription.setText(lang[2])
            self.summaries.append(sumWidgt)
            self.connect(sumWidgt.leLanguage, SIGNAL("textChanged(const QString&)"), self.languageChanging)
            if activeLanguage:
                self.activateLangPage(languages, activeLanguage)

    def activateLangPage(self, langs, lang):
        for i, l in enumerate(langs):
            if l[0] == lang:
                self.tbLanguage.setCurrentIndex(i)
                break

    def getResult(self):
        ret = []
        for sum in self.summaries:
            l = []
            l.append(str(sum.leLanguage.text()))
            l.append(unicode(sum.leSummary.text()))
            l.append(unicode(sum.teDescription.text()))
            ret.append(l)
        return ret

    def languageChanging(self, newLang):
        self.tbLanguage.setItemLabel(self.tbLanguage.currentIndex(), "Language %s:" % newLang)
