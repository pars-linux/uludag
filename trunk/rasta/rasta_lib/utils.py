#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Rasta RST Editor
    2010 - Gökmen Göksel <gokmen:pardus.org.tr> """

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as Published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Python Core
import os
import sys

# Piksemel
try:
    import piksemel
except ImportError:
    sys.exit("Please install 'piksemel' package.")

# Docutils
try:
    import docutils.io
    import docutils.nodes
    from docutils.core import Publisher
    from StringIO import StringIO
except ImportError:
    sys.exit("Please install 'docutils' package.")

# PyQt4 Core Libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
    from PyQt4.Qsci import QsciScintilla
except ImportError:
    sys.exit("Please install 'qscintilla2-python' package.")

# Rasta Core Library
try:
    from mainWindow import Ui_Rasta
except ImportError:
    sys.exit("Please run 'setup.py build' first.")

# RstLexer for Docutils
from rst_lexer import RstLexer
from model import LogTableModel

TMPFILE = "/tmp/untitled.rst"

# Global Publisher for Docutils
PUB = Publisher(source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput)
PUB.set_reader('standalone', None, 'restructuredtext')
PUB.set_writer('html')
PUB.get_settings()
PUB.settings.halt_level = 7
PUB.settings.warning_stream = StringIO()

def clear_log(log):
    """ Removes not needed lines from log output """
    try:
        piks = piksemel.parseString(unicode(log))
        return piks.getAttribute("line"), piks.getTagData("paragraph")
    except:
        return 1,"Rasta parse error: %s" % log


