# -*- coding: utf-8 -*-

"""
    LDAP access contol string (olcAccess) management library.

    Examples:
        # Everyone can change their own passwords
        p = Policy()
        p.set_target_attributes(['userPassword'])
        p.set_write_access(slf=True)
        p.set_private(True)
        print p

        # Everyone can read everything
        p = Policy()
        p.set_target_everything()
        p.set_read_access(everyone=True)
        print p

        # X group can edit Y node
        p = Policy()
        p.set_target_node(y_node, scope='subtree')
        p.set_write_access(group=x_node)
        print p

        # Import directive from LDAP
        p = Policy()
        directive = 'to * by * read'
        if p.import_directive(directive):
            print 'Policy imported'
"""

# Standard modules
import re

# Directory modules
from node import Node


class Policy:
    def __init__(self):
        self.target = None
        self.access = []
        self.private = False
        self.bind_required = False
        self.self_write = False
        self.filtr = None

    def set_target_everything(self):
        self.target = {'type': 'everything'}

    def set_target_attribute(self, attribute, value, scope=None):
        self.target = {'type': 'attribute', 'attribute': attributes, 'value': value, 'scope': scope}

    def set_target_attributes(self, attributes):
        self.target = {'type': 'attributes', 'attributes': attributes}

    def set_target_node(self, node, scope=None):
        self.set_target_address(node.get_address(), scope)

    def set_target_address(self, address, scope=None):
        self.target = {'type': 'address', 'address': address, 'scope': scope}

    def set_target_filter(self, filtr):
        self.target['filter'] = filtr

    def get_target_type(self):
        return self.target['type']

    def get_target_attribute(self):
        return self.target['attribute'], self.target['value'], self.target['scope']

    def get_target_attributes(self):
        return self.target['attributes']

    def get_target_address(self):
        return self.target['address'], self.target['scope']

    def clear_access(self):
        """
        Clears whole access list.
        """
        self.access = []

    def set_access(self, operation, node=None, address=None, group=None, everyone=False, users=False, slf=False, anonymous=None, scope=None, group_filter=None):
        """
        Sets access rights for given operation.

        One and only one of node, group, users, everyone or slf should be given.

        Arguments:
            operation: 'read' or 'write'
            node: Node object of element
            address: LDAP distinguished name
            group: Node object of group
            everyone: True or False (Effects both authenticated and unauthenticated users)
            users: True or False (Effects authenticated users only)
            slf: True or False (Works if node or address is used as target)
            anonymous: Anonymous connections
            scope: 
            group_filter: 
        """
        access = {'operation': operation, 'scope': scope}

        if node:
            access['type'] = 'address'
            access['address'] = node.get_address()
        elif address:
            access['type'] = 'address'
            access['address'] = address
        elif group:
            access['type'] = 'group'
            if isinstance(group, Node):
                access['address'] = group.get_address()
            else:
                access['address'] = group
            access['group_filter'] = group_filter
        elif everyone:
            access['type'] = 'everyone'
        elif users:
            access['type'] = 'users'
        elif slf:
            access['type'] = 'self'
        elif anonymous:
            access['type'] = 'anonymous'

        self.access.append(access)

    def set_read_access(self, node=None, address=None, group=None, everyone=False, users=False, slf=False, anonymous=None, scope=None, group_filter=None):
        """
        Shortcut for set_access('read', ...)
        """
        self.set_access('read', node, address, group, everyone, users, slf, anonymous, scope, group_filter)

    def set_write_access(self, node=None, address=None, group=None, everyone=False, users=False, slf=False, anonymous=None, scope=None, group_filter=None):
        """
        Shortcut for set_access('write', ...)
        """
        self.set_access('write', node, address, group, everyone, users, slf, anonymous, scope, group_filter)

    def get_access_list(self):
        return self.access

    def __str__(self):
        directive = ['to']

        typ = self.get_target_type()

        if typ == 'everything':
            directive.append('*')
        elif typ == 'address':
            address, scope = self.get_target_address()
            if scope:
                scope = '.%s' % scope
            directive.append('dn%s="%s"' % (scope, address))
        elif typ == 'attribute':
            attr, value, scope = self.get_target_attribute()
            if scope:
                scope = '.%s' % scope
            directive.append('attr=%s val%s="%s"' % (attr, scope, value))
        elif typ == 'attributes':
            attributes = ','.join(self.get_target_attributes())
            directive.append('attrs=%s' % attributes)

        for access in self.access:
            typ = access['type']
            operation = access['operation']
            scope = access['scope']
            if scope:
                scope = '.%s' % scope
            if typ in ('node', 'address'):
                address = access['address']
                directive.append('by dn%s="%s" %s' % (scope, address, operation))
            elif typ == 'group':
                address = access['address']
                group_filter = access['group_filter']
                if group_filter:
                    group_filter = '/%s' % group_filter
                else:
                    group_filter = ''
                directive.append('by group%s%s="%s" %s' % (group_filter, scope, address, operation))
            elif typ == 'everyone':
                directive.append('by * %s' % operation)
            elif typ == 'users':
                directive.append('by users %s' % operation)
            elif typ == 'self':
                directive.append('by self %s' % operation)

        return ' '.join(directive)

    def import_directive(self, directive):
        targets, controls = parse_olc_directive(directive)

        if len(targets) == 0:
            return False

        for target in targets:
            if target['target'] == 'all':
                self.set_target_everything()
            elif target['target'] == 'dn':
                self.set_target_address(target['dn'], target['scope'])
            elif target['target'] == 'filter':
                self.set_target_filter(target['filter'])
            elif target['target'] == 'attributes':
                self.set_target_attributes(target['attributes'])
            else:
                return False

        for control in controls:
            """
            if control['operation'] == 'none':
                if control['by'] in ('all', 'anonymous'):
                    self.set_private(True)
                    continue
            elif control['operation'] == 'auth':
                if control['by'] in ('all', 'anonymous'):
                    self.set_bind_required(True)
            elif control['operation'] not in ('read', 'write'):
                return False
            """

            if control['by'] == 'all':
                self.set_access(control['operation'], everyone=True)
            elif control['by'] == 'anonymous':
                self.set_access(control['operation'], anonymous=True)
            elif control['by'] == 'users':
                self.set_access(control['operation'], users=True)
            elif control['by'] == 'self':
                self.set_access(control['operation'], slf=True)
            elif control['by'] == 'dn':
                self.set_access(control['operation'], address=control['dn'], scope=control['scope'])
            elif control['by'] == 'group':
                self.set_access(control['operation'], group=control['group'], scope=control['scope'], group_filter=control['filter'])
            else:
                print control
                return False

        if len(controls) == 0:
            return False

        return True

    def to_pretty(self):
        return str(self)


