#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    LDAP backend API
"""

# Standard modules
import sys

# LDAP modules
import ldap


class LDAP:
    """
        LDAP Wrapper Class

        Usage:
            api = API()
            api.login_simple("127.0.0.1", "dc=test", "cn=admin, dc=test", "*****")
            print api.list_children("dc=test")
    """

    def __init__(self):
        """
            LDAP wrapper constructor.
        """
        self.connection = None

    def login_simple(self, host, domain, user, password):
        """
            Logs in to the server.

            Arguments:
                host: Server address
                domain: Domain name (LDAP style)
                user: User name (LDAP style)
                password: User password
        """
        self.host = host
        self.domain = domain

        self.connection = ldap.initialize('ldap://%s' % host)
        self.connection.simple_bind_s(user, password)

    def get_info(self, node):
        """
            Returns node information.

            Arguments:
                node: Node name (LDAP style)
            Returns:
                ...
        """
        return self.connection.search_s(node, ldap.SCOPE_BASE)[0][1]

    def list_children(self, node):
        """
            Lists child nodes.

            Arguments:
                node: Node name (LDAP style)
            Returns:
                List of child node names.
        """
        return [x[0] for x in self.connection.search_s(node, ldap.SCOPE_ONELEVEL)]

    def list_members(self, node):
        """
            Lists members of an OU node.

            Arguments:
                node: Node name (LDAP style)
            Returns:
                List of member names.
        """
        return [x[0] for x in self.connection.search_s(self.domain, ldap.SCOPE_SUBTREE, '(ou=%s)' % node)]

    def add_node(self, node, attributes):
        """
            Adds a node to domain.

            Arguments:
                node: Node name (LDAP style)
                attributes: LDAP attributes (dict)
        """
        pass

    def modify_node(self, node, attributes):
        """
            Modifies a node in domain.

            Arguments:
                node: Node name (LDAP style)
                attributes: LDAP attributes (dict)
        """
        pass

    def remove_node(self, node):
        """
            Removes a node.

            Arguments:
                node: Node name (LDAP style)
        """
        pass


def main():
    """
        Main
    """
    api = LDAP()
    api.login_simple("127.0.0.1", "dc=pardus", "cn=admin, dc=pardus", "123456")
    print api.get_info("dc=pardus")
    print api.list_children("dc=pardus")
    print api.list_children("cn=admin, dc=pardus")

if __name__ == '__main__':
    main()
