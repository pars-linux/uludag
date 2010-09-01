#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Plugin management tools
"""

# Standard Modules
import os

# Plugin types
TYPE_SINGLE = 0
TYPE_GLOBAL = 1


def load_plugins(root="plugins"):
    """
        Gets all plugins under given directory.

        Arguments:
            root: Plugin directory
        Returns: Dictionary containing plugins with names as keys
                 and widget classes as values.
    """
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
    try:
        locals = globals = {}
        code = open(filename).read()
        exec compile(code, "error", "exec") in locals, globals
    except IOError, e:
        print "Unable to read plugin (%s): %s" % (filename, e)
    except SyntaxError, e:
        print "SyntaxError in plugin (%s): %s" % (filename, e)
    return locals
