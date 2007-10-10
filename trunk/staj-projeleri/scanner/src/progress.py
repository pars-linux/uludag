from qt import *
from kdeui import *
from utility import *

class Progress(QProgressDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QProgressDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Progress")

        self.languageChange()
	#self.setFixedSize(QSize(312, 121))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Please Wait"))
        self.setLabelText(i18n("<p align=\"center\">Scanning in progress</p>"))


    #def __tr(self,s,c = None):
        #return qApp.translate("Progress",s,c)

class Info(KDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        KDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Information")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(0,0,300,100))
	
        self.languageChange()
	self.setFixedSize(QSize(300, 100))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Please Wait"))
        self.textLabel1.setText(i18n("<p align=\"center\">Scanning in progress.</p>"))


    #def __tr(self,s,c = None):
        #return qApp.translate("Information",s,c)