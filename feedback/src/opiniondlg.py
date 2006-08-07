# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opiniondlg.ui'
#
# Created: Paz Tem 9 09:41:15 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060407
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class OpinionDlg(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("OpinionDlg")



        self.opinionEdit = QTextEdit(self,"opinionEdit")
        self.opinionEdit.setGeometry(QRect(173,160,380,100))

        self.opinionLabel = QLabel(self,"opinionLabel")
        self.opinionLabel.setGeometry(QRect(170,60,420,40))
        opinionLabel_font = QFont(self.opinionLabel.font())
        self.opinionLabel.setFont(opinionLabel_font)
        self.opinionLabel.setTextFormat(QLabel.RichText)
        self.opinionLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.opinionMiniLabel = QLabel(self,"opinionMiniLabel")
        self.opinionMiniLabel.setGeometry(QRect(160,100,400,41))
        self.opinionMiniLabel.setPaletteForegroundColor(QColor(0,0,0))
        self.opinionMiniLabel.setAlignment(QLabel.WordBreak | QLabel.AlignBottom | QLabel.AlignRight)

        self.stepLabel = QLabel(self,"stepLabel")
        self.stepLabel.setGeometry(QRect(160,20,100,21))
        self.stepLabel.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel.setFrameShape(QLabel.NoFrame)
        self.stepLabel.setFrameShadow(QLabel.Plain)

        self.opinionPixmap = QLabel(self,"opinionPixmap")
        self.opinionPixmap.setGeometry(QRect(-5,0,142,290))
        self.opinionPixmap.setScaledContents(1)

        self.languageChange()

        self.resize(QSize(619,286).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback Wizard"))
        self.opinionLabel.setText(i18n("<h2>Your opinions about Pardus?</h2>"))
        self.opinionMiniLabel.setText(i18n("(Ease of installation and use, capability of software,\n"
"general quality, adoptability, suitability to requirements, etc)"))
        self.stepLabel.setText(i18n("<b>Step 5 of 7</b>"))

