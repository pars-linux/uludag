#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard Python Modules
import sys

# QT Modules
from qt import *
import kdedesigner

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

        QObject.connect(self.pushAddRemove, SIGNAL("clicked()"), self.slotAddRemove)

        self.clearWState(Qt.WState_Polished)

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

class multilang(QVBox):
    def __init__(self, parent = None, name = None):
        QVBox.__init__(self, parent, name)

        self.layout().setSpacing(6)

        self.languages = []

        x = self.addLang()
        x.setLang("en")

    def addLang(self):
        ord = len(self.languages)
        lang = multilang_text(self, str(ord))

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

    def getLanguages(self):
        langs = {}
        for item in self.languages:
            if item.getLang():
                langs[item.getLang()] = item.getText()

        return langs

    def slotAddRemove(self, item):
        if item.getMode() == "new":
            x = self.addLang()
            x.show()
        else:
            self.removeLang(item)

    def resizeEvent(self, qr):
        parent = self.parent()
        height = parent.insideSpacing() + parent.insideMargin() * 2 + self.height()
        parent.setMinimumSize(QSize(250, height))

class plsaindex(mainform):
    def __init__(self,parent = None,name = None):
        mainform.__init__(self, parent, name)

        # Multilang titles
        self.groupTitles.setMinimumSize(QSize(250, 50))
        self.groupTitles.setColumnLayout(0, Qt.Vertical)
        groupTitlesLayout = QGridLayout(self.groupTitles.layout())
        groupTitlesLayout.setAlignment(Qt.AlignTop)

        self.title = multilang(self.groupTitles, "multilang")
        groupTitlesLayout.addWidget(self.title, 0, 0)

def main():
    app = QApplication(sys.argv)
    w = plsaindex()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()

if __name__ == "__main__":
    main()
