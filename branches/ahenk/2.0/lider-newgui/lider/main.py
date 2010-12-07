#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Main window
"""

# Standard modules
import logging
import sys

# Qt4 modules
from PyQt4 import QtCore
from PyQt4 import QtGui

# Generated UI module
from ui_main import Ui_windowMain

# Screens
#from screens.connection.bookmarks import main as screen_bookmarks
from screens.network.tree import main as screen_tree
from screens.network.search import main as screen_search
from screens.local.home import main as screen_home
from screens.local.help import main as screen_help
from screens.local.about import main as screen_about
from screens.local.logs import main as screen_logs

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
        self.__state_home()

        # Screens
        # Home
        self.widget_home = screen_home.WidgetModule(self.stackMisc)
        self.stackMisc.addWidget(self.widget_home)

        # Help
        self.widget_help = screen_help.WidgetModule(self.stackMisc)
        self.stackMisc.addWidget(self.widget_help)

        # About
        self.widget_about = screen_about.WidgetModule(self.stackMisc)
        self.stackMisc.addWidget(self.widget_about)

        # Logs
        self.widget_logs = screen_logs.WidgetModule(self.stackMisc)
        self.stackMisc.addWidget(self.widget_logs)

        # Network Tree
        self.widget_tree = screen_tree.WidgetModule(self.stackNetwork)
        self.stackNetwork.addWidget(self.widget_tree)

        # Network Search
        self.widget_search = screen_search.WidgetModule(self.stackNetwork)
        self.stackNetwork.addWidget(self.widget_search)

        # Load node screens
        self.__load_screens()

        # Logging
        self.__init_log()

        # UI events
        self.connect(self.stackScreens, QtCore.SIGNAL('currentChanged(int)'), self.__slot_screen_changed)
        #self.connect(self.actionConnection, QtCore.SIGNAL('triggered(bool)'), self.__slot_connection)
        self.connect(self.actionNetwork, QtCore.SIGNAL('triggered(bool)'), self.__slot_network_tree)
        self.connect(self.actionSearch, QtCore.SIGNAL('triggered(bool)'), self.__slot_network_search)
        self.connect(self.actionLogs, QtCore.SIGNAL('triggered(bool)'), self.__slot_logs)
        self.connect(self.actionHelp, QtCore.SIGNAL('triggered(bool)'), self.__slot_help)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered(bool)'), self.__slot_about)
        self.connect(self.widget_tree, QtCore.SIGNAL('selectedItem()'), self.__slot_node)
        self.connect(self.widget_search, QtCore.SIGNAL('selectedItem()'), self.__slot_node)

    def __init_log(self):
        """
            ...
        """
        class X(logging.StreamHandler):
            def write(_self, text):
                pass
                #self.widget_logs.treeLog.addItem(text.strip())
            def flush(_self):
                pass
        x = X()

        logging.basicConfig(level=logging.NOTSET, stream=x)
        logging.info("test 1")
        logging.info("test 2")

    def __load_screens(self):
        """
            Loads node configuration screens.
        """
        return
        # Software
        from screens.node.software import main as mainSoftware
        widget = mainSoftware.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

        # Authentication
        from screens.node.authentication import main as mainAuthentication
        widget = mainAuthentication.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

    # Screens

    def __state_network_tree(self):
        """
            Shows network tree screen.
        """
        # Jump to second screen
        self.stackScreens.setCurrentIndex(1)

        # Show network tree
        self.stackNetwork.setCurrentIndex(0)

    def __state_network_search(self):
        """
            Shows network search screen.
        """
        # Jump to second screen
        self.stackScreens.setCurrentIndex(1)

        # Show network tree
        self.stackNetwork.setCurrentIndex(1)

    def __state_node(self):
        """
            Shows node screen.
        """
        # Jump to third screen
        self.stackScreens.setCurrentIndex(2)

        # Populate mini tree
        #

        # Always expand mini tree
        item = self.treeNetwork.topLevelItem(0)
        while item:
            item.setExpanded(True)
            item = item.child(0)

    def __state_home(self):
        """
            Shows home screen.
        """
        # Jump to first screen
        self.stackScreens.setCurrentIndex(0)

        # Show home
        self.stackMisc.setCurrentIndex(0)

    def __state_help(self):
        """
            Shows help screen.
        """
        # Jump to first screen
        self.stackScreens.setCurrentIndex(0)

        # Show help
        self.stackMisc.setCurrentIndex(1)

    def __state_about(self):
        """
            Shows about screen.
        """
        # Jump to first screen
        self.stackScreens.setCurrentIndex(0)

        # Show about
        self.stackMisc.setCurrentIndex(2)

    def __state_logs(self):
        """
            Shows logs screen.
        """
        # Jump to first screen
        self.stackScreens.setCurrentIndex(0)

        # Show logs
        self.stackMisc.setCurrentIndex(3)

    # Slots

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

    def __slot_network_tree(self, checked=False):
        """
            Triggered when user clicks "Network" button.
        """
        # Show network tree interface
        self.__state_network_tree()

    def __slot_network_search(self, checked=False):
        """
            Triggered when user clicks "Search" button.
        """
        # Show network search interface
        self.__state_network_search()

    def __slot_help(self, checked=False):
        """
            Triggered when user clicks "Help" button.
        """
        # Show help interface
        self.__state_help()

    def __slot_about(self, checked=False):
        """
            Triggered when user clicks "About" button.
        """
        # Show about interface
        self.__state_about()

    def __slot_logs(self, checked=False):
        """
            Triggered when user clicks "Logs" button.
        """
        # Show logs interface
        self.__state_logs()

    def __slot_node(self):
        """
            Triggered when user clicks a node.
        """
        self.__state_node()

    # Events

    def closeEvent(self, event):
        """
            Things to do when window is closed.
        """
        event.accept()

