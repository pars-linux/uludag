#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import os

# Helper modules
import profile
import profilereader

# Profile file
PROFILE_FILE = os.path.expanduser("~/.ahenk-lider")

class ProfileWriter:
    """
        Writing last connection details at the top of the previous connections into config file.

        Usage:
            writer = ProfileWriter()
            writer.save_as_last_profile(last_profile)
    """

    def __init__(self):
        """
            Loads existing profiles form config file into profiles list.
        """
        self.profiles = []
        reader = profilereader.ProfileReader()
        if reader.is_file_exists():
            self.profiles = reader.read()

    def save_as_last_profile(self, last_profile):
        """
            Rearrange profiles list. First element of list is the last used connection.

            Arguments:
                last_profile: Last connection profile object
        """
        while self.profiles.count(last_profile) > 0:
            self.profiles.remove(last_profile)

        self.profiles.insert(0, last_profile)
        self.__write_into_file()

    def __write_into_file(self):
        """
            Writing profiles into disk.
        """
        lines = []
        for i in range(0, len(self.profiles)):
            lines.append("domain=%s" % self.profiles[i].get_domain())
            lines.append("address=%s" % self.profiles[i].get_address())
            lines.append("username=%s" % self.profiles[i].get_username())
            lines.append("-")

            file_content = "\n".join(lines)

            file(PROFILE_FILE, "w").write(file_content)
