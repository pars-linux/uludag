# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'feedback.ui'
#
# Created: Pzt Ara 5 21:18:17 2005
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20051013
#
# WARNING! All changes made in this file will be lost!


from qt import *


class FeedbackForm(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("FeedbackForm")

        f = QFont(self.font())
        f.setBold(1)
        self.setTitleFont(f)


        self.PageWelcome = QWidget(self,"PageWelcome")

        self.welcomePixmap = QLabel(self.PageWelcome,"welcomePixmap")
        self.welcomePixmap.setGeometry(QRect(0,5,142,290))
        self.welcomePixmap.setScaledContents(1)

        self.welcomeLabel = QLabel(self.PageWelcome,"welcomeLabel")
        self.welcomeLabel.setGeometry(QRect(168,65,420,160))
        self.welcomeLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)
        self.addPage(self.PageWelcome,QString(""))

        self.PageExperience = QWidget(self,"PageExperience")

        self.experiencebuttonGroup = QButtonGroup(self.PageExperience,"experiencebuttonGroup")
        self.experiencebuttonGroup.setGeometry(QRect(175,115,400,140))

        self.questionFour = QRadioButton(self.experiencebuttonGroup,"questionFour")
        self.questionFour.setGeometry(QRect(20,110,318,19))
        self.experiencebuttonGroup.insert( self.questionFour,3)

        self.questionOne = QRadioButton(self.experiencebuttonGroup,"questionOne")
        self.questionOne.setGeometry(QRect(20,20,318,19))
        self.questionOne.setChecked(1)
        self.experiencebuttonGroup.insert( self.questionOne,1)

        self.questionTwo = QRadioButton(self.experiencebuttonGroup,"questionTwo")
        self.questionTwo.setGeometry(QRect(20,50,318,19))
        self.experiencebuttonGroup.insert( self.questionTwo,0)

        self.questionThree = QRadioButton(self.experiencebuttonGroup,"questionThree")
        self.questionThree.setGeometry(QRect(20,80,318,19))
        self.experiencebuttonGroup.insert( self.questionThree,4)

        self.experiencePixmap = QLabel(self.PageExperience,"experiencePixmap")
        self.experiencePixmap.setGeometry(QRect(0,5,142,290))
        self.experiencePixmap.setScaledContents(1)

        self.experienceLabel = QLabel(self.PageExperience,"experienceLabel")
        self.experienceLabel.setGeometry(QRect(168,65,420,40))
        experienceLabel_font = QFont(self.experienceLabel.font())
        self.experienceLabel.setFont(experienceLabel_font)
        self.experienceLabel.setTextFormat(QLabel.RichText)
        self.experienceLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.stepLabel = QLabel(self.PageExperience,"stepLabel")
        self.stepLabel.setGeometry(QRect(165,25,100,21))
        self.stepLabel.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel.setFrameShape(QLabel.NoFrame)
        self.stepLabel.setFrameShadow(QLabel.Plain)
        self.addPage(self.PageExperience,QString(""))

        self.PageWhy = QWidget(self,"PageWhy")

        self.buttonGroup = QButtonGroup(self.PageWhy,"buttonGroup")
        self.buttonGroup.setGeometry(QRect(175,135,400,120))

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

        self.purposeLabel = QLabel(self.PageWhy,"purposeLabel")
        self.purposeLabel.setGeometry(QRect(168,65,420,40))
        purposeLabel_font = QFont(self.purposeLabel.font())
        self.purposeLabel.setFont(purposeLabel_font)
        self.purposeLabel.setTextFormat(QLabel.RichText)
        self.purposeLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.purposePixmap = QLabel(self.PageWhy,"purposePixmap")
        self.purposePixmap.setGeometry(QRect(0,5,142,290))
        self.purposePixmap.setScaledContents(1)

        self.stepLabel_2 = QLabel(self.PageWhy,"stepLabel_2")
        self.stepLabel_2.setGeometry(QRect(165,25,100,21))
        self.stepLabel_2.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel_2.setFrameShape(QLabel.NoFrame)
        self.stepLabel_2.setFrameShadow(QLabel.Plain)

        self.purposeMiniLabel = QLabel(self.PageWhy,"purposeMiniLabel")
        self.purposeMiniLabel.setGeometry(QRect(315,105,260,20))
        self.addPage(self.PageWhy,QString(""))

        self.PageWhere = QWidget(self,"PageWhere")

        self.usageLabel = QLabel(self.PageWhere,"usageLabel")
        self.usageLabel.setGeometry(QRect(168,65,420,40))
        usageLabel_font = QFont(self.usageLabel.font())
        self.usageLabel.setFont(usageLabel_font)
        self.usageLabel.setTextFormat(QLabel.RichText)
        self.usageLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.usageMiniLabel = QLabel(self.PageWhere,"usageMiniLabel")
        self.usageMiniLabel.setGeometry(QRect(305,105,270,24))

        self.usagebuttonGroup = QButtonGroup(self.PageWhere,"usagebuttonGroup")
        self.usagebuttonGroup.setGeometry(QRect(175,135,400,120))

        LayoutWidget_2 = QWidget(self.usagebuttonGroup,"layout")
        LayoutWidget_2.setGeometry(QRect(18,11,160,100))
        layout = QVBoxLayout(LayoutWidget_2,11,6,"layout")

        self.usagecheckBoxOne = QCheckBox(LayoutWidget_2,"usagecheckBoxOne")
        layout.addWidget(self.usagecheckBoxOne)

        self.usagecheckBoxTwo = QCheckBox(LayoutWidget_2,"usagecheckBoxTwo")
        layout.addWidget(self.usagecheckBoxTwo)

        self.usagecheckBoxThree = QCheckBox(LayoutWidget_2,"usagecheckBoxThree")
        layout.addWidget(self.usagecheckBoxThree)

        self.stepLabel_3 = QLabel(self.PageWhere,"stepLabel_3")
        self.stepLabel_3.setGeometry(QRect(165,25,100,21))
        self.stepLabel_3.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel_3.setFrameShape(QLabel.NoFrame)
        self.stepLabel_3.setFrameShadow(QLabel.Plain)

        self.usagePixmap = QLabel(self.PageWhere,"usagePixmap")
        self.usagePixmap.setGeometry(QRect(0,5,142,290))
        self.usagePixmap.setScaledContents(1)
        self.addPage(self.PageWhere,QString(""))

        self.PageHow = QWidget(self,"PageHow")

        self.stepLabel_4 = QLabel(self.PageHow,"stepLabel_4")
        self.stepLabel_4.setGeometry(QRect(165,25,100,21))
        self.stepLabel_4.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel_4.setFrameShape(QLabel.NoFrame)
        self.stepLabel_4.setFrameShadow(QLabel.Plain)

        self.questionPixmap = QLabel(self.PageHow,"questionPixmap")
        self.questionPixmap.setGeometry(QRect(0,5,142,290))
        self.questionPixmap.setScaledContents(1)

        self.questionLabel = QLabel(self.PageHow,"questionLabel")
        self.questionLabel.setGeometry(QRect(168,65,420,40))
        questionLabel_font = QFont(self.questionLabel.font())
        self.questionLabel.setFont(questionLabel_font)
        self.questionLabel.setTextFormat(QLabel.RichText)
        self.questionLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.buttonGroup_2 = QButtonGroup(self.PageHow,"buttonGroup_2")
        self.buttonGroup_2.setGeometry(QRect(175,135,400,110))

        self.questionOne_2 = QRadioButton(self.buttonGroup_2,"questionOne_2")
        self.questionOne_2.setGeometry(QRect(21,15,343,19))
        self.questionOne_2.setChecked(1)
        self.buttonGroup_2.insert( self.questionOne_2,0)

        self.questionTwo_2 = QRadioButton(self.buttonGroup_2,"questionTwo_2")
        self.questionTwo_2.setGeometry(QRect(21,45,343,19))
        self.buttonGroup_2.insert( self.questionTwo_2,1)

        self.questionThree_2 = QRadioButton(self.buttonGroup_2,"questionThree_2")
        self.questionThree_2.setGeometry(QRect(21,75,343,19))
        self.buttonGroup_2.insert( self.questionThree_2,2)
        self.addPage(self.PageHow,QString(""))

        self.PageOpinions = QWidget(self,"PageOpinions")

        self.stepLabel_5 = QLabel(self.PageOpinions,"stepLabel_5")
        self.stepLabel_5.setGeometry(QRect(165,25,100,21))
        self.stepLabel_5.setPaletteForegroundColor(QColor(77,77,77))
        self.stepLabel_5.setFrameShape(QLabel.NoFrame)
        self.stepLabel_5.setFrameShadow(QLabel.Plain)

        self.opinionPixmap = QLabel(self.PageOpinions,"opinionPixmap")
        self.opinionPixmap.setGeometry(QRect(0,5,142,290))
        self.opinionPixmap.setScaledContents(1)

        self.opinionEdit = QTextEdit(self.PageOpinions,"opinionEdit")
        self.opinionEdit.setGeometry(QRect(178,165,380,100))

        self.opinionMiniLabel = QLabel(self.PageOpinions,"opinionMiniLabel")
        self.opinionMiniLabel.setGeometry(QRect(165,105,400,41))
        self.opinionMiniLabel.setPaletteForegroundColor(QColor(0,0,0))
        self.opinionMiniLabel.setAlignment(QLabel.WordBreak | QLabel.AlignBottom | QLabel.AlignRight)

        self.opinionLabel = QLabel(self.PageOpinions,"opinionLabel")
        self.opinionLabel.setGeometry(QRect(168,65,420,40))
        opinionLabel_font = QFont(self.opinionLabel.font())
        self.opinionLabel.setFont(opinionLabel_font)
        self.opinionLabel.setTextFormat(QLabel.RichText)
        self.opinionLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)
        self.addPage(self.PageOpinions,QString(""))

        self.PageHardware = QWidget(self,"PageHardware")

        self.hardwareInfoBox = QCheckBox(self.PageHardware,"hardwareInfoBox")
        self.hardwareInfoBox.setGeometry(QRect(235,245,340,20))

        self.hardwareInfoPixmap = QLabel(self.PageHardware,"hardwareInfoPixmap")
        self.hardwareInfoPixmap.setGeometry(QRect(0,5,142,290))
        self.hardwareInfoPixmap.setScaledContents(1)

        self.stepLabel_6 = QLabel(self.PageHardware,"stepLabel_6")
        self.stepLabel_6.setGeometry(QRect(165,25,100,21))
        self.stepLabel_6.setPaletteForegroundColor(QColor(77,77,77))

        self.hardwareInfoLabel = QLabel(self.PageHardware,"hardwareInfoLabel")
        self.hardwareInfoLabel.setGeometry(QRect(168,55,420,180))
        hardwareInfoLabel_font = QFont(self.hardwareInfoLabel.font())
        self.hardwareInfoLabel.setFont(hardwareInfoLabel_font)
        self.hardwareInfoLabel.setTextFormat(QLabel.RichText)
        self.hardwareInfoLabel.setAlignment(QLabel.WordBreak | QLabel.AlignTop)
        self.addPage(self.PageHardware,QString(""))

        self.PageUpload = QWidget(self,"PageUpload")

        self.buttonRetry = QPushButton(self.PageUpload,"buttonRetry")
        self.buttonRetry.setGeometry(QRect(169,242,120,31))

        self.hardwareInfoLabel_2 = QLabel(self.PageUpload,"hardwareInfoLabel_2")
        self.hardwareInfoLabel_2.setGeometry(QRect(168,55,420,26))
        hardwareInfoLabel_2_font = QFont(self.hardwareInfoLabel_2.font())
        self.hardwareInfoLabel_2.setFont(hardwareInfoLabel_2_font)
        self.hardwareInfoLabel_2.setTextFormat(QLabel.RichText)
        self.hardwareInfoLabel_2.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.uploadPixmap = QLabel(self.PageUpload,"uploadPixmap")
        self.uploadPixmap.setGeometry(QRect(0,5,142,290))
        self.uploadPixmap.setScaledContents(1)

        self.labelStatus = QLabel(self.PageUpload,"labelStatus")
        self.labelStatus.setGeometry(QRect(173,85,420,150))
        labelStatus_font = QFont(self.labelStatus.font())
        self.labelStatus.setFont(labelStatus_font)
        self.labelStatus.setTextFormat(QLabel.RichText)
        self.labelStatus.setAlignment(QLabel.WordBreak | QLabel.AlignTop)
        self.addPage(self.PageUpload,QString(""))

        self.PageThank = QWidget(self,"PageThank")

        self.goodbyeLabel_2 = QLabel(self.PageThank,"goodbyeLabel_2")
        self.goodbyeLabel_2.setGeometry(QRect(175,65,400,140))
        self.goodbyeLabel_2.setAlignment(QLabel.WordBreak | QLabel.AlignTop)

        self.goodbyePixmap = QLabel(self.PageThank,"goodbyePixmap")
        self.goodbyePixmap.setGeometry(QRect(0,5,142,290))
        self.goodbyePixmap.setScaledContents(1)
        self.addPage(self.PageThank,QString(""))

        self.languageChange()

        self.resize(QSize(600,373).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Feedback"))
        self.welcomeLabel.setText(self.__tr("<h2>Welcome to Pardus</h2>\n"
"\n"
"With this small wizard, you can send your messages to Pardus \n"
"developers and help Pardus be the best Linux in the world.\n"
"\n"
"<p>\n"
"The information you will give here will accelerate Pardus development. \n"
"Please click on \"Forward\" button for the next step.\n"
"<p>"))
        self.setTitle(self.PageWelcome,self.__tr("Welcome"))
        self.experiencebuttonGroup.setTitle(QString.null)
        self.questionFour.setText(self.__tr("Experienced system administrator"))
        self.questionOne.setText(self.__tr("New user"))
        self.questionTwo.setText(self.__tr("Home/office productivity user"))
        self.questionThree.setText(self.__tr("Experienced user"))
        self.experienceLabel.setText(self.__tr("<h2>What is your experience level?</h2>"))
        self.stepLabel.setText(self.__tr("<b>Step 1 of 6</b>"))
        self.setTitle(self.PageExperience,self.__tr("Experience"))
        self.buttonGroup.setTitle(QString.null)
        self.checkBox2_3.setText(self.__tr("Daily use"))
        self.checkBox2.setText(self.__tr("It's my hobby"))
        self.checkBox2_2.setText(self.__tr("For internet access"))
        self.checkBox2_3_2.setText(self.__tr("For business"))
        self.checkBox2_4.setText(self.__tr("Entertainment purposes"))
        self.checkBox2_2_2.setText(self.__tr("Educational purposes"))
        self.purposeLabel.setText(self.__tr("<h2>Why do you use Pardus?</h2>"))
        self.stepLabel_2.setText(self.__tr("<b>Step 2 of 6</b>"))
        self.purposeMiniLabel.setText(self.__tr("<p align=\"right\">(You can click on multiple items)</p>"))
        self.setTitle(self.PageWhy,self.__tr("Why?"))
        self.usageLabel.setText(self.__tr("<h2>Where do you use Pardus?</h2>"))
        self.usageMiniLabel.setText(self.__tr("<p align=\"right\">(You can click on multiple items)</p>"))
        self.usagebuttonGroup.setTitle(QString.null)
        self.usagecheckBoxOne.setText(self.__tr("At home"))
        self.usagecheckBoxTwo.setText(self.__tr("At work"))
        self.usagecheckBoxThree.setText(self.__tr("At school"))
        self.stepLabel_3.setText(self.__tr("<b>Step 3 of 6</b>"))
        self.setTitle(self.PageWhere,self.__tr("Where?"))
        self.stepLabel_4.setText(self.__tr("<b>Step 4 of 6</b>"))
        self.questionLabel.setText(self.__tr("<h2>How does Pardus fit your needs?</h2>"))
        self.buttonGroup_2.setTitle(QString.null)
        self.questionOne_2.setText(self.__tr("Very satisfying. Pardus fulfils my requirements"))
        self.questionTwo_2.setText(self.__tr("Good, however it lacks some capabilities"))
        self.questionThree_2.setText(self.__tr("It has insufficient areas"))
        self.setTitle(self.PageHow,self.__tr("How?"))
        self.stepLabel_5.setText(self.__tr("<b>Step 5 of 6</b>"))
        self.opinionMiniLabel.setText(self.__tr("(Ease of installation and use, capability of software,\n"
"general quality, adoptability, suitability to requirements, etc)"))
        self.opinionLabel.setText(self.__tr("<h2>Your opinions about Pardus?</h2>"))
        self.setTitle(self.PageOpinions,self.__tr("Opinions?"))
        self.hardwareInfoBox.setText(self.__tr("&Do not send my computer's hardware information"))
        self.hardwareInfoBox.setAccel(self.__tr("Alt+D"))
        self.stepLabel_6.setText(self.__tr("<b>Step 6 of 6</b>"))
        self.hardwareInfoLabel.setText(self.__tr("<h2>Computer information</h2>\n"
"Pardus Hardware CollectInfo Wizard will now gather information from\n"
"your hardware, including CPU, memory and network cards. This \n"
"information will be sent to Pardus Development Center, in order to\n"
"build more stable and secure Pardus. You will need an internet\n"
"access for this operation to complete. \n"
"\n"
"<b>Note that we will not collect any of your personal documents.</b>"))
        self.setTitle(self.PageHardware,self.__tr("Hardware Info"))
        self.buttonRetry.setText(self.__tr("Retry"))
        self.hardwareInfoLabel_2.setText(self.__tr("<h2>Upload</h2>"))
        self.setTitle(self.PageUpload,self.__tr("Upload"))
        self.goodbyeLabel_2.setText(self.__tr("<h2>Thank you</h2>\n"
"We have collected all necessary information in order to send \n"
"to Pardus developers.\n"
"<p>\n"
"Thank you for your support to Pardus operating system."))
        self.setTitle(self.PageThank,self.__tr("Thank you"))


    def __tr(self,s,c = None):
        return qApp.translate("FeedbackForm",s,c)
