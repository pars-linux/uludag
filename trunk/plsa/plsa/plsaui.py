#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard Python Modules
import sys
import time

# QT Modules
from qt import *
import kdedesigner

# PLSA Modules
from plsa import *

# Forms
from mainform import mainform

class multilang_text(QWidget):
    def __init__(self, parent = None, name = None):
        QWidget.__init__(self, parent, name)

        multilang_textLayout = QGridLayout(self, 1, 3, 0, 5, "multilang_textLayout")

        self.lineLang = QLineEdit(self, "lineLang")
        self.lineLang.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed, 0, 0, self.lineLang.sizePolicy().hasHeightForWidth()))
        self.lineLang.setMinimumSize(QSize(25,21))
        self.lineLang.setMaximumSize(QSize(25,21))
        multilang_textLayout.addWidget(self.lineLang, 0, 0)

        self.lineText = QLineEdit(self, "lineText")
        multilang_textLayout.addWidget(self.lineText, 0, 1)

        self.pushAddRemove = QPushButton(self, "pushAddRemove")
        self.pushAddRemove.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed, 0, 0, self.pushAddRemove.sizePolicy().hasHeightForWidth()))
        self.pushAddRemove.setMinimumSize(QSize(20,20))
        self.pushAddRemove.setMaximumSize(QSize(20,20))
        multilang_textLayout.addWidget(self.pushAddRemove, 0, 2)

        self.setMode("new")

        # Signals
        QObject.connect(self.pushAddRemove, SIGNAL("clicked()"), self.slotAddRemove)
        QObject.connect(self.lineLang, SIGNAL("lostFocus()"), self.slotSave)
        QObject.connect(self.lineText, SIGNAL("lostFocus()"), self.slotSave)

        self.clearWState(Qt.WState_Polished)
        self.show()

    def setMode(self, mode):
        self.mode = mode
        if mode == "new":
            self.pushAddRemove.setText("\xbb")
        elif mode == "remove":
            self.pushAddRemove.setText("x")

    def getMode(self):
        return self.mode

    def setLang(self, lang):
        self.lineLang.setText(lang)

    def getLang(self):
        return str(self.lineLang.text())

    def setText(self, text):
        self.lineText.setText(text)

    def getText(self):
        return str(self.lineText.text())

    def slotAddRemove(self):
        if self.parent().slotAddRemove:
            self.parent().slotAddRemove(self)

    def slotSave(self):
        if not self.getLang():
            return

        parent = self.parent()

        if parent.name().startswith("adv"):
            # If member of advisory details box
            item = w.listAdvisories.selectedItem()
            save_list = {"advtitle": item.node.title,
                         "advsummary": item.node.summary,
                         "advdescription": item.node.description}

            if parent.name() in save_list:
                node = save_list[parent.name()]
                if self.getText():
                    node[self.getLang()] = self.getText()
                elif self.getLang() in node:
                    del node[self.getLang()]
        else:
            # Else (if it's advisory title)
            if self.getText():
                w.plsa.title[self.getLang()] = self.getText()
            elif self.getLang() in w.plsa.title:
                del w.plsa.title[self.getLang()]

class multilang(QVBox):
    def __init__(self, parent = None, name = None):
        QVBox.__init__(self, parent, name)

        self.layout().setSpacing(6)

        self.languages = []
        self.clear()

    def addLang(self, lng=""):
        ord = len(self.languages)
        lang = multilang_text(self, str(ord))

        if lng:
            lang.setLang(lng)

        if len(self.languages):
            last = self.languages[-1]
            last.setMode("remove")

        self.languages.append(lang)
        return lang

    def removeLang(self, item):
        self.languages.remove(item)
        self.removeChild(item)

        last = self.languages[-1]
        last.setMode("new")

    def clear(self):
        for i in self.languages:
            self.removeChild(i)
        self.languages = []

    def getLanguages(self):
        langs = {}
        for item in self.languages:
            if item.getLang():
                langs[item.getLang()] = item.getText()

        return langs

    def slotAddRemove(self, item):
        if item.getMode() == "new":
            x = self.addLang()
        else:
            self.removeLang(item)

    def resizeEvent(self, qr):
        parent = self.parent()
        height = parent.insideSpacing() + parent.insideMargin() * 2 + self.height()
        parent.setMinimumSize(QSize(250, height))

class loadxml_thread(QThread):
    def run(self):
        w.progress.show()
        w.progress.setProgress(0)

        w.plsa = PLSAFile(w.xml)

        for lang in w.plsa.title:
            x = w.titles.addLang(lang)
            x.setText(unicode(w.plsa.title[lang]))

        inc = 1
        total = len(w.plsa.advisories)
        for adv in w.plsa.advisories:
            item = QListViewItem(w.listAdvisories, None)
            item.setText(0, adv.id)
            item.setText(1, adv.title["en"])
            item.node = adv
            w.progress.setProgress(inc * 100 / total)
            inc += 1

        time.sleep(3)
        w.progress.setProgress(0)
        w.progress.hide()

