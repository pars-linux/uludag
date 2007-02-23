# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bocukForm.ui'
#
# Created: Cts Şub 24 00:08:35 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!

from kdecore import *
from kdeui import *
from kfile import *
from qt import *

image0_data = \
    "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
    "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
    "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
    "\xdb\x49\x44\x41\x54\x38\x8d\xed\x94\x3d\x4e\xc3" \
    "\x40\x10\x46\xdf\xac\x8d\x12\x81\x08\x4d\xaa\x94" \
    "\xb9\x41\xe8\xd3\x71\x0e\x5f\x8d\xb3\xb8\xa0\x8c" \
    "\xb8\x82\x9b\x94\x14\x91\xa2\xc8\x5e\x7b\x67\x28" \
    "\x12\x1b\x23\xaf\x65\x0a\xd2\xf9\x49\x9f\x34\xfb" \
    "\xa3\xa7\x9d\x62\x16\x66\xee\x8d\xb4\xc5\xe7\x1b" \
    "\x98\xb2\x5d\xac\xd8\xbb\x04\x41\x01\xbb\x25\x56" \
    "\xf7\xf6\x54\xb1\x2a\x90\x0b\x14\xbb\xfc\xea\x4b" \
    "\x5b\xf1\xe3\x1a\x9a\x92\xfd\xe6\x95\xf7\xe5\x13" \
    "\x98\x07\xea\xe9\x48\x0d\x65\x89\x1d\xcf\x64\xa9" \
    "\x50\xb4\xbe\x4e\x9c\x3c\x80\x36\xc8\xe2\x05\x96" \
    "\xcf\x08\x15\xe0\x6f\xe9\xd7\x1e\x48\x00\xf7\xd3" \
    "\xaf\xd5\xe0\x04\x71\x5d\xff\xd7\xe3\xdf\x58\x24" \
    "\x53\x77\x22\x0c\xc5\xff\xc4\x2c\x9e\xc5\x7f\x11" \
    "\x4b\x24\x53\x77\x22\x74\x93\x17\x3c\x68\x83\x55" \
    "\x27\x6c\x30\xba\xfd\xf1\x6e\x86\xeb\x32\xa0\x6a" \
    "\x58\x88\x89\x2f\x5f\x60\x4a\x7e\x3c\x90\x39\x47" \
    "\xfc\x03\x1a\xf9\x90\x54\x31\x1f\xf8\x90\x91\xd7" \
    "\xcf\xdc\x87\x6f\x9b\x2f\x71\x37\xec\x4e\x14\x84" \
    "\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"

