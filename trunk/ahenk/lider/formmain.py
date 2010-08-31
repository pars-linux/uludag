#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Main window
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from ui_formmain import Ui_FormMain

# Connection dialog
from connection import DialogConnection
from computer import DialogComputer
from folder import DialogFolder

# Helper modules
from helpers import directory
from helpers import plugins
from helpers import talk
from helpers import wrappers


class FormMain(QtGui.QWidget, Ui_FormMain):
    """
        Main window.

        Usage:
            win = FormMain()
            win.show()
    """

    def __init__(self, app):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        QtGui.QWidget.__init__(self)

        # Application
        self.app = app

        # Attach generated UI
        self.setupUi(self)

        # Fine tune UI
        self.treeComputers.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

        # Popup for connection management
        menu = wrappers.Menu(self)
        menu.newAction("Connect", wrappers.Icon("online48"), self.__slot_connect)
        menu.newAction("Disconnect", wrappers.Icon("offline48"), self.__slot_disconnect)
        self.pushConnection.setMenu(menu)

        # Popup for new items
        menu = wrappers.Menu(self)
        menu.newAction("New Folder", wrappers.Icon("folder48"), self.__slot_new_folder)
        menu.newAction("New Computer", wrappers.Icon("computer48"), self.__slot_new_computer)
        self.pushNew.setMenu(menu)

        # Backends
        self.talk = talk.Talk()
        self.directory = directory.Directory()

        # Backend statuses
        self.status_directory = "offline"
        self.status_talk = "offline"

        # UI events
        self.connect(self.talk, QtCore.SIGNAL("stateChanged(int)"), self.__slot_talk_state)
        self.connect(self.talk, QtCore.SIGNAL("messageFetched(QString, QString)"), self.__slot_talk_message)
        self.connect(self.talk, QtCore.SIGNAL("userStatusChanged(QString, int)"), self.__slot_talk_status)
        self.connect(self.pushMain, QtCore.SIGNAL("clicked()"), self.__slot_main)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.__slot_tree_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.__slot_tree_expand)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.__slot_tree_collapse)

        # Initialize "talk" backend
        self.talk_online = []
        self.talk.start()

        # Directory nodes
        self.item = None
        self.policy = {}
        self.nodes_cn = {}
        self.nodes_dn = {}

        # Load plugins
        self.__load_plugins()

        # Reset UI
        self.__slot_disconnect()

    def closeEvent(self, event):
        """
            Things to do when window is closed.
        """
        self.__slot_disconnect()
        event.accept()

    def __update_icon(self, name, status=None):
        """
            Updates Talk status of a directory node.

            Arguments:
                name: Node name
                status: talk.Online, talk.Offline or None
        """
        name = name.lower()
        if name in self.nodes_cn:
            if not status:
                if name in self.talk_online:
                    status = talk.Online
                else:
                    status = talk.Offline
            node = self.nodes_cn[name]
            if status == talk.Online:
                icon = wrappers.Icon("computer48", 32, [("online8", 1, 1)])
            else:
                icon = wrappers.Icon("computer48")
            node.setIcon(0, icon)

    def __update_status(self, backend, status):
        """
            Updates backend statuses.

            Arguments:
                backend: Name of backend (talk, directory)
                status: Status (online, offline, error)
        """
        if backend == "directory":
            self.status_directory = status
        elif backend == "talk":
            self.status_talk = status

        if self.status_directory == "offline":
            icon = wrappers.Icon("offline48")
        elif self.status_directory == "error":
            icon = wrappers.Icon("error48")
        elif self.status_directory == "online":
            if self.status_talk == "online":
                icon = wrappers.Icon("online48")
            else:
                icon = wrappers.Icon("partial48")
        self.pushConnection.setIcon(icon)

    def __update_toolbar(self):
        """
            Updates status of toolbar.
        """
        if self.item:
            self.pushPolicies.setEnabled(True)
            self.pushNew.setEnabled(True)
        else:
            self.pushPolicies.setEnabled(False)
            self.pushNew.setEnabled(False)

    def __update_pluginbar(self):
        """
            Updates plugin information bar.
        """
        if self.stackedWidget.currentIndex() == 0:
            self.framePlugin.hide()
        else:
            widget = self.stackedWidget.currentWidget()
            self.pixmapPlugin.setPixmap(widget.windowIcon().pixmap(48))
            self.labelPlugin.setText(widget.windowTitle())
            self.labelPluginDesc.setText(widget.toolTip())
            self.framePlugin.show()

    def __load_plugins(self):
        """
            Loads plugins
        """

        # Popup for plugins
        menu = wrappers.Menu(self)

        for name, widget_class in plugins.load_plugins().iteritems():
            widget = widget_class()
            self.stackedWidget.addWidget(widget)
            action = menu.newAction(widget.windowTitle(), widget.windowIcon(), self.__slot_widget_stack)
            action.widget = widget # __slot_widget_stack method needs this

        self.pushPolicies.setMenu(menu)

    def  __list_items(self, root=None):
        if not root:
            root = QtGui.QTreeWidgetItem(self.treeComputers)
            root.dn = self.directory.directory_domain
            root.name = root.dn.split(",")[0].split("=")[1]
            root.folder = True
            root.setText(0, self.directory.get_name())
            root.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
            root.setIcon(0, wrappers.Icon("folder48"))
            return

        dn = root.dn

        results = self.directory.search(dn, ["o", "cn"], "one")
        fancy = len(results) < 100
        for dn, attrs in results:
            name = dn.split(",")[0].split("=")[1]
            label = name
            folder = dn.startswith("dc=")

            if folder and "o" in attrs:
                label = attrs["o"][0]

            item = QtGui.QTreeWidgetItem(root)
            item.dn = dn
            item.name = name
            item.folder = folder
            item.setText(0, label)

            self.nodes_dn[dn] = item

            if fancy:
                if folder:
                    item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
                    item.setIcon(0, wrappers.Icon("folder48"))
                else:
                    self.nodes_cn[name] = item
                    self.__update_icon(name)

    def __load_policy(self):
        """
            Returns policy of selected tree node.
        """
        if not self.item:
            return None
        try:
            results = self.directory.search(self.item.dn, scope="base")
        except directory.DirectoryConnectionError:
            self.__update_status("directory", "error")
            self.__slot_disconnect()
            QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
            return None
        except directory.DirectoryError:
            QtGui.QMessageBox.warning(self, "Connection Error", "Unable to get policy.")
            return None
        if len(results):
            dn, attrs = results[0]
            return attrs
        else:
            return {}

    # Events

    def __slot_connect(self):
        """
            Opens a dialog and tries to connect both backends
        """
        dialog = DialogConnection()
        if self.directory.host:
            # Fill fields if necessary
            dialog.set_host(self.directory.host)
            dialog.set_domain(self.directory.domain)
            dialog.set_user(self.directory.user)
            dialog.set_password(self.directory.password)
        if dialog.exec_():
            try:
                self.directory.connect(dialog.get_host(), dialog.get_domain(), dialog.get_user(), dialog.get_password())
            except directory.DirectoryError:
                self.__update_status("directory", "offline")
                self.__slot_disconnect()
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to connect to %s" % dialog.get_host())
                return
            try:
                directory_label = self.directory.get_name()
            except directory.DirectoryError:
                self.__update_status("directory", "error")
                self.__slot_disconnect()
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            self.__update_status("directory", "online")
        else:
            # User cancelled
            return

        # Connect to XMPP server
        self.talk.connect(self.directory.user, self.directory.domain, self.directory.password)

        # Set labels
        domain_label = "Network: %s" % self.directory.domain
        domain_desc = "Connected as %s" % self.directory.user.capitalize()
        if directory_label:
            domain_label = "Network: %s" % directory_label
            domain_desc = "Connected to %s as %s" % (self.directory.domain, self.directory.user.capitalize())
        self.labelTarget.setText(domain_label)
        self.labelTargetDesc.setText(domain_desc)

        # Enable main toolbar
        self.frameTools.setEnabled(True)

        # List components
        self.__list_items()

    def __slot_disconnect(self):
        """
            Disconnects from both backends and updates UI.
        """
        # Disconnect from XMPP server
        self.talk.disconnect()

        # Update connection status
        self.__update_status("directory", "offline")

        # Clear network labels
        self.labelTarget.setText("Remote Management Console")
        self.labelTargetDesc.setText("")

        # Disable main toolbar
        self.frameTools.setEnabled(False)

        # Clear tree
        self.treeComputers.clear()

        # Reset selected item
        self.item = None

        # Update toolbar and plugin information bars
        self.__update_pluginbar()
        self.__update_toolbar()

    def __slot_talk_state(self, state):
        """
            Triggered when XMPP connection status is changed.

            Arguments:
                state: talk.Online, talk.Offline or talk.Error)
        """
        if state == talk.Online:
            self.__update_status("talk", "online")
        elif state == talk.Offline:
            self.__update_status("talk", "offline")
        elif state == talk.Error:
            self.__update_status("talk", "error")

    def __slot_talk_message(self, sender, message):
        """
            Triggered when an XMPP message is received.

            Arguments:
                sender: Sender's JID
                message: Message content
        """
        self.talk.send_message(str(sender), "You said: %s" % message)

    def __slot_talk_status(self, sender, status):
        """
            Triggered when an XMPP client's status is changed.

            Arguments:
                sender: Sender's JID
                state: talk.Online or talk.Offline
        """
        username = str(sender).split("@")[0].lower()
        if status == talk.Online and username not in self.talk_online:
            self.talk_online.append(username)
        elif status == talk.Offline and username in self.talk_online:
            self.talk_online.remove(username)
        self.__update_icon(username, status)

    def __slot_main(self):
        """
            Triggered when user clicks main button
            Return to main screen.
        """
        self.stackedWidget.setCurrentIndex(0)
        self.__update_pluginbar()

    def __slot_tree_click(self, item, column):
        """
            Triggered when user clicks a node.
        """
        self.item = item
        self.__update_toolbar()

    def __slot_tree_expand(self, item):
        """
            Triggered when user expands a node.
        """
        self.__list_items(item)
        if item.childCount() == 0:
            item.setExpanded(False)

    def __slot_tree_collapse(self, item):
        """
            Triggered when user collapses a node.
        """
        for i in range(item.childCount()):
            node = item.takeChild(i)
            del node

    def __slot_new_computer(self):
        """
            Triggered when user wants to add a new computer.
        """
        if self.item.folder:
            parent_item = self.item
        else:
            parent_item = self.item.parent()

        parent_path = parent_item.dn

        dialog = DialogComputer()
        if dialog.exec_():
            name = dialog.get_name()
            password = dialog.get_password()
            try:
                self.directory.add_computer(parent_path, name, password)
            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                self.__slot_disconnect()
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to add folder.")
                return

            self.treeComputers.collapseItem(parent_item)
            self.treeComputers.expandItem(parent_item)
            item = self.nodes_cn[name]
            self.treeComputers.scrollToItem(item)
            self.treeComputers.setCurrentItem(item)

    def __slot_new_folder(self):
        """
            Triggered when user wants to add a new folder.
        """
        if self.item.folder:
            parent_item = self.item
        else:
            parent_item = self.item.parent()

        parent_path = parent_item.dn

        dialog = DialogFolder()
        if dialog.exec_():
            name = dialog.get_name()
            label = dialog.get_label()
            try:
                self.directory.add_folder(parent_path, name, label)
            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                self.__slot_disconnect()
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to add folder.")
                return

            self.treeComputers.collapseItem(parent_item)
            self.treeComputers.expandItem(parent_item)
            item = self.nodes_dn[dn]
            self.treeComputers.scrollToItem(item)
            self.treeComputers.setCurrentItem(item)


    def __slot_widget_stack(self, toggled):
        """
            Triggered when users activates a policy plugin.
        """
        widget = self.sender().widget
        self.policy = self.__load_policy()
        if self.policy != None:
            widget.load_policy(self.policy)
            self.stackedWidget.setCurrentWidget(widget)
            self.__update_pluginbar()
