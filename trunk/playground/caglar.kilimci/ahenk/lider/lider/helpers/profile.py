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
            last_profile = Profile()

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

        if not os.path.exists(PROFILE_FILE):
            return

        with file(PROFILE_FILE) as config_file:
            for line in config_file:
                line = line.strip()
                if line.startswith("domain="):
                    self.domain = line.split("=", 1)[1]
                elif line.startswith("address="):
                    self.address = line.split("=", 1)[1]
                elif line.startswith("username="):
                    self.username = line.split("=", 1)[1]

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

    def get_address(self):
        """
            Returns ip address.
        """
        return self.address

    def get_username(self):
        """
            Returns username.
        """
        return self.username

    def save(self):
        """
            Saves the exist information to the file.
        """
        lines = []

        if len(self.domain) != 0:
            lines.append("domain=%s" % self.domain)
        if len(self.address) !=0:
            lines.append("address=%s" % self.address)
        if len(self.username) != 0:
            lines.append("username=%s" % self.username)

        file_content = "\n".join(lines)

        file(PROFILE_FILE, "w").write(file_content)
