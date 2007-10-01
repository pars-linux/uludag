from qt import *

class Progress(QProgressDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QProgressDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Progress")

        self.languageChange()
	#self.setFixedSize(QSize(312, 121))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Please Wait"))
        self.setLabelText(self.__tr("<p align=\"center\">Scanning in progress</p>"))


    def __tr(self,s,c = None):
        return qApp.translate("Progress",s,c)
