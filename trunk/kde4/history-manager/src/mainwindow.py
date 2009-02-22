#!/usr/bin/python
# -*- coding: utf-8 -*-

from ui_mainwindow import Ui_MainManager


class MainManager(QtGui.QWidget):
    def __init__(self, parent, standAlone=True):
        QtGui.QWidget.__init__(self, parent)

        self.ui = Ui_MainManager()

        if standAlone:
            self.ui.setupUi(self)
        else:
            self.ui.setupUi(parent)

        self.link = comar.Link()

    def getServices(self):
        self.link.listenSignals("System.Manager", self.handler)
        # Get service list from comar link
        # self.link.System.Service.info(async=self.handleServices)

    def handler(self, package, signal, args):
        print(package)
        print(signal)
        print(args)

        #self.widgets[package].setState(args[1])
        # print args, signal, package

