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
import os

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
#from lider.ui_formmain import Ui_FormMain
from lider.main import Ui_Main

# Dialogs
from lider.connection import DialogConnection
from lider.computer import DialogComputer
from lider.folder import DialogFolder
from lider.search import DialogSearch
from lider.user import DialogUser
from lider.group import DialogGroup

# Helper modules
from lider.helpers import directory
from lider.helpers import plugins
from lider.helpers import talk
from lider.helpers import wrappers
from lider.helpers import i18n

# Plugin modules 
from lider.plugins.plugin_firewall import main

i18n = i18n.i18n

# Custom widgets
from lider.widgets.list_item import list_item

UNABLE_TO_CONNECT = 1
CONNECTION_LOST = 2

FIREWALL_FILE = "/usr/share/ahenk-lider/firewall.fwb"

from gui import *

from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import SLOT
from PyQt4.QtCore import QThread

class PThread(QThread):
    def __init__(self, parent, action, callback=None, \
                 args=[], kwargs={}, exceptionHandler=None):
        QThread.__init__(self,parent)

        if callback:
            parent.connect(self, SIGNAL("finished()"), callback)

        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.exceptionHandler = exceptionHandler
        self.data = None

    def run(self):
        try:
            self.data = self.action(*self.args, **self.kwargs)
        except Exception, e:
            if self.exceptionHandler:
                self.exceptionHandler(e)
        finally:
            self.connect(self.parent(), SIGNAL("cleanUp()"), SLOT("deleteLater()"))

    def cleanUp(self):
        self.deleteLater()

    def get(self):
        return self.data

