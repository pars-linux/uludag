#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    GUI test application for directory API tests.
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

    win = QtGui.QTreeWidget()
    win.setColumnCount(2)

    # GUI utilities
    items = {}
    def new_node(parent, node):
        """Adds new node to QTreeWidget"""
        widget = QtGui.QTreeWidgetItem(parent)
        widget.setText(0, node.get_data().get_title())
        widget.setText(1, node.get_data().get_description())
        widget.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        widget.node = node
        items[node] = widget

    from directory import Node, Data

    # Data
    tmp_db = {}
    tmp_db[0] = [
        Data(1, "Releases", ""),
        Data(2, "Upcoming", ""),
    ]
    tmp_db[1] = [
        Data(3, "2009", "Pardus 2009"),
        Data(4, "2011", "Pardus 2011"),
    ]
    tmp_db[2] = [
        Data(5, "Corporate 2", "Pardus Corporate 2"),
    ]

    # Functions
    def populate_tree(node, callback):
        """Hook function that populates child nodes"""
        data = node.get_data()
        uid = data.get_uid()

        nodes = []
        for item in tmp_db.get(uid, []):
            nodes.append(item)

        callback(nodes)

    def draw_tree(node, children):
        """Callback function that draws tree"""
        item = items[node]
        for child in children:
            new_node(item, child)

    # Root node
    root = Node()
    root.set_data(Data(0, "Pardus", "Pardus Linux"))

    # GUI item for root node
    new_node(win, root)

    # Register functions
    root.register_hook_populate(populate_tree)
    root.register_cb_populate(draw_tree)

    # Method for populating node children on demand
    def slot_populate(item):
        node = item.node
        node.populate_children()
    win.connect(win, QtCore.SIGNAL('itemExpanded(QTreeWidgetItem*)'), slot_populate)

    # Size and visibility
    win.resize(600, 400)
    win.show()

    # Run application
    app.exec_()

if __name__ == "__main__":
    main()
