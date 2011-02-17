#!/usr/bin/python
# -*- coding: utf-8 -*-

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

    def __eq__(self, tmp_profile):
        """
            Operator for equality, "=="
        """
        if type(self) != type(tmp_profile):
            return False

        if tmp_profile.get_domain() == self.domain and \
                tmp_profile.get_address() == self.address and \
                tmp_profile.get_username() == self.username:
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
