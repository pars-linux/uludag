#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import os

# Helper modules
import profile

# Profile file
PROFILE_FILE = os.path.expanduser("~/.ahenk-lider")

class ProfileReader:
    """
        Reading previous connection from config file.

        Usage:
            reader = ProfileReader()
            if reader.is_file_exists():
                profiles = reader.read()
    """

    def __init__(self):
        """
            Construstor for profile reader. Sets there is a config file or not.
        """
        self.file_exists = os.path.exists(PROFILE_FILE)
        self.profiles = []

    def is_file_exists(self):
        """
            Returns file_exists.
        """
        return self.file_exists

    def read(self):
        """
            Reads the config file and puts them into a list.

            Returns:
                self.profiles: Profile objects list that it has been used
        """
        with file(PROFILE_FILE) as config_file:
            for line in config_file:
                line = line.strip()
                if line.startswith("domain="):
                    tmp_profile = profile.Profile()
                    tmp_profile.set_domain(line.split("=", 1)[1])
                    line = config_file.next().strip()
                    if line.startswith("address="):
                        tmp_profile.set_address(line.split("=", 1)[1])
                        line = config_file.next().strip()
                        if line.startswith("username="):
                            tmp_profile.set_username(line.split("=", 1)[1])
                            self.profiles.append(tmp_profile)
                            config_file.next()

        return self.profiles

    def get_last_profile(self):
        """
            Returns the last conenction object.

            Returns:
                self.profiles[0]: Last connection profile object
        """
        if len(self.profiles):
            return self.profiles[0]
