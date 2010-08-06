#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This module is based on the ANSI escape sequences
# The Pardus color scheme is used 

COLOR = {
        'red': '\033[1;31m',
        'green': '\033[1;32m',
        'blue': '\033[1;34m',
        'yellow': '\033[01;33m',
        'bold': '\033[1m'
        }

RESET = '\033[0m'       


def colorize(text, color):
    """Return the text with the selected color."""
    return '{0}{1}{2}'.format(COLOR[color], text, RESET)