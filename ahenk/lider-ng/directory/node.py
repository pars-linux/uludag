# -*- coding: utf-8 -*-

"""
"""

# Standard modules
from multiprocessing import Lock

# Ldap modules
import ldap.dn

# Node database
NODE_LOCK = Lock()
NODE_DB = {}

class Node:
    address = None
    classes = []
    attributes = {}
    parent = None

    def __init__(self, address):
        self.set_address(address)
        self.set_classes([])
        self.set_parent(None)

    def set_address(self, address):
        NODE_LOCK.acquire()
        if self.address and self.address in NODE_DB:
            del NODE_DB[self.address]
        self.address = ldap.dn.dn2str(ldap.dn.str2dn(address))
        NODE_DB[self.address] = self
        NODE_LOCK.release()

    def get_address(self):
        return self.address

    def get_classes(self):
        return self.classes

    def is_fetch_required(self):
        return len(self.attributes) == 0
        return len(self.classes) == 0

    def set_classes(self, classes):
        self.classes = []
        for cls in classes:
            self.classes.append(cls.lower())

    def get_attributes(self):
        return self.attributes

    def set_attributes(self, attributes):
        self.attributes = attributes

    def get_label(self):
        dn = ldap.dn.str2dn(self.address)
        return dn[0][0][1]

    def get_description(self):
        desc = self.attributes.get('description', [''])[0]
        return unicode(desc)

    def get_parent(self):
        return self.parent

    def set_parent(self, node):
        self.parent = node

    def is_group(self):
        return 'groupofnames' in self.classes

    def is_folder(self):
        return 'dcobject' in self.classes

    def is_user(self):
        return 'organizationalrole' in self.classes

    def is_device(self):
        return 'device' in self.classes

    @staticmethod
    def get_node_from_address(address):
        if address in NODE_DB:
            return NODE_DB[address]
        return None

    @staticmethod
    def get_or_create_node(address):
        node = Node.get_node_from_address(address)
        if node:
            return node, False
        else:
            return Node(address), True
