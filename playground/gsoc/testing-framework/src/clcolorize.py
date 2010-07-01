#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This module is based on the ANSI Escape Sequences.
# The following attributes and colors are supported:
# underline, red, green

# Using the color scheme of Pardus

COLOR = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[01;33m'    # brightyellow
        }

RESET = '\033[0m'       

def colorize(text, color):
    """Color the output text."""
    return '{0}{1}{2}'.format(COLOR[color], text, RESET)
    