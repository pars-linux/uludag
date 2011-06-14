#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Main window
"""

# Standard modules
import copy
import sys

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_main import Ui_MainWindow

# Directory
from directory import Connection, Node

# Helpers
import lider.wrappers as wrappers
from lider.utils import load_plugins
from lider import talk


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
        Main window.

        Usage:
            win = MainWindow()
            win.show()
    """

    viewMode = QtCore.pyqtSignal()
    editMode = QtCore.pyqtSignal()
    singleSelection = QtCore.pyqtSignal()
    multipleSelection = QtCore.pyqtSignal()

    def __init__(self, app):
        """
            Constructor for main window.

            Arguments:
                parent: Parent object
        """
        QtGui.QMainWindow.__init__(self)

        # Application
        self.app = app

        # Backend connections
        self.backend = Connection()
        from lider.connection import DialogConnection

        dialog = DialogConnection()
        while True:
            if not dialog.exec_():
                sys.exit()
            else:
                host = dialog.get_host()
                domain = dialog.get_domain()
                username = dialog.get_user()
                password = dialog.get_password()
                try:
                    self.backend.login_simple(host, domain, username, password)
                    break
                except:
                    pass

        # Plugins
        self.plugins = {}

        # XMPP backend
        self.xmpp_online = []
        self.xmpp = talk.Talk()
        self.xmpp.start()
        self.xmpp.connect(host, domain, username, password)

        # Attach generated UI
        self.setupUi(self)

        # Fine tune UI
        self.treeNodes.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

        # Configure state machine
        self.state = self.stateMachine()

        # Selection mode
        self.multiple = True

        # Selection
        self.selected = {}

        # View mode
        self.viewmode = None

        # Populate network view
        self.populateNetwork()

        # Populate plugin list
        self.populatePlugins()

        # XMPP events
        self.connect(self.xmpp, QtCore.SIGNAL("stateChanged(int)"), self.slotXMPPState)
        self.connect(self.xmpp, QtCore.SIGNAL("messageFetched(QString, QString, QString)"), self.slotXMPPMessage)
        self.connect(self.xmpp, QtCore.SIGNAL("userStatusChanged(QString, int)"), self.slotXMPPStatus)

        # UI events
        self.connect(self.treeNodes, QtCore.SIGNAL("itemChanged(QTreeWidgetItem*, int)"), self.slotTreeSelection)
        self.connect(self.treeNodes, QtCore.SIGNAL("itemSelectionChanged()"), self.slotTreeSelectionChanged)

        self.connect(self.actionNetworkView, QtCore.SIGNAL("triggered(bool)"), self.slotNetworkView)
        self.connect(self.actionPolicies, QtCore.SIGNAL("triggered(bool)"), self.slotPolicyView)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.slotRefresh)

        self.connect(self.radioFollow, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyEditable)
        self.connect(self.radioMultiple, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyEditable)

        self.connect(self.pushApply, QtCore.SIGNAL("clicked()"), self.slotApply)
        self.connect(self.pushRevert, QtCore.SIGNAL("clicked()"), self.slotRevert)

    def slotApply(self):
        widget = self.tabPolicy.currentWidget()
        print widget.dump_policy()

    def slotRevert(self):
        pass

    def slotXMPPState(self, state):
        pass

    def slotXMPPMessage(self, sender, message, arguments=""):
        pass

    def slotXMPPStatus(self, sender, status):
        if status == talk.Online and sender not in self.xmpp_online:
            self.xmpp_online.append(sender)
        elif status == talk.Offline and sender in self.xmpp_online:
            self.xmpp_online.remove(sender)

    def stateMachine(self):
        """
            Initiates a final state machine and configures it.

            Returns:
                QStateMachine object
        """
        machine = QtCore.QStateMachine()

        state_view = QtCore.QState()
        state_view_single = QtCore.QState(state_view)
        state_view_multiple = QtCore.QState(state_view)
        state_view.setInitialState(state_view_single)

        self.connect(state_view_single, QtCore.SIGNAL('entered()'), lambda: self.setState('view', 'single'))
        self.connect(state_view_multiple, QtCore.SIGNAL('entered()'), lambda: self.setState('view', 'multiple'))

        state_edit = QtCore.QState()
        state_edit_single = QtCore.QState(state_edit)
        state_edit_multiple = QtCore.QState(state_edit)
        state_edit.setInitialState(state_edit_single)

        self.connect(state_edit_single, QtCore.SIGNAL('entered()'), lambda: self.setState('edit', 'single'))
        self.connect(state_edit_multiple, QtCore.SIGNAL('entered()'), lambda: self.setState('edit', 'multiple'))

        machine.addState(state_view)
        machine.addState(state_edit)
        machine.setInitialState(state_view)

        state_edit.addTransition(self, QtCore.SIGNAL('viewMode()'), state_view)
        state_view.addTransition(self, QtCore.SIGNAL('editMode()'), state_edit)

        state_edit_single.addTransition(self, QtCore.SIGNAL('multipleSelection()'), state_edit_multiple)
        state_edit_multiple.addTransition(self, QtCore.SIGNAL('singleSelection()'), state_edit_single)

        state_view_single.addTransition(self, QtCore.SIGNAL('multipleSelection()'), state_view_multiple)
        state_view_multiple.addTransition(self, QtCore.SIGNAL('singleSelection()'), state_view_single)

        machine.start()

        return machine

    def setState(self, mode, selection):
        """
            Sets view states.
        """
        nodes = self.getSelectedNodes()
        if len(nodes) < 2:
            if selection == 'multiple':
                self.emit(QtCore.SIGNAL('singleSelection()'))
                return
        else:
            if selection == 'single':
                self.emit(QtCore.SIGNAL('multipleSelection()'))
                return

        if mode == 'view':
            self.framePolicy.hide()
            self.frameDetails.hide()
            self.groupInherited.hide()

            self.treeNodes.header().showSection(1)
            self.treeNodes.header().showSection(2)
            self.treeNodes.header().showSection(3)

            self.actionNetworkView.setChecked(True)
            self.actionPolicies.setChecked(False)

            if selection == 'single':
                pass
            elif selection == 'multiple':
                pass
        elif mode == 'edit':
            self.framePolicy.show()
            self.frameDetails.show()

            self.groupGMembers.hide()
            self.groupGMembership.hide()

            self.treeNodes.header().hideSection(1)
            self.treeNodes.header().hideSection(2)
            self.treeNodes.header().hideSection(3)

            self.actionNetworkView.setChecked(False)
            self.actionPolicies.setChecked(True)

            if selection == 'single':
                self.groupInherited.show()

                self.frameSingle.show()
                self.frameMultiple.hide()
                self.radioMultiple.hide()
            elif selection == 'multiple':
                self.groupInherited.hide()

                self.frameSingle.hide()
                self.frameMultiple.show()
                self.radioMultiple.show()

            self.slotTreeSelectionChanged()

    def populatePlugins(self):
        """
            Populates plugin list.
        """
        # Populate plugins
        self.tabPolicy.clear()
        for name, widget_class in load_plugins().iteritems():
            widget = widget_class(self.tabPolicy)
            self.tabPolicy.addTab(widget, widget.windowTitle())
            self.plugins[name] = widget

    def populateNetwork(self):
        """
            Populates network view with sample data.
        """
        self.treeNodes.clear()

        # GUI utilities
        items = {}
        def new_node(parent, node):
            """Adds new node to QTreeWidget"""
            widget = QtGui.QTreeWidgetItem(parent)
            widget.setText(0, unicode(node.get_label()))
            widget.setText(1, unicode(node.get_description()))

            if node.is_group():
                icon = wrappers.Icon('user48', size=22)
            elif node.is_folder():
                icon = wrappers.Icon('folder48', size=22)
            elif 'pardusComputer' in node.get_classes():
                icon = wrappers.Icon('computer48', size=22)
            elif 'organizationalRole' in node.get_classes():
                icon = wrappers.Icon('star32', size=22)
            else:
                icon = wrappers.Icon('error48', size=22)

            widget.setIcon(0, icon)

            #widget.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)

            if self.multiple:
                widget.setCheckState(0, False)

            widget.node = node
            items[node] = widget
            return widget

        # GUI item for root node
        self.backend.fetch_attributes(self.backend.get_root())
        widget = new_node(self.treeNodes, self.backend.get_root())
        widget.setSelected(True)

        # Functions
        def populate_tree(widget, node):
            for child in self.backend.list_children(node):
                self.backend.fetch_attributes(child)
                item = new_node(widget, child)
                if child.is_folder():
                    populate_tree(item, child)

        populate_tree(widget, widget.node)

    def populateMembers(self):
        """
            Populates members of selected group.
        """
        self.listGroupMembers.clear()
        nodes = self.getSelectedNodes()
        if len(nodes) == 1:
            node = nodes[0]
            self.backend.fetch_attributes(node)
            if node.is_group():
                name = node.get_label()
                for member in self.backend.list_members(node):
                    self.backend.fetch_attributes(member)
                    label = unicode(member.get_label())
                    self.listGroupMembers.addItem(label)

    def populateAppliedPolicies(self):
        """
            Populates list of applied policies for a domain.
        """
        self.listApplied.clear()
        nodes = self.getSelectedNodes()
        if len(nodes) == 1:
            node = nodes[0]
            for parent in self.backend.get_all_parents(node):
                self.backend.fetch_attributes(parent)
                label = unicode(parent.get_label())
                self.listApplied.addItem(label)

    def getSelectedNodes(self):
        """
            Returns list of selected nodes.
        """
        nodes = []
        for key in self.selected:
            nodes.append(self.selected[key].node)
        if not len(nodes):
            for item in self.treeNodes.selectedItems():
                nodes = [item.node]
                break
        return nodes

    def isPolicyEditable(self):
        """
            Returns if policy is editable.
        """
        return not (self.radioFollow.isChecked() or self.radioMultiple.isChecked())

    def slotPolicyEditable(self, state=None):
        """
            Triggered when user wants to follow parent policy.
        """
        self.tabPolicy.setEnabled(self.isPolicyEditable())

    def slotNetworkView(self, toggled):
        """
            Triggered when user activates Network View action.
        """
        self.emit(QtCore.SIGNAL('viewMode()'))

    def slotPolicyView(self, toggled):
        """
            Triggered when user activates Policy View action.
        """
        self.emit(QtCore.SIGNAL('editMode()'))

    def slotRefresh(self, toggled):
        """
            Triggered when user clicks on Refresh button.
        """
        self.treeNodes.setEnabled(False)
        self.populateNetwork()
        self.treeNodes.setEnabled(True)
        self.slotTreeSelectionChanged()

    def slotTreeSelection(self, item, column):
        """
            Triggered when users changes an item in tree widget.
        """
        if column != 0 or item.data(0, QtCore.Qt.CheckStateRole) == QtCore.QVariant():
            return

        def _setState(_item, _state):
            """Shows or hides item checkboxes on tree widget."""
            _item.setCheckState(0, _state)
            for i in range(_item.childCount()):
                _item2 = _item.child(i)
                _setState(_item2, _state)

        selection_last = copy.deepcopy(self.selected)

        state = item.checkState(0)

        if state == QtCore.Qt.Checked:
            self.selected[id(item)] = item
        else:
            if id(item) in self.selected:
                del self.selected[id(item)]

        _setState(item, state)

        if len(self.selected) > 1:
            self.emit(QtCore.SIGNAL('multipleSelection()'))
        else:
            self.emit(QtCore.SIGNAL('singleSelection()'))

        self.slotTreeSelectionChanged()

    def slotTreeSelectionChanged(self):
        """
            Triggered when tree selection is changed.
        """
        nodes = self.getSelectedNodes()

        for node in nodes:
            self.backend.fetch_attributes(node)

        # Group members and inherited policies lists
        if len(nodes) == 1:
            node = nodes[0]

            self.labelNodeURI.setText(node.get_address())
            self.labelNodeType.setText("...")

            if node.is_group():
                self.populateMembers()
                self.groupGMembers.show()
            else:
                self.groupGMembers.hide()

            self.populateAppliedPolicies()

        # Group memberships
        if len(nodes) > 1:
            groups = None
            for node in nodes:
                node = nodes[0]

                groups_tmp = []
                for group in self.backend.list_groups(node):
                    groups_tmp.append(group.get_address())
                groups_tmp = set(groups_tmp)

                if not groups:
                    groups = groups_tmp
                groups = groups.intersection(groups_tmp)

            if len(groups):
                group = self.backend.find_node_by_address(list(groups)[0])
                self.labelGroupOld.setText("These nodes are members of '%s' group." % group.get_label())
                self.stackedGMembership.setCurrentIndex(0)
            else:
                self.stackedGMembership.setCurrentIndex(1)

            self.groupGMembership.show()

        # Policy inheritance mode
        if len(nodes) > 0:
            if len(nodes) > 1:
                self.radioMultiple.setChecked(True)
            else:
                node = nodes[0]
                attributes = node.get_attributes()
                policy = attributes.get('parduspolicy', ['follow'])[0]
                if policy == 'new':
                    self.radioIgnore.setChecked(True)
                elif policy == 'extend':
                    self.radioExtend.setChecked(True)
                else:
                    self.radioFollow.setChecked(True)
                # Pass policies to plugins
                for name in self.plugins:
                    widget = self.plugins[name]
                    widget.load_policy(attributes)
