# -*- coding: utf-8 -*-

"""
Object oriented LDAP directory management library.
"""

# Standard modules
import copy

# LDAP modules
import ldap
import ldap.dn
import ldap.modlist

# Directory modules
from node import Node
from policy import Policy

class Connection:
    def __init__(self):
        self.host = None
        self.domain = None
        self.user = None
        self.user_dn = None
        self.conn = None
        self.conn_config = None
        self.login_type = None
        self.root_node = None
        self.schema = None
        self.classes = []

    def connect(self, host, domain):
        if domain == 'cn=config':
            self.conn_config = ldap.initialize('ldap://%s' % host)
            return True
        else:
            self.conn = ldap.initialize('ldap://%s' % host)
            try:
                search = self.conn.search_s(domain, ldap.SCOPE_BASE, attrlist=["objectClass"])
            except ldap.NO_SUCH_OBJECT:
                return False
            for dn, attrs in search:
                self.root_node, is_created = Node.get_or_create_node(dn)
                self.root_node.set_classes(attrs["objectClass"])
                self.host = host
                self.domain = dn
                self.fetch_schema()
                return True
            return False

    def login_simple(self, user, password, config=False):
        if config:
            try:
                self.conn_config.bind_s('cn=%s,cn=config' % user, password)
            except ldap.INVALID_CREDENTIALS:
                return False
            return True
        else:
            for dn, attrs in self.conn.search_s(self.domain, ldap.SCOPE_SUBTREE, '(cn=%s)' % user, []):
                self.user = user
                self.user_dn = dn
                self.login_type = 'simple'
                try:
                    self.conn.bind_s(dn, password)
                except ldap.INVALID_CREDENTIALS:
                    return False
                return True
            return False

    def enable_config(self, user, password):
        self.connect(self.host, 'cn=config')
        if self.login_type == 'simple':
            return self.login_simple(user, password, config=True)
        else:
            return False

    def fetch_schema(self):
        self.schema = self.load_schema()
        self.classes = {}
        for class_name in self.schema:
            self.classes[class_name] = [x[0] for x in self.schema[class_name]]

    def get_policies(self):
        for dn, attrs in self.conn_config.search_s('cn=config', ldap.SCOPE_SUBTREE, attrlist=['olcAccess']):
            if dn.endswith('db,cn=config'):
                access = []
                for directive in attrs['olcAccess']:
                    directive = directive.split('}', 1)[1]
                    p = Policy()
                    if p.import_directive(directive):
                        access.append(p)
                    else:
                        access.append(directive)
                return access
        return []

    def list_children(self, parent=None):
        if not parent:
            parent = self.get_root()
        children = []
        for dn, attrs in self.conn.search_s(parent.get_address(), ldap.SCOPE_ONELEVEL, attrlist=['objectClass']):
            node, is_created = Node.get_or_create_node(dn)
            if is_created:
                node.set_parent(parent)
                node.set_classes(attrs["objectClass"])
            children.append(node)
        return children

    def fetch_attributes(self, node):
        attributes = {}
        classes = []
        for dn, attrs in self.conn.search_s(node.get_address(), ldap.SCOPE_BASE):
            for key in attrs:
                if key == 'objectClass':
                    classes = attrs[key]
                else:
                    attributes[key.lower()] = attrs[key]
            node.set_classes(classes)
            node.set_attributes(attributes)
            break

    def list_members(self, node):
        if node.is_fetch_required():
            self.fetch_attributes(node)

        if not node.is_group():
            return []

        attributes = node.get_attributes()
        members = []
        for dn in attributes['member']:
            member, is_created = Node.get_or_create_node(dn)
            members.append(member)
        return members

    def list_groups(self, node):
        pattern = '(&(objectClass=groupofnames)(member=%s))' % node.get_address()
        groups = []
        for dn, attrs in self.conn.search_s(self.domain, ldap.SCOPE_SUBTREE, pattern, []):
            node, is_created = Node.get_or_create_node(dn)
            groups.append(node)
        return groups

    def set_members(self, parent, members):
        if not parent.is_group():
            return False

        if parent.is_fetch_required():
            self.fetch_attributes(parent)

        attributes = copy.deepcopy(parent.get_attributes())
        attributes['member'] = [x.get_address() for x in members]

        self.modify_node(parent, attributes)

    def get_root(self):
        return self.root_node

    def find_node_by_address(self, address):
        for dn, attrs in self.conn.search_s(address, ldap.SCOPE_BASE):
            node, is_created = Node.get_or_create_node(dn)
            if not is_created:
                return node
            node.set_classes(attrs["objectClass"])
            node_orig = node
            for parent_dn in self.get_parent_paths(dn):
                parent, is_created = Node.get_or_create_node(parent_dn)
                node.set_parent(parent)
                node = parent
            return node_orig

    def find_nodes_by_attributes(self, attributes):
        pattern = []
        for key, value in attributes.iteritems():
            pattern.append('(%s=%s)' % (key, value))
        pattern = '(&%s)' % ''.join(pattern)

        nodes = []
        for dn, attrs in self.conn.search_s(self.domain, ldap.SCOPE_SUBTREE, pattern, []):
            node = self.find_node_by_address(dn)
            nodes.append(node)
        return nodes

    def add_node(self, parent, name, node_type):
        """
        classes = ['top']
        if node_type == 'folder':
            classes.append('organization')
            classes.append('dcObject')
            attributes['o'] = [name]
            address = 'dc=%s, %s' % (name, parent.get_original())
        elif node_type == 'user':
            classes.append('organizationalRole')
            classes.append('simpleSecurityObject')
            address = 'cn=%s, %s' % (name, parent.get_original())
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
    """

    def modify_node(self, node, attributes, auto_class=True):
        if node.is_fetch_required():
            self.fetch_attributes(node)

        classes_old = copy.deepcopy(node.get_classes())
        classes_new = copy.deepcopy(node.get_classes())

        if auto_class:
            # Get allowed attributes
            attrs_allowed = []
            for class_name in self.classes:
                if class_name in classes_old:
                    attrs_allowed.extend(self.classes[class_name])

            # Add required object classes
            for key in attributes:
                key = key.lower()
                if key in attrs_allowed:
                    continue
                for class_name in self.classes:
                    if key in self.classes[class_name] and class_name not in classes_new:
                        classes_new.append(class_name)
                        attrs_allowed.extend(self.classes[class_name])

        # Build LDAP attribute list
        attrs_old = copy.deepcopy(node.get_attributes())
        attrs_old['objectclass'] = classes_old
        attrs_new = copy.deepcopy(node.get_attributes())
        attrs_new['objectclass'] = classes_new

        # Append new attributes
        for key in attributes:
            value = attributes[key]
            if not isinstance(value, list):
                value = [value]
            attrs_new[key.lower()] = value

        # Sanitize input
        for key in attrs_new:
            if attrs_new[key] is None:
                attrs_new[key] = []

        # Modify object
        diff = ldap.modlist.modifyModlist(attrs_old, attrs_new)
        self.conn.modify_s(node.get_address(), diff)

        # Re-fetch attributes
        self.fetch_attributes(node)

    def remove_node(self, node, recursive=False):
        if not recursive and len(self.list_children(node)):
            return False
        for child in self.list_children(node):
            self.remove_node(child)
        self.conn.delete_s(node.get_address())
        return True

    def copy_node(self, node, target_parent, new_name=None):
        address = node.get_address()
        rdn = address.split(',')[0]

        if new_name:
            rdn_tag = rdn.split('=')[0]
            new_rdn = '%s=%s' % (rdn_tag, new_name)

        if node.get_parent().get_address() == target_parent.get_address() and new_rdn.lower() == rdn.lower():
            return False

        if node.is_fetch_required():
            self.fetch_attributes(node)

        attributes = {}
        attributes['objectclass'] = node.get_classes()
        attributes.update(node.get_attributes())

        if new_name:
            new_address = '%s=%s,%s' % (rdn_tag, new_name, target_parent.get_address())
            attributes[rdn_tag] = [new_name]
        else:
            new_address = '%s,%s' % (rdn, target_parent.get_address())

        if self.find_node_by_address(new_address):
            return False

        diff = ldap.modlist.addModlist(attributes)
        self.conn.add_s(new_address, diff)

        new_node, is_created = Node.get_or_create_node(new_address)

        for child in self.list_children(node):
            self.copy_node(child, new_node)

    def move_node(self, node, new_parent, new_name=None):
        if self.copy_node(node, new_parent, new_name):
            self.remove_node(node, True)

    def rename_node(self, node, new_name):
        if self.copy_node(node, node.get_parent(), new_name):
            self.remove_node(node, True)

    def get_all_parents(self, node):
        parents = []
        while node:
            parents.append(node)
            node = node.get_parent()
        parents = parents[1:]
        parents.reverse()
        return parents

    def get_all_attributes(self, node):
        attributes = []
        for item in self.get_all_parents(node) + [node]:
            if item.is_fetch_required():
                self.fetch_attributes(item)
            attributes.append(item.get_attributes())
        return attributes

    def get_parent_paths(self, address):
        node_dn = ldap.dn.str2dn(address)
        root_dn = ldap.dn.str2dn(self.domain)
        parents = []
        for i in range(1, len(node_dn) - len(root_dn) + 1):
            parents.append(ldap.dn.dn2str(node_dn[i:]))
        return parents

    def load_schema(self):
        subentry = self.conn.search_subschemasubentry_s()

        attributes = {}
        if subentry != None:
            entry = self.conn.read_subschemasubentry_s(subentry)
            schema = ldap.schema.SubSchema(entry)

            for oids in schema.listall(ldap.schema.ObjectClass):
                obj = schema.get_obj(ldap.schema.ObjectClass, oids)

                for name in obj.names:
                    name = name.lower()

                    try:
                        must, may = schema.attribute_types([name])
                    except KeyError:
                        continue
                    for key, value in may.iteritems():
                        if key in ('objectclass', 'extensibleobject'):
                            continue
                        for a_name in value.names:
                            a_name = a_name.lower()
                            attributes.setdefault(name, []).append((a_name, value.single_value, True))
                    for key, value in must.iteritems():
                        if key in ('objectclass', 'extensibleobject'):
                            continue
                        for a_name in value.names:
                            a_name = a_name.lower()
                            attributes.setdefault(name, []).append((a_name, value.single_value, False))

        return attributes
