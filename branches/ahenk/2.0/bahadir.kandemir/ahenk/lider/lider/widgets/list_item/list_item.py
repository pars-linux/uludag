#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Custom QListWidget item

    See gui_test.py for usage information.
"""

# Qt4 modules
from PyQt4 import QtCore
from PyQt4 import QtGui

# Generated UI module
from ui_list_item import Ui_ItemWidget


def add_tree_item(parent, uid, title, description="", data=None, icon=None, status_icon=None, state=None, edit=None, delete=None):
    """
        Adds a new custom QTreeWidget item.

        If icon, state, edit or delete is None, these widgets will be hidden.

        Arguments:
            parent: Parent object
            uid: Unique ID of object, for internal use
            title: List item title
            description: List item description
            data: Internal storage, keeps any data you want
            icon: List item icon
            status_icon: Status icon. Pass None to hide.
            state: List item check state (True or False). Pass None to hide.
            edit: List item edit icon. Pass None to hide.
            delete: List item delete icon. Pass None to hide.
        Returns:
            TreeWidgetItem objec
    """
    widget_item = QtGui.QTreeWidgetItem(parent)
    tree_widget = widget_item.treeWidget()
    widget = ItemWidget(tree_widget, uid, title, description, data, icon, status_icon, state, edit, delete)
    widget_item.widget = widget
    tree_widget.setItemWidget(widget_item, 0, widget)
    return widget_item

def add_list_item(parent, uid, title, description="", data=None, icon=None, status_icon=None, state=None, edit=None, delete=None):
    """
        Adds a new custom QListWidget item.

        If icon, state, edit or delete is None, these widgets will be hidden.

        Arguments:
            parent: Parent object
            uid: Unique ID of object, for internal use
            title: List item title
            description: List item description
            data: Internal storage, keeps any data you want
            icon: List item icon
            status_icon: Status icon. Pass None to hide.
            state: List item check state (True or False). Pass None to hide.
            edit: List item edit icon. Pass None to hide.
            delete: List item delete icon. Pass None to hide.
        Returns:
            Widget object
    """
    widget = ItemWidget(parent, uid, title, description, data, icon, status_icon, state, edit, delete)
    widget_item = ItemWidgetItem(parent, widget)
    parent.setItemWidget(widget_item, widget)
    return widget

class ItemWidgetItem(QtGui.QListWidgetItem):
    """
        Custom QListWidget item.
    """

    def __init__(self, parent, widget):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.setSizeHint(QtCore.QSize(300, 48))

        self.widget = widget

    def get_uid(self):
        """
            Returns unique ID ob item.
        """
        return self.widget.get_uid()

    def get_data(self):
        """
            Returns data in internal storage.
        """
        return self.widget.get_data()


class ItemWidget(QtGui.QWidget, Ui_ItemWidget):
    def __init__(self, parent, uid, title="", description="", data=None, icon=None, status_icon=None, state=None, edit=None, delete=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.uid = uid
        self.data = data

        self.set_title(title)
        self.set_description(description)

        self.set_state(state)
        self.set_icon(icon)
        self.set_status_icon(status_icon)
        self.set_edit(edit)
        self.set_delete(delete)

        # Signals
        self.connect(self.checkState, QtCore.SIGNAL("stateChanged(int)"), lambda: self.emit(QtCore.SIGNAL("stateChanged(int)"), self.checkState.checkState()))
        self.connect(self.pushEdit, QtCore.SIGNAL("clicked()"), lambda: self.emit(QtCore.SIGNAL("editClicked()")))
        self.connect(self.pushDelete, QtCore.SIGNAL("clicked()"), lambda: self.emit(QtCore.SIGNAL("deleteClicked()")))

    def mouseDoubleClickEvent(self, event):
        if self.pushEdit.isVisible():
            self.pushEdit.animateClick(100)

    def get_uid(self):
        return self.uid

    def get_data(self):
        return self.data

    def set_title(self, title):
        self.labelTitle.setText(unicode(title))

    def get_title(self):
        return unicode(self.labelTitle.text())

    def set_description(self, description=""):
        self.labelDescription.setText(unicode(description))

    def get_description(self):
        return unicode(self.labelDescription.text())

    def set_icon(self, icon=None):
        if icon != None:
            if isinstance(icon, QtGui.QMovie):
                self.labelIcon.setMovie(icon)
                icon.start()
            elif isinstance(icon, QtGui.QIcon):
                self.labelIcon.setPixmap(icon.pixmap(32, 32))
            self.labelIcon.show()
        else:
            self.labelIcon.hide()

    def set_status_icon(self, status_icon=None):
        if status_icon != None:
            if isinstance(status_icon, QtGui.QMovie):
                self.labelStatusIcon.setMovie(status_icon)
                status_icon.start()
            elif isinstance(status_icon, QtGui.QIcon):
                self.labelStatusIcon.setPixmap(status_icon.pixmap(32, 32))
            self.labelStatusIcon.show()
        else:
            self.labelStatusIcon.hide()

    def get_state(self):
        return self.checkState.checkState() == QtCore.Qt.Checked

    def set_state(self, state=None):
        if state != None:
            if state == True:
                state = QtCore.Qt.Checked
            elif state == False:
                state = QtCore.Qt.Unchecked
            self.checkState.setCheckState(state)
            self.checkState.show()
        else:
            self.checkState.hide()

    def set_edit(self, edit=None):
        if edit != None:
            self.pushEdit.setIcon(edit)
            self.pushEdit.show()
        else:
            self.pushEdit.hide()

    def set_delete(self, delete=None):
        if delete != None:
            self.pushDelete.setIcon(delete)
            self.pushDelete.show()
        else:
            self.pushDelete.hide()
