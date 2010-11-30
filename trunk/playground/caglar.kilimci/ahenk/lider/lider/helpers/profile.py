#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Connection profile manager
"""

# Standard modules
import os

# Profile file
PROFILE_FILE = os.path.expanduser("~/.ahenk-lider")


class Profile:
    """
        Base class for connection profile.

        Usage:
            profile = Profile()

            or

            new_profile = Profile(domain, address, username)
            new_profile.save()
    """

    def __init__(self, domain="", address="", username=""):
        """
            Constructor for profile manager class.

            Arguments:
                domain: Domain name
                address: ip address of domain
                username: username of lider
        """
        self.domain = domain
        self.address = address
        self.username = username

    def is_set(self):
        """
            Return true if one of the properties set
        """
        if len(self.domain) or len(self.address) or len(self.username):
            return True
        return False

    def get_domain(self):
        """
            Returns domain.
        """
        return self.domain

    def set_domain(self, domain):
        """
            Sets domain.
        """
        self.domain = domain

    def get_address(self):
        """
            Returns ip address.
        """
        return self.address

    def set_address(self, address):
        """
            Sets ip address.
        """
        self.address = address

    def get_username(self):
        """
            Returns username.
        """
        return self.username

    def set_username(self, username):
        """
            Sets username.
        """
        self.username = username

    def save(self):
        """
            Saves the exist information to the file.
        """
        lines = []

        lines.append("domain=%s" % self.domain)
        lines.append("address=%s" % self.address)
        lines.append("username=%s" % self.username)
        lines.append("-")

        file_content = "\n".join(lines)

        file(PROFILE_FILE, "w").write(file_content)
