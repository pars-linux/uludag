# -*- coding: utf-8 -*-

# Standard Python Modules
import sys

# QT Modules
from qt import *

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

class multilang_group(QGroupBox):
    def __init__(self, parent = None, name = None):
        QGroupBox.__init__(self, parent, name)

        self.multilang_groupLayout = QBoxLayout(self, QBoxLayout.TopToBottom, 5, 5, "multilang_groupLayout")
        self.multilang_groupLayout.setAlignment(Qt.AlignTop)

        self.languages = []

        x = self.addLang()
        x = self.addLang()
        self.removeLang(x)

    def addLang(self):
        ord = len(self.languages)
        lang = multilang_text(self, str(ord))
        self.multilang_groupLayout.addWidget(lang)

        if len(self.languages):
            last = self.languages[-1]
            last.setMode("remove")

        self.languages.append(lang)
        return lang

    def removeLang(self, item):
        self.languages.remove(item)
        self.multilang_groupLayout.remove(item)
        item.hide()

        last = self.languages[-1]
        last.setMode("new")

    def getLanguages(self):
        langs = {}
        for item in self.languages:
            langs[item.getLang()] = item.getText()

        return langs

    def slotAddRemove(self, item):
        if item.getMode() == "new":
            x = self.addLang()
            x.show()
        else:
            self.removeLang(item)

class mainform(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        QMainWindow.__init__(self,parent,name,fl)

        if not name:
            self.setName("mainform")

        self.setCentralWidget(QWidget(self, "qt_central_widget"))
        Form1Layout = QGridLayout(self.centralWidget(), 2, 1, 11, 6, "Form1Layout")

        self.g = multilang_group(self.centralWidget(), "g")
        self.g.setGeometry(QRect(10, 10, 164, 305))
        self.g.setMinimumSize(QSize(400, 0))
        Form1Layout.addWidget(self.g, 0, 0)

        self.p = QPushButton(self.centralWidget(), "p")
        self.p.setText("print")
        Form1Layout.addWidget(self.p, 1, 0)

        QObject.connect(self.p, SIGNAL("clicked()"), self.slotPush)

    def slotPush(self):
        print self.g.getLanguages()


def main():
    app = QApplication(sys.argv)
    w = mainform()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()

if __name__ == "__main__":
    main()
