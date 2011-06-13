#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

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
