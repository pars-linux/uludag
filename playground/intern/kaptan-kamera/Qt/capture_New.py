# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_capture_New.ui'
#
# Created: Prş Eyl 18 09:20:49 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
import Cam

class Form1(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")



        self.btn_Capture = QPushButton(self,"btn_Capture")
        self.btn_Capture.setGeometry(QRect(190,330,130,50))

        self.btn_Start = QPushButton(self,"btn_Start")
        self.btn_Start.setGeometry(QRect(20,330,130,50))

        self.lbl_screen = QLabel(self,"lbl_screen")
        self.lbl_screen.setGeometry(QRect(10,70,320,240))

        self.cb_video = QComboBox(0,self,"cb_video")
        self.cb_video.setGeometry(QRect(90,11,161,40))

        self.languageChange()

        ################################
        # QTimer Object
        self.timer = QTimer(self, "timer")


        self.resize(QSize(340,398).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


        #################################
        # Cam Object
        self.cam = Cam.Cam(self)

        self.connect(self.btn_Start, SIGNAL("clicked()"), self.cam.start)
        self.connect(self.btn_Capture, SIGNAL("clicked()"), self.cam.capture)


    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.btn_Capture.setText(self.__tr("Capture"))
        self.btn_Start.setText(self.__tr("Start"))


    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Form1()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
