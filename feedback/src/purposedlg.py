# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'purposedlg.ui'
#
# Created: Pzt Ara 19 23:31:29 2005
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20051013
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class PurposeDlg(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("PurposeDlg")



        self.buttonGroup = QButtonGroup(self,"buttonGroup")
        self.buttonGroup.setGeometry(QRect(170,130,400,120))

        LayoutWidget = QWidget(self.buttonGroup,"layout6")
        LayoutWidget.setGeometry(QRect(16,11,370,100))
        layout6 = QHBoxLayout(LayoutWidget,11,6,"layout6")

        layout18 = QVBoxLayout(None,0,6,"layout18")

        self.checkBox2_3 = QCheckBox(LayoutWidget,"checkBox2_3")
        layout18.addWidget(self.checkBox2_3)

        self.checkBox2 = QCheckBox(LayoutWidget,"checkBox2")
        layout18.addWidget(self.checkBox2)

        self.checkBox2_2 = QCheckBox(LayoutWidget,"checkBox2_2")
        layout18.addWidget(self.checkBox2_2)
        layout6.addLayout(layout18)

        layout18_2 = QVBoxLayout(None,0,6,"layout18_2")

        self.checkBox2_3_2 = QCheckBox(LayoutWidget,"checkBox2_3_2")
        layout18_2.addWidget(self.checkBox2_3_2)

        self.checkBox2_4 = QCheckBox(LayoutWidget,"checkBox2_4")
        layout18_2.addWidget(self.checkBox2_4)

        self.checkBox2_2_2 = QCheckBox(LayoutWidget,"checkBox2_2_2")
        layout18_2.addWidget(self.checkBox2_2_2)
        layout6.addLayout(layout18_2)

        self.purposeMiniLabel = QLabel(self,"purposeMiniLabel")
        self.purposeMiniLabel.setGeometry(QRect(310,100,260,20))

        self.purposeLabel = QLabel(self,"purposeLabel")
        self.purposeLabel.setGeometry(QRect(170,60,420,40))
        purposeLabel_font = QFont(self.purposeLabel.font())
        self.purposeLabel.setFont(purposeLabel_font)
        self.purposeLabel.setTextFormat(QLabel.RichText)
        self.purposeLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.stepLabel = QLabel(self,"stepLabel")
        self.stepLabel.setGeometry(QRect(160,20,100,21))
        self.stepLabel.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel.setFrameShape(QLabel.NoFrame)
        self.stepLabel.setFrameShadow(QLabel.Plain)

        self.purposePixmap = QLabel(self,"purposePixmap")
        self.purposePixmap.setGeometry(QRect(-5,0,142,290))
        self.purposePixmap.setScaledContents(1)

        self.languageChange()

        self.resize(QSize(620,286).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback wizard"))
        self.buttonGroup.setTitle(QString.null)
        self.checkBox2_3.setText(i18n("Daily use"))
        self.checkBox2.setText(i18n("It's my hobby"))
        self.checkBox2_2.setText(i18n("For internet access"))
        self.checkBox2_3_2.setText(i18n("For business"))
        self.checkBox2_4.setText(i18n("Entertainment purposes"))
        self.checkBox2_2_2.setText(i18n("Educational purposes"))
        self.purposeMiniLabel.setText(i18n("<p align=\"right\">(You can click on multiple items)</p>"))
        self.purposeLabel.setText(i18n("<h2>Why do you use Pardus?</h2>"))
        self.stepLabel.setText(i18n("<b>Step 2 of 7</b>"))

