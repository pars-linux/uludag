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
from screens.connection.bookmarks import main as screen_bookmarks
from screens.network.tree import main as screen_tree
from screens.network.search import main as screen_search
from screens.misc.help import main as screen_help
from screens.misc.about import main as screen_about
from screens.misc.logs import main as screen_logs

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

        # Screens
        # Connection
        self.widget_connection = screen_bookmarks.WidgetModule(self.stackConnection)
        self.stackConnection.addWidget(self.widget_connection)

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

        # State machine
        self.__init_state_machine()

        # Load node screens
        self.__load_screens()

        # Logging
        self.__init_log()

        # UI events
        self.connect(self.stackScreens, QtCore.SIGNAL('currentChanged(int)'), self.__slot_screen_changed)
        self.connect(self.actionNetwork, QtCore.SIGNAL('triggered(bool)'), self.__slot_network_tree)
        self.connect(self.actionSearch, QtCore.SIGNAL('triggered(bool)'), self.__slot_network_search)
        self.connect(self.actionLogs, QtCore.SIGNAL('triggered(bool)'), self.__slot_logs)
        self.connect(self.actionHelp, QtCore.SIGNAL('triggered(bool)'), self.__slot_help)
        self.connect(self.actionAbout, QtCore.SIGNAL('triggered(bool)'), self.__slot_about)

        # Developer tools
        if '--dev' not in sys.argv[1:]:
            self.frameDeveloper.hide()

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

    def __init_state_machine(self):
        """
            Inializes state machine and sets transition triggers between states.
        """
        # States
        self.states = {
            'connection': QtCore.QState(),
            'network': QtCore.QState(),
            'node': QtCore.QState(),
            'misc': QtCore.QState(),
        }

        # Login -> Network transition
        self.states['connection'].addTransition(self.widget_connection, QtCore.SIGNAL('connected()'), self.states['network'])

        # Network -> Node transition
        self.states['network'].addTransition(self.widget_tree, QtCore.SIGNAL('selectedItem()'), self.states['node'])
        self.states['network'].addTransition(self.widget_search, QtCore.SIGNAL('selectedItem()'), self.states['node'])

        # * -> Login transition
        for key in self.states:
            if key != 'connection':
                self.states[key].addTransition(self.actionConnection, QtCore.SIGNAL('triggered(bool)'), self.states['connection'])

        # * -> Misc transition
        for key in self.states:
            if key != 'misc':
                self.states[key].addTransition(self.actionLogs, QtCore.SIGNAL('triggered(bool)'), self.states['misc'])
                self.states[key].addTransition(self.actionHelp, QtCore.SIGNAL('triggered(bool)'), self.states['misc'])
                self.states[key].addTransition(self.actionAbout, QtCore.SIGNAL('triggered(bool)'), self.states['misc'])

        # * -> Network transition
        for key in self.states:
            if key != 'network':
                self.states[key].addTransition(self.actionNetwork, QtCore.SIGNAL('triggered(bool)'), self.states['network'])
                self.states[key].addTransition(self.actionSearch, QtCore.SIGNAL('triggered(bool)'), self.states['network'])
        self.states['node'].addTransition(self.pushNodeExit, QtCore.SIGNAL('clicked()'), self.states['network'])

        # Main machine
        self.machine = QtCore.QStateMachine()
        for name, state in self.states.iteritems():
            self.machine.addState(state)
        self.machine.setInitialState(self.states['connection'])
        self.machine.start()

        # Events
        self.connect(self.states['connection'], QtCore.SIGNAL('entered()'), self.__slot_state_connection)
        self.connect(self.states['network'], QtCore.SIGNAL('entered()'), self.__slot_state_network)
        self.connect(self.states['node'], QtCore.SIGNAL('entered()'), self.__slot_state_node)
        self.connect(self.states['misc'], QtCore.SIGNAL('entered()'), self.__slot_state_misc)

    def __load_screens(self):
        """
            Loads node configuration screens.
        """

        # Software
        from screens.node.software import main as mainSoftware
        widget = mainSoftware.WidgetModule(self.stackNode)
        self.stackNode.addWidget(widget)

        # Authentication
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

    def __slot_state_connection(self):
        """
            Triggered when state is "connection"
        """
        # Jump to first screen
        self.stackScreens.setCurrentIndex(0)

        # Disable network buttons
        self.actionNetwork.setEnabled(False)
        self.actionSearch.setEnabled(False)

    def __slot_state_network(self):
        """
            Triggered when state is "network"
        """
        # Jump to second screen
        self.stackScreens.setCurrentIndex(1)

        # Enable network buttons
        self.actionNetwork.setEnabled(True)
        self.actionSearch.setEnabled(True)

    def __slot_state_node(self):
        """
            Triggered when state is "node"
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

    def __slot_state_misc(self):
        """
            Triggered when state is "misc"
        """
        # Jump to first screen
        self.stackScreens.setCurrentIndex(3)

    def __slot_network_tree(self, checked=False):
        """
            Triggered when user clicks "Network" button.
        """
        # Show network tree interface
        self.stackNetwork.setCurrentIndex(0)

    def __slot_network_search(self, checked=False):
        """
            Triggered when user clicks "Search" button.
        """
        # Show search interface
        self.stackNetwork.setCurrentIndex(1)

    def __slot_help(self, checked=False):
        """
            Triggered when user clicks "Help" button.
        """
        # Show help interface
        self.stackMisc.setCurrentIndex(0)

    def __slot_about(self, checked=False):
        """
            Triggered when user clicks "About" button.
        """
        # Show about interface
        self.stackMisc.setCurrentIndex(1)

    def __slot_logs(self, checked=False):
        """
            Triggered when user clicks "Logs" button.
        """
        # Show logs interface
        self.stackMisc.setCurrentIndex(2)
