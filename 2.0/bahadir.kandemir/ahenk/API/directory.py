#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Ahenk 2.0 Directory API Draft
"""

# Standard modules
import threading
import uuid


# UID database
UIDS = {}

def register_node(node):
    """
        Registers a node and returns its unique ID.

        WARNING: This experimental code is not thread safe.

        Arguments:
            node: Node object
        Returns
            Unique ID.
    """
    def make_uid():
        """Generates UUID"""
        return  str(uuid.uuid4())

    lock = threading.RLock()
    with lock:
        uid = make_uid()
        while uid in UIDS:
            uid = make_uid()
        UIDS[uid] = node
        return uid


class Node:
    """
        Node structure.

        Usage:
            root = Node()
            child = Node(parent=root)
    """

    def __init__(self, parent=None):
        """
            Node class constructor.

            Arguments:
                parent: Parent node
        """
        self.parent = parent
        self.uid = register_node(self)
        self.data = None
        self.children = []
        self.deep = False

        # Hook functions
        self.hook_populate = None

        # Callback functions
        self.cb_populate = None

        if parent:
            self.parent.append_child(self)

    def append_child(self, node):
        """
            Appends a child node.
            This method is called by child nodes.

            Arguments:
                node: Child node
        """
        self.children.append(node)

    def register_cb_populate(self, callback):
        """
            Registers callback function to be called after populating nodes.

            Arguments:
                callback: Callback function. Gets node and list of nodes as arguments.


            Use this callback function to update your GUI:

                def draw(node, children):
                    for child in children:
                        print child
                node.register_cb_populate(draw)
                node.populate_children()
        """
        self.cb_populate = callback

    def register_hook_populate(self, hook):
        """
            Registers hook function to be called while populating nodes.

            Arguments:
                hook: Hook function. Gets node and callback function as arguments.


            Use this hook function to add data to the model:

                def populate(node, cb):
                    nodes = [1, 2, 3]
                    cb(nodes)
                node.register_hook_populate(populate)
                node.populate_children()
        """
        self.hook_populate = hook

    def populate_children(self, deep=False):
        """
            Populates child nodes using hook function.

            Arguments:
                deep: If True, populates all children at once. Use while debugging only.
        """
        self.deep = deep
        if self.hook_populate:
            self.hook_populate(self, self.callback_populate)

    def callback_populate(self, children):
        """
            Method to be called by hook function.

            Arguments:
                uid: Node UID
                children: List of child node data
        """
        child_nodes = []
        for child in children:
            node = Node(self)
            node.set_data(child)
            child_nodes.append(node)

            if self.hook_populate:
                node.register_hook_populate(self.hook_populate)

            if self.cb_populate:
                node.register_cb_populate(self.cb_populate)

            if self.deep:
                node.populate_children(deep=True)

        if self.cb_populate:
            self.cb_populate(self, child_nodes)

    def get_uid(self):
        """
            Returns node id.
        """
        return self.uid

    def get_parent(self):
        """
            Returns parent node.
        """
        return self.parent

    def set_data(self, data):
        """
            Sets node data.

            Arguments:
                data: Arbitrary data
        """
        self.data = data

    def get_data(self):
        """
            Returns node data.
        """
        return self.data

    def __str__(self):
        """
            Returns node ID.
        """
        return self.uid

    def pretty_print(self, depth=0):
        """
            Prints node children as a tree.

            Warning: Use for debugging only.

            Arguments:
                depth: Initial indentation level.
        """
        print "%s%s (%s)" % ("  " * depth * 2, self.get_data(), self.get_uid())
        for child in self.children:
            child.pretty_print(depth + 1)

class Data:
    """
        Node data model.
    """

    def __init__(self, uid, title, description):
        self.uid = uid
        self.title = title
        self.description = description

    def get_uid(self):
        """
            Returns node id.
        """
        return self.uid

    def get_title(self):
        """
            Returns title.
        """
        return self.title

    def get_description(self):
        """
            Returns description.
        """
        return self.description

    def __str__(self):
        return "%s - %s" % (self.title, self.description)


def main():
    """
        Main
    """
    tmp_db = {}
    tmp_db[0] = [
        Data(1, "ULAKBİM", "Ankara'daki sunucular"),
        Data(2, "BİLGEM", "Gebze'deki sunucular"),
    ]
    tmp_db[1] = [
        Data(3, "TASMA", "Gateway"),
        Data(4, "Ahenk", "Redmine"),
    ]
    tmp_db[2] = [
        Data(5, "PiSi", "Web sunucusu"),
        Data(6, "Derin", "FTP sunucusu"),
    ]

    def populate(node, callback):
        """Populates nodes"""
        data = node.get_data()
        uid = data.get_uid()

        nodes = []
        for item in tmp_db.get(uid, []):
            nodes.append(item)

        callback(nodes)

    root = Node()
    root.set_data(Data(0, "Pardus", "Sunucular"))

    root.register_hook_populate(populate)
    root.populate_children(deep=True)

    root.pretty_print()

if __name__ == '__main__':
    main()
