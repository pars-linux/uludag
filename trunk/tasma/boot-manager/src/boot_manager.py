# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'boot_manager.ui'
#
# Created: Sal Mar 27 09:15:21 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class formMain(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("formMain")


        formMainLayout = QGridLayout(self,1,1,11,6,"formMainLayout")

        self.pushHelp = QPushButton(self,"pushHelp")
        self.pushHelp.setEnabled(0)

        formMainLayout.addMultiCellWidget(self.pushHelp,2,2,0,1)

        self.listEntries = KListView(self,"listEntries")
        self.listEntries.addColumn(i18n("Label"))
        self.listEntries.setFullWidth(1)

        formMainLayout.addWidget(self.listEntries,0,0)

        self.listCommands = KListView(self,"listCommands")
        self.listCommands.addColumn(i18n("Command"))
        self.listCommands.setFullWidth(1)

        formMainLayout.addWidget(self.listCommands,1,0)

        self.listOptions = KListView(self,"listOptions")
        self.listOptions.addColumn(i18n("Option"))
        self.listOptions.addColumn(i18n("Value"))
        self.listOptions.setMaximumSize(QSize(200,32767))
        self.listOptions.setFullWidth(1)

        formMainLayout.addMultiCellWidget(self.listOptions,0,1,1,1)

        self.languageChange()

        self.resize(QSize(548,340).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Form"))
        self.pushHelp.setText(i18n("help"))
        self.listEntries.header().setLabel(0,i18n("Label"))
        self.listCommands.header().setLabel(0,i18n("Command"))
        self.listOptions.header().setLabel(0,i18n("Option"))
        self.listOptions.header().setLabel(1,i18n("Value"))

