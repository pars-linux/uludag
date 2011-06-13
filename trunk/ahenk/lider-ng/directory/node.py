# -*- coding: utf-8 -*-

"""
"""

# Directory modules
from directory.utils import get_ldap_name

class Node:
    def __init__(self, address):
        self.parent = None
        self.address = address
        self.ldap_attributes = None
        self.ldap_classes = None
        self.description = ""

    def get_address(self):
        """
        Returns full address of node.

        Returns:
            DN of LDAP object
        """
        return self.address

    def get_classes(self):
        """
        Returns list of node classes.

        Returns:
            List of LDAP classes
        """
        return self.ldap_classes

    def set_classes(self, classes):
        self.ldap_classes = classes

    def get_attributes(self):
        """
        Returns a dictionary of node attributes.
        Classes are omitted.

        Returns:
            LDAP attributes
        """
        return self.ldap_attributes

    def set_attributes(self, attributes):
        self.ldap_attributes = {}
        self.ldap_classes = []
        for key in attributes:
            if key.lower() == 'objectclass':
                self.ldap_classes = attributes[key]
            else:
                self.ldap_attributes[key.lower()] = attributes[key]
        # Find description
        if 'description' in self.ldap_attributes:
            self.description = self.ldap_attributes['description'][0]

    def get_label(self):
        return get_ldap_name(self.address).capitalize()

    def get_description(self):
        return self.description

    def get_parent(self):
        return self.parent

    def set_parent(self, node):
        self.parent = node

    def is_group(self):
        return 'groupOfNames' in self.ldap_classes

    def is_folder(self):
        return self.address.startswith('dc=')
