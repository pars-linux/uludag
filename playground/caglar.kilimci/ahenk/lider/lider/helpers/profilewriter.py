#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import profile
import profilereader

PROFILE_FILE = os.path.expanduser("~/.ahenk-lider")

class ProfileWriter:

    def __init__(self):
        self.profiles = []
        reader = profilereader.ProfileReader()
        if reader.is_file_exists():
            profiles = reader.read()

    def save_as_last_profile(self, last_profile):
        last_profile.save()