# Regular expression patterns
REGEX_DN = '([a-zA-Z/]+)(\.[a-z,]+)?="([^"]*)"'
REGEX_FILTER = '([a-zA-Z0-9,=\(\)&|]+)'
REGEX_ATTRS = '([a-zA-Z0-9,]+)\s*(val(\.[a-z,]+)?="([^"]*)")?'
REGEX_CTRL = '(start|stop|break)'
REGEX_PRIV = '[=+-][mwrscxd0]+'
REGEX_LEVEL = '(none|disclose|auth|compare|search|read|write|manage)'
REGEX_WHO = '(\*|anonymous|users|self|%s)' % REGEX_DN
REGEX_WHAT = '(\*|(%s)?\s*(filter=%s)?\s*(attrs=%s)?)' % (REGEX_DN, REGEX_FILTER, REGEX_ATTRS)
REGEX_BY = '(\s+by %s %s)' % (REGEX_WHO, REGEX_LEVEL)
REGEX_DIR = '^to %s(%s+)$' % (REGEX_WHAT, REGEX_BY)


def parse_olc_directive(directive):
    """
        Parses LDAP dynamic acess control directive.

        Arguments:
            directive: LDAP olcAccess directive
        Returns:
            List of target elements and acl matrix.
    """
    targets = []
    controls = []
    match_dir = re.findall(REGEX_DIR, directive)
    if match_dir:
        match_dir = match_dir[0]
        for match_what in re.findall(REGEX_WHAT, match_dir[0]):
            if match_what[0]:
                if match_what[0] == '*':
                    targets.append({'target': 'all'})
                if match_what[2] == 'dn':
                    targets.append({'target': 'dn', 'dn': match_what[4], 'scope': match_what[3][1:]})
                if match_what[5]:
                    targets.append({'target': 'filter', 'filter': match_what[6]})
                if match_what[7]:
                    if match_what[11]:
                        targets.append({'target': 'attribute', 'attribute': match_what[8], 'value': match_what[11], 'scope': match_what[10][1:]})
                    else:
                        targets.append({'target': 'attributes', 'attributes': match_what[8].split(',')})
        for match_by in re.findall(REGEX_BY, match_dir[12]):
            if match_by[0]:
                if match_by[1] == '*':
                    controls.append({'by': 'all', 'operation': match_by[5]})
                elif match_by[1].startswith('dn'):
                    controls.append({'by': 'dn', 'dn': match_by[4], 'scope': match_by[3][1:], 'operation': match_by[5]})
                elif match_by[1].startswith('group'):
                    group_filter = match_by[2].split('/', 1)[1]
                    controls.append({'by': 'group', 'group': match_by[4], 'filter': group_filter, 'scope': match_by[3][1:], 'operation': match_by[5]})
                else:
                    controls.append({'by': match_by[1], 'operation': match_by[5]})
    return targets, controls
