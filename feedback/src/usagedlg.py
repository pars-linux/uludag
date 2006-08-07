# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'usagedlg.ui'
#
# Created: Paz Tem 9 09:41:15 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060407
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class UsageDlg(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("UsageDlg")



        self.usagebuttonGroup = QButtonGroup(self,"usagebuttonGroup")
        self.usagebuttonGroup.setGeometry(QRect(170,130,400,120))

        LayoutWidget = QWidget(self.usagebuttonGroup,"layout")
        LayoutWidget.setGeometry(QRect(18,11,160,100))
        layout = QVBoxLayout(LayoutWidget,11,6,"layout")

        self.usagecheckBoxOne = QCheckBox(LayoutWidget,"usagecheckBoxOne")
        layout.addWidget(self.usagecheckBoxOne)

        self.usagecheckBoxTwo = QCheckBox(LayoutWidget,"usagecheckBoxTwo")
        layout.addWidget(self.usagecheckBoxTwo)

        self.usagecheckBoxThree = QCheckBox(LayoutWidget,"usagecheckBoxThree")
        layout.addWidget(self.usagecheckBoxThree)

        self.usageMiniLabel = QLabel(self,"usageMiniLabel")
        self.usageMiniLabel.setGeometry(QRect(300,100,270,24))

        self.stepLabel = QLabel(self,"stepLabel")
        self.stepLabel.setGeometry(QRect(160,20,100,21))
        self.stepLabel.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel.setFrameShape(QLabel.NoFrame)
        self.stepLabel.setFrameShadow(QLabel.Plain)

        self.usagePixmap = QLabel(self,"usagePixmap")
        self.usagePixmap.setGeometry(QRect(-5,0,142,290))
        self.usagePixmap.setScaledContents(1)

        self.usageLabel = QLabel(self,"usageLabel")
        self.usageLabel.setGeometry(QRect(170,60,420,40))
        usageLabel_font = QFont(self.usageLabel.font())
        self.usageLabel.setFont(usageLabel_font)
        self.usageLabel.setTextFormat(QLabel.RichText)
        self.usageLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.languageChange()

        self.resize(QSize(619,286).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Feedback Wizard"))
        self.usagebuttonGroup.setTitle(QString.null)
        self.usagecheckBoxOne.setText(i18n("At home"))
        self.usagecheckBoxTwo.setText(i18n("At work"))
        self.usagecheckBoxThree.setText(i18n("At school"))
        self.usageMiniLabel.setText(i18n("<p align=\"right\">(You can click on multiple items)</p>"))
        self.stepLabel.setText(i18n("<b>Step 3 of 7</b>"))
        self.usageLabel.setText(i18n("<h2>Where do you use Pardus?</h2>"))

