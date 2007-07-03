# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created: Pzt Tem 2 20:57:23 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *


class ProgressWidget(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("ProgressWidget")


        ProgressWidgetLayout = QVBoxLayout(self,11,6,"ProgressWidgetLayout")

        self.text = QLabel(self,"text")
        ProgressWidgetLayout.addWidget(self.text)

        self.bar = QProgressBar(self,"bar")
        ProgressWidgetLayout.addWidget(self.bar)

        self.log = QTextEdit(self,"log")
        self.log.setTextFormat(QTextEdit.LogText)
        ProgressWidgetLayout.addWidget(self.log)

        self.languageChange()

        self.resize(QSize(345,322).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.text.setText(self.__trUtf8("\x44\x65\xc4\x9f\x69\xc5\x9f\x69\x6b\x6c\x69\x6b\x6c\x65\x72\x20\x79\x61\x70\xc4\xb1\x6c\xc4\xb1\x72\x6b\x65\x6e\x20\x6c\xc3\xbc\x74\x66\x65\x6e\x20\x62\x65\x6b\x6c\x65\x79\x69\x6e\x69\x7a\x2e\x2e\x2e"))


    def __tr(self,s,c = None):
        return qApp.translate("ProgressWidget",s,c)

    def __trUtf8(self,s,c = None):
        return qApp.translate("ProgressWidget",s,c,QApplication.UnicodeUTF8)
