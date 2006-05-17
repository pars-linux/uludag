# -*- coding: utf-8 -*-

from qt import *
from kdecore import *
from kdeui import *

class serviceWidget(QWidget):
    def __init__(self, parent = None, name = None):
        QWidget.__init__(self, parent, name)

        if not name:
            self.setName("serviceForm")

        self.setCaption(i18n("Service GUI"))

        serviceFormLayout = QGridLayout(self, 1, 1, 11, 6, "serviceFormLayout")

        layout2 = QHBoxLayout(None, 0, 6, "layout2")

        self.pushSwitch = KPushButton(self, "pushSwitch")
        self.pushSwitch.setText(i18n("Start"))
        self.pushSwitch.setEnabled(0)

        layout2.addWidget(self.pushSwitch)
        
        self.pushSwitch2 = KPushButton(self, "pushSwitch2")
        self.pushSwitch2.setText(i18n("Auto Start"))
        self.pushSwitch2.setEnabled(0)

        layout2.addWidget(self.pushSwitch2)

        spacer1 = QSpacerItem(355, 16, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout2.addItem(spacer1)

        self.pushHelp = KPushButton(self, "pushHelp")
        self.pushHelp.setText(i18n("Help"))

        layout2.addWidget(self.pushHelp)

        serviceFormLayout.addLayout(layout2, 2, 0)

        self.listServices = KListView(self, "listServices")
        self.listServices.addColumn("")
        self.listServices.addColumn(i18n("Service"))
        self.listServices.addColumn(i18n("Auto Start"))
        self.listServices.setAllColumnsShowFocus(1)
        self.listServices.setFullWidth(1)
        self.listServices.setItemsMovable(0)
        self.listServices.setAlternateBackground(QColor(238, 246, 255))

        serviceFormLayout.addWidget(self.listServices, 1, 0)

        self.lineSearch = KListViewSearchLineWidget(self.listServices, self, "lineSearch")

        serviceFormLayout.addWidget(self.lineSearch, 0, 0)

        self.resize(QSize(672,453).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
