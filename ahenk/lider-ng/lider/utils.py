#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import os
import sys

# Profile database
PROFILE_FILE = os.path.expanduser("~/.ahenk-lider")

def load_plugins(root="plugins"):
    """
        Gets all plugins under given directory.

        Arguments:
            root: Plugin directory
        Returns: Dictionary containing plugins with names as keys
                 and widget classes as values.
    """
    root = os.path.realpath(os.path.join(os.path.dirname(__file__), "plugins"))
    plugins = {}
    for plugin_dir in os.listdir(root):
        if not plugin_dir.startswith("plugin_"):
            continue
        plugin_file = os.path.join(root, plugin_dir, "main.py")
        name = plugin_dir.split("plugin_")[1]
        locals = import_plugin(plugin_file)
        widget_class = locals["WidgetModule"]
        plugins[name] = widget_class
    return plugins

def import_plugin(filename):
    """
        Compiles given Python file and returns it's globals.

        Arguments:
            filename: Path to Python file
        Returns: Dictionary containing globals
    """
    pathname = os.path.dirname(filename)
    sys.path.insert(0, pathname)
    locals = globals = {}
    try:
        code = open(filename).read()
        exec compile(code, filename, "exec") in locals, globals
    except IOError, e:
        print "Unable to read plugin (%s): %s" % (filename, e)
    except SyntaxError, e:
        print "SyntaxError in plugin (%s): %s" % (filename, e)
    except Exception, e:
        print "Error in plugin (%s): %s" % (filename, e)
    finally:
        try:
            sys.path.remove(pathname)
        except ValueError:
            pass
    return locals


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

        if self.domain:
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