class BocekForm(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self,parent,name,modal,fl)

        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data,"PNG")
        if not name:
            self.setName("BocekForm")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(621,503))
        self.setMaximumSize(QSize(621,503))
        self.setBaseSize(QSize(621,503))


        self.WizardPage = QWidget(self,"WizardPage")

        self.textLabel2 = QLabel(self.WizardPage,"textLabel2")
        self.textLabel2.setGeometry(QRect(24,17,570,41))

        self.textLabel3 = QLabel(self.WizardPage,"textLabel3")
        self.textLabel3.setGeometry(QRect(24,57,570,61))
        self.textLabel3.setTextFormat(QLabel.RichText)

        self.buttonGroup2 = QButtonGroup(self.WizardPage,"buttonGroup2")
        self.buttonGroup2.setGeometry(QRect(20,130,570,270))

        self.textLabel4_2 = QLabel(self.buttonGroup2,"textLabel4_2")
        self.textLabel4_2.setGeometry(QRect(54,97,81,21))

        self.textLabel4 = QLabel(self.buttonGroup2,"textLabel4")
        self.textLabel4.setGeometry(QRect(54,69,81,21))

        self.textLabel4_3 = QLabel(self.buttonGroup2,"textLabel4_3")
        self.textLabel4_3.setEnabled(0)
        self.textLabel4_3.setGeometry(QRect(54,172,81,21))

        self.textLabel6 = QLabel(self.buttonGroup2,"textLabel6")
        self.textLabel6.setEnabled(0)
        self.textLabel6.setGeometry(QRect(140,194,360,19))
        self.textLabel6.setPaletteForegroundColor(QColor(38,145,24))
        self.textLabel6.setTextFormat(QLabel.RichText)

        self.radioLogin = QRadioButton(self.buttonGroup2,"radioLogin")
        self.radioLogin.setGeometry(QRect(34,37,460,21))
        self.radioLogin.setChecked(1)

        self.loginUsername = QLineEdit(self.buttonGroup2,"loginUsername")
        self.loginUsername.setGeometry(QRect(140,70,220,21))

        self.rememberPass = QCheckBox(self.buttonGroup2,"rememberPass")
        self.rememberPass.setGeometry(QRect(370,97,191,21))

        self.newEmail = QLineEdit(self.buttonGroup2,"newEmail")
        self.newEmail.setEnabled(0)
        self.newEmail.setGeometry(QRect(140,173,220,21))

        self.loginPassword = QLineEdit(self.buttonGroup2,"loginPassword")
        self.loginPassword.setGeometry(QRect(140,97,221,21))
        self.loginPassword.setEchoMode(QLineEdit.Password)

        self.textLabel4_2_2 = QLabel(self.buttonGroup2,"textLabel4_2_2")
        self.textLabel4_2_2.setEnabled(0)
        self.textLabel4_2_2.setGeometry(QRect(54,221,81,21))

        self.newPassword = QLineEdit(self.buttonGroup2,"newPassword")
        self.newPassword.setEnabled(0)
        self.newPassword.setGeometry(QRect(140,221,221,21))
        self.newPassword.setEchoMode(QLineEdit.Password)

        self.buttonRegister = KPushButton(self.buttonGroup2,"buttonRegister")
        self.buttonRegister.setEnabled(0)
        self.buttonRegister.setGeometry(QRect(370,221,90,20))
        self.buttonRegister.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonRegister.sizePolicy().hasHeightForWidth()))
        self.buttonRegister.setIconSet(QIconSet(self.image0))

        self.radioNew = QRadioButton(self.buttonGroup2,"radioNew")
        self.radioNew.setGeometry(QRect(34,140,461,21))
        self.addPage(self.WizardPage,QString(""))

        self.WizardPage_2 = QWidget(self,"WizardPage_2")

        self.buttonGroup2_2 = QButtonGroup(self.WizardPage_2,"buttonGroup2_2")
        self.buttonGroup2_2.setGeometry(QRect(20,10,570,390))

        self.textLabel3_2 = QLabel(self.buttonGroup2_2,"textLabel3_2")
        self.textLabel3_2.setGeometry(QRect(55,150,91,21))

        self.textLabel1 = QLabel(self.buttonGroup2_2,"textLabel1")
        self.textLabel1.setEnabled(0)
        self.textLabel1.setGeometry(QRect(55,69,101,21))

        self.textLabel2_2 = QLabel(self.buttonGroup2_2,"textLabel2_2")
        self.textLabel2_2.setGeometry(QRect(55,180,101,21))

        self.radioOldBug = QRadioButton(self.buttonGroup2_2,"radioOldBug")
        self.radioOldBug.setGeometry(QRect(34,37,500,21))

        self.comboOldBug = QComboBox(0,self.buttonGroup2_2,"comboOldBug")
        self.comboOldBug.setEnabled(0)
        self.comboOldBug.setGeometry(QRect(160,70,370,20))

        self.radioNewBug = QRadioButton(self.buttonGroup2_2,"radioNewBug")
        self.radioNewBug.setGeometry(QRect(34,117,211,21))
        self.radioNewBug.setChecked(1)

        self.lineSummaryNewBug = QLineEdit(self.buttonGroup2_2,"lineSummaryNewBug")
        self.lineSummaryNewBug.setGeometry(QRect(160,150,371,21))

        self.textDescNewBug = QTextEdit(self.buttonGroup2_2,"textDescNewBug")
        self.textDescNewBug.setGeometry(QRect(160,180,370,190))
        self.addPage(self.WizardPage_2,QString(""))

        self.WizardPage_3 = QWidget(self,"WizardPage_3")

        self.buttonGroup2_2_2 = QButtonGroup(self.WizardPage_3,"buttonGroup2_2_2")
        self.buttonGroup2_2_2.setGeometry(QRect(20,10,570,390))

        self.labelStatus = QLabel(self.buttonGroup2_2_2,"labelStatus")
        self.labelStatus.setEnabled(0)
        self.labelStatus.setGeometry(QRect(30,326,510,21))

        self.addLogCheck = QCheckBox(self.buttonGroup2_2_2,"addLogCheck")
        self.addLogCheck.setGeometry(QRect(20,30,530,21))

        self.panelLogs = QButtonGroup(self.buttonGroup2_2_2,"panelLogs")
        self.panelLogs.setEnabled(0)
        self.panelLogs.setGeometry(QRect(30,70,510,210))
        self.panelLogs.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.panelLogs.sizePolicy().hasHeightForWidth()))
        self.panelLogs.setMinimumSize(QSize(189,140))

        self.line1 = QFrame(self.panelLogs,"line1")
        self.line1.setGeometry(QRect(10,39,488,16))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Plain)
        self.line1.setFrameShape(QFrame.HLine)

        self.textLabel2_3 = QLabel(self.panelLogs,"textLabel2_3")
        self.textLabel2_3.setEnabled(0)
        self.textLabel2_3.setGeometry(QRect(30,72,460,21))

        self.textLabel2_3_2 = QLabel(self.panelLogs,"textLabel2_3_2")
        self.textLabel2_3_2.setEnabled(0)
        self.textLabel2_3_2.setGeometry(QRect(30,110,460,21))

        self.textLabel2_3_2_2 = QLabel(self.panelLogs,"textLabel2_3_2_2")
        self.textLabel2_3_2_2.setEnabled(0)
        self.textLabel2_3_2_2.setGeometry(QRect(30,145,460,21))

        self.textLabel2_3_2_2_2 = QLabel(self.panelLogs,"textLabel2_3_2_2_2")
        self.textLabel2_3_2_2_2.setEnabled(0)
        self.textLabel2_3_2_2_2.setGeometry(QRect(30,181,460,21))

        self.checkBoxAll = QCheckBox(self.panelLogs,"checkBoxAll")
        self.checkBoxAll.setGeometry(QRect(11,21,488,20))
        self.checkBoxAll.setChecked(1)
        self.checkBoxAll.setTristate(0)

        self.checkBoxStandartLogs = QCheckBox(self.panelLogs,"checkBoxStandartLogs")
        self.checkBoxStandartLogs.setEnabled(0)
        self.checkBoxStandartLogs.setGeometry(QRect(11,56,488,20))
        self.checkBoxStandartLogs.setChecked(1)

        self.checkBoxHardware = QCheckBox(self.panelLogs,"checkBoxHardware")
        self.checkBoxHardware.setEnabled(0)
        self.checkBoxHardware.setGeometry(QRect(11,92,488,20))
        self.checkBoxHardware.setChecked(1)

        self.checkBoxConfig = QCheckBox(self.panelLogs,"checkBoxConfig")
        self.checkBoxConfig.setEnabled(0)
        self.checkBoxConfig.setGeometry(QRect(11,128,488,20))
        self.checkBoxConfig.setChecked(1)

        self.checkBoxPackages = QCheckBox(self.panelLogs,"checkBoxPackages")
        self.checkBoxPackages.setEnabled(0)
        self.checkBoxPackages.setGeometry(QRect(11,164,488,20))
        self.checkBoxPackages.setChecked(1)

        self.progressBar = KProgress(self.buttonGroup2_2_2,"progressBar")
        self.progressBar.setEnabled(0)
        self.progressBar.setGeometry(QRect(30,350,510,23))
        self.progressBar.setFrameShadow(KProgress.Plain)
        self.progressBar.setCenterIndicator(1)
        self.progressBar.setIndicatorFollowsStyle(1)
        self.progressBar.setPercentageVisible(1)

        self.buttonTakeScreen = KPushButton(self.buttonGroup2_2_2,"buttonTakeScreen")
        self.buttonTakeScreen.setEnabled(0)
        self.buttonTakeScreen.setGeometry(QRect(398,290,140,31))
        self.buttonTakeScreen.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.buttonTakeScreen.sizePolicy().hasHeightForWidth()))
        self.buttonTakeScreen.setIconSet(QIconSet(self.image0))
        self.addPage(self.WizardPage_3,QString(""))

        self.languageChange()

        self.resize(QSize(621,503).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.addLogCheck,SIGNAL("toggled(bool)"),self.progressBar.setEnabled)
        self.connect(self.addLogCheck,SIGNAL("toggled(bool)"),self.labelStatus.setEnabled)
        self.connect(self.addLogCheck,SIGNAL("toggled(bool)"),self.buttonTakeScreen.setEnabled)
        self.connect(self.addLogCheck,SIGNAL("toggled(bool)"),self.panelLogs.setEnabled)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxPackages.setDisabled)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxConfig.setDisabled)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxHardware.setDisabled)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxStandartLogs.setDisabled)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxPackages.setChecked)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxConfig.setChecked)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxHardware.setChecked)
        self.connect(self.checkBoxAll,SIGNAL("toggled(bool)"),self.checkBoxStandartLogs.setChecked)
        self.connect(self.radioLogin,SIGNAL("toggled(bool)"),self.rememberPass.setEnabled)
        self.connect(self.radioNew,SIGNAL("toggled(bool)"),self.textLabel6.setEnabled)
        self.connect(self.radioNewBug,SIGNAL("toggled(bool)"),self.lineSummaryNewBug.setEnabled)
        self.connect(self.radioNewBug,SIGNAL("toggled(bool)"),self.textLabel3_2.setEnabled)
        self.connect(self.radioOldBug,SIGNAL("toggled(bool)"),self.comboOldBug.setEnabled)
        self.connect(self.radioOldBug,SIGNAL("toggled(bool)"),self.textLabel1.setEnabled)
        self.connect(self.radioNew,SIGNAL("toggled(bool)"),self.textLabel4_2_2.setEnabled)
        self.connect(self.radioNew,SIGNAL("toggled(bool)"),self.textLabel4_3.setEnabled)
        self.connect(self.radioLogin,SIGNAL("toggled(bool)"),self.textLabel4_2.setEnabled)
        self.connect(self.radioLogin,SIGNAL("toggled(bool)"),self.textLabel4.setEnabled)
        self.connect(self.radioNew,SIGNAL("toggled(bool)"),self.newPassword.setEnabled)
        self.connect(self.radioNew,SIGNAL("toggled(bool)"),self.newEmail.setEnabled)
        self.connect(self.radioLogin,SIGNAL("toggled(bool)"),self.loginPassword.setEnabled)
        self.connect(self.radioLogin,SIGNAL("toggled(bool)"),self.loginUsername.setEnabled)
        self.connect(self.radioNew,SIGNAL("toggled(bool)"),self.buttonRegister.setEnabled)


    def languageChange(self):
        self.setCaption(self.__tr("Bocek"))
        self.textLabel2.setText(self.__tr("<b><font size=\"+3\">Welcome to the Bocek</font></b>"))
        self.textLabel3.setText(self.__tr("With using Bocek you can send bug reports to the Pardus Bug System(<b>bugs.pardus.org.tr</b>) easily. You must have an account on system, if you don't you can create a new one easily with bocek. Please follow the instructions."))
        self.buttonGroup2.setTitle(self.__tr("Choose a User Type"))
        self.textLabel4_2.setText(self.__tr("Password :"))
        self.textLabel4.setText(self.__tr("User Name :"))
        self.textLabel4_3.setText(self.__tr("E-mail :"))
        self.textLabel6.setText(self.__tr("You will get a confirmation mail, use correct e-mail address"))
        self.radioLogin.setText(self.__tr("Existing User"))
        self.rememberPass.setText(self.__tr("Remember my password"))
        self.textLabel4_2_2.setText(self.__tr("Password :"))
        self.buttonRegister.setText(self.__tr("Register"))
        self.radioNew.setText(self.__tr("New User"))
        self.setTitle(self.WizardPage,self.__tr("Welcome"))
        self.buttonGroup2_2.setTitle(self.__tr("Choose an Action"))
        self.textLabel3_2.setText(self.__tr("Summary :"))
        self.textLabel1.setText(self.__tr("Select the Bug :"))
        self.textLabel2_2.setText(self.__tr("Description :"))
        self.radioOldBug.setText(self.__tr("Old Bug (to add new comment or attachments)"))
        self.radioNewBug.setText(self.__tr("New Bug"))
        self.setTitle(self.WizardPage_2,self.__tr("Define the Bug"))
        self.buttonGroup2_2_2.setTitle(self.__tr("Add System Logs or Screenshots"))
        self.labelStatus.setText(self.__tr("<b>Status : </b>"))
        self.addLogCheck.setText(self.__tr("I want to add some attachments to the bug"))
        self.panelLogs.setTitle(self.__tr("System Information"))
        self.textLabel2_3.setText(self.__tr("Recommends for all type of bugs."))
        self.textLabel2_3_2.setText(self.__tr("Especially for hardware based problems developer needs them."))
        self.textLabel2_3_2_2.setText(self.__tr("If you modified your config files developer will needs them to see changes."))
        self.textLabel2_3_2_2_2.setText(self.__tr("If you think your problem depends on a package you must add these logs."))
        self.checkBoxAll.setText(self.__tr("All (Recommended)"))
        self.checkBoxStandartLogs.setText(self.__tr("Standard Logs"))
        self.checkBoxHardware.setText(self.__tr("Hardware Information"))
        self.checkBoxConfig.setText(self.__tr("Config Files"))
        self.checkBoxPackages.setText(self.__tr("Package Informations"))
        self.buttonTakeScreen.setText(self.__tr("Take Screenshot"))
        self.setTitle(self.WizardPage_3,self.__tr("Additional Files"))


    def __tr(self,s,c = None):
        return qApp.translate("BocekForm",s,c)
