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


class Policy:
    def __init__(self):
        self.target = None
        self.access = []
        self.private = False
        self.filtr = None

    def set_target_everything(self):
        self.target = {'type': 'everything'}

    def set_target_attribute(self, attribute, value):
        self.target = {'type': 'attribute', 'attribute': attributes, 'value': value}

    def set_target_attributes(self, attributes):
        self.target = {'type': 'attributes', 'attributes': attributes}

    def set_target_node(self, node, scope=None):
        self.target = {'type': 'node', 'node': node, 'scope': scope}

    def set_target_address(self, address, scope=None):
        self.target = {'type': 'address', 'address': address, 'scope': scope}

    def set_target_filter(self, filtr):
        self.target['filter'] = filtr

    def get_target_type(self):
        return self.target['type']

    def get_target_attribute(self):
        return self.target['attribute'], self.target['value']

    def get_target_attributes(self):
        return self.target['attributes']

    def get_target_node(self):
        return self.target['node']

    def get_target_address(self):
        return self.target['address']

    def get_target_scope(self):
        return self.target['scope']

    def clear_access(self):
        """
        Clears whole access list.
        """
        self.access = []
        self.private = False

    def set_access(self, operation, node=None, address=None, group=None, everyone=False, users=False, slf=False, scope=None):
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
            scope: 
        """
        access = {'operation': operation, 'scope': scope}

        if node:
            access['type'] = 'node'
            access['node'] = node
        elif address:
            access['type'] = 'address'
            access['address'] = address
        elif group:
            access['type'] = 'group'
            access['group'] = group
        elif everyone:
            access['type'] = 'everyone'
        elif users:
            access['type'] = 'users'
        elif slf:
            access['type'] = 'self'

        self.access.append(access)

    def set_read_access(self, node=None, address=None, group=None, everyone=False, users=False, slf=False, scope=None):
        """
        Shortcut for set_access('read', ...)
        """
        self.set_access('read', node, address, group, everyone, users, slf, scope)

    def set_write_access(self, node=None, address=None, group=None, everyone=False, users=False, slf=False, scope=None):
        """
        Shortcut for set_access('write', ...)
        """
        self.set_access('write', node, address, group, everyone, users, slf, scope)

    def get_access_list(self):
        return self.access

    def set_private(self, state):
        """
        Whether the target is private and must be hidden.

        Arguments:
            state: True or False
        """
        self.private = state

    def is_private(self):
        return self.private

    def __str__(self):
        directive = ['to']

        if self.get_target_type() == 'everything':
            directive.append('*')
        elif self.get_target_type() in ['address', 'node']:
            if self.get_target_type() == 'node':
                node = self.get_target_node()
                address = node.get_address()
            else:
                address = self.get_target_address()

            if self.get_target_scope():
                directive.append('dn.%s="%s"' % (self.get_target_scope(), address))
            else:
                directive.append('dn="%s"' % address)
        elif self.get_target_type() == 'attribute':
            directive.append('attr=%s val="%s"' % self.get_target_attribute())
        elif self.get_target_type() == 'attributes':
            attributes = ','.join(self.get_target_attributes())
            directive.append('attrs=%s' % attributes)

        for access in self.access:
            typ = access['type']
            operation = access['operation']
            if typ == 'node':
                address = access['node'].get_address()
                directive.append('by dn="%s" %s' % (address, operation))
            elif typ == 'address':
                address = access['address']
                directive.append('by dn="%s" %s' % (address, operation))
            elif typ == 'group':
                address = access['group'].get_address()
                directive.append('by group="%s" %s' % (address, operation))
            elif typ == 'everyone':
                directive.append('by * %s' % operation)
            elif typ == 'users':
                directive.append('by users %s' % operation)
            elif typ == 'self':
                directive.append('by self %s' % operation)

        if self.is_private():
            directive.append('by anonymous auth')
            directive.append('by * none')

        return ' '.join(directive)

    def import_directive(self, directive):
        targets, controls = parse_olc_directive(directive)

        if len(targets) == 0:
            return False

        for target in targets:
            if target['target'] == 'all':
                self.set_target_everything()
            elif target['target'] == 'dn':
                self.set_target_address(target['dn'], target['style'])
            elif target['target'] == 'filter':
                self.set_target_filter(target['filter'])
            elif target['target'] == 'attributes':
                self.set_target_attributes(target['attributes'])
            else:
                return False

        auth_needed = False
        default_none = False
        for control in controls:
            if control['operation'] == 'none':
                if control['by'] == 'all':
                    default_none = True
                    continue
                else:
                    return False
            elif control['operation'] == 'auth':
                if control['by'] == 'anonymous':
                    auth_needed = True
                    continue
                else:
                    return False
            elif control['operation'] not in ('read', 'write'):
                return False

            if control['by'] == 'all':
                self.set_access(control['operation'], everyone=True)
            elif control['by'] == 'self':
                self.set_access(control['operation'], slf=True)
            elif control['by'] == 'dn':
                self.set_access(control['operation'], address=control['dn'], scope=control['style'])
            elif control['by'] == 'group':
                self.set_access(control['operation'], address=control['group'])
            else:
                return False

        if auth_needed and default_none:
            self.set_private(True)
        elif auth_needed or default_none:
            return False

        if len(controls) == 0:
            return False

        return True


# Regular expression patterns
REGEX_DN = '([a-z]+)(\.[a-z,]+)?="([^"]*)"'
REGEX_FILTER = '([a-zA-Z0-9,=\(\)&|]+)'
REGEX_ATTRS = '([a-zA-Z0-9,]+)\s*(val(\.[a-z,]+)?="([^"]*)")?'
REGEX_CTRL = '(start|stop|break)'
REGEX_PRIV = '[=+-][mwrscxd0]+'
REGEX_LEVEL = '(none|disclose|auth|compare|search|read|write|manage)'
REGEX_WHO = '(\*|anonymous|users|self|%s)' % REGEX_DN
REGEX_WHAT = '(\*|(%s)?\s*(filter=%s)?\s*(attrs=%s)?)' % (REGEX_DN, REGEX_FILTER, REGEX_ATTRS)
REGEX_BY = '( by %s %s)' % (REGEX_WHO, REGEX_LEVEL)
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
                    targets.append({'target': 'dn', 'dn': match_what[4], 'style': match_what[3][1:]})
                if match_what[5]:
                    targets.append({'target': 'filter', 'filter': match_what[6]})
                if match_what[7]:
                    if match_what[11]:
                        targets.append({'target': 'attribute', 'attribute': match_what[8], 'value': match_what[11], 'style': match_what[10][1:]})
                    else:
                        targets.append({'target': 'attributes', 'attributes': match_what[8].split(',')})
        for match_by in re.findall(REGEX_BY, match_dir[12]):
            if match_by[0]:
                if match_by[1] == '*':
                    controls.append({'by': 'all', 'operation': match_by[5]})
                elif match_by[1].startswith('dn'):
                    controls.append({'by': 'dn', 'dn': match_by[4], 'style': match_by[3][1:], 'operation': match_by[5]})
                elif match_by[1].startswith('group'):
                    controls.append({'by': 'group', 'group': match_by[4], 'operation': match_by[5]})
                else:
                    controls.append({'by': match_by[1], 'operation': match_by[5]})
    return targets, controls

if __name__ == '__main__':
    #p = Policy()
    #p.set_target_attributes(['userPassword'])
    #p.set_write_access(slf=True)
    #p.set_private(True)
    #print p

    directives = [
        'to dn="cn=admin,dc=pardus" by dn="cn=admin,dc=pardus" write by * none by anonymous auth',
        'to dn.subtree="cn=admin,dc=pardus" by dn="cn=admin,dc=pardus" write by * none by anonymous auth',
        'to attrs=x val="none" by dn="cn=admin,dc=pardus" write by * none by anonymous auth',
        'to * by * read',
    ]

    for directive in directives:
        p = Policy()
        if p.import_directive(directive):
            print 'Policy imported:', p
        else:
            print 'Policy not imported:', directive
