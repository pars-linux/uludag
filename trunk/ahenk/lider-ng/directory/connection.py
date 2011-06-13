# -*- coding: utf-8 -*-

"""
Object oriented LDAP directory management library.

Example:
    api = Connection()
    api.login_simple('127.0.0.1', 'example.org', 'admin, '*****')
"""

# Standard modules
import copy

# LDAP modules
import ldap
import ldap.modlist

# Directory modules
from directory.utils import *
from directory.node import Node

# Node-Address mapping
ADDRESS = {}

def get_node_by_address(address):
    """
        Finds node by Address.
    """
    if address in ADDRESS:
        return ADDRESS[address]

def register_node(node):
    """
        Registers a node to address database.

        Arguments:
            node: Node data
    """
    ADDRESS[node.get_address()] = node


class Connection:
    def __init__(self):
        self.conn = None
        self.conn_config = None
        self.host = None
        self.domain = None
        self.user = None
        self.ldap_domain = None
        self.ldap_user = None
        self.root_node = None
        self.ldap_classes = {}

    def login_simple(self, host, domain, user, password):
        self.host = host

        # Sanitize domain name
        if 'dc=' not in domain:
            self.ldap_domain = get_ldap_domain(domain)
        else:
            self.ldap_domain = sanitize_ldap_address(domain)

        # Sanitize user name
        if not user.startswith('cn='):
            self.ldap_user = 'cn=%s, %s' % (user, self.ldap_domain)
        else:
            self.ldap_user = sanitize_ldap_address(user)

        # Save human readable domain and user name
        self.domain = get_inet_domain(self.ldap_domain)
        self.user = get_ldap_name(self.ldap_user)

        # Create root node
        self.root_node = Node(self.ldap_domain)
        register_node(self.root_node)

        # Open connection
        self.conn = ldap.initialize('ldap://%s' % self.host)
        self.conn.simple_bind_s(self.ldap_user, password)

        # Open connection for configuration
        self.conn_config = ldap.initialize('ldap://%s' % self.host)
        #self.conn_config.simple_bind_s('cn=%s,cn=config' % self.user, password)

        # Load LDAP classes and attributes
        self.__fetch_ldap_attributes()

    def list_children(self, node=None):
        if not node:
            node = self.root_node

        # Get LDAP address
        parent_address = node.get_address()

        # Populate child nodes
        children = []
        for child in self.conn.search_s(parent_address, ldap.SCOPE_ONELEVEL):
            item = self.find_node_by_address(child[0])
            item.set_parent(node)
            children.append(item)

        return children

    def fetch_attributes(self, node):
        address = node.get_address()
        attributes = self.conn.search_s(address, ldap.SCOPE_BASE)[0][1]
        node.set_attributes(attributes)

    def list_members(self, node):
        if not node.get_attributes():
            self.fetch_attributes(node)

        if not node.is_group():
            return []

        attributes = node.get_attributes()

        members = []
        if 'member' in attributes:
            for member in attributes['member']:
                item = self.find_node_by_address(member)
                members.append(item)
        return members

    def list_groups(self, node):
        name = node.get_address()
        pattern = get_pattern({'member': name})

        groups = []
        for child in self.conn.search_s(self.ldap_domain, ldap.SCOPE_SUBTREE, pattern):
            item = self.find_node_by_address(child[0])
            if item.get_address() == node.get_address():
                continue
            groups.append(item)

        return groups

    def add_member(self, parent, node):
        if not parent.is_group():
            return False

        if not parent.get_attributes():
            self.fetch_attributes(parent)

        # Modify "member" list
        attributes = copy.deepcopy(parent.get_attributes())
        if 'member' not in attributes:
            attributes['member'] = []

        if node.get_address() in attributes['member']:
            return False
        else:
            attributes['member'].append(node.get_original())
        self.modify_node(parent, attributes)

        return True

    def get_root(self):
        return self.root_node

    def find_node_by_address(self, address):
        if not len(address):
            address = self.ldap_domain

        address = sanitize_ldap_address(address)

        if address == self.ldap_domain:
            return self.root_node

        # Fetch LDAP classes
        try:
            results = self.conn.search_s(address, ldap.SCOPE_BASE, attrlist=['objectClass'])
        except ldap.NO_SUCH_OBJECT:
            return None

        classes = []
        for node in results:
            classes = node[1]['objectClass']
            break

        # Find node, or create if new
        item = get_node_by_address(address)
        if not item:
            item = Node(address)
            register_node(item)

        # Set classes
            item.set_classes(classes)

        # Create parent node, if it's missing
        if not item.get_parent():
            parent = self._parent_paths(address)[0]
            parent_item = self.find_node_by_address(parent)
            item.set_parent(parent_item)

        return item

    def find_nodes_by_attributes(self, attributes):
        pattern = get_pattern(attributes)

        nodes = []
        for child in self.conn.search_s(self.ldap_domain, ldap.SCOPE_SUBTREE, pattern):
            address = sanitize_ldap_address(child[0])
            nodes.append(self.find_node_by_address(address))

        return nodes

    def add_node(self, parent, name):
        classes = ['top']
        if node_type == 'folder':
            classes.append('organization')
            classes.append('dcObject')
            attributes['o'] = [label]
            address = 'dc=%s, %s' % (label, parent.get_original())
        elif node_type == 'user':
            classes.append('organizationalRole')
            classes.append('simpleSecurityObject')
            address = 'cn=%s, %s' % (label, parent.get_original())
        elif node_type == 'device':
            classes.append('device')
            classes.append('simpleSecurityObject')
            address = 'cn=%s, %s' % (label, parent.get_original())
        elif node_type == 'group':
            classes.append('groupOfNames')
            address = 'cn=%s, %s' % (label, parent.get_original())
        else:
            return None

        # Get allowed attributes
        attrs_allowed = []
        for class_name in self.ldap_classes:
            if class_name in classes:
                attrs_allowed.extend(self.ldap_classes[class_name])

        # Add required object classes
        for key in attributes:
            key = key.lower()
            if key in attrs_allowed:
                continue
            for class_name in self.ldap_classes:
                if key in self.ldap_classes[class_name] and class_name not in classes:
                    classes.append(class_name)

        attrs_new = {}
        attrs_new['objectclass'] = classes
        for key in attributes:
            attrs_new[key.lower()] = attributes[key]

        # Add object
        diff = ldap.modlist.addModlist(attrs_new)
        self.conn.add_s(address, diff)

        # Create node
        node = self.find_node_by_address(address)
        return node

    def modify_node(self, node, attributes):
        if not node.get_attributes():
            self.fetch_attributes(node)

        classes_new = copy.deepcopy(node.get_classes())

        # Get allowed attributes
        attrs_allowed = []
        for class_name in self.ldap_classes:
            if class_name in node.get_classes():
                attrs_allowed.extend(self.ldap_classes[class_name])

        # Add required object classes
        for key in attributes:
            key = key.lower()
            if key in attrs_allowed:
                continue
            for class_name in self.ldap_classes:
                if key in self.ldap_classes[class_name] and class_name not in classes_new:
                    classes_new.append(class_name)

        attrs_old = {}
        attrs_old['objectclass'] = node.get_classes()
        attrs_old.update(node.get_attributes())

        # Append new attributes
        attrs_new = copy.deepcopy(node.get_attributes())
        attrs_new['objectclass'] = classes_new
        for key in attributes:
            attrs_new[key.lower()] = attributes[key]

        # Sanitize input
        for key in attrs_new:
            if attrs_new[key] is None:
                attrs_new[key] = []

        # Modify object
        diff = ldap.modlist.modifyModlist(attrs_old, attrs_new)
        self.conn.modify_s(node.get_address(), diff)

        # Re-fetch attributes
        self.fetch_attributes(node)

    def remove_node(self, node):
        # Remove child nodes recursively
        for child in self.list_children(node):
            self.remove_node(child)

        # Remove node
        self.conn.delete_s(node.get_original())

    def get_all_parents(self, node):
        # Get groups
        groups = self.list_groups(node)

        # Get parent folders
        node = node.get_parent()
        parents = []
        while node:
            parents.append(node)
            node = node.get_parent()
        parents.reverse()

        return parents + groups

    def get_all_attributes(self, node):
        # Get parents
        items = self.get_all_parents(node)

        # Add node itself
        items.append(node)

        # Add attributes to stack
        stack = []
        for item in parents:
            if not item.get_attributes():
                self.fetch_attributes(item)
            stack.append(item.get_attributes())

        # Merge policies
        merged = {}
        for attrs in stack:
            merged.update(attrs)

        return stack, merged

    def _parent_paths(self, address):
        parents = []
        for i in range(address.count(',')):
            if i > self.ldap_domain.count(',') + 1:
                break

            parent = []
            for part in address.split(',')[i + 1:]:
                parent.append(part.strip())

            parent = ', '.join(parent)
            parents.append(parent)

        return parents

    def __fetch_ldap_attributes(self):
        subentry = self.conn.search_subschemasubentry_s()

        self.ldap_classes = {}
        if subentry != None:
            entry = self.conn.read_subschemasubentry_s(subentry)
            schema = ldap.schema.SubSchema(entry)
            for oids in schema.listall(ldap.schema.ObjectClass):
                obj = schema.get_obj(ldap.schema.ObjectClass, oids)

                must = []
                if len(obj.must) != 0:
                    must = [x.lower() for x in obj.must]

                may = []
                if len(obj.may) != 0:
                    may = [x.lower() for x in obj.may]

                for name in obj.names:
                    self.ldap_classes[name] = must + may
