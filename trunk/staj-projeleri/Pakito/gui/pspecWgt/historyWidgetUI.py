# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../../uis/pspecWidget/historyWidgetUI.ui'
#
# Created: Paz Eyl 2 20:08:30 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdeui import *



class HistoryWidgetUI(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("HistoryWidgetUI")


        HistoryWidgetUILayout = QHBoxLayout(self,11,6,"HistoryWidgetUILayout")

        self.lvHistory = KListView(self,"lvHistory")
        self.lvHistory.addColumn(self.__tr("Release"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.addColumn(self.__tr("Date"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.addColumn(self.__tr("Version"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.addColumn(self.__tr("Comment"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.addColumn(self.__tr("Name"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.addColumn(self.__tr("E-mail"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.addColumn(self.__tr("Type"))
        self.lvHistory.header().setClickEnabled(0,self.lvHistory.header().count() - 1)
        self.lvHistory.setAllColumnsShowFocus(1)
        self.lvHistory.setResizeMode(KListView.AllColumns)
        HistoryWidgetUILayout.addWidget(self.lvHistory)

        layout37 = QVBoxLayout(None,0,6,"layout37")

        self.pbAddHistory = KPushButton(self,"pbAddHistory")
        layout37.addWidget(self.pbAddHistory)

        self.pbRemoveHistory = KPushButton(self,"pbRemoveHistory")
        layout37.addWidget(self.pbRemoveHistory)
        spacer42 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout37.addItem(spacer42)

        self.pbBrowseHistory = KPushButton(self,"pbBrowseHistory")
        layout37.addWidget(self.pbBrowseHistory)
        HistoryWidgetUILayout.addLayout(layout37)

        self.languageChange()

        self.resize(QSize(640,395).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Form2"))
        self.lvHistory.header().setLabel(0,self.__tr("Release"))
        self.lvHistory.header().setLabel(1,self.__tr("Date"))
        self.lvHistory.header().setLabel(2,self.__tr("Version"))
        self.lvHistory.header().setLabel(3,self.__tr("Comment"))
        self.lvHistory.header().setLabel(4,self.__tr("Name"))
        self.lvHistory.header().setLabel(5,self.__tr("E-mail"))
        self.lvHistory.header().setLabel(6,self.__tr("Type"))
        self.pbAddHistory.setText(QString.null)
        self.pbRemoveHistory.setText(QString.null)
        self.pbBrowseHistory.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("HistoryWidgetUI",s,c)
