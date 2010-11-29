#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import profile

PROFILE_FILE = os.path.expanduser("~/.ahenk-lider")

class ProfileReader:

    def __init__(self):

        self.file_exists = os.path.exists(PROFILE_FILE)
        self.profiles = []

    def is_file_exists(self):
        return self.file_exists

    def read(self):
        tmp_profile = profile.Profile()
        with file(PROFILE_FILE) as config_file:
            for line in config_file:
                line = line.strip()
                if line.startswith("domain="):
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
        if len(self.profiles):
            return self.profiles[0]