#class FormMain(QtGui.QWidget, Ui_FormMain):
class FormMain(QtGui.QWidget, Ui_Main):
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
        self._busy = PMessageBox(self)
        self._busy_hide_button = QPushButton(i18n("Cancel"), self._busy)
        self._busy.layout.addWidget(self._busy_hide_button)
        self._busy_hide_button.clicked.connect(self._hide_busy_message)

        self.groupGMembers.hide()
        self.groupGMembership.hide()

        # Fine tune UI
        #self.treeComputers.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
        self.treeComputers.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.treeComputers.hide()

        # Hide search
        #self.pushSearch.hide()

        # Popup for connection management
        menu = wrappers.Menu(self)
        menu.newAction(i18n("Modify Default Firewall Rules"), wrappers.Icon("firewall32"), self.__slot_modify_default_firewall_rules)
        self.pushSettings.setMenu(menu)

        # Popup for items
        self.menu = wrappers.Menu(self)
        self.menu.newAction(i18n("Add Folder"), wrappers.Icon("folder48"), self.__slot_new_folder)
        self.menu.newAction(i18n("Add Computer"), wrappers.Icon("computer48"), self.__slot_new_computer)
        self.menu.newAction(i18n("Add User"), wrappers.Icon("user48"), self.__slot_new_user)
        self.menu.newAction(i18n("Add Group"), wrappers.Icon("group48"), self.__slot_new_group)
        self.menu.addSeparator()
        self.menu.newAction(i18n("Modify"), wrappers.Icon("preferences32"), self.__slot_modify)
        self.menu.newAction(i18n("Delete"), wrappers.Icon("edit-delete"), self.__slot_delete)

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
        #self.connect(self.pushMain, QtCore.SIGNAL("clicked()"), self.__slot_main)
        self.connect(self.pushDebug, QtCore.SIGNAL("toggled(bool)"), self.__slot_debug)
        #self.connect(self.pushSearch, QtCore.SIGNAL("clicked()"), self.__slot_search)

        #self.connect(self.treeComputers, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.__slot_tree_click)
        #self.connect(self.treeComputers, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.__slot_tree_double_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.__slot_tree_expand)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.__slot_tree_collapse)
        self.connect(self.treeComputers, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__slot_tree_menu)

        #self.connect(self.treeComputers, QtCore.SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.__slot_tree2_expand)
        #self.connect(self.treeComputers, QtCore.SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.__slot_tree2_collapse)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemClicked(QTreeWidgetItem*, int)"), self.__slot_tree2_click)
        self.connect(self.treeComputers, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.__slot_tree2_double_click)

        self.connect(self.radioPolicyInherit, QtCore.SIGNAL("toggled(bool)"), self.__slot_inherit_toggle)
        self.connect(self.pushCopyPolicy, QtCore.SIGNAL("clicked()"), self.__slot_copy)

        self.connect(self.pushSave, QtCore.SIGNAL("clicked()"), self.__slot_save)
        self.connect(self.pushReset, QtCore.SIGNAL("clicked()"), self.__slot_reset)
        self.connect(self.pushApply, QtCore.SIGNAL("clicked()"), self.__slot_apply)

        self.connect(self.pushConnection, QtCore.SIGNAL("clicked()"), self.__slot_disconnect)
        self.connect(self.pushRefreshNodes, QtCore.SIGNAL("clicked()"), self.__refresh_items)

        self.connect(self.tabPolicy, QtCore.SIGNAL("currentChanged(int)"), self.__slot_tab_clicked)

        #FILTER
        self.connect(self.lineFilterNodes, QtCore.SIGNAL("textChanged(QString)"), self.__slot_filter_nodes)

        self.defaultBrush = QtGui.QBrush(QtGui.QColor("black")) #self.treeComputers.itemAt(1,1).foreground(0)
        self.foundBrush = QtGui.QBrush(QtGui.QColor("green"))

        #collect all items in node tree
        self.collectItems()


        # Initialize "talk" backend
        self.talk.start()

        # Selected items
        self.items = []

        # Item name for comaparison
        self.item_name = ""

        # Groups
        self.groups = []

        # All Nodes
        self.nodes = []

        # Last fetched policy
        self.policy = {}

        # Default firewall rules file
        if not os.path.exists(FIREWALL_FILE):
            self.rules_xml = []
            self.pushSettings.setEnabled(False)
        else:
            self.rules_xml = file(FIREWALL_FILE).read()
            self.pushSettings.setEnabled(True) 

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

        #if self.__slot_connect() == False:
        self.__slot_connect()
        #    import sys
        #    sys.exit()

        # Expand first item
        self.__expand_first_item()

        self.splitter_2.setStretchFactor(0,1)
        self.splitter_2.setStretchFactor(1,0)

        self._thread = PThread(self, self.__wait_for_service_state, self.__service_updated)

    def __expand_first_item(self):
        first_node = self.treeComputers.itemAt(0,0)
        self.treeComputers.setCurrentItem(first_node)
        self.treeComputers.expandItem(first_node)

        # Show node information
        desc = first_node.widget.get_uid()
        title = first_node.widget.get_title()
        icon = first_node.widget.get_icon()

        self.labelNodeDesc.setText(desc)
        self.labelNode.setText(title)
        self.pixmapNode.setPixmap(icon.pixmap())


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
                self.__log(i18n("Directory connection established."), "directory", "info")
            elif status == "offline":
                self.__log(i18n("Directory connection closed."), "directory", "info")
            elif status == "error":
                self.__log(i18n("Directory connection error."), "directory", "error")
        elif backend == "talk":
            self.status_talk = status
            if status == "online":
                self.__log(i18n("XMPP connection established."), "talk", "info")
            elif status == "offline":
                self.__log(i18n("XMPP connection closed."), "talk", "info")
            elif status == "error":
                self.__log(i18n("XMPP connection error."), "talk", "error")

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
        """
        if self.directory.is_connected:
            self.pushMain.setEnabled(True)
            self.pushSearch.setEnabled(True)
        else:
            self.pushMain.setEnabled(False)
            self.pushSearch.setEnabled(False)
        """

        # currentIndex == 0 changed to -1
        if self.tabPolicy.currentIndex() == -1:
            # Disable unnecessary buttons
            """
            if len(self.items):
                self.pushPluginGlobal.setEnabled(True)
                #self.pushPluginItem.setEnabled(True)
            else:
                #self.pushPluginItem.setEnabled(False)
                if self.directory.is_connected:
                    self.pushPluginGlobal.setEnabled(True)
                else:
                    self.pushPluginGlobal.setEnabled(False)
            """
            # Show network information
            if self.directory.is_connected:
                domain_label = "Network: %s" % self.directory.domain
                domain_desc = "Connected as %s" % self.directory.user.capitalize()
                if self.directory_label:
                    domain_label = "Network: %s" % self.directory_label
                    domain_desc = "Connected to %s as %s" % (self.directory.domain, self.directory.user.capitalize())
                """
                self.labelPlugin.setText(domain_label)
                self.labelPluginDesc.setText(domain_desc)
                """
            else:
                self.labelNode.setText("Lider")
                self.labelNodeDesc.setText("")
            # Hide button box
            self.frameButtons.hide()
        else:
            widget = self.tabPolicy.currentWidget()
            # Disable unnecessary buttons
            if widget.get_type() == plugins.TYPE_GLOBAL:
                pass
                #self.pushPluginItem.setEnabled(False)
            else:
                pass
                #self.pushPluginItem.setEnabled(True)
            # Show button box
            self.frameButtons.show()

    def __load_plugins(self):
        """
            Loads plugins
        """
        """
        # Popup for global plugins
        menu_global = wrappers.Menu(self)

        # Popup for single object plugins
        menu_single = wrappers.Menu(self)
        """
        for name, widget_class in plugins.load_plugins().iteritems():
            widget = widget_class()
            self.tabPolicy.addTab(widget, widget.windowIcon(), widget.windowTitle())
            """
            if widget.get_type() == plugins.TYPE_GLOBAL:
                action = menu_global.newAction(widget.windowTitle(), widget.windowIcon(), self.__slot_widget_stack)
            else:
                action = menu_single.newAction(widget.windowTitle(), widget.windowIcon(), self.__slot_widget_stack)
            action.widget = widget # __slot_widget_stack method needs this
            """

        #self.pushPluginGlobal.setMenu(menu_global)
        #self.pushPluginItem.setMenu(menu_single)

    def __refresh_items(self):
        self.__list_items()
        self.__expand_first_item()


    ################################# 
    def __get_all_nodes(self):
        self.nodes = self.directory.search(self.directory.directory_domain, scope="sub", fields=["*"])
        self.__get_all_groups()

    def __get_all_groups(self):
        self.groups = []
        for dn, attrs in self.nodes:
            if "groupOfNames" in attrs["objectClass"]:
                self.groups.append(dn)

    def get_all_users(self, group):

        dn, old_properties = self.directory.search(group, scope="base", fields=["member"])[0]
        members = old_properties["member"]

        return members

    def get_groups_of_user(self, user):
        found_groups = []

        for group in self.groups:
            users = self.get_all_users(group)
            if user in users:
                found_groups.append(group)

        return found_groups



    def  __list_items(self, root=None, alternative=False):
        self.__get_all_nodes()
        self.listGMemberships.clear()
        self.listGroupMembers.clear()

        if not root:
            self.treeComputers.clear()

            """
            if alternative:
                root_alt = QtGui.QTreeWidgetItem(self.treeComputers)
                root_alt.setText(0, unicode(self.directory.get_name()))
                root_alt.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
                root_alt.dn = self.directory.directory_domain
                root_alt.name = root_alt.dn.split(",")[0].split("=")[1]
                root_alt.folder = True
                self.nodes_alt_dn[root_alt.dn] = root_alt
            else:
            """
            root = list_item.add_tree_item(self.treeComputers, self.directory.directory_domain, self.directory.get_name(), self.directory.directory_domain, icon=wrappers.Icon("folder48"))
            root.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
            root.dn = self.directory.directory_domain
            root.name = root.dn.split(",")[0].split("=")[1]
            root.folder = True
            self.nodes_dn[root.dn] = root

            return

        dn = root.dn

        results = self.directory.search(dn, ["o", "cn", "description", "objectClass"], "one")
        fancy = len(results) < 100
        for dn, attrs in results:
            name = dn.split(",")[0].split("=")[1]
            label = name
            folder = dn.startswith("dc=")
            user = "simpleSecurityObject" in attrs["objectClass"]
            group = "groupOfNames" in attrs["objectClass"]

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
            item.user = user
            item.group = group
            item.label = label
            item.description = description

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
            elif group:
                if alternative:
                    item.setIcon(0, wrappers.Icon("group48"))
                else:
                    item.widget.set_icon(wrappers.Icon("group48"))
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
            QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
            return None
        except directory.DirectoryError:
            QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to get policy."))
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

    def __slot_thread(self):

        while not self.thread.isFinished():
            pass

        self.rules_xml = self.thread.rules_xml
        self.rules_compiled = self.thread.rules_compiled

        f = open(FIREWALL_FILE, 'w+')
        f.write(self.rules_xml)
        f.close()


    def __slot_modify_default_firewall_rules(self):

        name = "Group"

        self.thread = main.ThreadFW(name, self.rules_xml)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.__slot_thread)
        self.thread.start()


    def __slot_connect(self):
        """
            Opens a dialog and tries to connect both backends
        """

        self.logged_in = False

        dialog = DialogConnection()
        if self.directory.host:
            # Fill fields if necessary
            dialog.set_host(self.directory.host)
            dialog.set_domain(self.directory.domain)
            dialog.set_user(self.directory.user)
            dialog.set_password(self.directory.password)

        while not self.logged_in:
            if dialog.exec_():
                try:
                    self.directory.connect(dialog.get_host(), dialog.get_domain(), dialog.get_user(), dialog.get_password())
                    self.logged_in = True
                except directory.DirectoryError:
                    traceback.print_exc()
                    self.__update_status("directory", "error")
                    # TODO: Disconnect
                    QtGui.QMessageBox.warning(self, i18n("Connection Error"), "Unable to connect to %s" % dialog.get_host())
                    #return UNABLE_TO_CONNECT
                try:
                    self.directory_label = self.directory.get_name()
                except directory.DirectoryError:
                    self.__update_status("directory", "error")
                    # TODO: Disconnect
                    QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                    #return CONNECTION_LOST
                self.__update_status("directory", "online")
            else:
                # User cancelled
                import sys
                sys.exit()

        # Connect to XMPP server
        self.talk.connect(self.directory.host, self.directory.domain, self.directory.user, self.directory.password)

        # List components
        self.__list_items()
        #self.__list_items(alternative=True)

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
        #self.treeComputers.clear()

        # Reset selected item
        self.items = []

        # Go to first screen
        #self.__slot_main()

        # Update toolbar
        self.__update_toolbar()

        # Go back to login screen
        self.hide()

        #if self.__slot_connect() == False:
        self.__slot_connect()
        #    import sys
        #    sys.exit()

        self.show()

        # Expand first item
        self.__expand_first_item()



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
        #print "XMPP message from: %s" % sender, "talk", "debug"
        self.__log("XMPP message from: %s" % sender, "talk", "debug")

        print "====================================="
        print "\n talk message current index %d \n\n" %self.tabPolicy.currentIndex()

        #if self.tabPolicy.currentIndex() != 0:
        if self.tabPolicy.currentIndex() != -1:
            sender = unicode(sender)
            widget = self.tabPolicy.currentWidget()
            try:
                if arguments:
                    arguments = simplejson.loads(unicode(arguments))
                else:
                    arguments = None
            except Exception, e:
                arguments = None

            if(sender == self.item_name):             
                try:
                    widget.talk_message(sender, message, arguments)
                except Exception, e:
                    pass
                except AttributeError:
                    pass

        self._hide_busy_message()

    def __slot_talk_status(self, sender, status):
        """
            Triggered when an XMPP client's status is changed.

            Arguments:
                sender: Sender's JID
                state: talk.Online or talk.Offline
        """
        sender = str(sender)
        if status == talk.Online and sender not in self.talk.online:
            self.__log(i18n("XMPP user is online: %s") % sender, "talk", "debug")
        elif status == talk.Offline and sender in self.talk.online:
            self.__log(i18n("XMPP user is offline: %s") % sender, "talk", "debug")
        self.__update_icon(sender, status)

        #if self.tabPolicy.currentIndex() != 0:
        if self.tabPolicy.currentIndex() != -1:
            widget = self.tabPolicy.currentWidget()
            try:
                widget.talk_status(sender, status)
            except AttributeError:
                pass
    """
    def __slot_main(self):
        self.tabPolicy.setCurrentIndex(0)
        #self.treeComputers.hide()
        self.__update_toolbar()
    """

    def __slot_tree_click(self, item, column):
        """
            Triggered when user clicks a node.
        """
        self.items = []
        for i in self.treeComputers.selectedItems():
            self.items.append(i)

        self.__update_toolbar()

        self.treeComputers.clearSelection()

        for item in self.items:
            item_alt = self.nodes_alt_dn[item.dn]
            self.treeComputers.setItemSelected(item_alt, True)

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

        try:
            item_alt = self.nodes_alt_dn[item.dn]
            self.treeComputers.expandItem(item_alt)
        except:
            pass

        if item.childCount() == 0:
            item.setExpanded(False)

    def __slot_tree_collapse(self, item):
        """
            Triggered when user collapses a node.
        """
        item.takeChildren()

        item_alt = self.nodes_alt_dn[item.dn]
        self.treeComputers.collapseItem(item_alt)

    def __slot_tree2_click(self, item, column):
        """
            Triggered when user clicks a node.
        """

        """
        if no multiple selection (if len(items) == 1)
            if item == group
               show group members box
                   list group members
                   (search pattern)
            else if item == user
               show membership box
               show membership
            else
               hide group members box and membership box
        else
           hide group members box and membership box
        """

        self.items = []
        for i in self.treeComputers.selectedItems():
            self.items.append(i)

        widget = self.tabPolicy.currentWidget()

        # Disable Save and Save&Apply buttons if the selected node is not a computer
        if self.items[0].folder or self.items[0].user or self.items[0].group:
            self.pushApply.setEnabled(False)
            self.pushSave.setEnabled(False)

            widget.set_item(item=None)
        else:
            self.pushApply.setEnabled(True)
            self.pushSave.setEnabled(True)

            self.splitter_2.refresh()

            self.__update_toolbar()

            self.treeComputers.clearSelection()

            for item in self.items:
                item_alt = self.nodes_dn[item.dn]
                self.treeComputers.setItemSelected(item_alt, True)

            self.item_name = item.name
            print "ITEM NAME   %s " %self.item_name

            if item.name in self.talk.online:
                if self.tabPolicy.currentWidget().get_classes() == ["servicePolicy"]:
                    self._show_busy_message(i18n("Getting service list..."))

                widget.showEvent()
                self.__show_widget(widget)
                widget.showEvent()
                self.__show_widget(widget)
            else:
                widget.set_item(item=None)

            # Show node information
            desc = item_alt.widget.get_uid()
            title = item_alt.widget.get_title()
            icon = item_alt.widget.get_icon()

            self.labelNodeDesc.setText(desc)
            self.labelNode.setText(title)
            self.pixmapNode.setPixmap(icon.pixmap())

            # Find group members or find memberships
            self.listGroupMembers.clear()

            dn = item_alt.widget.get_uid()
            dn, old_properties = self.directory.search(dn, scope="base", fields=["member", "description"])[0]

            if len(self.treeComputers.selectedItems()) == 1:

                try:
                    members = old_properties['member']

                    self.groupGMembers.show()
                    self.groupGMembership.hide()

                    for member in members:
                        dn = member

                        name = dn.split(",")[0].split("=")[1]
                        label = name
                        folder = dn.startswith("dc=")

                        self.listGroupMembers.addItem(label)

                        item = self.listGroupMembers.item(self.listGroupMembers.count() - 1)
                        item.setIcon(wrappers.Icon("user48"))

                except KeyError:
                    self.listGMemberships.clear()
                    memberships = self.get_groups_of_user(self.treeComputers.currentItem().dn)
                    for membership in memberships:
                        name = membership.split(",")[0].split("=")[1]

                        self.listGMemberships.addItem(name)

                        item = self.listGMemberships.item(self.listGMemberships.count() - 1)
                        item.setIcon(wrappers.Icon("group48"))

                    self.listGroupMembers.addItem(i18n("No members found"))
                    self.groupGMembers.hide()
                    self.groupGMembership.show()

                if self.listGMemberships.count() == 0:
                    self.groupGMembership.hide()

                if self.listGroupMembers.count() == 0:
                    self.groupGMembers.hide()

            else:
                self.groupGMembers.hide()
                self.groupGMembership.hide()

    def __slot_tab_clicked(self):
        """
            Triggered when user clicks a node.
        """

        item = self.treeComputers.currentItem()

        self.items = []
        for i in self.treeComputers.selectedItems():
            self.items.append(i)

        self.__update_toolbar()

        self.treeComputers.clearSelection()


        widget = self.tabPolicy.currentWidget()
        if self.items and (item.name in self.talk.online):

            # Show roller before retrieving service list when service tab is clicked
            if self.tabPolicy.currentWidget().get_classes() == ["servicePolicy"]:
                self._show_busy_message(i18n("Getting service list..."))

            for item in self.items:
                item_alt = self.nodes_dn[item.dn]
                self.treeComputers.setItemSelected(item_alt, True)

            if not self.items[0].folder:
                widget.showEvent()
                self.__show_widget(widget)
                widget.showEvent()
                self.__show_widget(widget)

            # widget = self.tabPolicy.currentWidget()
            # widget.showEvent()
            # self.__show_widget(widget)

            # Show node information
            try:
                desc = item_alt.widget.get_uid()
                title = item_alt.widget.get_title()
                icon = item_alt.widget.get_icon()
                self.labelNodeDesc.setText(desc)
                self.labelNode.setText(title)
                self.pixmapNode.setPixmap(icon.pixmap())
            except:
                pass
        else:
            widget.set_item(item=None)
            #rc = cb.count
            #for i in range(rc):
            #    cb.removeItem(i)

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

    def __slot_modify(self):
        """
            Triggered when user wants to modify an item
        """
        if len(self.items) != 1:
            QtGui.QMessageBox.warning(self, i18n("Warning", "Only one item at a time can be modified."))
            return

        item = self.items[0]

        try:
            if item.folder:
                dialog = DialogFolder()
                dialog.set_name(item.name)
                dialog.set_label(item.label)
                dialog.set_description(item.description)
                if dialog.exec_():
                    label = dialog.get_label()
                    description = dialog.get_description()
                    if item.label != label or item.description != description:
                        self.directory.modify_folder(item.dn, label, description)
            elif item.user:
                dialog = DialogUser()
                dialog.set_name(item.name)
                dialog.set_password("")
                dialog.set_description(item.description)
                if dialog.exec_():
                    password = dialog.get_password()
                    description = dialog.get_description()
                    if item.description != description or len(password):
                        self.directory.modify_user(item.dn, password, description)
            elif item.group:
                dn, old_properties = self.directory.search(item.dn, scope="base", fields=["member"])[0]
                old_members = old_properties["member"]

                people = []
                for dn, attrs in self.directory.search(self.directory.directory_domain, ["cn", "objectClass"], "sub"):
                    if dn.startswith("cn=") and "simpleSecurityObject" in attrs["objectClass"] or "pardusComputer" in attrs["objectClass"]:
                        people.append(dn)

                dialog = DialogGroup()
                dialog.set_name(item.name)
                dialog.set_description(item.description)
                dialog.set_members(old_members)
                dialog.set_people(people)
                if dialog.exec_():
                    description = dialog.get_description()
                    members = dialog.get_members()
                    if item.description != description or old_members != members:
                        self.directory.modify_group(item.dn, members, description)
            else:
                dialog = DialogComputer()
                dialog.set_name(item.name)
                dialog.set_password("")
                dialog.set_description(item.description)
                if dialog.exec_():
                    password = dialog.get_password()
                    description = dialog.get_description()
                    if item.description != description or len(password):
                        self.directory.modify_computer(item.dn, password, description)

        except directory.DirectoryConnectionError:
            self.__update_status("directory", "error")
            # TODO: Disconnect
            QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
            return
        except directory.DirectoryAccessError:
            QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Insufficient access."))
            return
        except directory.DirectoryError:
            QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to modify item."))
            return

        parent = item.parent()
        self.treeComputers.collapseItem(parent)
        self.treeComputers.expandItem(parent)
        self.treeComputers.scrollToItem(item)
        self.treeComputers.setCurrentItem(item)

    def __slot_delete(self):
        """
            Triggered when user wants to delete an item
        """
        if len(self.items) != 1:
            QtGui.QMessageBox.warning(self, i18n("Warning"), i18n("Only one item at a time can be deleted."))
            return

        item = self.items[0]

        if item.folder and len(self.directory.search(item.dn, scope="one", fields=["objectClass"])) > 0:
            QtGui.QMessageBox.warning(self, i18n("Warning"), i18n("The selected item is a non-empty directory. It cannot be deleted."))
            return

        reply = QtGui.QMessageBox.question(self, i18n("Warning"), i18n("This is not undoable. Are you sure you want to remove?"), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No )
        if reply == QtGui.QMessageBox.Yes:
            try:
                self.directory.delete_item(item.dn)
                index = item.parent().indexOfChild(self.treeComputers.currentItem())
                item.parent().takeChild(index)

            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                return
            except directory.DirectoryAccessError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Insufficient access."))
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to delete item."))
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
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                return
            except directory.DirectoryAccessError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Insufficient access."))
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to add computer."))
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
            description = dialog.get_description()
            try:
                dn = self.directory.add_user(parent_path, name, password, description)
            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                return
            except directory.DirectoryAccessError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Insufficient access."))
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to add user."))
                return

            self.treeComputers.collapseItem(parent_item)
            self.treeComputers.expandItem(parent_item)
            item = self.nodes_dn[dn]
            self.treeComputers.scrollToItem(item)
            self.treeComputers.setCurrentItem(item)

    def __slot_new_group(self):
        """
            Triggered when user wants to add a new group.
        """
        item = self.items[0]

        if item.folder:
            parent_item = item
        else:
            parent_item = item.parent()

        parent_path = parent_item.dn

        people = []
        for dn, attrs in self.directory.search(self.directory.directory_domain, ["cn", "objectClass"], "sub"):
            if dn.startswith("cn=") and "simpleSecurityObject" in attrs["objectClass"] or "pardusComputer" in attrs["objectClass"]:
                people.append(dn)

        dialog = DialogGroup()
        dialog.set_people(people)
        if dialog.exec_():
            name = dialog.get_name()
            members = dialog.get_members()
            description = dialog.get_description()
            try:
                dn = self.directory.add_group(parent_path, name, members, description)
            except directory.DirectoryConnectionError:
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                return
            except directory.DirectoryAccessError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Insufficient access."))
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to add group."))
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
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                return
            except directory.DirectoryAccessError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Insufficient access."))
                return
            except directory.DirectoryError:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to add folder."))
                return

            self.treeComputers.collapseItem(parent_item)
            self.treeComputers.expandItem(parent_item)
            item = self.nodes_dn[dn]
            self.treeComputers.scrollToItem(item)
            self.treeComputers.setCurrentItem(item)

    """
    def __slot_widget_stack(self, toggled):
            Triggered when users activates a policy plugin.
        widget = self.sender().widget
        self.__show_widget(widget)
    """

    def __show_widget(self, widget):
        """
            Shows a widget
        """
        policy_match = False
        policy_inherit = True
        self.treeComputers.show()

        if len(self.items) == 1:
            item = self.items[0]
        else:
            item = None

        if item and widget.get_type() == plugins.TYPE_SINGLE:
            paths = self.directory.get_parent_paths(item.dn)
            self_path = paths[-1]

            classes = {}
            for path in paths:
                search = self.directory.search(path, ["*"], "base")
                if len(search):
                    classes[path] = []
                    for oclass in search[0][1]["objectClass"]:
                        if oclass.endswith("Policy"):
                            classes[path].append(oclass)


            widget_classes = widget.get_classes()
            self_policies = classes[self_path]

            #self.treeApplied.clear()

            for path, policies in classes.iteritems():

                if self_path == path:
                    continue

                if len(set(widget_classes).intersection(set(policies))) > 0:
                    policy_match = True

                    if len(set(self_policies).intersection(set(widget_classes))) > 0:
                        policy_inherit = False
                        # Indentation of this break was one of the problems
                        break

                #if policy_inherit and classes[path] or len(set(widget_classes).intersection(set(policies))) > 0:
                #
                #    name = path.split(",")[0].split("=")[1]
                #    #node = QtGui.QTreeWidgetItem(self.treeApplied, [name], )
                #    #node.setExpanded(True)
                #    #node.setIcon(0, wrappers.Icon("star32"))
                #
                #
                #    for policy in classes[path]:
                #        p = QtGui.QTreeWidgetItem(node, [policy])
                #        p.setIcon(0, wrappers.Icon("policy32"))

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
            if item and ((item.name in self.talk.online) or item.folder):
                self.pushApply.show()
                self.pushApply.setEnabled(True)
            else:
                self.pushApply.setEnabled(False)
            self.policy = self.__load_policy()
            if self.policy != None:
                widget.policy = self.policy
                try:
                    widget.load_policy(self.policy)
                except AttributeError:
                    pass

        self.tabPolicy.setCurrentWidget(widget)
        self.__update_toolbar()

        if len(self.items) > 1:
            self.frameMulti.show()

        if policy_match:
            widget.policy_match = True
            #self.framePolicyInherit.show()
            self.framePolicyInherit.hide()
            if policy_inherit:
                #self.radioPolicyInherit.setChecked(True)
                #self.pushCopyPolicy.setEnabled(False)
                self.radioPolicyInherit.hide()
                self.pushCopyPolicy.hide()
            else:
                #self.radioPolicyNoInherit.setChecked(True)
                #self.pushCopyPolicy.setEnabled(True)
                self.radioPolicyNoInherit.hide()
                self.pushCopyPolicy.hide()
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
        #self.__slot_main()
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
            names = []
            for item in self.items:
                if item.folder:
                    for dn, attrs in self.directory.search(item.dn, scope="sub", fields=['objectClass']):
                        if dn.startswith("cn="):
                            names.append(dn.split(",")[0].split("=")[1])
                else:
                    names.append(item.name)

            if not len(names):
                return

            msg = QtGui.QMessageBox(self)
            msg.setIcon(QtGui.QMessageBox.Question)
            msg.setText(i18n("%d item(s) will be forced to update policy.") % len(names))
            msg.setInformativeText(i18n("Do you want to continue?"))
            msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            msg.setDefaultButton(QtGui.QMessageBox.Yes)

            if msg.exec_() != QtGui.QMessageBox.Yes:
                return

            for name in names:
                xmpp_update(name)

            if self.tabPolicy.currentWidget().get_classes() == ["servicePolicy"]:
                self._show_busy_message("Updating...")
                self._thread.start()

    def _show_busy_message(self, message=""):
        # self._busy_message_owner = self.tabPolicy.currentWidget()
        self._busy.enableOverlay(False)
        self._busy.busy.busy()
        self._busy.setMessage(message)
        self._busy.animate(start = MIDLEFT,
                           stop = MIDCENTER,
                           direction = IN)

    def _hide_busy_message(self):
        if self._busy.isVisible():# and self._busy_message_owner == self.tabPolicy.currentWidget():
            self._busy.busy.stopAnimation()
            self._busy.animate(start = CURRENT,
                               stop = MIDRIGHT,
                               direction = OUT)

    def __wait_for_service_state(self):
        # Wait for force.update to be completed
        import time
        time.sleep(5)
        return

    def __service_updated(self):
        widget = self.tabPolicy.currentWidget()
        widget.showEvent()
        self.__show_widget(widget)

    def __slot_save(self):
        """
            Triggered when user clicks 'save' button.
        """

        msg = QtGui.QMessageBox(self)
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText(i18n("Policy will be saved."))
        msg.setInformativeText(i18n("Do you want to continue?"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.setDefaultButton(QtGui.QMessageBox.No)

        if msg.exec_() != QtGui.QMessageBox.Yes:
            return

        widget = self.tabPolicy.currentWidget()

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
                self.__update_status("directory", "error")
                # TODO: Disconnect
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Connection lost. Please re-connect."))
                return False
            except directory.DirectoryError, e:
                QtGui.QMessageBox.warning(self, i18n("Connection Error"), i18n("Unable to modify node."))
                return False
            widget.policy = self.__load_policy()
            return True

    def __slot_reset(self):
        """
            Triggered when user clicks reset button.
        """

        #if self.tabPolicy.currentIndex() != 0:
        if self.tabPolicy.currentIndex() != -1:
            msg = QtGui.QMessageBox(self)
            msg.setIcon(QtGui.QMessageBox.Question)
            msg.setText(i18n("All changes will be reverted."))
            msg.setInformativeText(i18n("Do you want to continue?"))
            msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            msg.setDefaultButton(QtGui.QMessageBox.No)

            if msg.exec_() != QtGui.QMessageBox.Yes:
                return

            widget = self.tabPolicy.currentWidget()
            if widget.policy != None:
                try:
                    widget.load_policy(widget.policy)
                except AttributeError:
                    pass

    def __slot_inherit_toggle(self, state):
        """
            Triggered when user switches inheritance policy.
        """
        if self.radioPolicyNoInherit.isChecked():
            self.pushCopyPolicy.setEnabled(True)
        else:
            self.pushCopyPolicy.setEnabled(False)

    def __slot_copy(self):
        """
            Triggered when user clicks "Copy Policy" button.
        """
        msg = QtGui.QMessageBox(self)
        msg.setIcon(QtGui.QMessageBox.Question)
        msg.setText(i18n("Policy from parent directory will be copied."))
        msg.setInformativeText(i18n("Do you want to continue?"))
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        msg.setDefaultButton(QtGui.QMessageBox.Yes)

        if msg.exec_() != QtGui.QMessageBox.Yes:
            return

        widget = self.tabPolicy.currentWidget()
        item = widget.item.parent()
        policy = self.__load_policy(item)
        widget.load_policy(policy)

    # has text method to check given text is exist in given items index or not
    def has_text(self, item, index, text):
        return not unicode(item.text(index)).lower().find(unicode(text).lower()) == -1

    def collectItems(self):
        # get top-level items
        self.nodes = map(lambda x: self.treeComputers.topLevelItem(x), \
                             range(self.treeComputers.topLevelItemCount()))

        self.all_items = []

        # recursive method to add all tree to a list
        def add_recursive(item):
            self.all_items.append(item)
            if item.childCount() > 0:
                for index in range(item.childCount()):
                    add_recursive(item.child(index))

        # add all items to the list starting from the top-level items
        for item in self.nodes:
            add_recursive(item)

        count = len(self.all_items)

    def __slot_filter_nodes(self):
        self.collectItems()
        key = self.lineFilterNodes.text()

        found_items = []

        # walk in all items
        for item in self.all_items:
            # Search each column in every cycle
            for index in range(self.treeComputers.columnCount()):
                # if text in given index then add it into the found_items list
                # and dont forget to colorize the item.
                hasText = self.has_text(item, index, key)
                if key and hasText:
                    item.setForeground(index, self.foundBrush)
                    found_items.append(item)
                # Otherwise hide it and set its foreground to defaultBrush
                else:
                    item.setForeground(index, self.defaultBrush)
                    item.setHidden(True)

       # If there are found_items walk in them otherwise use all_items
        for item in found_items if key else self.all_items:
            # show the item itself
            item.setHidden(False)
            # walk in the item's child and show them also
            for i in range(item.childCount()):
                item.child(i).setHidden(False)
            # starting from the item to the top show all parents too
            while item.parent():
                item.parent().setHidden(False)
                item = item.parent()



