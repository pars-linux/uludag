#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Main window
"""

# Standard modules
import copy
import simplejson
import sys
import traceback

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_formmain import Ui_FormMain

# Dialogs
from lider.connection import DialogConnection
from lider.computer import DialogComputer
from lider.folder import DialogFolder
from lider.user import DialogUser

# Helper modules
from lider.helpers import directory
from lider.helpers import plugins
from lider.helpers import talk
from lider.helpers import wrappers


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
        self.treeComputers.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Popup for connection management
        menu = wrappers.Menu(self)
        menu.newAction("Connect", wrappers.Icon("online48"), self.__slot_connect)
        menu.newAction("Disconnect", wrappers.Icon("offline48"), self.__slot_disconnect)
        self.pushConnection.setMenu(menu)

        # Popup for new items
        self.menu = wrappers.Menu(self)
        self.menu.newAction("New Folder", wrappers.Icon("folder48"), self.__slot_new_folder)
        self.menu.newAction("New Computer", wrappers.Icon("computer48"), self.__slot_new_computer)
        self.menu.newAction("New User", wrappers.Icon("user48"), self.__slot_new_user)

        # Backends
        self.talk = talk.Talk()
        self.directory = directory.Directory()

        # Backend statuses
        self.status_directory = "offline"
        self.status_talk = "offline"

        # UI events
        self.connect(self.talk, QtCore.SIGNAL("stateChanged(int)"), self.__slot_talk_state)
        self.connect(self.talk, QtCore.SIGNAL("messageFetched(QString, QString, QString)"), self.__slot_talk_message)
        self.connect(self.talk, QtCore.SIGNAL("userStatusChanged(QString, int)"), self.__slot_talk_status)
        self.connect(self.pushMain, QtCore.SIGNAL("clicked()"), self.__slot_main)
        self.connect(self.pushDebug, QtCore.SIGNAL("toggled(bool)"), self.__slot_debug)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.__slot_tree_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.__slot_tree_double_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.__slot_tree_expand)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.__slot_tree_collapse)
        self.connect(self.treeComputers, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__slot_tree_menu)
        self.connect(self.pushApply, QtCore.SIGNAL("clicked()"), self.__slot_apply)
        self.connect(self.pushReset, QtCore.SIGNAL("clicked()"), self.__slot_reset)
        self.connect(self.pushOK, QtCore.SIGNAL("clicked()"), self.__slot_ok)

        # Initialize "talk" backend
        self.talk.start()

        # Directory nodes
        self.item = None
        self.policy = {}
        self.nodes_cn = {}
        self.nodes_dn = {}

        # Load plugins
        self.__load_plugins()

        # Reset UI
        self.__update_toolbar()
        self.__slot_debug(False)

    def closeEvent(self, event):
        """
            Things to do when window is closed.
        """
        # TODO: Disconnect
        event.accept()

    def __update_icon(self, name, status=None):
        """
            Updates Talk status of a directory node.

            Arguments:
                name: Node name
                status: talk.Online, talk.Offline (or None)
        """
        name = name.lower()
        if name in self.nodes_cn:
            if not status:
                if name in self.talk.online:
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
            if status == "online":
                self.__log("Directory connection established.", "directory", "info")
            elif status == "offline":
                self.__log("Directory connection closed.", "directory", "info")
            elif status == "error":
                self.__log("Directory connection error.", "directory", "error")
        elif backend == "talk":
            self.status_talk = status
            if status == "online":
                self.__log("XMPP connection established.", "talk", "info")
            elif status == "offline":
                self.__log("XMPP connection closed.", "talk", "info")
            elif status == "error":
                self.__log("XMPP connection error.", "talk", "error")

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
        if self.directory.is_connected:
            self.pushMain.setEnabled(True)
        else:
            self.pushMain.setEnabled(False)
        if self.stackedWidget.currentIndex() == 0:
            # Disable unnecessary buttons
            if self.item:
                self.pushPluginGlobal.setEnabled(True)
                self.pushPluginItem.setEnabled(True)
            else:
                self.pushPluginItem.setEnabled(False)
                if self.directory.is_connected:
                    self.pushPluginGlobal.setEnabled(True)
                else:
                    self.pushPluginGlobal.setEnabled(False)
            # Show network information
            self.pixmapPlugin.setPixmap(self.windowIcon().pixmap(48))
            if self.directory.is_connected:
                domain_label = "Network: %s" % self.directory.domain
                domain_desc = "Connected as %s" % self.directory.user.capitalize()
                if self.directory_label:
                    domain_label = "Network: %s" % self.directory_label
                    domain_desc = "Connected to %s as %s" % (self.directory.domain, self.directory.user.capitalize())
                self.labelPlugin.setText(domain_label)
                self.labelPluginDesc.setText(domain_desc)
            else:
                self.labelPlugin.setText("Lider")
                self.labelPluginDesc.setText("")
            # Hide button box
            self.frameButtons.hide()
        else:
            widget = self.stackedWidget.currentWidget()
            # Disable unnecessary buttons
            if widget.get_type() == plugins.TYPE_GLOBAL:
                self.pushPluginItem.setEnabled(False)
            else:
                self.pushPluginItem.setEnabled(True)
            # Show plugin information
            self.pixmapPlugin.setPixmap(widget.windowIcon().pixmap(48))
            self.labelPlugin.setText(widget.windowTitle())
            self.labelPluginDesc.setText(widget.toolTip())
            # Show button box
            self.frameButtons.show()

    def __load_plugins(self):
        """
            Loads plugins
        """

        # Popup for global plugins
        menu_global = wrappers.Menu(self)

        # Popup for single object plugins
        menu_single = wrappers.Menu(self)

        for name, widget_class in plugins.load_plugins().iteritems():
            widget = widget_class()
            self.stackedWidget.addWidget(widget)
            if widget.get_type() == plugins.TYPE_GLOBAL:
                action = menu_global.newAction(widget.windowTitle(), widget.windowIcon(), self.__slot_widget_stack)
            else:
                action = menu_single.newAction(widget.windowTitle(), widget.windowIcon(), self.__slot_widget_stack)
            action.widget = widget # __slot_widget_stack method needs this

        self.pushPluginGlobal.setMenu(menu_global)
        self.pushPluginItem.setMenu(menu_single)

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
            user = dn.startswith("uid=")

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
                elif user:
                    item.setIcon(0, wrappers.Icon("user48"))
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
            # TODO: Disconnect
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

    def __log(self, text, group="normal", type_="info"):
        """
            Appends a message to log.

            Arguments:
                text: Message
                group: directory, talk (xmpp), ...
                type_: debug, info, warning, error
        """
        colors = {
            "debug": "#505050",
            "info": "#000000",
            "warning": "#dc6e00",
            "error": "#ff0000",
        }
        color = colors.get(type_, "#000000")
        self.textLog.append("<font color='%s'>%s</font>" % (color, text))

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
                traceback.print_exc()
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to connect to %s" % dialog.get_host())
                return
            try:
                self.directory_label = self.directory.get_name()
            except directory.DirectoryError:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            self.__update_status("directory", "online")
        else:
            # User cancelled
            return

        # Connect to XMPP server
        self.talk.connect(self.directory.user, self.directory.domain, self.directory.password)

        # List components
        self.__list_items()

        # Update toolbar
        self.__update_toolbar()

    def __slot_disconnect(self):
        """
            Disconnects from both backends and updates UI.
        """
        # Disconnect from directory server
        self.directory.disconnect()

        # Disconnect from XMPP server
        self.talk.disconnect()

        # Update connection status
        self.__update_status("directory", "offline")

        # Clear tree
        self.treeComputers.clear()

        # Reset selected item
        self.item = None

        # Go to first screen
        self.__slot_main()

        # Update toolbar
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

    def __slot_talk_message(self, sender, message, arguments=""):
        """
            Triggered when an XMPP message is received.

            Arguments:
                sender: Sender's JID
                command: Command
                arguments: Arguments
        """
        self.__log("XMPP message from: %s" % sender, "talk", "debug")

        if self.stackedWidget.currentIndex() != 0:
            sender = unicode(sender)
            widget = self.stackedWidget.currentWidget()
            try:
                if arguments:
                    arguments = simplejson.loads(unicode(arguments))
                else:
                    arguments = None
            except Exception, e:
                arguments = None
            try:
                widget.talk_message(sender, message, arguments)
            except Exception, e:
                pass
            except AttributeError:
                pass

    def __slot_talk_status(self, sender, status):
        """
            Triggered when an XMPP client's status is changed.

            Arguments:
                sender: Sender's JID
                state: talk.Online or talk.Offline
        """
        sender = str(sender)
        if status == talk.Online and sender not in self.talk.online:
            self.__log("XMPP user is online: %s" % sender, "talk", "debug")
        elif status == talk.Offline and sender in self.talk.online:
            self.__log("XMPP user is offline: %s" % sender, "talk", "debug")
        self.__update_icon(sender, status)

        if self.stackedWidget.currentIndex() != 0:
            widget = self.stackedWidget.currentWidget()
            try:
                widget.talk_status(sender, status)
            except AttributeError:
                pass

    def __slot_main(self):
        """
            Triggered when user clicks main button
            Return to main screen.
        """
        self.stackedWidget.setCurrentIndex(0)
        self.__update_toolbar()

    def __slot_tree_click(self, item, column):
        """
            Triggered when user clicks a node.
        """
        self.item = item
        self.__update_toolbar()

    def __slot_tree_double_click(self, item, column):
        """
            Triggered when user double clicks a node.
        """
        self.item = item

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
        item.takeChildren()

    def __slot_tree_menu(self, pos):
        """
            Triggered when user right clicks a node.
        """
        if self.item:
            self.menu.exec_(self.treeComputers.mapToGlobal(pos))

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
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to add computer.")
                return

            self.treeComputers.collapseItem(parent_item)
            self.treeComputers.expandItem(parent_item)
            item = self.nodes_cn[name]
            self.treeComputers.scrollToItem(item)
            self.treeComputers.setCurrentItem(item)

    def __slot_new_user(self):
        """
            Triggered when user wants to add a new user.
        """
        if self.item.folder:
            parent_item = self.item
        else:
            parent_item = self.item.parent()

        parent_path = parent_item.dn

        dialog = DialogUser()
        if dialog.exec_():
            name = dialog.get_name()
            password = dialog.get_password()
            uid = dialog.get_uid()
            gid = dialog.get_gid()
            home = dialog.get_home()
            try:
                dn = self.directory.add_user(parent_path, name, password, uid, gid, home)
            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to add user.")
                return

            self.treeComputers.collapseItem(parent_item)
            self.treeComputers.expandItem(parent_item)
            item = self.nodes_dn[dn]
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
                # TODO: Disconnect
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
        try:
            widget.set_item(self.item)
        except AttributeError:
            pass
        try:
            widget.set_directory(self.directory)
        except AttributeError:
            pass
        try:
            widget.set_talk(self.talk)
        except AttributeError:
            pass

        if widget.get_type() == plugins.TYPE_SINGLE:
            self.policy = self.__load_policy()
            if self.policy != None:
                widget.policy = self.policy
                try:
                    widget.load_policy(self.policy)
                except AttributeError:
                    pass

        self.stackedWidget.setCurrentWidget(widget)
        self.__update_toolbar()

    def __slot_debug(self, state):
        """
            Triggered when user toggles debug button.
        """
        if state:
            self.textLog.show()
        else:
            self.textLog.hide()

    def __slot_ok(self):
        """
            Triggered when user clicks 'save & close' button.
        """
        self.__slot_apply()
        self.__slot_main()

    def __slot_apply(self):
        """
            Triggered when user clicks 'save' button.
        """
        if self.stackedWidget.currentIndex() != 0:
            widget = self.stackedWidget.currentWidget()
            old_policy = copy.deepcopy(widget.policy)
            new_policy = copy.deepcopy(old_policy)
            try:
                for key, values in widget.dump_policy().iteritems():
                    values = copy.deepcopy(values)
                    if key == "objectClass":
                        for value in values:
                            if value not in new_policy[key]:
                                new_policy[key].append(value)
                    else:
                        new_policy[key] = values
            except AttributeError:
                return
            try:
                self.directory.modify(self.item.dn, old_policy, new_policy)
            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to modify node.")
                return
            widget.policy = new_policy

    def __slot_reset(self):
        """
            Triggered when user clicks reset button.
        """
        if self.stackedWidget.currentIndex() != 0:
            widget = self.stackedWidget.currentWidget()
            if widget.policy != None:
                try:
                    widget.load_policy(widget.policy)
                except AttributeError:
                    pass
