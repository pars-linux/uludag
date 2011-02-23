#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
from qt import *

from temp import PListView
from temp import PListViewItem
from temp import PLVIconButton

import dbus
import dbus.mainloop.qt3

from kdecore import *
from kdeui import *
import kdedesigner


def AboutData():
    global version, description

    about_data = KAboutData("sample-application",
                            "Sample",
                            "1.0.2",
                            "A sample application",
                            KAboutData.License_GPL,
                            '(C) 2010-2010 UEKAE/TUBITAK',
                            None, None,
                            'mehmet@pardus.org.tr')

    about_data.addAuthor('Mehmet Özdemir', None, 'mehmet@pardus.org.tr')

    return about_data

class MainApplication(QDialog):
    def __init__(self, parent=None, name=None):
        QDialog.__init__(self, parent, name)
        self.setCaption("APP")
        mainLayout = QHBoxLayout(self)

        lv = PListView(self)
        mainLayout.addWidget(lv)

        lvi = PListViewItem(lv, "name", "Mesaj")
        lv.add(lvi)
        lvi.addWidgetItem(PListViewItem.PLVIconButtonType, ["help"])
        lvi.addWidgetItem(PListViewItem.PLVIconButtonType, ["configure"])
        lvi.addWidgetItem(PListViewItem.PLVRadioButtonType, None)
        lvi.addWidgetItem(PListViewItem.PLVRadioButtonType, None)
        lvi.addWidgetItem(PListViewItem.PLVRadioButtonType, None)
        lvi.addWidgetItem(PListViewItem.PLVRadioButtonType, None)

        #b1 = PLVIconButton(lvi, ["configure"])
        #lvi.widget = b1

def main(args):
    global kapp
    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)
    if not KUniqueApplication.start():
        print "This application already running"
        return
    kapp = KUniqueApplication(True, True, True)
    app = MainApplication()
    app.resize(QSize(600, 400).expandedTo(app.minimumSizeHint()))
    kapp.setMainWidget(app)
    sys.exit(app.exec_loop())

if __name__=="__main__":
        main(sys.argv)


