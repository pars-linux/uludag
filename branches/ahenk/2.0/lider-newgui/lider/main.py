#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Main window
"""

# Standard modules
import logging
import os
import sys
import StringIO

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

        # States
        self.states = {
            'login': QtCore.QState(),
            'network': QtCore.QState(),
            'node': QtCore.QState(),
            'help': QtCore.QState(),
        }

        self.connect(self.states['login'], QtCore.SIGNAL('entered()'), self.__slot_state_login)
        self.connect(self.states['network'], QtCore.SIGNAL('entered()'), self.__slot_state_network)
        self.connect(self.states['node'], QtCore.SIGNAL('entered()'), self.__slot_state_node)
        self.connect(self.states['help'], QtCore.SIGNAL('entered()'), self.__slot_state_help)

        # Load screens
        self.__load_screens()

        # State machine
        self.machine = QtCore.QStateMachine()
        for name, state in self.states.iteritems():
            self.machine.addState(state)
        self.machine.setInitialState(self.states['login'])
        self.machine.start()

        # Logging
        self.__init_log()

        # UI events
        self.connect(self.stackScreens, QtCore.SIGNAL('currentChanged(int)'), self.__slot_screen_changed)
        self.connect(self.pushNetwork, QtCore.SIGNAL('clicked()'), self.__slot_network_tree)
        self.connect(self.pushSearch, QtCore.SIGNAL('clicked()'), self.__slot_network_search)

        # Developer tools
        if '--dev' not in sys.argv[1:]:
            self.groupDeveloper.hide()

    def closeEvent(self, event):
        """
            Things to do when window is closed.
        """
        event.accept()

    def __init_log(self):
        """
            ...
        """
        class X(logging.StreamHandler):
            def write(_self, text):
                self.listLog.addItem(text.strip())
            def flush(_self):
                pass
        x = X()

        logging.basicConfig(level=logging.NOTSET, stream=x)
        logging.info("test 1")
        logging.info("test 2")

    def __load_screens(self):
        """
            ...
        """

        # Screens - Local - Connection
        from screens.local.connection import main as mainConnection
        widget = mainConnection.WidgetModule(self.stackLocal)
        self.stackLocal.addWidget(widget)

        # Login -> Network transition
        self.states['login'].addTransition(widget, QtCore.SIGNAL('connected()'), self.states['network'])

        # Screens - Local - Help
        from screens.local.help import main as mainHelp
        widget = mainHelp.WidgetModule(self.stackLocal)
        self.stackLocal.addWidget(widget)

        # Screens - Network - Tree
        from screens.network.tree import main as mainTree
        widget = mainTree.WidgetModule(self.stackNetwork)
        self.stackNetwork.addWidget(widget)

        # Network -> Node transition
        self.states['network'].addTransition(widget, QtCore.SIGNAL('selectedItem()'), self.states['node'])

        # Screens - Network - Search
        from screens.network.search import main as mainSearch
        widget = mainSearch.WidgetModule(self.stackNetwork)
        self.stackNetwork.addWidget(widget)

        # Network -> Node transition
        self.states['network'].addTransition(widget, QtCore.SIGNAL('selectedItem()'), self.states['node'])

        # Screens - Node - Software
        from screens.node.software import main as mainSoftware
        widget = mainSoftware.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

        # Screens - Node - Authentication
        from screens.node.authentication import main as mainAuthentication
        widget = mainAuthentication.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

        # * -> Login transition
        for key in self.states:
            if key != 'login':
                self.states[key].addTransition(self.pushConnect, QtCore.SIGNAL('clicked()'), self.states['login'])

        # * -> Help transition
        for key in self.states:
            if key != 'help':
                self.states[key].addTransition(self.pushHelp, QtCore.SIGNAL('clicked()'), self.states['help'])

        # * -> Network
        for key in self.states:
            if key != 'network':
                self.states[key].addTransition(self.pushNetwork, QtCore.SIGNAL('clicked()'), self.states['network'])
                self.states[key].addTransition(self.pushSearch, QtCore.SIGNAL('clicked()'), self.states['network'])
        self.states['node'].addTransition(self.pushNodeExit, QtCore.SIGNAL('clicked()'), self.states['network'])

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

    def __slot_state_login(self):
        """
            Triggered when state is "login"
        """
        self.stackScreens.setCurrentIndex(0)
        self.stackLocal.setCurrentIndex(0)
        self.pushNetwork.setEnabled(False)
        self.pushSearch.setEnabled(False)

    def __slot_state_network(self):
        """
            Triggered when state is "network"
        """
        self.stackScreens.setCurrentIndex(1)
        self.pushNetwork.setEnabled(True)
        self.pushSearch.setEnabled(True)

    def __slot_state_node(self):
        """
            Triggered when state is "node"
        """
        self.stackScreens.setCurrentIndex(2)

    def __slot_state_help(self):
        """
            Triggered when state is "help"
        """
        self.stackScreens.setCurrentIndex(0)
        self.stackLocal.setCurrentIndex(1)

    def __slot_network_tree(self):
        """
            Triggered when user clicks "Network" button.
        """
        self.stackNetwork.setCurrentIndex(0)

    def __slot_network_search(self):
        """
            Triggered when user clicks "Search" button.
        """
        self.stackNetwork.setCurrentIndex(1)
