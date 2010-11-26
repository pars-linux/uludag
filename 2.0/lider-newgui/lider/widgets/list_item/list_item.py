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


def add_list_item(parent, uid, title, description="", data=None, icon=None, state=None, edit=None, delete=None):
    """
        Adds a new custom QListWidget item.

        Arguments:
            parent: Parent object
            uid: Unique ID of object, for internal use
            title: List item title
            description: List item description
            data: Internal storage, keeps any data you want
            icon: List item icon
            state: List item check state (True or False). Pass None to hide.
            edit: List item edit icon. Pass None to hide.
            delete: List item delete icon. Pass None to hide.
        Returns:
            Widget object
    """
    widget = ItemWidget(parent, uid, title, description, data, icon, state, edit, delete)
    widget_item = ItemWidgetItem(parent, widget)
    parent.setItemWidget(widget_item, widget)
    return widget

class ItemWidgetItem(QtGui.QListWidgetItem):
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
    def __init__(self, parent, uid, title="", description="", data=None, icon=None, state=None, edit=None, delete=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.uid = uid
        self.data = data

        self.set_title(title)
        self.set_description(description)

        self.set_state(state)
        self.set_icon(icon)
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
            self.labelIcon.setPixmap(icon.pixmap(32, 32))
            self.labelIcon.show()
        else:
            self.labelIcon.hide()

    def get_state(self):
        return self.checkState.checkState()

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