class plsaindex(mainform):
    def __init__(self,parent = None,name = None):
        mainform.__init__(self, parent, name)

        # PLSA
        self.plsa = None
        self.xml = ""
        self.fileSaveAction.setEnabled(0)
        self.fileSAction.setEnabled(0)

        # Multilang titles
        self.groupTitles.setMinimumSize(QSize(250, 50))
        self.groupTitles.setColumnLayout(0, Qt.Vertical)
        groupTitlesLayout = QGridLayout(self.groupTitles.layout())
        groupTitlesLayout.setAlignment(Qt.AlignTop)

        self.titles = multilang(self.groupTitles, "titles")
        groupTitlesLayout.addWidget(self.titles, 0, 0)
        x = self.titles.addLang()
        x.setLang("en")

        # Advisory Title
        self.groupAdvTitle.setMinimumSize(QSize(250, 50))
        self.groupAdvTitle.setColumnLayout(0, Qt.Vertical)
        groupAdvTitleLayout = QGridLayout(self.groupAdvTitle.layout())
        groupAdvTitleLayout.setAlignment(Qt.AlignTop)

        self.advtitle = multilang(self.groupAdvTitle, "advtitle")
        groupAdvTitleLayout.addWidget(self.advtitle, 0, 0)

        # Advisory Summary
        self.groupAdvSummary.setMinimumSize(QSize(250, 50))
        self.groupAdvSummary.setColumnLayout(0, Qt.Vertical)
        groupAdvSummaryLayout = QGridLayout(self.groupAdvSummary.layout())
        groupAdvSummaryLayout.setAlignment(Qt.AlignTop)

        self.advsummary = multilang(self.groupAdvSummary, "advsummary")
        groupAdvSummaryLayout.addWidget(self.advsummary, 0, 0)

        # Advisory Description
        self.groupAdvDescription.setMinimumSize(QSize(250, 50))
        self.groupAdvDescription.setColumnLayout(0, Qt.Vertical)
        groupAdvDescriptionLayout = QGridLayout(self.groupAdvDescription.layout())
        groupAdvDescriptionLayout.setAlignment(Qt.AlignTop)

        self.advdescription = multilang(self.groupAdvDescription, "advdescription")
        groupAdvDescriptionLayout.addWidget(self.advdescription, 0, 0)

        # Progress bar
        self.progress = QProgressBar(self.statusBar(), "progress")
        self.progress.setGeometry(QRect(5, 0, 200, 15))
        self.progress.hide()

        # Dialog
        self.dialog = QFileDialog(self)
        self.dialog.addFilter("PLSA Index (*.xml)");

        # Signals
        QObject.connect(self.fileNewAction, SIGNAL("activated()"), self.slotNew)
        QObject.connect(self.fileOpenAction, SIGNAL("activated()"), self.slotOpenXMLDialog)
        QObject.connect(self.fileSaveAction, SIGNAL("activated()"), self.slotSaveXML)
        QObject.connect(self.fileExitAction, SIGNAL("activated()"), self.slotExit)
        QObject.connect(self.dialog, SIGNAL("fileSelected(const QString &)"), self.slotOpenXML)
        QObject.connect(self.listAdvisories, SIGNAL("clicked(QListViewItem *)"), self.slotAdvSelected)

        # Threads
        self.thread_xml = loadxml_thread()

    def clear(self):
        self.titles.clear()
        self.listAdvisories.clear()
        self.frameAdvisory.setEnabled(0)

        self.plsa = None
        self.xml = ""
        self.fileSaveAction.setEnabled(0)
        self.fileSAction.setEnabled(0)

    def slotNew(self):
        self.clear()

        x = self.titles.addLang()
        x.setLang("en")

    def slotExit(self):
        self.close()

    def slotOpenXMLDialog(self):
        self.dialog.show()

    def slotOpenXML(self, file):
        if file:
            self.clear()
            self.xml = str(file)

            self.thread_xml.start()

            self.fileSaveAction.setEnabled(1)
            self.fileSAction.setEnabled(1)

    def slotSaveXML(self):
        self.plsa.write(self.xml)

    def slotAdvSelected(self, item):
        self.frameAdvisory.setEnabled(1)

        for obj in [self.advtitle, self.advsummary, self.advdescription]:
            obj.clear()

        self.lineID.setText(item.node.id)

        titles = item.node.title
        for lang in titles:
            x = self.advtitle.addLang(lang)
            x.setText(titles[lang])

        summaries = item.node.summary
        for lang in summaries:
            x = self.advsummary.addLang(lang)
            x.setText(summaries[lang])

        descriptions = item.node.description
        for lang in descriptions:
            x = self.advdescription.addLang(lang)
            x.setText(descriptions[lang])

def main():
    global w
    app = QApplication(sys.argv)
    w = plsaindex()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()

if __name__ == "__main__":
    main()
