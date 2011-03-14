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
from lider.search import DialogSearch
from lider.user import DialogUser

# Helper modules
from lider.helpers import directory
from lider.helpers import plugins
from lider.helpers import talk
from lider.helpers import wrappers

# Custom widgets
from widgets.list_item import list_item


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
        self.treeSummary.hide()

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
        self.menu.newAction("Delete", wrappers.Icon("edit-delete"), self.__slot_delete)

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
        self.connect(self.pushSearch, QtCore.SIGNAL("clicked()"), self.__slot_search)

        self.connect(self.treeComputers, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.__slot_tree_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.__slot_tree_double_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.__slot_tree_expand)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.__slot_tree_collapse)
        self.connect(self.treeComputers, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__slot_tree_menu)

        self.connect(self.treeSummary, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.__slot_tree2_expand)
        self.connect(self.treeSummary, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.__slot_tree2_collapse)
        self.connect(self.treeSummary, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.__slot_tree2_click)
        self.connect(self.treeSummary, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.__slot_tree2_double_click)


        self.connect(self.pushSave, QtCore.SIGNAL("clicked()"), self.__slot_save)
        self.connect(self.pushReset, QtCore.SIGNAL("clicked()"), self.__slot_reset)
        self.connect(self.pushApply, QtCore.SIGNAL("clicked()"), self.__slot_apply)

        # Initialize "talk" backend
        self.talk.start()

        # Selected items
        self.items = []

        # Last fetched olicy
        self.policy = {}

        # Directory nodes
        self.nodes_cn = {}
        self.nodes_dn = {}

        self.nodes_alt_cn = {}
        self.nodes_alt_dn = {}

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
                node.widget.set_status_icon(wrappers.Icon("online48"))
            else:
                node.widget.set_status_icon()

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
        self.framePolicyInherit.hide()
        self.frameMulti.hide()
        if self.directory.is_connected:
            self.pushMain.setEnabled(True)
            self.pushSearch.setEnabled(True)
        else:
            self.pushMain.setEnabled(False)
            self.pushSearch.setEnabled(False)
        if self.stackedWidget.currentIndex() == 0:
            # Disable unnecessary buttons
            if len(self.items):
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

    def  __list_items(self, root=None, alternative=False):
        if not root:
            if alternative:
                root_alt = QtGui.QTreeWidgetItem(self.treeSummary)
                root_alt.setText(0, unicode(self.directory.get_name()))
                root_alt.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
                root_alt.dn = self.directory.directory_domain
                root_alt.name = root_alt.dn.split(",")[0].split("=")[1]
                root_alt.folder = True
                self.nodes_alt_dn[root_alt.dn] = root_alt
            else:
                root = list_item.add_tree_item(self.treeComputers, self.directory.directory_domain, self.directory.get_name(), self.directory.directory_domain, icon=wrappers.Icon("folder48"))
                root.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
                root.dn = self.directory.directory_domain
                root.name = root.dn.split(",")[0].split("=")[1]
                root.folder = True
                self.nodes_dn[root.dn] = root

            return

        dn = root.dn

        results = self.directory.search(dn, ["o", "cn", "description"], "one")
        fancy = len(results) < 100
        for dn, attrs in results:
            name = dn.split(",")[0].split("=")[1]
            label = name
            folder = dn.startswith("dc=")
            user = dn.startswith("uid=")

            if "description" in attrs:
                description = attrs["description"][0]
            else:
                description = ""

            if folder and "o" in attrs:
                label = attrs["o"][0]

            if alternative:
                item = QtGui.QTreeWidgetItem(root)
                item.setText(0, unicode(label))
            else:
                item = list_item.add_tree_item(root, dn, label, description, icon=wrappers.Icon("computer48"))

            item.dn = dn
            item.name = name
            item.folder = folder

            if alternative:
                self.nodes_alt_dn[dn] = item
            else:
                self.nodes_dn[dn] = item

            if folder:
                if alternative:
                    item.setIcon(0, wrappers.Icon("folder48"))
                    item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
                else:
                    item.widget.set_icon(wrappers.Icon("folder48"))
                    item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
            elif user:
                if alternative:
                    item.setIcon(0, wrappers.Icon("user48"))
                else:
                    item.widget.set_icon(wrappers.Icon("user48"))
            else:
                if alternative:
                    item.setIcon(0, wrappers.Icon("computer48"))
                else:
                    self.nodes_cn[name] = item
                    self.__update_icon(name)

    def __load_policy(self, item=None):
        """
            Returns policy of selected tree node.
        """
        if item:
            dn = item.dn
        else:
            if len(self.items) == 1:
                dn = self.items[0].dn
            else:
                return {}

        try:
            results = self.directory.search(dn, scope="base")
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
        self.__list_items(alternative=True)

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
        self.items = []

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
        self.treeSummary.hide()
        self.__update_toolbar()

    def __slot_tree_click(self, item, column):
        """
            Triggered when user clicks a node.
        """
        self.items = []
        for i in self.treeComputers.selectedItems():
            self.items.append(i)

        self.__update_toolbar()

        self.treeSummary.clearSelection()

        for item in self.items:
            item_alt = self.nodes_alt_dn[item.dn]
            self.treeSummary.setItemSelected(item_alt, True)

    def __slot_tree_double_click(self, item, column):
        """
            Triggered when user double clicks a node.
        """
        self.items = [item]

    def __slot_tree_expand(self, item):
        """
            Triggered when user expands a node.
        """
        self.__list_items(item)

        item_alt = self.nodes_alt_dn[item.dn]
        self.treeSummary.expandItem(item_alt)

        if item.childCount() == 0:
            item.setExpanded(False)

    def __slot_tree_collapse(self, item):
        """
            Triggered when user collapses a node.
        """
        item.takeChildren()

        item_alt = self.nodes_alt_dn[item.dn]
        self.treeSummary.collapseItem(item_alt)

    def __slot_tree2_click(self, item, column):
        """
            Triggered when user clicks a node.
        """
        self.items = []
        for i in self.treeSummary.selectedItems():
            self.items.append(i)

        self.__update_toolbar()

        self.treeComputers.clearSelection()

        for item in self.items:
            item_alt = self.nodes_dn[item.dn]
            self.treeComputers.setItemSelected(item_alt, True)

        widget = self.stackedWidget.currentWidget()
        self.__show_widget(widget)

    def __slot_tree2_double_click(self, item, column):
        """
            Triggered when user double clicks a node.
        """
        self.items = [item]

    def __slot_tree2_expand(self, item):
        """
            Triggered when user expands a node.
        """
        self.__list_items(item, True)

        item_alt = self.nodes_dn[item.dn]
        self.treeComputers.expandItem(item_alt)

        if item.childCount() == 0:
            item.setExpanded(False)

    def __slot_tree2_collapse(self, item):
        """
            Triggered when user collapses a node.
        """
        item.takeChildren()

        item_alt = self.nodes_dn[item.dn]
        self.treeComputers.collapseItem(item_alt)

    def __slot_tree_menu(self, pos):
        """
            Triggered when user right clicks a node.
        """
        item = self.treeComputers.itemAt(pos)
        if item:
            self.items = [item]
            self.treeComputers.setCurrentItem(item)
            self.menu.exec_(self.treeComputers.mapToGlobal(pos))

    def __slot_delete(self):
        """
            Triggered when user wants to delete an item
        """
        if len(self.items) != 1:
            QtGui.QMessageBox.warning(self, "Warning", "Only one item at a time can be deleted.")

        item = self.items[0]

        dn = item.dn
        results = self.directory.search(dn, scope="one", fields=["objectClass"])

        if dn.startswith('dc=') and len(results) > 0:
            QtGui.QMessageBox.warning(self, "Warning", "The selected item is a non-empty directory. It cannot be deleted.")
        else:
            msg = str()
            reply = QtGui.QMessageBox.question(self, "Warning", "This is not undoable. Are you sure you want to remove?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No )
            if reply == QtGui.QMessageBox.Yes:
                try:
                    self.directory.delete_item(dn)
                    index = item.parent().indexOfChild(self.treeComputers.currentItem())
                    item.parent().takeChild(index)

                except directory.DirectoryConnectionError:
                    self.__update_status("directory", "error")
                    # TODO: Disconnect
                    QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                    return
                except directory.DirectoryError:
                    QtGui.QMessageBox.warning(self, "Connection Error", "Unable to delete item.")
                    return

    def __slot_new_computer(self):
        """
            Triggered when user wants to add a new computer.
        """
        item = self.items[0]

        if item.folder:
            parent_item = item
        else:
            parent_item = item.parent()

        parent_path = parent_item.dn

        dialog = DialogComputer()
        if dialog.exec_():
            name = dialog.get_name()
            password = dialog.get_password()
            description = dialog.get_description()
            try:
                self.directory.add_computer(parent_path, name, password, description)
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
        item = self.items[0]

        if item.folder:
            parent_item = item
        else:
            parent_item = item.parent()

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
        item = self.items[0]

        if item.folder:
            parent_item = item
        else:
            parent_item = item.parent()

        parent_path = parent_item.dn

        dialog = DialogFolder()
        if dialog.exec_():
            name = dialog.get_name()
            label = dialog.get_label()
            description = dialog.get_description()
            try:
                self.directory.add_folder(parent_path, name, label, description)
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
        self.__show_widget(widget)

    def __show_widget(self, widget):
        """
            Shows a widget
        """
        policy_match = False
        policy_inherit = True
        self.treeSummary.show()

        if len(self.items) == 1:
            item = self.items[0]
        else:
            item = None

        if item and widget.get_type() == plugins.TYPE_SINGLE:
            paths = self.directory.get_parent_paths(item.dn)
            self_path = paths[-1]
            classes = {}
            for path in paths:
                search = self.directory.search(path, ["objectClass"], "base")
                if len(search):
                    classes[path] = []
                    for oclass in search[0][1]["objectClass"]:
                        if oclass.endswith("Policy"):
                            classes[path].append(oclass)

            widget_classes = widget.get_classes()
            self_policies = classes[self_path]

            for path, policies in classes.iteritems():
                if self_path == path:
                    continue
                if len(set(widget_classes).intersection(set(policies))) > 0:
                    policy_match = True
                    if len(set(self_policies).intersection(set(widget_classes))) > 0:
                        policy_inherit = False
                    break

        try:
            widget.set_item(item)
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
            if item and (item.name in self.talk.online) or item.folder:
                self.pushApply.show()
            else:
                self.pushApply.hide()
            self.policy = self.__load_policy()
            if self.policy != None:
                widget.policy = self.policy
                try:
                    widget.load_policy(self.policy)
                except AttributeError:
                    pass

        self.stackedWidget.setCurrentWidget(widget)
        self.__update_toolbar()

        if len(self.items) > 1:
            self.frameMulti.show()

        if policy_match:
            widget.policy_match = True
            self.framePolicyInherit.show()
            if policy_inherit:
                self.radioPolicyInherit.setChecked(True)
            else:
                self.radioPolicyNoInherit.setChecked(True)
        else:
            widget.policy_match = False

    def __slot_debug(self, state):
        """
            Triggered when user toggles debug button.
        """
        if state:
            self.textLog.show()
        else:
            self.textLog.hide()

    def __slot_search(self):
        """
            Triggered when user clicks search button.
        """
        dialog = DialogSearch()
        if dialog.exec_():
            print "Searching:", dialog.get_query()

    def __slot_apply(self):
        """
            Triggered when user clicks 'save & apply' button.
        """
        def xmpp_update(_name):
            if _name in self.talk.online:
                jid = "%s@%s" % (_name, self.talk.domain)
                self.talk.send_command(jid, "ahenk.force_update")

        if self.__slot_save():
            for item in self.items:
                if item.folder:
                    for dn, attrs in self.directory.search(item.dn, scope="sub", fields=['objectClass']):
                        if dn.startswith("cn="):
                            xmpp_update(dn.split(",")[0].split("=")[1])
                else:
                    xmpp_update(item.name)

    def __slot_save(self):
        """
            Triggered when user clicks 'save' button.
        """
        if self.stackedWidget.currentIndex() == 0:
            return False

        widget = self.stackedWidget.currentWidget()

        remove = False
        if widget.policy_match:
            if self.radioPolicyInherit.isChecked():
                remove = True

        if len(self.items) != 1:
            for item in self.items:
                widget.policy = self.__load_policy(item)
                classes_now, policy_now, classes_new, policy_new = widget.mod_policy(remove=remove)

                try:
                    if remove:
                        self.directory.modify(item.dn, policy_now, policy_new)
                        self.directory.modify(item.dn, {"objectClass": classes_now}, {"objectClass": classes_new})
                    else:
                        self.directory.modify(item.dn, {"objectClass": classes_now}, {"objectClass": classes_new})
                        self.directory.modify(item.dn, policy_now, policy_new)
                except directory.DirectoryConnectionError, e:
                    pass
                except directory.DirectoryError, e:
                    pass
        else:
            item = self.items[0]

            classes_now, policy_now, classes_new, policy_new = widget.mod_policy(remove=remove)

            try:
                if remove:
                    self.directory.modify(item.dn, policy_now, policy_new)
                    self.directory.modify(item.dn, {"objectClass": classes_now}, {"objectClass": classes_new})
                else:
                    self.directory.modify(item.dn, {"objectClass": classes_now}, {"objectClass": classes_new})
                    self.directory.modify(item.dn, policy_now, policy_new)
            except directory.DirectoryConnectionError, e:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, "Connection Error", "Connection lost. Please re-connect.")
                return False
            except directory.DirectoryError, e:
                QtGui.QMessageBox.warning(self, "Connection Error", "Unable to modify node.")
                return False
            widget.policy = self.__load_policy()
            return True

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
