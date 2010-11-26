#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Main window
"""

# Standard modules
import os
import sys

# Qt4 modules
from PyQt4 import QtCore
from PyQt4 import QtGui

# Generated UI module
from ui_main import Ui_windowMain

# Helper modules
#


class WindowMain(QtGui.QMainWindow, Ui_windowMain):
    """
        Main window.

        Usage:
            win = WindowMain()
            win.show()
    """

    def __init__(self, app):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        QtGui.QMainWindow.__init__(self)

        # Application
        self.app = app

        # Attach generated UI
        self.setupUi(self)

        # Fine tune UI
        self.stackScreens.setCurrentIndex(0)

        # Load screens
        self.__load_screens()

        # UI events
        self.connect(self.stackScreens, QtCore.SIGNAL('currentChanged(int)'), self.__slot_screen_changed)
        self.connect(self.pushNextScreen, QtCore.SIGNAL('clicked()'), self.__slot_next_screen)
        self.connect(self.pushNextPage, QtCore.SIGNAL('clicked()'), self.__slot_next_page)

        # Developer tools
        if '--dev' not in sys.argv[1:]:
            self.groupDeveloper.hide()

    def closeEvent(self, event):
        """
            Things to do when window is closed.
        """
        event.accept()

    def __load_screens(self):
        """
            ...
        """

        # Screens - Local - Connection
        from screens.local.connection import main as mainConnection
        widget = mainConnection.WidgetModule(self.stackLocal)
        self.stackLocal.addWidget(widget)
        # Screens - Local - Help
        from screens.local.help import main as mainHelp
        widget = mainHelp.WidgetModule(self.stackLocal)
        self.stackLocal.addWidget(widget)

        # Screens - Network - Tree
        from screens.network.tree import main as mainTree
        widget = mainTree.WidgetModule(self.stackNetwork)
        self.stackNetwork.addWidget(widget)

        # Screens - Network - Search
        from screens.network.search import main as mainSearch
        widget = mainSearch.WidgetModule(self.stackNetwork)
        self.stackNetwork.addWidget(widget)

        # Screens - Node - Software
        from screens.node.software import main as mainSoftware
        widget = mainSoftware.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

        # Screens - Node - Authentication
        from screens.node.authentication import main as mainAuthentication
        widget = mainAuthentication.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

    def __slot_screen_changed(self, index):
        """
            Triggered when screen is changed.
        """
        widget = self.stackScreens.widget(index)
        if widget.objectName() == 'pageNode':
            # Remove previously added mini network widget(s)
            while self.stackMiniNetwork.count() > 0:
                mini_widget = self.stackMiniNetwork.currentWidget()
                self.stackMiniNetwork.removeWidget(mini_widget)
            # Add mini widget of active network widget
            net_widget = self.stackNetwork.currentWidget()
            mini_widget = net_widget.get_mini(self.stackMiniNetwork)
            self.stackMiniNetwork.addWidget(mini_widget)

    def __slot_next_screen(self):
        """
            Triggered when developer clicks "Next screen" button.
        """
        count = self.stackScreens.count()
        ix = self.stackScreens.currentIndex() + 1
        self.stackScreens.setCurrentIndex(ix % count)

    def __slot_next_page(self):
        """
            Triggered when developer clicks "Next page" button.
        """
        ix = self.stackScreens.currentIndex()

        if ix == 0:
            widget = self.stackLocal
        elif ix == 1:
            widget = self.stackNetwork
        elif ix == 2:
            widget = self.stackNode

        count = widget.count()
        ix = widget.currentIndex() + 1
        widget.setCurrentIndex(ix % count)
