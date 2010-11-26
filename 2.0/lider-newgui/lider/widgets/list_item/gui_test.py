#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    GUI test application for custom QListWidget item
"""

# Standard modules
import sys

# Qt4 modules
from PyQt4 import QtCore
from PyQt4 import QtGui


def main():
    """
        Main function
    """
    app = QtGui.QApplication(sys.argv)
    win = QtGui.QListWidget()

    import list_item

    # Icons
    icon1 = QtGui.QIcon(QtGui.QPixmap("/usr/share/icons/oxygen/48x48/actions/text-speak.png"))
    icon2 = QtGui.QIcon(QtGui.QPixmap("/usr/share/icons/oxygen/48x48/actions/edit-rename.png"))
    icon3 = QtGui.QIcon(QtGui.QPixmap("/usr/share/icons/oxygen/48x48/actions/trash-empty.png"))

    # Signal handlers
    def state_changed(state):
        print "State", win.sender().get_uid(), state
    def edit_clicked():
        print "Edit", win.sender().get_uid()
    def delete_clicked():
        print "Delete", win.sender().get_uid()

    # ID, Title, description, icon, check box, edit and delete buttons
    widget1 = list_item.add_list_item(win, 1, "Title 1", "Description 1", icon=icon1, state=True, edit=icon2, delete=icon3)
    widget2 = list_item.add_list_item(win, 2, "Title 2", "Description 2", icon=icon1, state=True, edit=icon2, delete=icon3)

    # Bind handlers
    win.connect(widget1, QtCore.SIGNAL("stateChanged(int)"), state_changed)
    win.connect(widget1, QtCore.SIGNAL("editClicked()"), edit_clicked)
    win.connect(widget1, QtCore.SIGNAL("deleteClicked()"), delete_clicked)
    win.connect(widget2, QtCore.SIGNAL("stateChanged(int)"), state_changed)
    win.connect(widget2, QtCore.SIGNAL("editClicked()"), edit_clicked)
    win.connect(widget2, QtCore.SIGNAL("deleteClicked()"), delete_clicked)

    win.show()

    app.exec_()

if __name__ == "__main__":
    main()
