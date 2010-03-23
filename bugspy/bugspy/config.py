#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser
import os

class Config(object):
    """Configuration class for BugSPY.conf

    It parses the configuration and passes key/value to the class.

    Assume that we have a configuration as:

    [Authentication]
    userName = eren@pardus.org.tr
    passWord = Pass

    We can use it as:

    c = Config()
    c.username
    c.password
    """

    def __init__(self, conf_file=None):
        """Initialises the class and read configuration

        Args:
            conf_file: Config file to use. Default is: ~/.bugspy.conf
        """
        if not conf_file:
            conf_file = "%s/.bugspy.conf" % os.environ.get("HOME")

        self.__items = dict()

        self.configuration = ConfigParser.ConfigParser()
        self.configuration.read(conf_file)
        self.read()

    def read(self):
        for s in self.configuration.sections():
            self.__items.update(dict(self.configuration.items(s)))

    def __getattr__(self, attr):
        value = self.__items.get(attr, None)
        if value:
            if value in ("True", "False"):
                # the value from ConfigParser is always string, so control it and return bool
                if value == "True":
                    return True
                else:
                    return False
            elif "," in value:
                value = value.split(",")
            else:
                return value
        else:
            return None
